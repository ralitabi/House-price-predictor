export default function ChartTooltip({ active, payload, label }) {
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
