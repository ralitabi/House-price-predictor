import { useEffect, useState } from "react";
import {
  CartesianGrid,
  Line,
  LineChart,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";
import { TrendingUp } from "lucide-react";
import { fetchMarketTrends } from "../services/api";

function CustomTooltip({ active, payload, label }) {
  if (!active || !payload?.length) return null;
  return (
    <div className="bg-slate-900 border border-slate-700 rounded-xl px-4 py-2.5 text-sm shadow-xl">
      <p className="text-slate-400 mb-0.5">{label}</p>
      <p className="font-semibold text-white">
        £{Number(payload[0].value).toLocaleString("en-GB")}
      </p>
    </div>
  );
}

export default function MarketTrends({ region }) {
  const [data, setData]     = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError]   = useState(null);

  useEffect(() => {
    setLoading(true);
    setError(null);
    fetchMarketTrends(region)
      .then(setData)
      .catch(() => setError("Could not load trend data"))
      .finally(() => setLoading(false));
  }, [region]);

  const trends = data?.trends ?? [];
  const yMin = trends.length ? Math.min(...trends.map((t) => t.average_price)) * 0.97 : 0;
  const yMax = trends.length ? Math.max(...trends.map((t) => t.average_price)) * 1.03 : 1;

  return (
    <div className="bg-slate-900/60 backdrop-blur rounded-2xl border border-slate-800 p-6">
      <div className="flex items-center justify-between mb-5">
        <h2 className="text-lg font-semibold flex items-center gap-2">
          <TrendingUp className="w-5 h-5 text-indigo-400" />
          24-Month Price Trend — {region}
        </h2>
        {data?.source && (
          <span className="text-xs text-slate-600">Source: {data.source}</span>
        )}
      </div>

      {loading ? (
        <div className="h-64 flex items-center justify-center text-slate-500">Loading…</div>
      ) : error ? (
        <div className="h-64 flex items-center justify-center text-red-400 text-sm">{error}</div>
      ) : trends.length === 0 ? (
        <div className="h-64 flex items-center justify-center text-slate-500">No data available</div>
      ) : (
        <ResponsiveContainer width="100%" height={280}>
          <LineChart data={trends} margin={{ top: 4, right: 16, left: 0, bottom: 0 }}>
            <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" />
            <XAxis
              dataKey="month"
              tickFormatter={(v) => v.slice(0, 7)}
              tick={{ fill: "#64748b", fontSize: 11 }}
              tickLine={false}
              axisLine={false}
            />
            <YAxis
              domain={[yMin, yMax]}
              tickFormatter={(v) => `£${(v / 1000).toFixed(0)}k`}
              tick={{ fill: "#64748b", fontSize: 11 }}
              tickLine={false}
              axisLine={false}
              width={52}
            />
            <Tooltip content={<CustomTooltip />} />
            <Line
              type="monotone"
              dataKey="average_price"
              stroke="#6366f1"
              strokeWidth={2.5}
              dot={false}
              activeDot={{ r: 5, fill: "#818cf8", strokeWidth: 0 }}
            />
          </LineChart>
        </ResponsiveContainer>
      )}
    </div>
  );
}
