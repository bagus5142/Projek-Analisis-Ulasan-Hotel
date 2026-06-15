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
  "Des 2011",
  "Jan 2012",
  "Des 2012",
  "Jan 2013",
  "Des 2013",
  "Jan 2014",
  "Des 2014",
  "Jan 2015",
  "Des 2015",
  "Jan 2016",
  "Des 2016",
  "Jan 2017",
  "Des 2017",
  "Jan 2018",
  "Des 2018",
  "Jan 2019",
  "Des 2019",
  "Jan 2020",
  "Des 2020",
  "Jan 2021",
  "Des 2021",
  "Jan 2022",
  "Des 2022",
  "Jan 2023",
  "Des 2023",
  "Jan 2024",
  "Des 2024",
  "Jan 2025",
  "Feb 2025",
  "Mar 2025",
  "Apr 2025",
  "Mei 2025",
  "Jun 2025",
  "Jul 2025",
  "Agt 2025",
  "Sep 2025",
  "Okt 2025",
  "Nov 2025",
  "Des 2025",
  "Jan 2026"
] as const;

export const fmt = (n: number) => n.toLocaleString("id-ID");
export const pct = (n: number) => `${n.toLocaleString("id-ID", { maximumFractionDigits: 1 })}%`;
