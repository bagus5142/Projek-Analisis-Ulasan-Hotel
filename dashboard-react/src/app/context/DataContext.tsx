import { createContext, useContext, useMemo, useState, type ReactNode } from "react";
import hotelsData from "../data/hotels.json";
import type { DataSource, HotelAgg } from "../data/types";

interface DataCtx {
  hotels: HotelAgg[];
  source: DataSource;
  setUploaded: (hotels: HotelAgg[]) => void;
  resetToMock: () => void;
}

const Ctx = createContext<DataCtx | null>(null);

export function DataProvider({ children }: { children: ReactNode }) {
  const [hotels, setHotels] = useState<HotelAgg[]>(hotelsData as HotelAgg[]);
  const [source, setSource] = useState<DataSource>("uploaded");

  const value = useMemo<DataCtx>(
    () => ({
      hotels,
      source,
      setUploaded: (h) => {
        setHotels(h);
        setSource("uploaded");
      },
      resetToMock: () => {
        setHotels(hotelsData as HotelAgg[]);
        setSource("uploaded");
      },
    }),
    [hotels, source],
  );

  return <Ctx.Provider value={value}>{children}</Ctx.Provider>;
}

export function useData() {
  const c = useContext(Ctx);
  if (!c) throw new Error("useData must be used within DataProvider");
  return c;
}
