import axios from "axios";

const api = axios.create({ baseURL: "/api" });

export async function predictPrice(data) {
  const res = await api.post("/predict", data);
  return res.data;
}

export async function fetchMarketTrends(region) {
  const res = await api.get("/market-trends", { params: { region } });
  return res.data;
}

export async function fetchRegionalAverages() {
  const res = await api.get("/regional-averages");
  return res.data;
}
