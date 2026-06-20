import { useMemo } from "react";
import { COLORS } from "../../data/constants";
import { useData } from "../../context/DataContext";
import { useFilter } from "../../context/FilterContext";
import {
  aspectByKategori,
  aspectPosScore,
  gapAnalysis,
  scopeHotels,
} from "../../lib/aggregate";
import { ChartCard } from "../charts/ChartCard";
import { GroupedAspectBar } from "../charts/GroupedAspectBar";
import { GapDivergingBar } from "../charts/GapDivergingBar";
import { AspectHeatmap } from "../charts/AspectHeatmap";
import { InsightBox } from "../charts/InsightBox";

export function ComparisonPage() {
  const { hotels } = useData();
  const { filter } = useFilter();
  const scoped = useMemo(() => scopeHotels(hotels, { ...filter, kategori: "SEMUA" }), [hotels, filter]);

  const grouped = useMemo(() => aspectByKategori(scoped), [scoped]);
  const gap = useMemo(() => gapAnalysis(scoped), [scoped]);

  const heatScores = useMemo(
    () => ({
      BUMN: aspectPosScore(scoped.filter((h) => h.kategori === "BUMN")),
      KOMPETITOR: aspectPosScore(scoped.filter((h) => h.kategori === "KOMPETITOR")),
    }),
    [scoped],
  );

  const groupInsight = useMemo(() => {
    if (!grouped.length) return "";
    let bumnWins = 0;
    grouped.forEach(g => { if (g.BUMN > g.KOMPETITOR) bumnWins++; });
    const pct = Math.round((bumnWins / grouped.length) * 100);
    return `BUMN mendominasi ${bumnWins} dari ${grouped.length} aspek pelayanan (${pct}% win-rate). ${pct >= 50 ? 'Posisi BUMN secara umum lebih tangguh dan siap memimpin standar industri.' : 'Kompetitor menunjukkan keunggulan yang mengancam kepemimpinan BUMN di pasar.'}`;
  }, [grouped]);

  const gapInsight = useMemo(() => {
    if (!gap.length) return "";
    const sorted = [...gap].sort((a, b) => b.gap - a.gap);
    const win = sorted[0];
    const lose = sorted[sorted.length - 1];
    return `Keunggulan margin BUMN paling tebal ada di lini "${win.aspek}" (+${win.gap.toFixed(1)}%). Namun, manajemen harus mewaspadai lini "${lose.aspek}" di mana Kompetitor berhasil memimpin dengan selisih ${Math.abs(lose.gap).toFixed(1)}%.`;
  }, [gap]);

  return (
    <div className="flex flex-col gap-6">
      <ChartCard title="Sentimen Positif per Aspek" description="Perbandingan BUMN vs Kompetitor di seluruh aspek pelayanan">
        <GroupedAspectBar data={grouped} />
        <InsightBox text={groupInsight} />
      </ChartCard>

      <div className="grid grid-cols-1 gap-6 lg:grid-cols-2">
        <ChartCard title="Analisis Selisih (Gap)" description="Aspek tempat BUMN unggul atau tertinggal dari Kompetitor">
          <GapDivergingBar data={gap} />
          <InsightBox text={gapInsight} />
        </ChartCard>
        <ChartCard title="Peta Panas Aspek" description="Skor positif per aspek, BUMN vs Kompetitor">
          <AspectHeatmap
            columns={[{ key: "BUMN", label: "BUMN" }, { key: "KOMPETITOR", label: "Kompetitor" }]}
            scores={heatScores}
          />
          <InsightBox text="Distribusi warna pekat (hijau) mengindikasikan dominasi area kekuatan sentimen, memberikan panduan visual cepat bagi pengambil keputusan." />
        </ChartCard>
      </div>
    </div>
  );
}
