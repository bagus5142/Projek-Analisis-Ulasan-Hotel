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
} from "recharts";
import { COLORS } from "../../data/constants";
import type { TrendPoint } from "../../lib/aggregate";

export function TrendLine({ data }: { data: TrendPoint[] }) {
  const avg = data.length ? +(data.reduce((s, d) => s + d.pctPos, 0) / data.length).toFixed(1) : 0;
  return (
    <ResponsiveContainer width="100%" height={300}>
      <ComposedChart data={data} margin={{ top: 8, right: 16, left: 0, bottom: 4 }}>
        <defs>
          <linearGradient id="posFill" x1="0" y1="0" x2="0" y2="1">
            <stop offset="0%" stopColor={COLORS.pos} stopOpacity={0.25} />
            <stop offset="100%" stopColor={COLORS.pos} stopOpacity={0} />
          </linearGradient>
        </defs>
        <CartesianGrid stroke={COLORS.grid} vertical={false} />
        <XAxis dataKey="bulan" tick={{ fontSize: 11, fill: COLORS.muted }} axisLine={false} tickLine={false} />
        <YAxis domain={[40, 100]} tickFormatter={(v) => `${v}%`} tick={{ fontSize: 11, fill: COLORS.muted }} axisLine={false} tickLine={false} />
        <Tooltip formatter={(v: number) => [`${v}%`, "Sentimen Positif"]} contentStyle={{ fontSize: 12, borderRadius: 8, border: `1px solid ${COLORS.grid}` }} />
        <ReferenceLine y={avg} stroke={COLORS.muted} strokeDasharray="5 5" label={{ value: `Rata-rata ${avg}%`, position: "right", fontSize: 11, fill: COLORS.muted }} />
        <Area type="monotone" dataKey="pctPos" stroke="none" fill="url(#posFill)" />
        <Line type="monotone" dataKey="pctPos" stroke={COLORS.pos} strokeWidth={2.5} dot={{ r: 3, fill: COLORS.pos }} />
      </ComposedChart>
    </ResponsiveContainer>
  );
}
