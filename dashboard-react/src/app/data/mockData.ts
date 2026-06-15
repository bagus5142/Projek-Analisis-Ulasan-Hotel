import { ASPECTS, MONTHS, type Aspect, type Kategori, type Star } from "./constants";
import type { AspectScore, HotelAgg, MonthlyPoint, Phrase } from "./types";

// Deterministic seeded RNG (mulberry32) so the demo data is stable across renders.
function mulberry32(seed: number) {
  return function () {
    seed |= 0;
    seed = (seed + 0x6d2b79f5) | 0;
    let t = Math.imul(seed ^ (seed >>> 15), 1 | seed);
    t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
}

interface Seed {
  nama: string;
  kategori: Kategori;
  bintang: Star;
  totalUlasan: number;
  basePos: number; // target % positif
}

// Total dirancang agar sesuai agregat brief: BUMN 55.697, Kompetitor 110.265 (total 165.962).
const SEEDS: Seed[] = [
  // BUMN (jumlah = 55.697)
  { nama: "Grand Inna Kuta", kategori: "BUMN", bintang: "bintang5", totalUlasan: 9800, basePos: 76 },
  { nama: "The Grand Bali Beach", kategori: "BUMN", bintang: "bintang5", totalUlasan: 9100, basePos: 78 },
  { nama: "Grand Inna Malioboro", kategori: "BUMN", bintang: "bintang4", totalUlasan: 8800, basePos: 73 },
  { nama: "Inna Samudra Beach", kategori: "BUMN", bintang: "bintang3", totalUlasan: 6497, basePos: 68 },
  { nama: "Grand Inna Medan", kategori: "BUMN", bintang: "bintang4", totalUlasan: 6100, basePos: 71 },
  { nama: "Inna Bali Heritage", kategori: "BUMN", bintang: "bintang4", totalUlasan: 5200, basePos: 70 },
  { nama: "Banaran 9 Resort", kategori: "BUMN", bintang: "bintang4", totalUlasan: 4200, basePos: 74 },
  { nama: "Inna Parapat", kategori: "BUMN", bintang: "bintang3", totalUlasan: 3400, basePos: 65 },
  { nama: "Inna Tretes", kategori: "BUMN", bintang: "bintang3", totalUlasan: 2600, basePos: 63 },
  // KOMPETITOR (jumlah = 110.265)
  { nama: "Mercure Jakarta", kategori: "KOMPETITOR", bintang: "bintang4", totalUlasan: 16465, basePos: 76 },
  { nama: "Hotel Indonesia Kempinski", kategori: "KOMPETITOR", bintang: "bintang5", totalUlasan: 14200, basePos: 84 },
  { nama: "The Trans Luxury Bandung", kategori: "KOMPETITOR", bintang: "bintang5", totalUlasan: 13100, basePos: 83 },
  { nama: "The Ritz-Carlton Jakarta", kategori: "KOMPETITOR", bintang: "bintang5", totalUlasan: 12800, basePos: 85 },
  { nama: "Padma Resort Ubud", kategori: "KOMPETITOR", bintang: "bintang5", totalUlasan: 11500, basePos: 82 },
  { nama: "Harris Hotel", kategori: "KOMPETITOR", bintang: "bintang4", totalUlasan: 9300, basePos: 75 },
  { nama: "Santika Premiere", kategori: "KOMPETITOR", bintang: "bintang4", totalUlasan: 8600, basePos: 74 },
  { nama: "Aston Priority Simatupang", kategori: "KOMPETITOR", bintang: "bintang4", totalUlasan: 7400, basePos: 73 },
  { nama: "Swiss-Belhotel", kategori: "KOMPETITOR", bintang: "bintang4", totalUlasan: 6900, basePos: 72 },
  { nama: "POP! Hotel", kategori: "KOMPETITOR", bintang: "bintang3", totalUlasan: 5200, basePos: 69 },
  { nama: "favehotel", kategori: "KOMPETITOR", bintang: "bintang3", totalUlasan: 4800, basePos: 68 },
];

// Bobot porsi ulasan yang menyebut tiap aspek (jumlah > 1 karena 1 ulasan bisa banyak tema).
const ASPECT_WEIGHT: Record<Aspect, number> = {
  Kebersihan: 0.42,
  "Kualitas Kamar": 0.5,
  "Fasilitas Hotel": 0.38,
  "Makanan & Minuman": 0.47,
  "Pelayanan Staf": 0.55,
  "Kecepatan Layanan": 0.28,
  "Proses Check-in/out": 0.22,
  Lokasi: 0.4,
  Harga: 0.35,
  Keamanan: 0.18,
  "Penanganan Keluhan": 0.15,
  "Fasilitas Khusus": 0.2,
};

// Bias kekuatan/kelemahan per aspek (poin % ditambahkan ke base positif).
const ASPECT_BIAS: Record<Aspect, number> = {
  Kebersihan: 4,
  "Kualitas Kamar": 2,
  "Fasilitas Hotel": -2,
  "Makanan & Minuman": 5,
  "Pelayanan Staf": 6,
  "Kecepatan Layanan": -8,
  "Proses Check-in/out": -5,
  Lokasi: 9,
  Harga: -3,
  Keamanan: 3,
  "Penanganan Keluhan": -11,
  "Fasilitas Khusus": 0,
};

// BUMN cenderung lebih lemah pada aspek operasional tertentu (narasi proyek).
const BUMN_ASPECT_PENALTY: Partial<Record<Aspect, number>> = {
  "Kecepatan Layanan": -6,
  "Penanganan Keluhan": -7,
  "Fasilitas Hotel": -4,
  "Proses Check-in/out": -3,
};

const POS_PHRASES = [
  "staf ramah", "sarapan enak", "kamar bersih", "lokasi strategis", "pemandangan indah",
  "pelayanan memuaskan", "kolam renang bagus", "kebun kopi", "kasur nyaman", "harga terjangkau",
  "dekat pantai", "suasana tenang", "resepsionis cepat", "makanan lezat", "wifi kencang",
  "parkir luas", "kamar mandi bersih", "view gunung", "spa relaksasi", "interior elegan",
];
const NEG_PHRASES = [
  "ac rusak", "pelayanan lambat", "tidak terawat", "kamar bau", "wifi lemot",
  "sarapan monoton", "kamar mandi kotor", "harga mahal", "check-in lama", "staf cuek",
  "kasur keras", "antrian panjang", "lift rusak", "kamar sempit", "bising malam hari",
  "keluhan diabaikan", "air panas mati", "parkir penuh", "kebersihan kurang", "bau rokok",
];

function buildHotel(seed: Seed, idx: number): HotelAgg {
  const rng = mulberry32(idx * 9973 + 7);
  const { totalUlasan, basePos, kategori } = seed;

  const pctNeu = 2.4 + rng() * 1.8; // ~2.4–4.2%
  const pctPos = basePos + (rng() - 0.5) * 3;
  const pctNeg = 100 - pctPos - pctNeu;

  // Aspek
  const aspek = {} as Record<Aspect, AspectScore>;
  for (const a of ASPECTS) {
    const total = Math.round(totalUlasan * ASPECT_WEIGHT[a] * (0.85 + rng() * 0.3));
    let posRate = pctPos + ASPECT_BIAS[a] + (rng() - 0.5) * 6;
    if (kategori === "BUMN" && BUMN_ASPECT_PENALTY[a]) posRate += BUMN_ASPECT_PENALTY[a]!;
    posRate = Math.max(20, Math.min(98, posRate));
    const neuShare = pctNeu / 100;
    const pos = Math.round(total * (posRate / 100) * (1 - neuShare));
    const neg = Math.max(0, total - pos - Math.round(total * neuShare));
    aspek[a] = { pos, neg, total };
  }

  // Frasa kunci — pilih deterministik dari pool, urutkan berdasar bobot.
  const pickPhrases = (pool: string[], sign: 1 | -1): Phrase[] => {
    const used = new Set<number>();
    const out: Phrase[] = [];
    while (out.length < 5) {
      const i = Math.floor(rng() * pool.length);
      if (used.has(i)) continue;
      used.add(i);
      const mag = 0.3 + rng() * 1.6;
      out.push({ phrase: pool[i], bobot: +(sign * mag).toFixed(4) });
    }
    return out.sort((a, b) => Math.abs(b.bobot) - Math.abs(a.bobot));
  };
  const frasaPos = pickPhrases(POS_PHRASES, 1);
  const frasaNeg = pickPhrases(NEG_PHRASES, -1);

  // Distribusi ulasan per bulan (sedikit tren naik) + sentimen per bulan.
  const monthWeights = MONTHS.map(() => 0.6 + rng());
  const wSum = monthWeights.reduce((s, x) => s + x, 0);
  const slope = (rng() - 0.35) * 0.8; // kecenderungan membaik dari waktu ke waktu
  const trenBulanan: MonthlyPoint[] = MONTHS.map((bulan, i) => {
    const vol = Math.max(1, Math.round((totalUlasan * monthWeights[i]) / wSum));
    const mp = Math.max(40, Math.min(96, pctPos + slope * (i - 5.5) + (rng() - 0.5) * 5));
    const volNeu = Math.round(vol * (pctNeu / 100));
    const volPos = Math.round((vol - volNeu) * (mp / 100));
    const volNeg = Math.max(0, vol - volNeu - volPos);
    return { bulan, pctPos: +mp.toFixed(1), volPos, volNeg, volNeu };
  });

  // Distribusi rating 1..5 dari komposisi sentimen.
  const posCount = Math.round(totalUlasan * (pctPos / 100));
  const negCount = Math.round(totalUlasan * (pctNeg / 100));
  const neuCount = Math.max(0, totalUlasan - posCount - negCount);
  const r5 = Math.round(posCount * 0.62);
  const r4 = posCount - r5;
  const r3 = neuCount + Math.round(negCount * 0.22);
  const r2 = Math.round(negCount * 0.33);
  const r1 = Math.max(0, negCount - Math.round(negCount * 0.22) - r2);
  const ratingDist = [r1, r2, r3, r4, r5];
  const ratingSum = ratingDist.reduce((s, c, i) => s + c * (i + 1), 0);
  const rating = +(ratingSum / Math.max(1, totalUlasan)).toFixed(2);

  return {
    id: `h${idx}`,
    nama: seed.nama,
    kategori,
    bintang: seed.bintang,
    totalUlasan,
    rating,
    pctPos: +pctPos.toFixed(1),
    pctNeg: +pctNeg.toFixed(1),
    pctNeu: +pctNeu.toFixed(1),
    ratingDist,
    aspek,
    frasaPos,
    frasaNeg,
    trenBulanan,
  };
}

export const MOCK_HOTELS: HotelAgg[] = SEEDS.map(buildHotel);
