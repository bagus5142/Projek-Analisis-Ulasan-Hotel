import { createContext, useContext, useEffect, useMemo, useState, type ReactNode } from "react";
import { DEFAULT_FILTER, type Filter } from "../lib/aggregate";
import { useData } from "./DataContext";

interface FilterCtx {
  filter: Filter;
  setKategori: (k: Filter["kategori"]) => void;
  setBintang: (b: Filter["bintang"]) => void;
  setHotelId: (id: string | null) => void;
  setPeriode: (p: [number, number]) => void;
  reset: () => void;
}

const Ctx = createContext<FilterCtx | null>(null);

export function FilterProvider({ children }: { children: ReactNode }) {
  const { source } = useData();
  const [filter, setFilter] = useState<Filter>(DEFAULT_FILTER);

  // Saat sumber data berganti (mis. setelah upload), reset pilihan hotel.
  useEffect(() => {
    setFilter((f) => ({ ...f, hotelId: null }));
  }, [source]);

  const value = useMemo<FilterCtx>(
    () => ({
      filter,
      setKategori: (kategori) => setFilter((f) => ({ ...f, kategori, hotelId: null })),
      setBintang: (bintang) => setFilter((f) => ({ ...f, bintang, hotelId: null })),
      setHotelId: (hotelId) => setFilter((f) => ({ ...f, hotelId })),
      setPeriode: (periode) => setFilter((f) => ({ ...f, periode })),
      reset: () => setFilter(DEFAULT_FILTER),
    }),
    [filter],
  );

  return <Ctx.Provider value={value}>{children}</Ctx.Provider>;
}

export function useFilter() {
  const c = useContext(Ctx);
  if (!c) throw new Error("useFilter must be used within FilterProvider");
  return c;
}
