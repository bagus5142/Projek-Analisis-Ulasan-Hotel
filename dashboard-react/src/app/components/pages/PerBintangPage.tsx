import { useMemo } from "react";
import { COLORS, STAR_LABEL, STARS, fmt, pct, type Star } from "../../data/constants";
import { useData } from "../../context/DataContext";
import { useFilter } from "../../context/FilterContext";
import { byStar, metrics, ratingDistribution, scopeHotels } from "../../lib/aggregate";
import { ChartCard } from "../charts/ChartCard";
import { StarGroupedBar } from "../charts/StarGroupedBar";
import { RatingHistogram } from "../charts/RatingHistogram";
import { InsightBox } from "../charts/InsightBox";
import { Card } from "../ui/card";

export function PerBintangPage() {
  const { hotels } = useData();
  const { filter } = useFilter();
  const scoped = useMemo(() => scopeHotels(hotels, { ...filter, kategori: "SEMUA", bintang: "SEMUA" }), [hotels, filter]);

  const star = useMemo(() => byStar(scoped), [scoped]);
  const ratings = useMemo(() => ratingDistribution(scoped), [scoped]);

  const tiles = useMemo(
    () =>
      STARS.map((s) => {
        const subset = scoped.filter((h) => h.bintang === s);
        const m = metrics(subset, { ...filter, periode: [0, 11] });
        const bumn = subset.filter((h) => h.kategori === "BUMN").length;
        const komp = subset.filter((h) => h.kategori === "KOMPETITOR").length;
        return { star: s as Star, m, bumn, komp };
      }),
    [scoped, filter],
  );

  const starInsight = useMemo(() => {
    if (!star.length) return "";
    let bestStar = "";
    let highestScore = 0;
    let bumnWin = false;
    star.forEach(s => {
      const max = Math.max(s.BUMN, s.KOMPETITOR);
      if (max > highestScore) { 
        highestScore = max; 
        bestStar = s.bintang; 
        bumnWin = s.BUMN >= s.KOMPETITOR;
      }
    });
    return `Ekspektasi kualitas layanan tertinggi terpenuhi pada segmen Bintang ${bestStar} (skor puncak ${highestScore}% oleh ${bumnWin ? 'BUMN' : 'Kompetitor'}). Tren ini menegaskan bahwa penambahan kelas bintang harus diikuti dengan peningkatan standar layanan yang proporsional.`;
  }, [star]);

  const ratingInsight = useMemo(() => {
    if (!ratings.length) return "";
    let bumn5 = ratings.find(r => r.rating === "5★")?.BUMN || 0;
    let komp5 = ratings.find(r => r.rating === "5★")?.KOMPETITOR || 0;
    if (bumn5 >= komp5) {
      return `BUMN memimpin dalam mendulang rating 5-bintang sempurna (${bumn5.toLocaleString("id-ID")} ulasan), membuktikan kemampuan eksekusi layanan yang melampaui ekspektasi ("Wow Factor") dibandingkan kompetitor.`;
    } else {
      return `Kompetitor mendominasi perolehan rating 5-bintang absolut (${komp5.toLocaleString("id-ID")} ulasan), mengindikasikan mereka lebih mahir menciptakan pengalaman berkesan ("Wow Factor") yang mendorong loyalitas merek.`;
    }
  }, [ratings]);

  return (
    <div className="flex flex-col gap-6">
      <div className="grid grid-cols-1 gap-4 md:grid-cols-3">
        {tiles.map((t) => (
          <Card key={t.star} className="gap-0 p-5">
            <div className="flex items-center justify-between">
              <span style={{ fontSize: 14, fontWeight: 600 }}>{STAR_LABEL[t.star]}</span>
              <span className="text-muted-foreground" style={{ fontSize: 12 }}>{fmt(t.m.totalUlasan)} ulasan</span>
            </div>
            <div className="mt-3" style={{ fontSize: 28, fontWeight: 700, color: COLORS.pos }}>{pct(t.m.pctPos)}</div>
            <div className="text-muted-foreground" style={{ fontSize: 12 }}>sentimen positif · rating {t.m.rating.toLocaleString("id-ID")}</div>
            <div className="mt-3 flex gap-3" style={{ fontSize: 12 }}>
              <span className="flex items-center gap-1.5"><span className="inline-block size-2.5 rounded-sm" style={{ background: COLORS.bumn }} />{t.bumn} BUMN</span>
              <span className="flex items-center gap-1.5"><span className="inline-block size-2.5 rounded-sm" style={{ background: COLORS.komp }} />{t.komp} Kompetitor</span>
            </div>
          </Card>
        ))}
      </div>

      <ChartCard title="Sentimen Positif per Kelas Bintang" description="BUMN vs Kompetitor pada tiap tingkat bintang">
        <StarGroupedBar data={star} />
        <InsightBox text={starInsight} />
      </ChartCard>

      <ChartCard title="Distribusi Rating" description="Sebaran rating 1–5 bintang, BUMN vs Kompetitor">
        <RatingHistogram data={ratings} />
        <InsightBox text={ratingInsight} />
      </ChartCard>
    </div>
  );
}
