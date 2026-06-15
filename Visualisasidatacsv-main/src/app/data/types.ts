import type { Aspect, Kategori, Star } from "./constants";

export interface Phrase {
  phrase: string;
  bobot: number;
}

export interface AspectScore {
  pos: number; // jumlah ulasan positif menyebut aspek ini
  neg: number; // jumlah ulasan negatif
  total: number; // total ulasan menyebut aspek ini
}

export interface MonthlyPoint {
  bulan: string;
  pctPos: number;
  volPos: number;
  volNeg: number;
  volNeu: number;
}

export interface HotelAgg {
  id: string;
  nama: string;
  kategori: Kategori;
  bintang: Star;
  totalUlasan: number;
  rating: number;
  pctPos: number;
  pctNeg: number;
  pctNeu: number;
  ratingDist: number[]; // index 0..4 = rating 1..5
  aspek: Record<Aspect, AspectScore>;
  frasaPos: Phrase[];
  frasaNeg: Phrase[];
  trenBulanan: MonthlyPoint[];
}

export type DataSource = "mock" | "uploaded";
