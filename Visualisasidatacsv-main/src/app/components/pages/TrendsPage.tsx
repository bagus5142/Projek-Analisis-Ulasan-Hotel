import { useMemo } from "react";
import { COLORS } from "../../data/constants";
import { useData } from "../../context/DataContext";
import { useFilter } from "../../context/FilterContext";
import { monthlyTrend, scopeHotels } from "../../lib/aggregate";
import { ChartCard } from "../charts/ChartCard";
import { TrendLine } from "../charts/TrendLine";
import { VolumeStackedBar } from "../charts/VolumeStackedBar";
import { Legend } from "../charts/Legend";
import {
  CartesianGrid,
  Line,
  LineChart,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";

export function TrendsPage() {
  const { hotels } = useData();
  const { filter } = useFilter();
  const scoped = useMemo(() => scopeHotels(hotels, filter), [hotels, filter]);

  const trend = useMemo(() => monthlyTrend(scoped, filter), [scoped, filter]);
  const compare = useMemo(() => {
    const bumn = monthlyTrend(scoped.filter((h) => h.kategori === "BUMN"), filter);
    const komp = monthlyTrend(scoped.filter((h) => h.kategori === "KOMPETITOR"), filter);
    return bumn.map((p, i) => ({ bulan: p.bulan, BUMN: p.pctPos, KOMPETITOR: komp[i]?.pctPos ?? 0 }));
  }, [scoped, filter]);

  return (
    <div className="flex flex-col gap-6">
      <ChartCard title="Tren Sentimen Positif" description="Persentase ulasan positif per bulan dengan garis rata-rata">
        <TrendLine data={trend} />
      </ChartCard>

      <ChartCard title="Volume Ulasan per Bulan" description="Jumlah ulasan positif dan negatif setiap bulan">
        <VolumeStackedBar data={trend} />
      </ChartCard>

      <ChartCard title="Perbandingan Tren: BUMN vs Kompetitor" description="% sentimen positif bulanan kedua kelompok">
        <ResponsiveContainer width="100%" height={300}>
          <LineChart data={compare} margin={{ top: 8, right: 16, left: 0, bottom: 4 }}>
            <CartesianGrid stroke={COLORS.grid} vertical={false} />
            <XAxis dataKey="bulan" tick={{ fontSize: 11, fill: COLORS.muted }} axisLine={false} tickLine={false} />
            <YAxis domain={[40, 100]} tickFormatter={(v) => `${v}%`} tick={{ fontSize: 11, fill: COLORS.muted }} axisLine={false} tickLine={false} />
            <Tooltip formatter={(v: number, n) => [`${v}%`, n === "KOMPETITOR" ? "Kompetitor" : "BUMN"]} contentStyle={{ fontSize: 12, borderRadius: 8, border: `1px solid ${COLORS.grid}` }} />
            <Line type="monotone" dataKey="BUMN" stroke={COLORS.bumn} strokeWidth={2.5} dot={{ r: 3 }} />
            <Line type="monotone" dataKey="KOMPETITOR" stroke={COLORS.komp} strokeWidth={2.5} dot={{ r: 3 }} />
          </LineChart>
        </ResponsiveContainer>
        <div className="mt-3">
          <Legend items={[{ label: "BUMN", color: COLORS.bumn }, { label: "Kompetitor", color: COLORS.komp }]} />
        </div>
      </ChartCard>
    </div>
  );
}
