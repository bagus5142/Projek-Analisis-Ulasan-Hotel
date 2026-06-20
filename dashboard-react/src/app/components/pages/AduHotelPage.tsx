import { useMemo, useState } from "react";
import { COLORS, KATEGORI_LABEL, STAR_LABEL, fmt, pct } from "../../data/constants";
import { useData } from "../../context/DataContext";
import { useFilter } from "../../context/FilterContext";
import { aspectPosScore, scopeHotels } from "../../lib/aggregate";
import type { HotelAgg } from "../../data/types";
import { ChartCard } from "../charts/ChartCard";
import { AspectRadar } from "../charts/AspectRadar";
import { KeyPhrases } from "../charts/KeyPhrasesCard";
import { InsightBox } from "../charts/InsightBox";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "../ui/select";
import { Badge } from "../ui/badge";

const A_COLOR = COLORS.bumn;
const B_COLOR = COLORS.komp;

function HotelPicker({
  label,
  color,
  value,
  onChange,
  hotels,
}: {
  label: string;
  color: string;
  value: string;
  onChange: (v: string) => void;
  hotels: HotelAgg[];
}) {
  return (
    <div className="flex-1">
      <span className="mb-1 block" style={{ fontSize: 11, fontWeight: 600, color }}>{label}</span>
      <Select value={value} onValueChange={onChange}>
        <SelectTrigger className="w-full"><SelectValue placeholder="Pilih hotel" /></SelectTrigger>
        <SelectContent>
          {hotels.map((h) => (
            <SelectItem key={h.id} value={h.id}>
              {h.nama} · {KATEGORI_LABEL[h.kategori]}
            </SelectItem>
          ))}
        </SelectContent>
      </Select>
    </div>
  );
}

function CompareRow({
  label,
  a,
  b,
  better,
}: {
  label: string;
  a: string;
  b: string;
  better?: "a" | "b" | null;
}) {
  return (
    <div className="grid grid-cols-[1fr_auto_1fr] items-center gap-3 border-b py-2 last:border-b-0">
      <div className="text-right tabular-nums" style={{ fontSize: 14, fontWeight: better === "a" ? 700 : 500, color: better === "a" ? A_COLOR : undefined }}>
        {a}
      </div>
      <div className="text-muted-foreground text-center uppercase" style={{ fontSize: 10, letterSpacing: "0.04em", minWidth: 90 }}>
        {label}
      </div>
      <div className="tabular-nums" style={{ fontSize: 14, fontWeight: better === "b" ? 700 : 500, color: better === "b" ? B_COLOR : undefined }}>
        {b}
      </div>
    </div>
  );
}

