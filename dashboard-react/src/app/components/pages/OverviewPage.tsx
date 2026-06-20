import { useMemo } from "react";
import { MessageSquare, ThumbsDown, ThumbsUp, Star } from "lucide-react";
import { ASPECTS, COLORS, KATEGORI_LABEL, STAR_LABEL, fmt, pct } from "../../data/constants";
import { useData } from "../../context/DataContext";
import { useFilter } from "../../context/FilterContext";
import {
  aspectPosScore,
  aspectSentiment,
  findHotel,
  metrics,
  scopeHotels,
  topicDistribution,
  monthlyTrend,
} from "../../lib/aggregate";
import { MetricCard } from "../charts/MetricCard";
import { ChartCard } from "../charts/ChartCard";
import { DivergingAspectBar } from "../charts/DivergingAspectBar";
import { TopicBar } from "../charts/TopicBar";
import { AspectRadar } from "../charts/AspectRadar";
import { KeyPhrases } from "../charts/KeyPhrasesCard";
import { RatingHistogram } from "../charts/RatingHistogram";
import { TrendLine } from "../charts/TrendLine";
import { Badge } from "../ui/badge";
import { InsightBox } from "../charts/InsightBox";

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

  const aspectRows = useMemo(() => {
    if (!selected) return [];
    return ASPECTS.map((a) => {
      const s = selected.aspek[a];
      const score = +((s.pos / (s.pos + s.neg || 1)) * 100).toFixed(1);
      return { aspek: a, score, total: s.total };
    }).sort((x, y) => y.score - x.score);
  }, [selected]);

  const trend = useMemo(() => (selected ? monthlyTrend([selected], { ...filter, periode: [0, 11] }) : []), [selected, filter]);
  const ratingRows = useMemo(() => {
    if (!selected) return [];
    return [1, 2, 3, 4, 5].map((r) => ({ rating: `${r}★`, BUMN: 0, KOMPETITOR: 0, total: selected.ratingDist[r - 1] }));
  }, [selected]);

  // Executive Insights Logic
  const aspectInsight = useMemo(() => {
    if (!aspects.length) return "";
    const sortedPos = [...aspects].sort((a, b) => b.pos - a.pos);
    const sortedNeg = [...aspects].sort((a, b) => b.neg - a.neg);
    return `Kekuatan utama terletak pada aspek "${sortedPos[0].aspek}" dengan sentimen positif tertinggi. Sebaliknya, aspek "${sortedNeg[0].aspek}" mencatatkan keluhan terbanyak dan memerlukan atensi manajemen untuk perbaikan segera.`;
  }, [aspects]);

  const topicInsight = useMemo(() => {
    if (!topics.length) return "";
    const top = topics[0];
    return `Tamu sangat vokal menyoroti isu "${top.aspek}" (${top.total.toLocaleString("id-ID")} ulasan). Mengoptimalkan area ini akan memberikan dampak signifikan terhadap kepuasan pelanggan secara keseluruhan.`;
  }, [topics]);

  const radarInsight = useMemo(() => {
    if (!selected) return "";
    return `Membandingkan kinerja spesifik ${selected.nama} terhadap tolok ukur (benchmark) rata-rata ${KATEGORI_LABEL[selected.kategori]}. Area grafik yang berada di bawah garis benchmark merupakan peluang esensial untuk peningkatan layanan.`;
  }, [selected]);

  const ratingInsight = useMemo(() => {
    if (!selected || !ratingRows.length) return "";
    const total = ratingRows.reduce((acc, curr) => acc + curr.total, 0) || 1;
    const bintang45 = ratingRows[3].total + ratingRows[4].total;
    const pct = Math.round((bintang45 / total) * 100);
    return `${pct}% tamu memberikan rating 4 atau 5 bintang, merefleksikan tingkat kepuasan pasar yang ${pct >= 70 ? 'sangat memuaskan dan menguntungkan reputasi merek' : 'membutuhkan evaluasi strategis guna mencapai standar prima'}.`;
  }, [selected, ratingRows]);

  const aspectRankInsight = useMemo(() => {
    if (!aspectRows.length) return "";
    const top = aspectRows[0];
    const bot = aspectRows[aspectRows.length - 1];
    return `Keunggulan kompetitif dipertahankan pada lini "${top.aspek}" dengan skor positif ${top.score}%. Investasi operasional harus difokuskan untuk mendongkrak kelemahan pada lini "${bot.aspek}" (${bot.score}%).`;
  }, [aspectRows]);

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
        <InsightBox text={aspectInsight} />
      </ChartCard>

      <div className="grid grid-cols-1 gap-6 lg:grid-cols-2">
        <ChartCard title="Distribusi Topik" description="Aspek yang paling sering dibahas tamu">
          <TopicBar data={topics} />
          <InsightBox text={topicInsight} />
        </ChartCard>

        {selected ? (
          <ChartCard title="Profil Aspek" description={`${selected.nama} vs rata-rata ${KATEGORI_LABEL[selected.kategori]}`}>
            <AspectRadar series={radarSeries} />
            <InsightBox text={radarInsight} />
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
        <>
          <ChartCard title="Top 5 Kata Kunci" description="Kata-kata yang paling memengaruhi sentimen ulasan tamu">
            <KeyPhrases frasaPos={selected.frasaPos} frasaNeg={selected.frasaNeg} />
          </ChartCard>

          <div className="grid grid-cols-1 gap-6 lg:grid-cols-2">
            <ChartCard title="Distribusi Rating" description="Sebaran rating 1–5 bintang">
              <RatingHistogram data={ratingRows} split={false} />
              <InsightBox text={ratingInsight} />
            </ChartCard>
            <ChartCard title="Tren Sentimen Positif" description="Perkembangan 12 bulan terakhir">
              <TrendLine data={trend} />
              <InsightBox text="Akselerasi performa bulanan mengindikasikan efektivitas strategi layanan terkini dalam mempertahankan retensi konsumen." />
            </ChartCard>
          </div>

          <ChartCard title="Peringkat Aspek" description="Aspek terkuat hingga terlemah berdasarkan skor positif">
            <div className="grid grid-cols-1 gap-x-8 gap-y-2 sm:grid-cols-2">
              {aspectRows.map((r) => (
                <div key={r.aspek} className="flex items-center gap-3">
                  <span className="w-40 truncate" style={{ fontSize: 13 }}>{r.aspek}</span>
                  <div className="bg-muted h-2 flex-1 overflow-hidden rounded-full">
                    <div className="h-full rounded-full" style={{ width: `${r.score}%`, background: r.score >= 70 ? COLORS.pos : r.score >= 55 ? COLORS.komp : COLORS.neg }} />
                  </div>
                  <span className="w-12 text-right tabular-nums" style={{ fontSize: 12, fontWeight: 600 }}>{r.score}%</span>
                </div>
              ))}
            </div>
            <InsightBox text={aspectRankInsight} />
          </ChartCard>
        </>
      )}
    </div>
  );
}
