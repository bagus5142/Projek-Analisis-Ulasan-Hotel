import {
  CartesianGrid,
  ReferenceLine,
  ResponsiveContainer,
  Scatter,
  ScatterChart,
  Tooltip,
  XAxis,
  YAxis,
  ZAxis,
} from "recharts";
import { COLORS, fmt } from "../../data/constants";
import type { BubblePoint } from "../../lib/aggregate";
import { Legend } from "./Legend";

export function BubbleScatter({ data }: { data: BubblePoint[] }) {
  const bumn = data.filter((d) => d.kategori === "BUMN");
  const komp = data.filter((d) => d.kategori === "KOMPETITOR");
  const avgX = data.length ? data.reduce((s, d) => s + d.x, 0) / data.length : 0;
  const avgY = data.length ? data.reduce((s, d) => s + d.y, 0) / data.length : 0;

  return (
    <div>
      <ResponsiveContainer width="100%" height={380}>
        <ScatterChart margin={{ top: 10, right: 20, left: 0, bottom: 16 }}>
          <CartesianGrid stroke={COLORS.grid} />
          <XAxis
            type="number"
            dataKey="x"
            name="% Positif"
            domain={["dataMin - 3", "dataMax + 3"]}
            tickFormatter={(v) => `${Math.round(v)}%`}
            tick={{ fontSize: 11, fill: COLORS.muted }}
            label={{ value: "% Sentimen Positif", position: "insideBottom", offset: -8, fontSize: 12, fill: COLORS.muted }}
          />
          <YAxis
            type="number"
            dataKey="y"
            name="Rating"
            domain={["dataMin - 0.2", "dataMax + 0.2"]}
            tick={{ fontSize: 11, fill: COLORS.muted }}
            label={{ value: "Rating", angle: -90, position: "insideLeft", fontSize: 12, fill: COLORS.muted }}
          />
          <ZAxis type="number" dataKey="z" range={[80, 900]} name="Ulasan" />
          <ReferenceLine x={avgX} stroke={COLORS.muted} strokeDasharray="4 4" />
          <ReferenceLine y={avgY} stroke={COLORS.muted} strokeDasharray="4 4" />
          <Tooltip
            cursor={{ strokeDasharray: "3 3" }}
            contentStyle={{ fontSize: 12, borderRadius: 8, border: `1px solid ${COLORS.grid}` }}
            formatter={(v: number, n) => {
              if (n === "Ulasan") return [fmt(v), n];
              if (n === "% Positif") return [`${v}%`, n];
              return [v, n];
            }}
            labelFormatter={() => ""}
            content={({ payload }) => {
              if (!payload?.length) return null;
              const p = payload[0].payload as BubblePoint;
              return (
                <div className="rounded-lg border bg-popover px-3 py-2 shadow-md" style={{ fontSize: 12, borderColor: COLORS.grid }}>
                  <div style={{ fontWeight: 600 }}>{p.nama}</div>
                  <div className="text-muted-foreground">{p.kategori === "BUMN" ? "BUMN" : "Kompetitor"}</div>
                  <div>% Positif: {p.x}%</div>
                  <div>Rating: {p.y}</div>
                  <div>Ulasan: {fmt(p.z)}</div>
                </div>
              );
            }}
          />
          <Scatter name="BUMN" data={bumn} fill={COLORS.bumn} fillOpacity={0.65} />
          <Scatter name="Kompetitor" data={komp} fill={COLORS.komp} fillOpacity={0.65} />
        </ScatterChart>
      </ResponsiveContainer>
      <div className="mt-2">
        <Legend items={[{ label: "BUMN", color: COLORS.bumn }, { label: "Kompetitor", color: COLORS.komp }]} />
      </div>
    </div>
  );
}
