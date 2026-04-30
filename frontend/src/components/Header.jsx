import { Home } from "lucide-react";

export default function Header() {
  return (
    <header className="bg-slate-900/80 backdrop-blur-sm border-b border-slate-800 sticky top-0 z-10">
      <div className="max-w-7xl mx-auto px-6 py-4 flex items-center gap-3">
        <div className="bg-indigo-600 p-2 rounded-xl">
          <Home className="w-5 h-5 text-white" />
        </div>
        <div>
          <h1 className="text-lg font-bold tracking-tight">UK House Price Predictor</h1>
          <p className="text-xs text-slate-400">
            Random Forest ML · Live HM Land Registry Data
          </p>
        </div>
      </div>
    </header>
  );
}
