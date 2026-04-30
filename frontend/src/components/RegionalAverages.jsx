import { useEffect, useState } from "react";
import {
  Bar,
  BarChart,
  Cell,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";
import { MapPin } from "lucide-react";
import { fetchRegionalAverages } from "../services/api";
import ChartTooltip from "./ChartTooltip";

export default function RegionalAverages() {
  const [data, setData] = useState(null);

  useEffect(() => {
    fetchRegionalAverages().then(setData).catch(console.error);
  }, []);

  const sorted = (data?.data ?? []).slice().sort((a, b) => b.average_price - a.average_price);

  return (
    <div className="bg-slate-900/60 backdrop-blur rounded-2xl border border-slate-800 p-6">
      <div className="flex items-center justify-between mb-5">
        <h2 className="text-lg font-semibold flex items-center gap-2">
          <MapPin className="w-5 h-5 text-indigo-400" />
          Average Prices by Region
        </h2>
        {data?.source && (
          <span className="text-xs text-slate-600">Source: {data.source}</span>
        )}
      </div>

      {sorted.length === 0 ? (
        <div className="h-72 flex items-center justify-center text-slate-500">Loading…</div>
      ) : (
        <ResponsiveContainer width="100%" height={320}>
          <BarChart
            data={sorted}
            layout="vertical"
            margin={{ top: 4, right: 24, left: 0, bottom: 0 }}
          >
            <XAxis
              type="number"
              tickFormatter={(v) => `£${(v / 1000).toFixed(0)}k`}
              tick={{ fill: "#64748b", fontSize: 11 }}
              axisLine={false}
              tickLine={false}
            />
            <YAxis
              type="category"
              dataKey="region"
              tick={{ fill: "#94a3b8", fontSize: 11 }}
              width={172}
              axisLine={false}
              tickLine={false}
            />
            <Tooltip content={<ChartTooltip />} cursor={{ fill: "rgba(99,102,241,0.08)" }} />
            <Bar dataKey="average_price" radius={[0, 6, 6, 0]}>
              {sorted.map((_, i) => (
                <Cell key={i} fill={i === 0 ? "#6366f1" : "#1e293b"} />
              ))}
            </Bar>
          </BarChart>
        </ResponsiveContainer>
      )}
    </div>
  );
}
