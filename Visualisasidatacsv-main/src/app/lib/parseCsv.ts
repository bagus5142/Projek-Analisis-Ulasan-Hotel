import Papa from "papaparse";
import { ASPECTS, MONTHS, type Aspect, type Kategori, type Star } from "../data/constants";
import type { AspectScore, HotelAgg, MonthlyPoint, Phrase } from "../data/types";

type Row = Record<string, string>;

interface Acc {
  nama: string;
  kategori: Kategori;
  bintang: Star;
  total: number;
  pos: number;
  neg: number;
  neu: number;
  ratingSum: number;
  ratingDist: number[];
  aspek: Record<Aspect, AspectScore>;
  monthly: Record<number, { pos: number; neg: number; neu: number }>;
}

function get(row: Row, keys: string[]): string {
  for (const k of Object.keys(row)) {
    const norm = k.trim().toLowerCase().replace(/\s+/g, "");
    for (const want of keys) {
      if (norm === want.toLowerCase().replace(/\s+/g, "")) return (row[k] ?? "").trim();
    }
  }
  return "";
}

function normStar(s: string): Star {
  const d = s.replace(/\D/g, "");
  if (d === "5") return "bintang5";
  if (d === "3") return "bintang3";
  return "bintang4";
}

function normKategori(s: string): Kategori {
  return s.trim().toUpperCase().startsWith("BUMN") ? "BUMN" : "KOMPETITOR";
}

function normSentiment(s: string): "pos" | "neg" | "neu" {
  const v = s.trim().toLowerCase();
  if (v.startsWith("pos")) return "pos";
  if (v.startsWith("neg")) return "neg";
  return "neu";
}

function monthIndex(dateStr: string): number {
  // Petakan tanggal ke salah satu dari 12 bulan demo; bila gagal, abaikan.
  const d = new Date(dateStr);
  if (isNaN(d.getTime())) return -1;
  const ref = new Date("2026-06-15");
  const diff = (ref.getFullYear() - d.getFullYear()) * 12 + (ref.getMonth() - d.getMonth());
  const idx = MONTHS.length - 1 - diff;
  return idx >= 0 && idx < MONTHS.length ? idx : -1;
}

function emptyAspek(): Record<Aspect, AspectScore> {
  const a = {} as Record<Aspect, AspectScore>;
  for (const x of ASPECTS) a[x] = { pos: 0, neg: 0, total: 0 };
  return a;
}

function matchAspect(theme: string): Aspect | null {
  const t = theme.trim().toLowerCase();
  if (!t) return null;
  for (const a of ASPECTS) if (a.toLowerCase() === t) return a;
  for (const a of ASPECTS) if (t.includes(a.toLowerCase()) || a.toLowerCase().includes(t)) return a;
  return null;
}

export interface ParseResult {
  hotels: HotelAgg[];
  warnings: string[];
}

