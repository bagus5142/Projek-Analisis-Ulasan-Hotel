import { ASPECTS, MONTHS, STARS, type Aspect, type Kategori, type Star } from "../data/constants";
import type { HotelAgg } from "../data/types";

export interface Filter {
  kategori: "SEMUA" | Kategori;
  bintang: "SEMUA" | Star;
  hotelId: string | null;
  periode: [number, number]; // index bulan inklusif
}

export const DEFAULT_FILTER: Filter = {
  kategori: "SEMUA",
  bintang: "SEMUA",
  hotelId: null,
  periode: [0, MONTHS.length - 1],
};

/** Hotel yang lolos filter kategori + bintang (filter hotel tunggal ditangani terpisah). */
export function scopeHotels(hotels: HotelAgg[], f: Filter): HotelAgg[] {
  return hotels.filter(
    (h) =>
      (f.kategori === "SEMUA" || h.kategori === f.kategori) &&
      (f.bintang === "SEMUA" || h.bintang === f.bintang),
  );
}

/** Faktor porsi periode terpilih terhadap 12 bulan (untuk menskalakan total). */
function periodeFactor(f: Filter): number {
  const span = f.periode[1] - f.periode[0] + 1;
  return span / MONTHS.length;
}

export interface Metrics {
  totalUlasan: number;
  pctPos: number;
  pctNeg: number;
  pctNeu: number;
  rating: number;
}

export function metrics(hotels: HotelAgg[], f: Filter): Metrics {
  const factor = periodeFactor(f);
  let total = 0;
  let pos = 0;
  let neg = 0;
  let neu = 0;
  let ratingW = 0;
  for (const h of hotels) {
    const t = h.totalUlasan;
    total += t;
    pos += (t * h.pctPos) / 100;
    neg += (t * h.pctNeg) / 100;
    neu += (t * h.pctNeu) / 100;
    ratingW += h.rating * t;
  }
  const scaledTotal = Math.round(total * factor);
  return {
    totalUlasan: scaledTotal,
    pctPos: total ? +((pos / total) * 100).toFixed(1) : 0,
    pctNeg: total ? +((neg / total) * 100).toFixed(1) : 0,
    pctNeu: total ? +((neu / total) * 100).toFixed(1) : 0,
    rating: total ? +(ratingW / total).toFixed(2) : 0,
  };
}

export interface AspectRow {
  aspek: Aspect;
  pos: number; // % positif
  neg: number; // % negatif (nilai negatif untuk diverging)
  posCount: number;
  negCount: number;
  total: number;
}

export function aspectSentiment(hotels: HotelAgg[]): AspectRow[] {
  return ASPECTS.map((a) => {
    let pos = 0;
    let neg = 0;
    let total = 0;
    for (const h of hotels) {
      pos += h.aspek[a].pos;
      neg += h.aspek[a].neg;
      total += h.aspek[a].total;
    }
    const base = pos + neg || 1;
    return {
      aspek: a,
      pos: +((pos / base) * 100).toFixed(1),
      neg: -+((neg / base) * 100).toFixed(1),
      posCount: pos,
      negCount: neg,
      total,
    };
  }).sort((x, y) => y.pos - x.pos);
}

/** Skor positif per aspek (0-100) untuk radar. */
export function aspectPosScore(hotels: HotelAgg[]): Record<Aspect, number> {
  const out = {} as Record<Aspect, number>;
  for (const a of ASPECTS) {
    let pos = 0;
    let neg = 0;
    for (const h of hotels) {
      pos += h.aspek[a].pos;
      neg += h.aspek[a].neg;
    }
    out[a] = +((pos / (pos + neg || 1)) * 100).toFixed(1);
  }
  return out;
}

export function topicDistribution(hotels: HotelAgg[]): { aspek: Aspect; total: number }[] {
  return ASPECTS.map((a) => {
    let total = 0;
    for (const h of hotels) total += h.aspek[a].total;
    return { aspek: a, total };
  }).sort((x, y) => y.total - x.total);
}

export interface GapRow {
  aspek: Aspect;
  bumn: number;
  komp: number;
  gap: number; // bumn - komp
}

export function gapAnalysis(hotels: HotelAgg[]): GapRow[] {
  const bumn = aspectPosScore(hotels.filter((h) => h.kategori === "BUMN"));
  const komp = aspectPosScore(hotels.filter((h) => h.kategori === "KOMPETITOR"));
  return ASPECTS.map((a) => ({
    aspek: a,
    bumn: bumn[a],
    komp: komp[a],
    gap: +(bumn[a] - komp[a]).toFixed(1),
  })).sort((x, y) => y.gap - x.gap);
}

