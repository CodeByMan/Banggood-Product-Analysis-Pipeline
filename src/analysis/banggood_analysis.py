import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os
from util.file_paths import CLEAN_DATA_DIR, IMAGE_DIR

df = pd.read_csv(os.path.join(CLEAN_DATA_DIR, "combined_cleaned.csv"))
os.makedirs(IMAGE_DIR, exist_ok=True)

# 1 – Price Distribution
plt.figure(figsize=(10,5))
sns.histplot(df, x="price_clean", hue="category", kde=True)
plt.title("Price Distribution per Category")
plt.savefig(os.path.join(IMAGE_DIR, "price_distribution.png"))
plt.close()

# 2 – Rating vs Price
plt.figure(figsize=(10,5))
sns.scatterplot(df, x="price_clean", y="rating_clean", hue="category")
plt.title("Rating vs Price")
plt.savefig(os.path.join(IMAGE_DIR, "rating_vs_price.png"))
plt.close()

# 3 – Reviews vs Rating
plt.figure(figsize=(10,5))
sns.scatterplot(df, x="reviews_clean", y="rating_clean", hue="category")
plt.title("Reviews vs Ratings")
plt.savefig(os.path.join(IMAGE_DIR, "reviews_vs_ratings.png"))
plt.close()

# 4 – Discount % Distribution
plt.figure(figsize=(10,5))
sns.histplot(df["discount_pct"], bins=20, color="orange", kde=True)
plt.title("Discount Percentage Distribution")
plt.savefig(os.path.join(IMAGE_DIR, "discount_distribution.png"))
plt.close()

# 5 – Price Bucket Counts
plt.figure(figsize=(10,5))
sns.countplot(df, x="price_bucket", hue="category")
plt.title("Price Bucket Distribution by Category")
plt.savefig(os.path.join(IMAGE_DIR, "price_buckets.png"))
plt.close()

print(f"All 5 graphs generated and stored in {IMAGE_DIR}/")