/** Parse tabel utama (per ulasan) + opsional tabel frasa, hasilkan HotelAgg[]. */
export function parseDataset(reviewsFile: File, phrasesFile: File | null): Promise<ParseResult> {
  return new Promise((resolve, reject) => {
    const accs = new Map<string, Acc>();

    Papa.parse<Row>(reviewsFile, {
      header: true,
      skipEmptyLines: true,
      worker: true,
      step: (res) => {
        const row = res.data as Row;
        const nama = get(row, ["Nama Hotel", "NamaHotel", "Nama_Hotel", "hotel"]);
        if (!nama) return;
        let acc = accs.get(nama);
        if (!acc) {
          acc = {
            nama,
            kategori: normKategori(get(row, ["Kategori", "kategori"])),
            bintang: normStar(get(row, ["Bintang", "bintang"])),
            total: 0,
            pos: 0,
            neg: 0,
            neu: 0,
            ratingSum: 0,
            ratingDist: [0, 0, 0, 0, 0],
            aspek: emptyAspek(),
            monthly: {},
          };
          accs.set(nama, acc);
        }
        acc.total++;
        const sent = normSentiment(get(row, ["AI_Sentiment", "AISentiment", "sentiment"]));
        acc[sent]++;

        const rating = parseInt(get(row, ["Rating", "rating"]), 10);
        if (rating >= 1 && rating <= 5) {
          acc.ratingSum += rating;
          acc.ratingDist[rating - 1]++;
        }

        const primary = matchAspect(get(row, ["AI_Primary_Theme", "AIPrimaryTheme", "theme"]));
        if (primary) {
          acc.aspek[primary].total++;
          if (sent === "pos") acc.aspek[primary].pos++;
          else if (sent === "neg") acc.aspek[primary].neg++;
        }

        const mi = monthIndex(get(row, ["Review Time", "ReviewTime", "review_time", "date"]));
        if (mi >= 0) {
          const m = acc.monthly[mi] ?? { pos: 0, neg: 0, neu: 0 };
          m[sent]++;
          acc.monthly[mi] = m;
        }
      },
      complete: () => {
        const finish = (phraseMap: Map<string, { pos: Phrase[]; neg: Phrase[] }>) => {
          const hotels: HotelAgg[] = [];
          let i = 0;
          for (const acc of accs.values()) {
            const total = acc.total || 1;
            const trenBulanan: MonthlyPoint[] = MONTHS.map((bulan, idx) => {
              const m = acc.monthly[idx] ?? { pos: 0, neg: 0, neu: 0 };
              return {
                bulan,
                pctPos: +((m.pos / (m.pos + m.neg || 1)) * 100).toFixed(1),
                volPos: m.pos,
                volNeg: m.neg,
                volNeu: m.neu,
              };
            });
            const ph = phraseMap.get(acc.nama);
            hotels.push({
              id: `u${i++}`,
              nama: acc.nama,
              kategori: acc.kategori,
              bintang: acc.bintang,
              totalUlasan: acc.total,
              rating: +(acc.ratingSum / total).toFixed(2),
              pctPos: +((acc.pos / total) * 100).toFixed(1),
              pctNeg: +((acc.neg / total) * 100).toFixed(1),
              pctNeu: +((acc.neu / total) * 100).toFixed(1),
              ratingDist: acc.ratingDist,
              aspek: acc.aspek,
              frasaPos: ph?.pos ?? [],
              frasaNeg: ph?.neg ?? [],
              trenBulanan,
            });
          }
          if (!hotels.length) {
            reject(new Error("Tidak ada baris valid. Pastikan kolom 'Nama Hotel' tersedia."));
            return;
          }
          resolve({ hotels, warnings: [] });
        };

        if (phrasesFile) {
          parsePhrases(phrasesFile).then(finish).catch(() => finish(new Map()));
        } else {
          finish(new Map());
        }
      },
      error: (err) => reject(err),
    });
  });
}

function parsePhrases(file: File): Promise<Map<string, { pos: Phrase[]; neg: Phrase[] }>> {
  return new Promise((resolve, reject) => {
    const map = new Map<string, { pos: Phrase[]; neg: Phrase[] }>();
    Papa.parse<Row>(file, {
      header: true,
      skipEmptyLines: true,
      complete: (res) => {
        for (const row of res.data) {
          const nama = get(row, ["Nama_Hotel", "Nama Hotel", "NamaHotel"]);
          if (!nama) continue;
          const entry = map.get(nama) ?? { pos: [], neg: [] };
          const pp = get(row, ["Top_Positif_Phrase", "TopPositifPhrase"]);
          const np = get(row, ["Top_Negatif_Phrase", "TopNegatifPhrase"]);
          const bp = parseFloat(get(row, ["Bobot_Pos", "BobotPos"]));
          const bn = parseFloat(get(row, ["Bobot_Neg", "BobotNeg"]));
          if (pp) entry.pos.push({ phrase: pp, bobot: isNaN(bp) ? 0 : bp });
          if (np) entry.neg.push({ phrase: np, bobot: isNaN(bn) ? 0 : bn });
          map.set(nama, entry);
        }
        for (const e of map.values()) {
          e.pos.sort((a, b) => Math.abs(b.bobot) - Math.abs(a.bobot));
          e.neg.sort((a, b) => Math.abs(b.bobot) - Math.abs(a.bobot));
          e.pos = e.pos.slice(0, 5);
          e.neg = e.neg.slice(0, 5);
        }
        resolve(map);
      },
      error: (err) => reject(err),
    });
  });
}
