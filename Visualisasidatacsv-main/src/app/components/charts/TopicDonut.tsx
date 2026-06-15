import { Cell, Pie, PieChart, ResponsiveContainer, Tooltip } from "recharts";
import { COLORS, fmt, type Aspect } from "../../data/constants";

const PALETTE = [
  "#3b82f6", "#22c55e", "#f59e0b", "#8b5cf6", "#ef4444", "#06b6d4",
  "#ec4899", "#84cc16", "#f97316", "#14b8a6", "#a855f7", "#64748b",
];

export function TopicDonut({ data }: { data: { aspek: Aspect; total: number }[] }) {
  const top = data.slice(0, 12);
  const grand = top.reduce((s, d) => s + d.total, 0) || 1;
  return (
    <div className="flex flex-col items-center gap-4 sm:flex-row">
      <ResponsiveContainer width="100%" height={240} className="max-w-[260px]">
        <PieChart>
          <Pie data={top} dataKey="total" nameKey="aspek" innerRadius={55} outerRadius={95} paddingAngle={1}>
            {top.map((d, i) => (
              <Cell key={d.aspek} fill={PALETTE[i % PALETTE.length]} />
            ))}
          </Pie>
          <Tooltip
            formatter={(v: number, n) => [`${fmt(v)} (${((v / grand) * 100).toFixed(1)}%)`, n as string]}
            contentStyle={{ fontSize: 12, borderRadius: 8, border: `1px solid ${COLORS.grid}` }}
          />
        </PieChart>
      </ResponsiveContainer>
      <div className="grid w-full grid-cols-1 gap-x-4 gap-y-1.5 sm:grid-cols-2">
        {top.map((d, i) => (
          <div key={d.aspek} className="flex items-center justify-between gap-2" style={{ fontSize: 12 }}>
            <span className="flex items-center gap-1.5 truncate">
              <span className="inline-block size-2.5 shrink-0 rounded-sm" style={{ background: PALETTE[i % PALETTE.length] }} />
              <span className="truncate">{d.aspek}</span>
            </span>
            <span className="text-muted-foreground shrink-0">{((d.total / grand) * 100).toFixed(1)}%</span>
          </div>
        ))}
      </div>
    </div>
  );
}
