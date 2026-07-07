import pandas as pd
import os
import re
from util.file_paths import RAW_DATA_DIR, CLEAN_DATA_DIR

# Ensure output directory exists
os.makedirs(CLEAN_DATA_DIR, exist_ok=True)

# --- Cleaning functions ---
def clean_price(x):
    if pd.isna(x):
        return None
    x = str(x).replace("Â", "")
    x = re.sub(r"[^\d.]", "", x)
    return float(x) if x else None

def clean_discount(x):
    if pd.isna(x):
        return 0
    nums = re.findall(r"\d+", str(x))
    return float(nums[0]) if nums else 0

def clean_rating(x):
    if pd.isna(x):
        return None
    x = str(x)
    if "★" in x:
        return float(x.count("★"))
    match = re.search(r"(\d+(?:\.\d+)?)", x)
    if match:
        return float(match.group(1))
    x = re.sub(r"[^\d.]", "", x)
    return float(x) if x else None

def clean_reviews(x):
    if pd.isna(x):
        return 0
    nums = re.findall(r"\d+", str(x))
    return int(nums[0]) if nums else 0

# --- Main cleaning function ---
def main():
    dfs = []

    for file in os.listdir(RAW_DATA_DIR):
        if file.endswith(".csv"):
            df = pd.read_csv(os.path.join(RAW_DATA_DIR, file))

            # --- Clean numeric columns ---
            df["price_clean"] = df["price"].apply(clean_price)
            df["old_price_clean"] = df["old_price"].apply(clean_price)
            df["discount_clean"] = df["discount"].apply(clean_discount)
            df["rating_clean"] = df["rating"].apply(clean_rating)
            df["reviews_clean"] = df["reviews"].apply(clean_reviews)

            # Fill missing numeric values
            df["price_clean"].fillna(df["price_clean"].median(), inplace=True)
            df["rating_clean"].fillna(df["rating_clean"].median(), inplace=True)
            df["reviews_clean"].fillna(0, inplace=True)

            # --- Add derived columns ---
            df["value_score"] = df["rating_clean"] * (df["reviews_clean"] + 1)
            df["price_bucket"] = pd.cut(
                df["price_clean"],
                bins=[0, 10, 50, 100, 300, 1000, 5000],
                labels=["very_low", "low", "medium", "high", "premium", "ultra"]
            )
            df["discount_pct"] = df["discount_clean"]

            dfs.append(df)

    # Combine all CSVs, keep all columns
    combined = pd.concat(dfs, ignore_index=True)

    # Save cleaned combined data
    combined.to_csv(os.path.join(CLEAN_DATA_DIR, "combined_cleaned.csv"), index=False)
    print("CLEANING COMPLETE → combined_cleaned.csv saved.")

if __name__ == "__main__":
    main()
