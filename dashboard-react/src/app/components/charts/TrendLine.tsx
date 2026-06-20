import {
  Area,
  CartesianGrid,
  ComposedChart,
  Line,
  ReferenceLine,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
  Legend as RechartsLegend,
} from "recharts";
import { COLORS } from "../../data/constants";
import type { TrendPoint } from "../../lib/aggregate";

export function TrendLine({ data }: { data: TrendPoint[] }) {
  const avg = data.length ? Math.round(data.reduce((s, d) => s + d.volPos, 0) / data.length) : 0;
  return (
    <ResponsiveContainer width="100%" height={300}>
      <ComposedChart data={data} margin={{ top: 8, right: 16, left: 0, bottom: 4 }}>
        <defs>
          <linearGradient id="posFill" x1="0" y1="0" x2="0" y2="1">
            <stop offset="0%" stopColor={COLORS.pos} stopOpacity={0.25} />
            <stop offset="100%" stopColor={COLORS.pos} stopOpacity={0} />
          </linearGradient>
          <linearGradient id="negFill" x1="0" y1="0" x2="0" y2="1">
            <stop offset="0%" stopColor={COLORS.neg} stopOpacity={0.25} />
            <stop offset="100%" stopColor={COLORS.neg} stopOpacity={0} />
          </linearGradient>
        </defs>
        <CartesianGrid stroke={COLORS.grid} vertical={false} />
        <XAxis dataKey="bulan" tick={{ fontSize: 11, fill: COLORS.muted }} axisLine={false} tickLine={false} />
        <YAxis tickFormatter={(v) => v.toLocaleString()} tick={{ fontSize: 11, fill: COLORS.muted }} axisLine={false} tickLine={false} />
        <Tooltip 
          formatter={(v: number, name: string) => [v.toLocaleString(), name === "volPos" ? "Volume Positif" : "Volume Negatif"]} 
          contentStyle={{ fontSize: 12, borderRadius: 8, border: `1px solid ${COLORS.grid}` }} 
        />
        <ReferenceLine y={avg} stroke={COLORS.muted} strokeDasharray="5 5" label={{ value: `Rata-rata Positif: ${avg.toLocaleString()}`, position: "top", fontSize: 11, fill: COLORS.muted }} />
        <Area type="monotone" dataKey="volPos" stroke="none" fill="url(#posFill)" connectNulls />
        <Line type="monotone" name="volPos" dataKey="volPos" stroke={COLORS.pos} strokeWidth={2.5} dot={{ r: 3, fill: COLORS.pos }} connectNulls />
        
        <Area type="monotone" dataKey="volNeg" stroke="none" fill="url(#negFill)" connectNulls />
        <Line type="monotone" name="volNeg" dataKey="volNeg" stroke={COLORS.neg} strokeWidth={2.5} dot={{ r: 3, fill: COLORS.neg }} connectNulls />
        <RechartsLegend verticalAlign="top" wrapperStyle={{ fontSize: 12, paddingBottom: 10 }} formatter={(value) => value === "volPos" ? "Volume Positif" : "Volume Negatif"} />
      </ComposedChart>
    </ResponsiveContainer>
  );
}
