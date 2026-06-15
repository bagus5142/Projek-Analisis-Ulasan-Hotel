import { useState } from "react";
import { FileUp, Loader2, RotateCcw } from "lucide-react";
import { useData } from "../context/DataContext";
import { parseDataset } from "../lib/parseCsv";
import { Button } from "./ui/button";
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from "./ui/dialog";

function FileInput({
  label,
  hint,
  file,
  onChange,
}: {
  label: string;
  hint: string;
  file: File | null;
  onChange: (f: File | null) => void;
}) {
  return (
    <label className="flex cursor-pointer flex-col gap-1 rounded-lg border border-dashed p-4 transition-colors hover:bg-accent">
      <span style={{ fontSize: 13, fontWeight: 600 }}>{label}</span>
      <span className="text-muted-foreground" style={{ fontSize: 12 }}>
        {file ? file.name : hint}
      </span>
      <input
        type="file"
        accept=".csv,text/csv"
        className="hidden"
        onChange={(e) => onChange(e.target.files?.[0] ?? null)}
      />
    </label>
  );
}

export function UploadDialog({ open, onOpenChange }: { open: boolean; onOpenChange: (o: boolean) => void }) {
  const { setUploaded, resetToMock, source } = useData();
  const [reviews, setReviews] = useState<File | null>(null);
  const [phrases, setPhrases] = useState<File | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleParse = async () => {
    if (!reviews) {
      setError("File data ulasan wajib dipilih.");
      return;
    }
    setLoading(true);
    setError(null);
    try {
      const res = await parseDataset(reviews, phrases);
      setUploaded(res.hotels);
      onOpenChange(false);
      setReviews(null);
      setPhrases(null);
    } catch (e) {
      setError(e instanceof Error ? e.message : "Gagal memproses file.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent>
        <DialogHeader>
          <DialogTitle>Muat Data CSV</DialogTitle>
          <DialogDescription>
            Unggah hasil analisis dari model Anda. Kolom mengikuti format pada brief (Nama Hotel, Kategori,
            Bintang, Rating, AI_Sentiment, AI_Primary_Theme, Review Time).
          </DialogDescription>
        </DialogHeader>

        <div className="flex flex-col gap-3">
          <FileInput
            label="Data Ulasan (wajib)"
            hint="Klik untuk memilih file CSV ulasan per baris"
            file={reviews}
            onChange={(f) => {
              setReviews(f);
              setError(null);
            }}
          />
          <FileInput
            label="Frasa Kunci per Hotel (opsional)"
            hint="Nama_Hotel, Top_Positif_Phrase, Bobot_Pos, Top_Negatif_Phrase, Bobot_Neg"
            file={phrases}
            onChange={setPhrases}
          />
          {error && <p style={{ fontSize: 12, color: "#ef4444" }}>{error}</p>}
        </div>

        <DialogFooter className="gap-2 sm:justify-between">
          {source === "uploaded" ? (
            <Button variant="ghost" onClick={() => { resetToMock(); onOpenChange(false); }} className="gap-1.5">
              <RotateCcw className="size-4" /> Kembali ke data demo
            </Button>
          ) : (
            <span />
          )}
          <Button onClick={handleParse} disabled={loading} className="gap-1.5">
            {loading ? <Loader2 className="size-4 animate-spin" /> : <FileUp className="size-4" />}
            {loading ? "Memproses…" : "Proses & Tampilkan"}
          </Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  );
}