/** % positif per aspek, terpisah BUMN vs Kompetitor (grouped bar). */
export function aspectByKategori(hotels: HotelAgg[]) {
  const bumn = aspectPosScore(hotels.filter((h) => h.kategori === "BUMN"));
  const komp = aspectPosScore(hotels.filter((h) => h.kategori === "KOMPETITOR"));
  return ASPECTS.map((a) => ({ aspek: a, BUMN: bumn[a], KOMPETITOR: komp[a] }));
}

/** % positif per bintang, terpisah kategori (grouped bar per tier). */
export function byStar(hotels: HotelAgg[]) {
  return STARS.map((s) => {
    const subset = hotels.filter((h) => h.bintang === s);
    const m = (k: Kategori) => {
      const list = subset.filter((h) => h.kategori === k);
      const tot = list.reduce((sx, h) => sx + h.totalUlasan, 0);
      const pos = list.reduce((sx, h) => sx + (h.totalUlasan * h.pctPos) / 100, 0);
      return tot ? +((pos / tot) * 100).toFixed(1) : 0;
    };
    return { bintang: s, BUMN: m("BUMN"), KOMPETITOR: m("KOMPETITOR") };
  });
}

export function ratingDistribution(hotels: HotelAgg[]) {
  const out = [1, 2, 3, 4, 5].map((r) => ({ rating: `${r}★`, BUMN: 0, KOMPETITOR: 0, total: 0 }));
  for (const h of hotels) {
    for (let i = 0; i < 5; i++) {
      out[i][h.kategori] += h.ratingDist[i];
      out[i].total += h.ratingDist[i];
    }
  }
  return out;
}

export interface RankRow {
  rank: number;
  id: string;
  nama: string;
  kategori: Kategori;
  bintang: Star;
  totalUlasan: number;
  pctPos: number;
  pctNeg: number;
  rating: number;
  aspekTerlemah: Aspect;
}

export function rankHotels(hotels: HotelAgg[]): RankRow[] {
  const rows = hotels
    .map((h) => {
      let worst: Aspect = ASPECTS[0];
      let worstScore = Infinity;
      for (const a of ASPECTS) {
        const s = h.aspek[a].pos / (h.aspek[a].pos + h.aspek[a].neg || 1);
        if (s < worstScore) {
          worstScore = s;
          worst = a;
        }
      }
      return {
        id: h.id,
        nama: h.nama,
        kategori: h.kategori,
        bintang: h.bintang,
        totalUlasan: h.totalUlasan,
        pctPos: h.pctPos,
        pctNeg: h.pctNeg,
        rating: h.rating,
        aspekTerlemah: worst,
      };
    })
    .sort((a, b) => b.pctPos - a.pctPos);
  return rows.map((r, i) => ({ rank: i + 1, ...r }));
}

export interface BubblePoint {
  id: string;
  nama: string;
  kategori: Kategori;
  x: number; // % positif
  y: number; // rating
  z: number; // volume
}

export function bubbleData(hotels: HotelAgg[]): BubblePoint[] {
  return hotels.map((h) => ({
    id: h.id,
    nama: h.nama,
    kategori: h.kategori,
    x: h.pctPos,
    y: h.rating,
    z: h.totalUlasan,
  }));
}

export interface TrendPoint {
  bulan: string;
  pctPos: number;
  volPos: number;
  volNeg: number;
}

export function monthlyTrend(hotels: HotelAgg[], f: Filter): TrendPoint[] {
  const [a, b] = f.periode;
  const out: TrendPoint[] = [];
  MONTHS.forEach((bulan, i) => {
    if (i < a || i > b) return;
    let volPos = 0;
    let volNeg = 0;
    for (const h of hotels) {
      const p = h.trenBulanan[i];
      volPos += p.volPos;
      volNeg += p.volNeg;
    }
    out.push({
      bulan,
      pctPos: +((volPos / (volPos + volNeg || 1)) * 100).toFixed(1),
      volPos,
      volNeg,
    });
  });
  return out;
}

export function avgOf(nums: number[]): number {
  if (!nums.length) return 0;
  return +(nums.reduce((s, x) => s + x, 0) / nums.length).toFixed(1);
}

export function findHotel(hotels: HotelAgg[], id: string | null): HotelAgg | null {
  if (!id) return null;
  return hotels.find((h) => h.id === id) ?? null;
}
