import { Bar, BarChart, Cell, ResponsiveContainer, Tooltip, XAxis, YAxis } from "recharts";
import { COLORS, fmt, type Aspect } from "../../data/constants";

const PALETTE = [
  "#3b82f6", "#22c55e", "#f59e0b", "#8b5cf6", "#ef4444", "#06b6d4",
  "#ec4899", "#84cc16", "#f97316", "#14b8a6", "#a855f7", "#64748b",
];

export function TopicBar({ data }: { data: { aspek: Aspect; total: number }[] }) {
  // Sort data by total descending to show largest bars first
  const sorted = [...data].sort((a, b) => b.total - a.total).slice(0, 12);
  const grand = sorted.reduce((s, d) => s + d.total, 0) || 1;

  return (
    <div className="flex flex-col w-full h-full min-h-[280px]">
      <ResponsiveContainer width="100%" height={280}>
        <BarChart data={sorted} layout="vertical" margin={{ top: 0, right: 30, left: 0, bottom: 0 }}>
          <XAxis type="number" hide />
          <YAxis 
            dataKey="aspek" 
            type="category" 
            width={130} 
            tick={{ fontSize: 12 }} 
            axisLine={false} 
            tickLine={false} 
          />
          <Tooltip
            cursor={{ fill: "transparent" }}
            formatter={(v: number, n) => [`${fmt(v)} (${((v / grand) * 100).toFixed(1)}%)`, "Total"]}
            contentStyle={{ fontSize: 12, borderRadius: 8, border: `1px solid ${COLORS.grid}` }}
          />
          <Bar dataKey="total" radius={[0, 4, 4, 0]} barSize={16}>
            {sorted.map((d, i) => (
              <Cell key={d.aspek} fill={PALETTE[i % PALETTE.length]} />
            ))}
          </Bar>
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
}
