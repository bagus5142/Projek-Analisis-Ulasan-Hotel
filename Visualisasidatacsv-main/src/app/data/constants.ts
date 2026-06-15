export const ASPECTS = [
  "Kebersihan",
  "Kualitas Kamar",
  "Fasilitas Hotel",
  "Makanan & Minuman",
  "Pelayanan Staf",
  "Kecepatan Layanan",
  "Proses Check-in/out",
  "Lokasi",
  "Harga",
  "Keamanan",
  "Penanganan Keluhan",
  "Fasilitas Khusus",
] as const;

export type Aspect = (typeof ASPECTS)[number];

export const STARS = ["bintang3", "bintang4", "bintang5"] as const;
export type Star = (typeof STARS)[number];

export const STAR_LABEL: Record<Star, string> = {
  bintang3: "Bintang 3",
  bintang4: "Bintang 4",
  bintang5: "Bintang 5",
};

export type Kategori = "BUMN" | "KOMPETITOR";

export const COLORS = {
  pos: "#22c55e",
  neg: "#ef4444",
  neu: "#94a3b8",
  bumn: "#3b82f6",
  komp: "#f59e0b",
  accent: "#8b5cf6",
  posSoft: "#dcfce7",
  negSoft: "#fee2e2",
  grid: "#e5e7eb",
  text: "#111827",
  muted: "#6b7280",
} as const;

export const KATEGORI_COLOR: Record<Kategori, string> = {
  BUMN: COLORS.bumn,
  KOMPETITOR: COLORS.komp,
};

export const KATEGORI_LABEL: Record<Kategori, string> = {
  BUMN: "BUMN",
  KOMPETITOR: "Kompetitor",
};

// 12 bulan terakhir hingga Juni 2026
export const MONTHS = [
  "Jul 25",
  "Agu 25",
  "Sep 25",
  "Okt 25",
  "Nov 25",
  "Des 25",
  "Jan 26",
  "Feb 26",
  "Mar 26",
  "Apr 26",
  "Mei 26",
  "Jun 26",
] as const;

export const fmt = (n: number) => n.toLocaleString("id-ID");
export const pct = (n: number) => `${n.toLocaleString("id-ID", { maximumFractionDigits: 1 })}%`;
