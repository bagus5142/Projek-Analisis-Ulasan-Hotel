import { createContext, useContext, useMemo, useState, type ReactNode } from "react";
import { MOCK_HOTELS } from "../data/mockData";
import type { DataSource, HotelAgg } from "../data/types";

interface DataCtx {
  hotels: HotelAgg[];
  source: DataSource;
  setUploaded: (hotels: HotelAgg[]) => void;
  resetToMock: () => void;
}

const Ctx = createContext<DataCtx | null>(null);

export function DataProvider({ children }: { children: ReactNode }) {
  const [hotels, setHotels] = useState<HotelAgg[]>(MOCK_HOTELS);
  const [source, setSource] = useState<DataSource>("mock");

  const value = useMemo<DataCtx>(
    () => ({
      hotels,
      source,
      setUploaded: (h) => {
        setHotels(h);
        setSource("uploaded");
      },
      resetToMock: () => {
        setHotels(MOCK_HOTELS);
        setSource("mock");
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
