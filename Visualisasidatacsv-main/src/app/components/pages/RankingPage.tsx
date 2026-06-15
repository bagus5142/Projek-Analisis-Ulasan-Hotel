import { useMemo } from "react";
import { COLORS, KATEGORI_LABEL, STAR_LABEL, fmt } from "../../data/constants";
import { useData } from "../../context/DataContext";
import { useFilter } from "../../context/FilterContext";
import { bubbleData, rankHotels, scopeHotels } from "../../lib/aggregate";
import { ChartCard } from "../charts/ChartCard";
import { BubbleScatter } from "../charts/BubbleScatter";
import { Badge } from "../ui/badge";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "../ui/table";

function posColor(v: number): string {
  if (v >= 80) return "#dcfce7";
  if (v >= 72) return "#ecfccb";
  if (v >= 65) return "#fef9c3";
  if (v >= 55) return "#fed7aa";
  return "#fee2e2";
}

export function RankingPage() {
  const { hotels } = useData();
  const { filter } = useFilter();
  const scoped = useMemo(() => scopeHotels(hotels, { ...filter, kategori: "SEMUA" }), [hotels, filter]);
  const rows = useMemo(() => rankHotels(scoped), [scoped]);
  const bubbles = useMemo(() => bubbleData(scoped), [scoped]);

  return (
    <div className="flex flex-col gap-6">
      <ChartCard title="Peringkat Hotel" description="Diurutkan berdasarkan % sentimen positif tertinggi">
        <Table>
          <TableHeader>
            <TableRow>
              <TableHead className="w-12">#</TableHead>
              <TableHead>Nama Hotel</TableHead>
              <TableHead>Kategori</TableHead>
              <TableHead>Bintang</TableHead>
              <TableHead className="text-right">Total Ulasan</TableHead>
              <TableHead className="text-right">% Positif</TableHead>
              <TableHead className="text-right">% Negatif</TableHead>
              <TableHead className="text-right">Rating</TableHead>
              <TableHead>Aspek Terlemah</TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            {rows.map((r) => (
              <TableRow key={r.id}>
                <TableCell className="text-muted-foreground tabular-nums">{r.rank}</TableCell>
                <TableCell style={{ fontWeight: 600 }}>{r.nama}</TableCell>
                <TableCell>
                  <Badge
                    variant="outline"
                    style={{ borderColor: r.kategori === "BUMN" ? COLORS.bumn : COLORS.komp, color: r.kategori === "BUMN" ? COLORS.bumn : COLORS.komp }}
                  >
                    {KATEGORI_LABEL[r.kategori]}
                  </Badge>
                </TableCell>
                <TableCell className="text-muted-foreground">{STAR_LABEL[r.bintang]}</TableCell>
                <TableCell className="text-right tabular-nums">{fmt(r.totalUlasan)}</TableCell>
                <TableCell className="text-right tabular-nums">
                  <span className="rounded-md px-2 py-0.5" style={{ background: posColor(r.pctPos), fontWeight: 600 }}>
                    {r.pctPos}%
                  </span>
                </TableCell>
                <TableCell className="text-right tabular-nums" style={{ color: COLORS.neg }}>{r.pctNeg}%</TableCell>
                <TableCell className="text-right tabular-nums">{r.rating.toLocaleString("id-ID")}</TableCell>
                <TableCell className="text-muted-foreground">{r.aspekTerlemah}</TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </ChartCard>

      <ChartCard title="Positioning Hotel" description="% Positif vs Rating · ukuran titik = jumlah ulasan · garis = rata-rata (4 kuadran)">
        <BubbleScatter data={bubbles} />
      </ChartCard>
    </div>
  );
}
