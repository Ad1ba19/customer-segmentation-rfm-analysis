import pandas as pd

from src.rfm import assign_segments, build_rfm, score_rfm


def _tx(rows):
    df = pd.DataFrame(rows, columns=["user_id", "order_id", "event_time", "price"])
    df["event_time"] = pd.to_datetime(df["event_time"], utc=True)
    return df


def test_build_rfm_is_one_row_per_customer():
    df = _tx([
        (1, 10, "2020-06-01", 100.0),
        (1, 10, "2020-06-01", 50.0),   # second item in the same order
        (1, 11, "2020-06-05", 20.0),
        (2, 12, "2020-05-01", 5.0),
    ])
    rfm = build_rfm(df, reference_date=pd.Timestamp("2020-06-06", tz="UTC"))
    assert list(rfm.index) == [1, 2]
    assert rfm.loc[1, "frequency"] == 2          # distinct orders, not rows
    assert rfm.loc[1, "monetary"] == 170.0
    assert rfm.loc[1, "recency"] == 1
    assert rfm.loc[2, "recency"] == 36


def test_scores_are_in_range_and_every_customer_gets_one_segment():
    rows = [(u, u, f"2020-06-{(u % 28) + 1:02d}", float(u)) for u in range(1, 41)]
    rows += [(1, 100, "2020-06-28", 10.0), (1, 101, "2020-06-28", 10.0)]
    seg = assign_segments(score_rfm(build_rfm(_tx(rows))))
    for col in ["R", "F", "M"]:
        assert seg[col].between(1, 4).all()
    assert seg["segment"].notna().all()
    assert seg.index.is_unique


def test_recent_frequent_customer_is_champion():
    rows = [(u, u, "2020-05-01", 10.0) for u in range(2, 10)]
    rows += [(1, 100 + i, "2020-06-10", 50.0) for i in range(4)]
    seg = assign_segments(score_rfm(build_rfm(_tx(rows))))
    assert seg.loc[1, "segment"] == "Champions"
