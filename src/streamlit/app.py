import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import warnings
from pathlib import Path


# -----------------------------
# SUPPRESS WARNINGS
# -----------------------------
warnings.simplefilter(action='ignore', category=FutureWarning)
warnings.simplefilter(action='ignore', category=UserWarning)

# -----------------------------
# CONFIG
# -----------------------------
st.set_page_config(
    page_title="Banggood Product Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

BASE_DIR = Path(__file__).resolve().parents[2]
DATA_PATH = BASE_DIR / "data" / "cleaned" / "combined_cleaned.csv"

# -----------------------------
# LOAD DATA
# -----------------------------
@st.cache_data
def load_data():
    return pd.read_csv(DATA_PATH)

df = load_data()

# -----------------------------
# SIDEBAR CONTROLS
# -----------------------------
st.sidebar.title("Filters 🔧")

categories = df["category"].unique().tolist()
selected_categories = st.sidebar.multiselect("Select Categories:", categories, default=categories)

min_price, max_price = st.sidebar.slider(
    "Price Range",
    min_value=float(df["price_clean"].min()),
    max_value=float(df["price_clean"].max()),
    value=(float(df["price_clean"].min()), float(df["price_clean"].max()))
)

search_term = st.sidebar.text_input("Search Product Name:")

top_n = st.sidebar.slider("Top N Products:", 1, 20, 5)

# -----------------------------
# FILTER DATA
# -----------------------------
filtered_df = df[
    (df["category"].isin(selected_categories)) &
    (df["price_clean"] >= min_price) &
    (df["price_clean"] <= max_price)
]

if search_term:
    filtered_df = filtered_df[filtered_df["product_name"].str.contains(search_term, case=False, na=False)]

# -----------------------------
# PAGE TITLE
# -----------------------------
st.title("📊 Banggood Product Dashboard")
st.markdown("---")

# -----------------------------
# METRIC CARDS
# -----------------------------
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Products", len(filtered_df))
col2.metric("Average Price", f"${filtered_df['price_clean'].mean():.2f}" if not filtered_df.empty else "$0.00")
col3.metric("Average Rating", f"{filtered_df['rating_clean'].mean():.2f}" if not filtered_df.empty else "0.00")
col4.metric("Top Reviews", f"{filtered_df['reviews_clean'].max()}" if not filtered_df.empty else "0")

# -----------------------------
# TABS: PLOTS / TOP PRODUCTS / DATA TABLE
# -----------------------------
tab1, tab2, tab3 = st.tabs(["📈 Plots", "🏆 Top Products", "📄 Data Table"])

def remove_legend(ax):
    legend = ax.get_legend()
    if legend is not None:
        legend.remove()

with tab1:
    st.subheader("Price Distribution by Category")
    fig, ax = plt.subplots(figsize=(10,5))
    sns.histplot(filtered_df, x="price_clean", hue="category", kde=True, palette="tab10")
    remove_legend(ax)
    st.pyplot(fig)

    st.subheader("Rating vs Price")
    fig2, ax2 = plt.subplots(figsize=(10,5))
    sns.scatterplot(data=filtered_df, x="price_clean", y="rating_clean", hue="category", alpha=0.7, palette="tab10")
    remove_legend(ax2)
    st.pyplot(fig2)

    st.subheader("Reviews vs Ratings")
    fig3, ax3 = plt.subplots(figsize=(10,5))
    sns.scatterplot(data=filtered_df, x="reviews_clean", y="rating_clean", hue="category", alpha=0.7, palette="tab10")
    remove_legend(ax3)
    st.pyplot(fig3)

    st.subheader("Discount Distribution")
    fig4, ax4 = plt.subplots(figsize=(10,5))
    sns.histplot(filtered_df, x="discount_clean", hue="category", kde=True, palette="tab10")
    remove_legend(ax4)
    st.pyplot(fig4)

    st.subheader("Price Bucket Distribution")
    fig5, ax5 = plt.subplots(figsize=(10,5))
    sns.countplot(data=filtered_df, x="price_bucket", hue="category", dodge=False, palette="tab10")
    remove_legend(ax5)
    st.pyplot(fig5)

    st.subheader("Value Score Distribution")
    fig6, ax6 = plt.subplots(figsize=(10,5))
    sns.histplot(filtered_df, x="value_score", hue="category", kde=True, palette="tab10")
    remove_legend(ax6)
    st.pyplot(fig6)

    st.subheader("Old Price vs New Price")
    fig7, ax7 = plt.subplots(figsize=(10,5))
    sns.scatterplot(data=filtered_df, x="old_price_clean", y="price_clean", hue="category", palette="tab10")
    remove_legend(ax7)
    st.pyplot(fig7)

    st.subheader("Category-wise Discount Boxplot")
    fig8, ax8 = plt.subplots(figsize=(10,5))
    sns.boxplot(
        data=filtered_df,
        x="category",
        y="discount_clean",
        hue="category",
        dodge=False,
        palette="tab10",
        showfliers=False
    )
    remove_legend(ax8)
    st.pyplot(fig8)

with tab2:
    st.subheader("🔥 Top Reviewed Products")
    top_reviews = filtered_df.sort_values("reviews_clean", ascending=False).head(top_n)
    st.dataframe(top_reviews[["product_name", "category", "reviews_clean", "price_clean"]])

    st.subheader("💎 Best Value Products")
    best_value = filtered_df.sort_values("value_score", ascending=False).head(top_n)
    st.dataframe(best_value[["product_name", "category", "value_score", "price_clean", "rating_clean"]])

with tab3:
    st.subheader("📄 Filtered Data Table")
    st.dataframe(filtered_df)

    st.subheader("⬇ Download Filtered CSV")
    csv_bytes = filtered_df.to_csv(index=False).encode("utf-8")
    st.download_button("Download CSV", data=csv_bytes, file_name="filtered_banggood_data.csv", mime="text/csv")
