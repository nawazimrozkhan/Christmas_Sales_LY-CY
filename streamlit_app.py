import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# =====================================================
# PAGE CONFIG
# =====================================================
st.set_page_config(
    page_title="Christmas Sales LY-CY",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("Christmas Sales LY-CY (2024 vs 2025)")
st.caption("Christmas Window vs Full December | YOY Review")

# =====================================================
# LOAD FILES
# =====================================================
@st.cache_data
def load_sheets(path):
    return pd.read_excel(path, sheet_name=None)

CHRISTMAS_FILE = "YOY COMPARISION OF STORES & HO.xlsx"
DEC_FILE = "DEC 2024-2025.xlsx"

sheets = load_sheets(CHRISTMAS_FILE)
dec_sheets = load_sheets(DEC_FILE)

# =====================================================
# SIDEBAR – VIEW MODE
# =====================================================
st.sidebar.title("View Mode")

view_mode = st.sidebar.radio(
    "Select Analysis",
    [
        "YOY – Like-to-Like Stores (LFL)",
        "YOY of HO",
        "Closed Stores",
        "New Stores"
    ]
)

# =====================================================
# 1️⃣ LFL – YOY
# =====================================================
if view_mode == "YOY – Like-to-Like Stores (LFL)":

    tab1, tab2 = st.tabs(["Christmas (20–25 Dec)", "Full December"])

    # ---------------------------
    # CHRISTMAS
    # ---------------------------
    with tab1:
        df_raw = sheets["YOY – Like-to-Like Stores (LFL)"].copy()

        qty_2024 = next((c for c in df_raw.columns if "qty" in c.lower() and "2024" in c), None)
        qty_2025 = next((c for c in df_raw.columns if "qty" in c.lower() and "2025" in c), None)

        df = df_raw.rename(columns={
            "Site": "Store",
            "Net Sale Amount - 2024": "Sales_LY",
            "Net Sale Amount - 2025": "Sales_CY",
            qty_2024: "Qty_LY",
            qty_2025: "Qty_CY"
        })

        df["Date"] = pd.to_datetime(df["Date"])
        df["Daily_YOY"] = df["Sales_CY"] - df["Sales_LY"]

        agg = df.groupby("Store").agg(
            Sales_LY=("Sales_LY", "sum"),
            Sales_CY=("Sales_CY", "sum"),
            Qty_LY=("Qty_LY", "sum"),
            Qty_CY=("Qty_CY", "sum"),
            Max_Daily_YOY=("Daily_YOY", "max"),
            Avg_Daily_YOY=("Daily_YOY", "mean")
        ).reset_index()

        agg["YOY_Δ"] = agg["Sales_CY"] - agg["Sales_LY"]
        agg["YOY_%"] = agg["YOY_Δ"] / agg["Sales_LY"]
        agg["Qty_YOY_%"] = (agg["Qty_CY"] - agg["Qty_LY"]) / agg["Qty_LY"]

        total_ly = agg["Sales_LY"].sum()
        total_cy = agg["Sales_CY"].sum()
        net = total_cy - total_ly

        c1, c2, c3 = st.columns(3)
        c1.metric("Sales 2024", f"₹{total_ly:,.0f}")
        c2.metric("Sales 2025", f"₹{total_cy:,.0f}")
        c3.metric("Net YOY", f"₹{net:,.0f}")

        st.plotly_chart(
            px.bar(
                agg.sort_values("YOY_Δ"),
                x="YOY_Δ",
                y="Store",
                orientation="h",
                title="Christmas – Store-wise YOY Impact"
            ),
            use_container_width=True
        )

        st.dataframe(agg, use_container_width=True)

    # ---------------------------
    # FULL DECEMBER
    # ---------------------------
    with tab2:
        df_raw = dec_sheets["YOY – Like-to-Like Stores (LFL)"].copy()

        qty_2024 = next((c for c in df_raw.columns if "qty" in c.lower() and "2024" in c), None)
        qty_2025 = next((c for c in df_raw.columns if "qty" in c.lower() and "2025" in c), None)

        df = df_raw.rename(columns={
            "Site": "Store",
            "Net Sale Amount - 2024": "Sales_LY",
            "Net Sale Amount - 2025": "Sales_CY",
            qty_2024: "Qty_LY",
            qty_2025: "Qty_CY"
        })

        agg = df.groupby("Store").agg(
            Sales_LY=("Sales_LY", "sum"),
            Sales_CY=("Sales_CY", "sum")
        ).reset_index()

        agg["YOY_Δ"] = agg["Sales_CY"] - agg["Sales_LY"]

        total_ly = agg["Sales_LY"].sum()
        total_cy = agg["Sales_CY"].sum()
        net = total_cy - total_ly

        c1, c2, c3 = st.columns(3)
        c1.metric("Dec 2024", f"₹{total_ly:,.0f}")
        c2.metric("Dec 2025", f"₹{total_cy:,.0f}")
        c3.metric("Net YOY", f"₹{net:,.0f}")

        st.plotly_chart(
            px.bar(
                agg.sort_values("YOY_Δ"),
                x="YOY_Δ",
                y="Store",
                orientation="h",
                title="Full December – Store-wise YOY Impact"
            ),
            use_container_width=True
        )

        st.dataframe(agg, use_container_width=True)

# =====================================================
# 2️⃣ YOY OF HO
# =====================================================
elif view_mode == "YOY of HO":

    tab1, tab2 = st.tabs(["Christmas (20–25 Dec)", "Full December"])

    with tab1:
        df = sheets["YOY OF HO"].copy()
        df["Date"] = pd.to_datetime(df["Date"])

        ho = df.groupby("Date").agg(
            Sales_LY=("Net Sale Amount - 2024", "sum"),
            Sales_CY=("Net Sale Amount - 2025", "sum")
        ).reset_index()

        ho["YOY_Δ"] = ho["Sales_CY"] - ho["Sales_LY"]
        st.plotly_chart(px.bar(ho, x="Date", y="YOY_Δ", title="HO – Christmas YOY"), use_container_width=True)

    with tab2:
        df = dec_sheets["YOY OF HO"].copy()

        total_ly = df["Net Sale Amount - 2024"].sum()
        total_cy = df["Net Sale Amount - 2025"].sum()

        c1, c2, c3 = st.columns(3)
        c1.metric("Dec 2024", f"₹{total_ly:,.0f}")
        c2.metric("Dec 2025", f"₹{total_cy:,.0f}")
        c3.metric("Net YOY", f"₹{(total_cy-total_ly):,.0f}")

# =====================================================
# 3️⃣ CLOSED STORES
# =====================================================
elif view_mode == "Closed Stores":

    tab1, tab2 = st.tabs(["Christmas (20–25 Dec)", "Full December"])

    with tab1:
        df = sheets["Closed Stores"].copy()
        st.metric("Christmas Loss", f"₹{df['Net Sale Amount - 2024'].sum():,.0f}")

    with tab2:
        df = dec_sheets["Closed Stores"].copy()
        st.metric("December Loss", f"₹{df['Net Sale Amount - 2024'].sum():,.0f}")

# =====================================================
# 4️⃣ NEW STORES
# =====================================================
elif view_mode == "New Stores":

    tab1, tab2 = st.tabs(["Christmas (20–25 Dec)", "Full December"])

    with tab1:
        df = sheets["New Stores"].copy()
        st.metric("Christmas Sales", f"₹{df['Net Sale Amount - 2025'].sum():,.0f}")

    with tab2:
        df = dec_sheets["New Stores"].copy()
        st.metric("December Sales", f"₹{df['Net Sale Amount - 2025'].sum():,.0f}")
