import logging

import requests

logger = logging.getLogger(__name__)

# 2024 Q4 estimates (HM Land Registry UK House Price Index)
REGIONAL_AVERAGES: dict[str, int] = {
    "London":                         527_000,
    "South East":                     392_000,
    "East of England":                335_000,
    "South West":                     300_000,
    "West Midlands":                  248_000,
    "East Midlands":                  237_000,
    "Yorkshire and The Humber":       215_000,
    "North West":                     228_000,
    "North East":                     178_000,
    "Wales":                          205_000,
    "Scotland":                       200_000,
}

_REGION_SLUG: dict[str, str] = {
    "england":                        "england",
    "London":                         "london",
    "South East":                     "south-east",
    "East of England":                "east-of-england",
    "South West":                     "south-west",
    "West Midlands":                  "west-midlands",
    "East Midlands":                  "east-midlands",
    "Yorkshire and The Humber":       "yorkshire-and-the-humber",
    "North West":                     "north-west",
    "North East":                     "north-east",
    "Wales":                          "wales",
    "Scotland":                       "scotland",
}

_UKHPI_BASE = "https://landregistry.data.gov.uk/api/1/datasets/ukhpi.json"


class MarketDataFetcher:

    def fetch_price_trends(self, region: str = "england") -> dict:
        slug       = _REGION_SLUG.get(region, region.lower().replace(" ", "-"))
        region_uri = f"http://landregistry.data.gov.uk/id/region/{slug}"

        params = {
            "_view":     "basic",
            "_pageSize": 24,
            "_sort":     "-refMonth",
            "region":    region_uri,
        }

        try:
            resp = requests.get(_UKHPI_BASE, params=params, timeout=8)
            resp.raise_for_status()
            items = resp.json().get("result", {}).get("items", [])

            if not items:
                raise ValueError("Empty response from Land Registry API")

            trends = []
            for item in reversed(items):
                ref   = item.get("refMonth", {})
                month = ref.get("_value", "") if isinstance(ref, dict) else str(ref)
                avg   = item.get("averagePrice", {})
                price = avg.get("_value", 0) if isinstance(avg, dict) else avg
                if month and price:
                    trends.append({"month": month, "average_price": float(price)})

            return {"region": region, "trends": trends, "source": "HM Land Registry UKHPI"}

        except Exception as exc:
            logger.warning("Land Registry API unavailable (%s) — using fallback data", exc)
            return self._fallback_trends(region)

    def fetch_regional_averages(self) -> dict:
        results = [
            {"region": r, "average_price": v}
            for r, v in REGIONAL_AVERAGES.items()
        ]
        return {"data": results, "source": "HM Land Registry (2024 Q4)"}

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _fallback_trends(self, region: str) -> dict:
        base   = REGIONAL_AVERAGES.get(region, 280_000)
        trends = []
        for i in range(23, -1, -1):
            total_months = 23 - i
            year  = 2023 + (total_months // 12)
            month = 1 + (total_months % 12)
            growth = 1 + total_months * 0.0028
            trends.append({
                "month":         f"{year}-{month:02d}",
                "average_price": round(base * growth),
            })
        return {"region": region, "trends": trends, "source": "Estimated (Land Registry unavailable)"}
