import { useMemo } from "react";
import { MessageSquare, ThumbsDown, ThumbsUp, Star } from "lucide-react";
import { COLORS, KATEGORI_LABEL, STAR_LABEL, fmt, pct } from "../../data/constants";
import { useData } from "../../context/DataContext";
import { useFilter } from "../../context/FilterContext";
import {
  aspectPosScore,
  aspectSentiment,
  findHotel,
  metrics,
  scopeHotels,
  topicDistribution,
} from "../../lib/aggregate";
import { MetricCard } from "../charts/MetricCard";
import { ChartCard } from "../charts/ChartCard";
import { DivergingAspectBar } from "../charts/DivergingAspectBar";
import { TopicDonut } from "../charts/TopicDonut";
import { AspectRadar } from "../charts/AspectRadar";
import { KeyPhrases } from "../charts/KeyPhrasesCard";
import { Badge } from "../ui/badge";

export function OverviewPage() {
  const { hotels } = useData();
  const { filter } = useFilter();
  const scoped = useMemo(() => scopeHotels(hotels, filter), [hotels, filter]);
  const selected = findHotel(hotels, filter.hotelId);

  const base = selected ? [selected] : scoped;
  const m = useMemo(() => metrics(base, filter), [base, filter]);
  const aspects = useMemo(() => aspectSentiment(base), [base]);
  const topics = useMemo(() => topicDistribution(base), [base]);

  const radarSeries = useMemo(() => {
    if (!selected) return [];
    const kategoriAvg = aspectPosScore(scoped.filter((h) => h.kategori === selected.kategori));
    return [
      { name: selected.nama, color: COLORS.bumn, scores: aspectPosScore([selected]) },
      { name: `Rata-rata ${KATEGORI_LABEL[selected.kategori]}`, color: COLORS.komp, scores: kategoriAvg },
    ];
  }, [selected, scoped]);

  return (
    <div className="flex flex-col gap-6">
      {selected && (
        <div className="flex flex-wrap items-center gap-2">
          <h2 style={{ fontSize: 18, fontWeight: 700 }}>{selected.nama}</h2>
          <Badge variant="secondary">{KATEGORI_LABEL[selected.kategori]}</Badge>
          <Badge variant="outline">{STAR_LABEL[selected.bintang]}</Badge>
        </div>
      )}

      <div className="grid grid-cols-2 gap-4 lg:grid-cols-4">
        <MetricCard label="Total Ulasan" value={fmt(m.totalUlasan)} icon={<MessageSquare className="size-4" />} hint="pada periode terpilih" />
        <MetricCard label="Sentimen Positif" value={pct(m.pctPos)} accent={COLORS.pos} icon={<ThumbsUp className="size-4" />} />
        <MetricCard label="Sentimen Negatif" value={pct(m.pctNeg)} accent={COLORS.neg} icon={<ThumbsDown className="size-4" />} />
        <MetricCard label="Rating Rata-rata" value={`${m.rating.toLocaleString("id-ID")} / 5`} accent={COLORS.komp} icon={<Star className="size-4" />} />
      </div>

      <ChartCard title="Sentimen per Aspek" description="Persentase ulasan positif (kanan) vs negatif (kiri) untuk tiap aspek pelayanan">
        <DivergingAspectBar data={aspects} />
      </ChartCard>

      <div className="grid grid-cols-1 gap-6 lg:grid-cols-2">
        <ChartCard title="Distribusi Topik" description="Aspek yang paling sering dibahas tamu">
          <TopicDonut data={topics} />
        </ChartCard>

        {selected ? (
          <ChartCard title="Profil Aspek" description={`${selected.nama} vs rata-rata ${KATEGORI_LABEL[selected.kategori]}`}>
            <AspectRadar series={radarSeries} />
          </ChartCard>
        ) : (
          <ChartCard title="Profil Aspek" description="Pilih satu hotel pada filter untuk melihat profil & frasa kunci">
            <div className="flex h-[300px] items-center justify-center text-center text-muted-foreground" style={{ fontSize: 13 }}>
              Pilih satu hotel di sidebar untuk menampilkan radar profil aspek dan frasa kunci.
            </div>
          </ChartCard>
        )}
      </div>

      {selected && (
        <ChartCard title="Frasa Kunci" description="Akar masalah kelemahan dan kekuatan menurut ulasan tamu">
          <KeyPhrases frasaPos={selected.frasaPos} frasaNeg={selected.frasaNeg} />
        </ChartCard>
      )}
    </div>
  );
}
