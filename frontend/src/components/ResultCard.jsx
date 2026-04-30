import { Minus, PoundSterling, TrendingDown, TrendingUp } from "lucide-react";

function fmt(n) {
  return `£${Number(n).toLocaleString("en-GB", { maximumFractionDigits: 0 })}`;
}

export default function ResultCard({ result }) {
  const {
    predicted_price,
    lower_bound,
    upper_bound,
    price_per_sqft,
    regional_average,
    vs_regional_avg_pct,
  } = result;

  const diff = vs_regional_avg_pct;
  const TrendIcon = diff > 2 ? TrendingUp : diff < -2 ? TrendingDown : Minus;
  const trendColour =
    diff > 2 ? "text-emerald-400" : diff < -2 ? "text-red-400" : "text-slate-400";

  const range = upper_bound - lower_bound;
  const markerPct =
    range > 0 ? Math.min(90, Math.max(10, ((predicted_price - lower_bound) / range) * 80 + 10)) : 50;

  return (
    <div className="bg-slate-900/60 backdrop-blur rounded-2xl border border-slate-800 p-6 space-y-5">
      <h2 className="text-lg font-semibold flex items-center gap-2">
        <PoundSterling className="w-5 h-5 text-indigo-400" />
        Estimated Value
      </h2>

      {/* Hero price */}
      <div className="text-center py-4">
        <p className="text-5xl font-bold tracking-tight">{fmt(predicted_price)}</p>
        <p className="text-sm text-slate-400 mt-2">
          95% confidence: {fmt(lower_bound)} – {fmt(upper_bound)}
        </p>
      </div>

      {/* Stats */}
      <div className="grid grid-cols-2 gap-3">
        <div className="bg-slate-800/60 rounded-xl p-4">
          <p className="text-xs text-slate-400 mb-1">Price per sq ft</p>
          <p className="text-xl font-semibold">£{Number(price_per_sqft).toLocaleString("en-GB")}</p>
        </div>
        <div className="bg-slate-800/60 rounded-xl p-4">
          <p className="text-xs text-slate-400 mb-1">Regional average</p>
          <p className="text-xl font-semibold">{fmt(regional_average)}</p>
        </div>
      </div>

      {/* vs average */}
      <div className="flex items-center gap-3 bg-slate-800/60 rounded-xl p-4">
        <TrendIcon className={`w-6 h-6 flex-shrink-0 ${trendColour}`} />
        <div>
          <p className="text-sm text-slate-300">
            <span className={`font-semibold ${trendColour}`}>
              {diff > 0 ? "+" : ""}
              {diff}%
            </span>{" "}
            vs regional average
          </p>
          <p className="text-xs text-slate-500">
            {diff > 2 ? "Above market rate" : diff < -2 ? "Below market rate" : "At market rate"}
          </p>
        </div>
      </div>

      {/* Range bar */}
      <div>
        <div className="flex justify-between text-xs text-slate-500 mb-1.5">
          <span>{fmt(lower_bound)}</span>
          <span className="text-slate-400 font-medium">Range</span>
          <span>{fmt(upper_bound)}</span>
        </div>
        <div className="relative h-2 bg-slate-700 rounded-full">
          <div className="absolute inset-y-0 left-[10%] right-[10%] bg-indigo-900 rounded-full" />
          <div
            className="absolute w-3.5 h-3.5 bg-indigo-400 rounded-full top-1/2 -translate-y-1/2 border-2 border-slate-900 shadow"
            style={{ left: `${markerPct}%`, transform: "translate(-50%, -50%)" }}
          />
        </div>
      </div>
    </div>
  );
}
