import { useState } from "react";
import { Calculator, Car, MapPin, TreePine } from "lucide-react";

const REGIONS = [
  "London",
  "South East",
  "East of England",
  "South West",
  "West Midlands",
  "East Midlands",
  "Yorkshire and The Humber",
  "North West",
  "North East",
  "Wales",
  "Scotland",
];

const PROPERTY_TYPES = ["detached", "semi-detached", "terraced", "flat"];

const DEFAULTS = {
  bedrooms:      3,
  bathrooms:     2,
  sqft:          1200,
  property_type: "semi-detached",
  region:        "South East",
  age:           30,
  has_garden:    true,
  has_parking:   true,
};

function NumberInput({ label, value, onChange, min, max, step = 1 }) {
  return (
    <div>
      <label className="block text-xs font-medium text-slate-400 mb-1">{label}</label>
      <input
        type="number"
        value={value}
        min={min}
        max={max}
        step={step}
        onChange={(e) => onChange(Number(e.target.value))}
        className="w-full bg-slate-800 border border-slate-700 rounded-xl px-3 py-2.5 text-white
                   text-sm focus:border-indigo-500 focus:outline-none focus:ring-1 focus:ring-indigo-500/40"
      />
    </div>
  );
}

function Toggle({ label, icon: Icon, active, onClick }) {
  return (
    <button
      type="button"
      onClick={onClick}
      className={`flex items-center gap-2 px-4 py-2.5 rounded-xl border text-sm font-medium transition-all ${
        active
          ? "bg-indigo-600 border-indigo-500 text-white shadow-lg shadow-indigo-900/30"
          : "bg-slate-800 border-slate-700 text-slate-400 hover:border-slate-600"
      }`}
    >
      <Icon className="w-4 h-4" />
      {label}
    </button>
  );
}

export default function PredictionForm({ onPredict, loading }) {
  const [form, setForm] = useState(DEFAULTS);
  const set = (key, val) => setForm((prev) => ({ ...prev, [key]: val }));

  const handleSubmit = (e) => {
    e.preventDefault();
    onPredict({
      ...form,
      has_garden:  form.has_garden  ? 1 : 0,
      has_parking: form.has_parking ? 1 : 0,
    });
  };

  return (
    <form
      onSubmit={handleSubmit}
      className="bg-slate-900/60 backdrop-blur rounded-2xl border border-slate-800 p-6 space-y-5"
    >
      <h2 className="text-lg font-semibold flex items-center gap-2">
        <Calculator className="w-5 h-5 text-indigo-400" />
        Property Details
      </h2>

      {/* Property type */}
      <div>
        <p className="text-xs font-medium text-slate-400 mb-2">Property Type</p>
        <div className="grid grid-cols-2 gap-2">
          {PROPERTY_TYPES.map((type) => (
            <button
              key={type}
              type="button"
              onClick={() => set("property_type", type)}
              className={`py-2 px-3 rounded-xl text-sm font-medium capitalize border transition-all ${
                form.property_type === type
                  ? "bg-indigo-600 border-indigo-500 text-white shadow-lg shadow-indigo-900/30"
                  : "bg-slate-800 border-slate-700 text-slate-300 hover:border-slate-600"
              }`}
            >
              {type}
            </button>
          ))}
        </div>
      </div>

      {/* Region */}
      <div>
        <label className="flex items-center gap-1 text-xs font-medium text-slate-400 mb-2">
          <MapPin className="w-3.5 h-3.5" /> Region
        </label>
        <select
          value={form.region}
          onChange={(e) => set("region", e.target.value)}
          className="w-full bg-slate-800 border border-slate-700 rounded-xl px-3 py-2.5 text-white text-sm
                     focus:border-indigo-500 focus:outline-none focus:ring-1 focus:ring-indigo-500/40"
        >
          {REGIONS.map((r) => (
            <option key={r} value={r}>{r}</option>
          ))}
        </select>
      </div>

      {/* Numeric grid */}
      <div className="grid grid-cols-2 gap-4">
        <NumberInput label="Bedrooms"       value={form.bedrooms}  onChange={(v) => set("bedrooms", v)}  min={1} max={10} />
        <NumberInput label="Bathrooms"      value={form.bathrooms} onChange={(v) => set("bathrooms", v)} min={1} max={8}  />
        <NumberInput label="Square Footage" value={form.sqft}      onChange={(v) => set("sqft", v)}      min={100} max={15000} step={50} />
        <NumberInput label="Age (years)"    value={form.age}       onChange={(v) => set("age", v)}       min={0}   max={200} />
      </div>

      {/* Toggles */}
      <div className="flex gap-3">
        <Toggle label="Garden"  icon={TreePine} active={form.has_garden}  onClick={() => set("has_garden",  !form.has_garden)}  />
        <Toggle label="Parking" icon={Car}      active={form.has_parking} onClick={() => set("has_parking", !form.has_parking)} />
      </div>

      <button
        type="submit"
        disabled={loading}
        className="w-full bg-indigo-600 hover:bg-indigo-500 disabled:opacity-50 disabled:cursor-not-allowed
                   text-white font-semibold py-3 rounded-xl transition-all shadow-lg shadow-indigo-900/30"
      >
        {loading ? (
          <span className="flex items-center justify-center gap-2">
            <svg className="animate-spin w-4 h-4" viewBox="0 0 24 24" fill="none">
              <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" />
              <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v8H4z" />
            </svg>
            Calculating…
          </span>
        ) : (
          "Estimate Price"
        )}
      </button>
    </form>
  );
}
