import { useState, useMemo } from "react";
import { COLORS, MONTHS } from "../../data/constants";
import { useData } from "../../context/DataContext";
import { useFilter } from "../../context/FilterContext";
import { monthlyTrend, yearlyTrend, scopeHotels } from "../../lib/aggregate";
import { ChartCard } from "../charts/ChartCard";
import { TrendLine } from "../charts/TrendLine";
import { VolumeStackedBar } from "../charts/VolumeStackedBar";
import { Legend } from "../charts/Legend";
import { InsightBox } from "../charts/InsightBox";
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
  const [viewMode, setViewMode] = useState<"tahunan" | "bulanan">("tahunan");
  
  const years = useMemo(() => Array.from(new Set(MONTHS.map(m => m.split(' ')[1]))).filter(Boolean), []);
  const [selectedYear, setSelectedYear] = useState<string>(years[years.length - 1] || "2025");
  
  const scoped = useMemo(() => scopeHotels(hotels, filter), [hotels, filter]);

  const yearTrend = useMemo(() => yearlyTrend(scoped, filter), [scoped, filter]);
  const monthTrendAll = useMemo(() => monthlyTrend(scoped, filter), [scoped, filter]);
  
  const trend = useMemo(() => {
    if (viewMode === "tahunan") return yearTrend;
    return monthTrendAll.filter(d => d.bulan.endsWith(selectedYear));
  }, [viewMode, yearTrend, monthTrendAll, selectedYear]);
  
  const compare = useMemo(() => {
    if (viewMode === "tahunan") {
      const bumn = yearlyTrend(scoped.filter((h) => h.kategori === "BUMN"), filter);
      const komp = yearlyTrend(scoped.filter((h) => h.kategori === "KOMPETITOR"), filter);
      return bumn.map((p, i) => ({ 
        bulan: p.bulan, 
        BUMN_Pos: p.volPos || null, 
        BUMN_Neg: p.volNeg || null,
        KOMP_Pos: komp[i]?.volPos || null,
        KOMP_Neg: komp[i]?.volNeg || null,
      }));
    } else {
      const bumn = monthlyTrend(scoped.filter((h) => h.kategori === "BUMN"), filter).filter(d => d.bulan.endsWith(selectedYear));
      const komp = monthlyTrend(scoped.filter((h) => h.kategori === "KOMPETITOR"), filter).filter(d => d.bulan.endsWith(selectedYear));
      return bumn.map((p, i) => ({ 
        bulan: p.bulan, 
        BUMN_Pos: p.volPos || null, 
        BUMN_Neg: p.volNeg || null,
        KOMP_Pos: komp[i]?.volPos || null,
        KOMP_Neg: komp[i]?.volNeg || null,
      }));
    }
  }, [scoped, filter, viewMode, selectedYear]);

  const trendInsight = useMemo(() => {
    if (!trend.length) return "";
    let maxPos = 0;
    let maxBulan = "";
    let sumPos = 0;
    trend.forEach(d => {
      if (d.volPos > maxPos) { maxPos = d.volPos; maxBulan = d.bulan; }
      sumPos += d.volPos;
    });
    const avg = Math.round(sumPos / trend.length);
    return `Kinerja sentimen terbaik tercatat pada ${maxBulan} dengan ${maxPos.toLocaleString("id-ID")} ulasan positif. Rata-rata pergerakan sentimen positif berada di angka ${avg.toLocaleString("id-ID")} ulasan/periode.`;
  }, [trend]);

  const volumeInsight = useMemo(() => {
    if (!trend.length) return "";
    let maxTotal = 0;
    let maxBulan = "";
    trend.forEach(d => {
      const t = d.volPos + d.volNeg;
      if (t > maxTotal) { maxTotal = t; maxBulan = d.bulan; }
    });
    return `Intensitas interaksi tamu tertinggi terjadi pada ${maxBulan} dengan total ${maxTotal.toLocaleString("id-ID")} ulasan, menandakan periode puncak keterlibatan (engagement) pelanggan.`;
  }, [trend]);

  const compareInsight = useMemo(() => {
    if (!compare.length) return "";
    let bumnPos = 0;
    let kompPos = 0;
    compare.forEach(d => {
      bumnPos += (d.BUMN_Pos || 0);
      kompPos += (d.KOMP_Pos || 0);
    });
    if (bumnPos >= kompPos) {
      return `Secara keseluruhan, BUMN memimpin pangsa sentimen positif dengan total ${bumnPos.toLocaleString("id-ID")} ulasan, melampaui Kompetitor (${kompPos.toLocaleString("id-ID")} ulasan). BUMN berhasil mempertahankan keunggulan reputasi di pasar.`;
    } else {
      return `Kompetitor saat ini memimpin pangsa sentimen positif dengan total ${kompPos.toLocaleString("id-ID")} ulasan, melampaui BUMN (${bumnPos.toLocaleString("id-ID")} ulasan). Evaluasi strategi layanan kompetitif mungkin diperlukan untuk mengejar ketertinggalan.`;
    }
  }, [compare]);

  return (
    <div className="flex flex-col gap-6">
      <div className="flex justify-end items-center gap-4">
        {viewMode === "bulanan" && (
          <div className="flex items-center gap-2">
            <span className="text-sm font-medium text-muted-foreground">Pilih Tahun:</span>
            <select 
              value={selectedYear} 
              onChange={e => setSelectedYear(e.target.value)}
              className="text-sm border border-border rounded-md px-2 py-1.5 bg-background text-foreground focus:outline-none focus:ring-2 focus:ring-primary/20"
            >
              {years.map(y => <option key={y} value={y}>{y}</option>)}
            </select>
          </div>
        )}
        <div className="flex items-center gap-1 bg-muted/50 p-1 rounded-lg border border-border">
          <button
            onClick={() => setViewMode("tahunan")}
            className={`px-3 py-1.5 text-sm font-medium rounded-md transition-colors ${viewMode === "tahunan" ? "bg-background shadow-sm text-foreground" : "text-muted-foreground hover:text-foreground"}`}
          >
            Tahunan
          </button>
          <button
            onClick={() => setViewMode("bulanan")}
            className={`px-3 py-1.5 text-sm font-medium rounded-md transition-colors ${viewMode === "bulanan" ? "bg-background shadow-sm text-foreground" : "text-muted-foreground hover:text-foreground"}`}
          >
            Bulanan
          </button>
        </div>
      </div>

      <ChartCard title={`Tren Sentimen Positif (${viewMode === "tahunan" ? "Tahunan" : "Bulanan"})`} description={`Volume ulasan positif & negatif per ${viewMode === "tahunan" ? "tahun" : "bulan"} dengan garis rata-rata`}>
        <TrendLine data={trend} />
        <InsightBox text={trendInsight} />
      </ChartCard>

      <ChartCard title={`Volume Ulasan (${viewMode === "tahunan" ? "Tahunan" : "Bulanan"})`} description={`Jumlah ulasan positif dan negatif setiap ${viewMode === "tahunan" ? "tahun" : "bulan"}`}>
        <VolumeStackedBar data={trend} />
        <InsightBox text={volumeInsight} />
      </ChartCard>

      <ChartCard title="Perbandingan Volume: BUMN vs Kompetitor" description="Jumlah volume ulasan positif & negatif kedua kelompok">
        <ResponsiveContainer width="100%" height={300}>
          <LineChart data={compare} margin={{ top: 8, right: 16, left: 0, bottom: 4 }}>
            <CartesianGrid stroke={COLORS.grid} vertical={false} />
            <XAxis dataKey="bulan" tick={{ fontSize: 11, fill: COLORS.muted }} axisLine={false} tickLine={false} />
            <YAxis tickFormatter={(v) => v.toLocaleString()} tick={{ fontSize: 11, fill: COLORS.muted }} axisLine={false} tickLine={false} />
            <Tooltip 
              formatter={(v: number, n: string) => [
                v.toLocaleString(), 
                n === "BUMN_Pos" ? "BUMN (Positif)" :
                n === "BUMN_Neg" ? "BUMN (Negatif)" :
                n === "KOMP_Pos" ? "Kompetitor (Positif)" : "Kompetitor (Negatif)"
              ]} 
              contentStyle={{ fontSize: 12, borderRadius: 8, border: `1px solid ${COLORS.grid}` }} 
            />
            <Line type="monotone" name="BUMN_Pos" dataKey="BUMN_Pos" stroke={COLORS.bumn} strokeWidth={2.5} dot={{ r: 3 }} connectNulls />
            <Line type="monotone" name="BUMN_Neg" dataKey="BUMN_Neg" stroke={COLORS.bumn} strokeDasharray="5 5" strokeWidth={2.5} dot={{ r: 3 }} connectNulls />
            <Line type="monotone" name="KOMP_Pos" dataKey="KOMP_Pos" stroke={COLORS.komp} strokeWidth={2.5} dot={{ r: 3 }} connectNulls />
            <Line type="monotone" name="KOMP_Neg" dataKey="KOMP_Neg" stroke={COLORS.komp} strokeDasharray="5 5" strokeWidth={2.5} dot={{ r: 3 }} connectNulls />
          </LineChart>
        </ResponsiveContainer>
        <div className="mt-3">
          <Legend items={[
            { label: "BUMN Positif", color: COLORS.bumn }, 
            { label: "BUMN Negatif", color: COLORS.bumn, dashed: true },
            { label: "Kompetitor Positif", color: COLORS.komp },
            { label: "Kompetitor Negatif", color: COLORS.komp, dashed: true }
          ]} />
        </div>
        <InsightBox text={compareInsight} />
      </ChartCard>
    </div>
  );
}
