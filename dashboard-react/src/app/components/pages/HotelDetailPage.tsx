import { useMemo, useState } from "react";
import { ASPECTS, COLORS, KATEGORI_LABEL, STAR_LABEL, fmt, pct } from "../../data/constants";
import { useData } from "../../context/DataContext";
import { useFilter } from "../../context/FilterContext";
import { aspectPosScore, monthlyTrend } from "../../lib/aggregate";
import { ChartCard } from "../charts/ChartCard";
import { AspectRadar } from "../charts/AspectRadar";
import { KeyPhrases } from "../charts/KeyPhrasesCard";
import { RatingHistogram } from "../charts/RatingHistogram";
import { TrendLine } from "../charts/TrendLine";
import { MetricCard } from "../charts/MetricCard";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "../ui/select";
import { Badge } from "../ui/badge";

export function HotelDetailPage() {
  const { hotels } = useData();
  const { filter } = useFilter();
  const sorted = useMemo(() => [...hotels].sort((a, b) => a.nama.localeCompare(b.nama)), [hotels]);
  const [id, setId] = useState<string>(filter.hotelId ?? sorted[0]?.id ?? "");
  const hotel = hotels.find((h) => h.id === id) ?? sorted[0];

  const radarSeries = useMemo(() => {
    if (!hotel) return [];
    const kategoriPeers = hotels.filter((h) => h.kategori === hotel.kategori);
    const starPeers = hotels.filter((h) => h.bintang === hotel.bintang);
    return [
      { name: hotel.nama, color: COLORS.bumn, scores: aspectPosScore([hotel]) },
      { name: `Rata-rata ${KATEGORI_LABEL[hotel.kategori]}`, color: COLORS.komp, scores: aspectPosScore(kategoriPeers) },
      { name: `Rata-rata ${STAR_LABEL[hotel.bintang]}`, color: COLORS.accent, scores: aspectPosScore(starPeers) },
    ];
  }, [hotel, hotels]);

  const aspectRows = useMemo(() => {
    if (!hotel) return [];
    return ASPECTS.map((a) => {
      const s = hotel.aspek[a];
      const score = +((s.pos / (s.pos + s.neg || 1)) * 100).toFixed(1);
      return { aspek: a, score, total: s.total };
    }).sort((x, y) => y.score - x.score);
  }, [hotel]);

  const trend = useMemo(() => (hotel ? monthlyTrend([hotel], { ...filter, periode: [0, 11] }) : []), [hotel, filter]);
  const ratingRows = useMemo(() => {
    if (!hotel) return [];
    return [1, 2, 3, 4, 5].map((r) => ({ rating: `${r}★`, BUMN: 0, KOMPETITOR: 0, total: hotel.ratingDist[r - 1] }));
  }, [hotel]);

  if (!hotel) return null;

  return (
    <div className="flex flex-col gap-6">
      <div className="flex flex-col gap-3 sm:flex-row sm:items-end sm:justify-between">
        <div className="max-w-md flex-1">
          <span className="text-muted-foreground mb-1 block uppercase" style={{ fontSize: 11, fontWeight: 600, letterSpacing: "0.05em" }}>Pilih Hotel</span>
          <Select value={id} onValueChange={setId}>
            <SelectTrigger className="w-full"><SelectValue /></SelectTrigger>
            <SelectContent>
              {sorted.map((h) => <SelectItem key={h.id} value={h.id}>{h.nama}</SelectItem>)}
            </SelectContent>
          </Select>
        </div>
        <div className="flex items-center gap-2">
          <Badge variant="outline" style={{ borderColor: hotel.kategori === "BUMN" ? COLORS.bumn : COLORS.komp, color: hotel.kategori === "BUMN" ? COLORS.bumn : COLORS.komp }}>
            {KATEGORI_LABEL[hotel.kategori]}
          </Badge>
          <Badge variant="secondary">{STAR_LABEL[hotel.bintang]}</Badge>
        </div>
      </div>

      <div className="grid grid-cols-2 gap-4 lg:grid-cols-4">
        <MetricCard label="Total Ulasan" value={fmt(hotel.totalUlasan)} />
        <MetricCard label="Sentimen Positif" value={pct(hotel.pctPos)} accent={COLORS.pos} />
        <MetricCard label="Sentimen Negatif" value={pct(hotel.pctNeg)} accent={COLORS.neg} />
        <MetricCard label="Rating" value={`${hotel.rating.toLocaleString("id-ID")} / 5`} accent={COLORS.komp} />
      </div>

      <div className="grid grid-cols-1 gap-6 lg:grid-cols-2">
        <ChartCard title="Profil Aspek" description="Dibandingkan dengan rata-rata kategori dan kelas bintang">
          <AspectRadar series={radarSeries} />
        </ChartCard>
        <ChartCard title="Frasa Kunci" description="Akar masalah kelemahan dan kekuatan">
          <KeyPhrases frasaPos={hotel.frasaPos} frasaNeg={hotel.frasaNeg} />
        </ChartCard>
      </div>

      <div className="grid grid-cols-1 gap-6 lg:grid-cols-2">
        <ChartCard title="Distribusi Rating" description="Sebaran rating 1–5 bintang">
          <RatingHistogram data={ratingRows} split={false} />
        </ChartCard>
        <ChartCard title="Tren Sentimen Positif" description="Perkembangan 12 bulan terakhir">
          <TrendLine data={trend} />
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
      </ChartCard>
    </div>
  );
}
