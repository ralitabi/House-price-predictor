import { useState } from "react";
import Header from "./components/Header";
import MarketTrends from "./components/MarketTrends";
import PredictionForm from "./components/PredictionForm";
import RegionalAverages from "./components/RegionalAverages";
import ResultCard from "./components/ResultCard";
import { predictPrice } from "./services/api";

export default function App() {
  const [result, setResult]         = useState(null);
  const [loading, setLoading]       = useState(false);
  const [error, setError]           = useState(null);
  const [selectedRegion, setRegion] = useState("South East");

  const handlePredict = async (formData) => {
    setLoading(true);
    setError(null);
    try {
      const data = await predictPrice(formData);
      setResult(data);
      setRegion(formData.region);
    } catch (err) {
      setError(err.response?.data?.error ?? err.message ?? "Prediction failed");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-950 via-slate-900 to-indigo-950">
      <Header />

      <main className="max-w-7xl mx-auto px-4 sm:px-6 py-8 space-y-8">
        {/* Top row: form + result */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          <PredictionForm onPredict={handlePredict} loading={loading} />

          <div className="space-y-6">
            {error && (
              <div className="bg-red-950/60 border border-red-800/50 rounded-2xl p-5 text-red-300 text-sm">
                {error}
              </div>
            )}
            {result && <ResultCard result={result} />}
            {!result && !error && (
              <div className="bg-slate-900/40 rounded-2xl border border-slate-800 border-dashed p-12 flex items-center justify-center">
                <p className="text-slate-600 text-sm">
                  Fill in the details and click <strong className="text-slate-500">Estimate Price</strong>
                </p>
              </div>
            )}
          </div>
        </div>

        {/* Charts row */}
        <MarketTrends region={selectedRegion} />
        <RegionalAverages />
      </main>
    </div>
  );
}
