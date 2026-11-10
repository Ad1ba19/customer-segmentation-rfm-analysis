"""Customer-level RFM (Recency, Frequency, Monetary) segmentation.

Usage as a library:
    from src.rfm import load_transactions, build_rfm, score_rfm, assign_segments

Usage from the command line:
    python -m src.rfm "Transaction_Cleaned_Data (1).csv" --out outputs/customer_segments.csv
"""
from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd

# Segments are checked top to bottom; the first rule a customer matches wins,
# so every customer lands in exactly one segment.
SEGMENT_RULES = [
    ("Champions",              lambda d: (d.R >= 3) & (d.F >= 3)),
    ("Loyal Customers",        lambda d: (d.R >= 3) & (d.F == 2)),
    ("At Risk Repeat Buyers",  lambda d: (d.R <= 2) & (d.F >= 2)),
    ("New High-Value",         lambda d: (d.R == 4) & (d.F == 1) & (d.M >= 3)),
    ("New Customers",          lambda d: (d.R == 4) & (d.F == 1)),
    ("Promising",              lambda d: (d.R == 3) & (d.F == 1)),
    ("Big Spenders Slipping",  lambda d: (d.R <= 2) & (d.F == 1) & (d.M == 4)),
    ("Hibernating",            lambda d: (d.R == 2) & (d.F == 1)),
    ("Lost",                   lambda d: (d.R == 1) & (d.F == 1)),
]
SEGMENT_ORDER = [name for name, _ in SEGMENT_RULES]


def load_transactions(path: str | Path) -> pd.DataFrame:
    """Read the cleaned transaction file and drop exact duplicate rows."""
    df = pd.read_csv(path)
    df["event_time"] = pd.to_datetime(df["event_time"], utc=True)
    df = df.dropna(subset=["user_id", "order_id", "price"]).drop_duplicates()
    df["user_id"] = df["user_id"].astype("int64")
    return df


def build_rfm(df: pd.DataFrame, reference_date: pd.Timestamp | None = None) -> pd.DataFrame:
    """One row per customer: recency (days), frequency (distinct orders), monetary (total spend)."""
    if reference_date is None:
        reference_date = df["event_time"].max().normalize() + pd.Timedelta(days=1)
    rfm = df.groupby("user_id").agg(
        last_purchase=("event_time", "max"),
        frequency=("order_id", "nunique"),
        monetary=("price", "sum"),
    )
    rfm["recency"] = (reference_date - rfm["last_purchase"]).dt.days
    return rfm[["recency", "frequency", "monetary"]]


def score_rfm(rfm: pd.DataFrame) -> pd.DataFrame:
    """Add R, F and M scores from 1 (worst) to 4 (best).

    R and M use quartiles. Ranking first breaks ties so qcut always gets 4 bins.
    F uses fixed cut-offs (1, 2, 3, 4+ orders) because most customers order once,
    which makes frequency quartiles meaningless.
    """
    out = rfm.copy()
    out["R"] = pd.qcut(out["recency"].rank(method="first"), 4, labels=[4, 3, 2, 1]).astype(int)
    out["M"] = pd.qcut(out["monetary"].rank(method="first"), 4, labels=[1, 2, 3, 4]).astype(int)
    out["F"] = out["frequency"].clip(upper=4).astype(int)
    out["rfm_code"] = out["R"].astype(str) + out["F"].astype(str) + out["M"].astype(str)
    return out


def assign_segments(scored: pd.DataFrame) -> pd.DataFrame:
    out = scored.copy()
    out["segment"] = None
    for name, rule in SEGMENT_RULES:
        mask = out["segment"].isna() & rule(out)
        out.loc[mask, "segment"] = name
    out["segment"] = out["segment"].fillna("Other")
    return out


def segment_summary(segmented: pd.DataFrame) -> pd.DataFrame:
    """Customers, revenue and averages per segment, in segment order."""
    s = segmented.groupby("segment").agg(
        customers=("recency", "size"),
        revenue=("monetary", "sum"),
        avg_recency_days=("recency", "mean"),
        avg_orders=("frequency", "mean"),
        avg_spend=("monetary", "mean"),
    )
    s["customer_share_pct"] = 100 * s["customers"] / s["customers"].sum()
    s["revenue_share_pct"] = 100 * s["revenue"] / s["revenue"].sum()
    order = [x for x in SEGMENT_ORDER if x in s.index] + [x for x in s.index if x not in SEGMENT_ORDER]
    return s.loc[order].round(1)


def run(path: str | Path) -> tuple[pd.DataFrame, pd.DataFrame]:
    segmented = assign_segments(score_rfm(build_rfm(load_transactions(path))))
    return segmented, segment_summary(segmented)


def main() -> None:
    ap = argparse.ArgumentParser(description="Customer-level RFM segmentation")
    ap.add_argument("csv", help="cleaned transactions CSV")
    ap.add_argument("--out", default="outputs/customer_segments.csv")
    args = ap.parse_args()
    segmented, summary = run(args.csv)
    Path(args.out).parent.mkdir(parents=True, exist_ok=True)
    segmented.to_csv(args.out)
    print(summary.to_string())
    print(f"\nWrote {len(segmented):,} customers to {args.out}")


if __name__ == "__main__":
    main()
