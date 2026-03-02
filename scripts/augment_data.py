"""Phase B: EDA augmentation (train split only, minority classes).

Techniques used (no external LLM):
  - synonym_replacement: replace n words with WordNet synonyms
  - random_swap: swap two random words
  - random_deletion: randomly delete words with probability p
"""

import os
import random
import re
import sys

import pandas as pd
from nltk.corpus import wordnet

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

PROCESSED_DIR = os.path.join(os.path.dirname(__file__), "..", "data", "processed")
TRAIN_CSV = os.path.join(PROCESSED_DIR, "train.csv")
SYNTH_CSV = os.path.join(PROCESSED_DIR, "train_synth.csv")
HYBRID_CSV = os.path.join(PROCESSED_DIR, "train_hybrid.csv")

random.seed(42)

# ---------------------------------------------------------------------------
# EDA helpers
# ---------------------------------------------------------------------------

def _synonyms(word: str) -> list[str]:
    syns = set()
    for syn in wordnet.synsets(word):
        for lemma in syn.lemmas():
            name = lemma.name().replace("_", " ")
            if name.lower() != word.lower():
                syns.add(name)
    return list(syns)


def synonym_replacement(text: str, n: int = 2) -> str:
    words = text.split()
    if not words:
        return text
    candidates = [i for i, w in enumerate(words) if _synonyms(w)]
    random.shuffle(candidates)
    replaced = words[:]
    for idx in candidates[:n]:
        syns = _synonyms(replaced[idx])
        if syns:
            replaced[idx] = random.choice(syns)
    return " ".join(replaced)


def random_swap(text: str, n: int = 2) -> str:
    words = text.split()
    if len(words) < 2:
        return text
    for _ in range(n):
        i, j = random.sample(range(len(words)), 2)
        words[i], words[j] = words[j], words[i]
    return " ".join(words)


def random_deletion(text: str, p: float = 0.15) -> str:
    words = text.split()
    if len(words) == 1:
        return text
    kept = [w for w in words if random.random() > p]
    return " ".join(kept) if kept else random.choice(words)


_OPS = [synonym_replacement, random_swap, random_deletion]


def augment_text(text: str) -> str:
    op = random.choice(_OPS)
    return op(text)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    train = pd.read_csv(TRAIN_CSV)
    counts = train["Topic_group"].value_counts()
    majority_count = int(counts.iloc[0])
    target_count = int(majority_count * 0.70)

    print(f"Majority class size : {majority_count}")
    print(f"Augmentation target : {target_count} per class\n")

    synth_rows = []

    for label, count in counts.items():
        if count >= target_count:
            print(f"  SKIP  {label:<30} ({count} >= {target_count})")
            continue

        needed = target_count - count
        pool = train.loc[train["Topic_group"] == label, "Document"].tolist()
        print(f"  AUG   {label:<30} ({count} -> +{needed})")

        generated = 0
        pool_idx = 0
        while generated < needed:
            original = pool[pool_idx % len(pool)]
            pool_idx += 1
            aug = augment_text(str(original))
            synth_rows.append({"Document": aug, "Topic_group": label})
            generated += 1

    synth_df = pd.DataFrame(synth_rows)
    synth_df.to_csv(SYNTH_CSV, index=False)
    print(f"\nSynthetic samples : {len(synth_df)}")

    hybrid_df = pd.concat([train, synth_df], ignore_index=True)
    hybrid_df.to_csv(HYBRID_CSV, index=False)
    print(f"Hybrid total      : {len(hybrid_df)}")
    print("\nHybrid class distribution:")
    print(hybrid_df["Topic_group"].value_counts().to_string())


if __name__ == "__main__":
    main()
