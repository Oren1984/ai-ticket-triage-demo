"""Phase A: Stratified 80/10/10 split of the Kaggle CSV."""

import os
import sys
import pandas as pd
from sklearn.model_selection import train_test_split

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

RAW_CSV = os.path.join(os.path.dirname(__file__), "..", "data", "raw",
                       "all_tickets_processed_improved_v3.csv")
PROCESSED_DIR = os.path.join(os.path.dirname(__file__), "..", "data", "processed")
REPORTS_DIR = os.path.join(os.path.dirname(__file__), "..", "reports")


def main():
    os.makedirs(PROCESSED_DIR, exist_ok=True)
    os.makedirs(REPORTS_DIR, exist_ok=True)

    df = pd.read_csv(RAW_CSV)
    df = df.dropna(subset=["Document", "Topic_group"]).reset_index(drop=True)
    print(f"Total samples: {len(df)}")

    # 80 / 20 stratified first pass
    train, temp = train_test_split(
        df, test_size=0.20, stratify=df["Topic_group"], random_state=42
    )
    # 20 → 10 val / 10 test
    val, test = train_test_split(
        temp, test_size=0.50, stratify=temp["Topic_group"], random_state=42
    )

    train.to_csv(os.path.join(PROCESSED_DIR, "train.csv"), index=False)
    val.to_csv(os.path.join(PROCESSED_DIR, "val.csv"), index=False)
    test.to_csv(os.path.join(PROCESSED_DIR, "test.csv"), index=False)

    print(f"Train: {len(train)}  Val: {len(val)}  Test: {len(test)}")

    # Save distribution stats
    lines = [
        "=== Dataset split statistics ===\n",
        f"Total samples : {len(df)}\n",
        f"Train         : {len(train)}\n",
        f"Val           : {len(val)}\n",
        f"Test          : {len(test)}\n\n",
    ]
    for split_name, split_df in [("TRAIN", train), ("VAL", val), ("TEST", test)]:
        lines.append(f"--- {split_name} class distribution ---\n")
        vc = split_df["Topic_group"].value_counts()
        for label, count in vc.items():
            lines.append(f"  {label:<30} {count}\n")
        lines.append("\n")

    stats_path = os.path.join(REPORTS_DIR, "data_stats.txt")
    with open(stats_path, "w", encoding="utf-8") as f:
        f.writelines(lines)
    print(f"Stats saved to {stats_path}")


if __name__ == "__main__":
    main()