export function AduHotelPage() {
  const { hotels } = useData();
  const { filter } = useFilter();
  const scoped = useMemo(() => scopeHotels(hotels, { ...filter, kategori: "SEMUA" }), [hotels, filter]);

  const allHotels = useMemo(() => [...scoped].sort((a, b) => a.nama.localeCompare(b.nama)), [scoped]);
  const defaultA = useMemo(() => scoped.find((h) => h.kategori === "BUMN") ?? scoped[0], [scoped]);
  const defaultB = useMemo(() => scoped.find((h) => h.kategori === "KOMPETITOR") ?? scoped[1] ?? scoped[0], [scoped]);

  const [aId, setAId] = useState<string>(defaultA?.id ?? "");
  const [bId, setBId] = useState<string>(defaultB?.id ?? "");
  const hA = scoped.find((h) => h.id === aId) ?? defaultA;
  const hB = scoped.find((h) => h.id === bId) ?? defaultB;

  const radarSeries = useMemo(() => {
    const s = [];
    if (hA) s.push({ name: hA.nama, color: A_COLOR, scores: aspectPosScore([hA]) });
    if (hB) s.push({ name: hB.nama, color: B_COLOR, scores: aspectPosScore([hB]) });
    return s;
  }, [hA, hB]);

  const headToHeadInsight = useMemo(() => {
    if (!hA || !hB) return "";
    let aWins = 0;
    let bWins = 0;
    
    if (hA.pctPos > hB.pctPos) aWins++; else if (hB.pctPos > hA.pctPos) bWins++;
    if (hA.rating > hB.rating) aWins++; else if (hB.rating > hA.rating) bWins++;
    if (hA.pctNeg < hB.pctNeg) aWins++; else if (hB.pctNeg < hA.pctNeg) bWins++;

    let winner = "";
    if (aWins > bWins) winner = `"${hA.nama}" keluar sebagai pemimpin performa`;
    else if (bWins > aWins) winner = `"${hB.nama}" keluar sebagai pemimpin performa`;
    else winner = `kedua hotel menunjukkan kekuatan yang relatif seimbang`;

    return `Berdasarkan metrik utama (Sentimen Positif, Sentimen Negatif, dan Rating), ${winner}. Perbandingan langsung (head-to-head) ini memungkinkan manajemen untuk melakukan 'competitive benchmarking' secara tajam dan membedah profil keunggulan lawan.`;
  }, [hA, hB]);

  return (
    <div className="flex flex-col gap-6">
      <ChartCard title="Adu Hotel" description="Pilih dua hotel mana pun (BUMN atau Kompetitor) lalu bandingkan secara langsung">
        <div className="mb-5 flex flex-col items-stretch gap-3 sm:flex-row sm:items-center">
          <HotelPicker label="HOTEL A" color={A_COLOR} value={aId} onChange={setAId} hotels={allHotels} />
          <span className="text-muted-foreground self-center px-2" style={{ fontSize: 13, fontWeight: 600 }}>vs</span>
          <HotelPicker label="HOTEL B" color={B_COLOR} value={bId} onChange={setBId} hotels={allHotels} />
        </div>

        {hA && hB && (
          <div className="flex flex-col gap-6">
            <div className="flex items-center justify-between gap-2">
              <div className="flex items-center gap-2">
                <span className="inline-block size-3 rounded-sm" style={{ background: A_COLOR }} />
                <span style={{ fontSize: 14, fontWeight: 600 }}>{hA.nama}</span>
                <Badge variant="outline">{KATEGORI_LABEL[hA.kategori]}</Badge>
              </div>
              <div className="flex items-center gap-2">
                <Badge variant="outline">{KATEGORI_LABEL[hB.kategori]}</Badge>
                <span style={{ fontSize: 14, fontWeight: 600 }}>{hB.nama}</span>
                <span className="inline-block size-3 rounded-sm" style={{ background: B_COLOR }} />
              </div>
            </div>

            <div className="rounded-lg border px-4 py-1">
              <CompareRow label="Kategori" a={KATEGORI_LABEL[hA.kategori]} b={KATEGORI_LABEL[hB.kategori]} />
              <CompareRow label="Bintang" a={STAR_LABEL[hA.bintang]} b={STAR_LABEL[hB.bintang]} />
              <CompareRow label="Total Ulasan" a={fmt(hA.totalUlasan)} b={fmt(hB.totalUlasan)} better={hA.totalUlasan >= hB.totalUlasan ? "a" : "b"} />
              <CompareRow label="% Positif" a={pct(hA.pctPos)} b={pct(hB.pctPos)} better={hA.pctPos >= hB.pctPos ? "a" : "b"} />
              <CompareRow label="% Negatif" a={pct(hA.pctNeg)} b={pct(hB.pctNeg)} better={hA.pctNeg <= hB.pctNeg ? "a" : "b"} />
              <CompareRow label="Rating" a={`${hA.rating.toLocaleString("id-ID")} / 5`} b={`${hB.rating.toLocaleString("id-ID")} / 5`} better={hA.rating >= hB.rating ? "a" : "b"} />
            </div>

            <div className="grid grid-cols-1 gap-6 lg:grid-cols-2">
              <div>
                <AspectRadar series={radarSeries} />
              </div>
              <div className="flex flex-col gap-4">
                <div>
                  <div className="mb-2" style={{ fontSize: 13, fontWeight: 600, color: A_COLOR }}>{hA.nama}</div>
                  <KeyPhrases frasaPos={hA.frasaPos} frasaNeg={hA.frasaNeg} />
                </div>
                <div>
                  <div className="mb-2" style={{ fontSize: 13, fontWeight: 600, color: B_COLOR }}>{hB.nama}</div>
                  <KeyPhrases frasaPos={hB.frasaPos} frasaNeg={hB.frasaNeg} />
                </div>
              </div>
            </div>
            <InsightBox text={headToHeadInsight} />
          </div>
        )}
      </ChartCard>
    </div>
  );
}
