import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# =====================================================
# PAGE CONFIG
# =====================================================
st.set_page_config(
    page_title="Christmas Sales LY-CY",
    layout="wide"
)

st.title("Christmas Sales LY-CY (2024 vs 2025)")
st.caption("Execution View | Christmas vs Full December")

# =====================================================
# LOAD FILES
# =====================================================
@st.cache_data
def load_sheets(path):
    return pd.read_excel(path, sheet_name=None)

CHRISTMAS_FILE = "YOY COMPARISION OF STORES & HO.xlsx"
DEC_FILE = "DEC 2024-2025.xlsx"

christmas_sheets = load_sheets(CHRISTMAS_FILE)
dec_sheets = load_sheets(DEC_FILE)

# =====================================================
# TOP PERIOD TOGGLE (GLOBAL)
# =====================================================
period = st.radio(
    "Select Period",
    ["Christmas (20–25 Dec)", "Full December"],
    horizontal=True
)

data_source = christmas_sheets if period == "Christmas (20–25 Dec)" else dec_sheets

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

    df_raw = data_source["YOY – Like-to-Like Stores (LFL)"].copy()

    qty_2024 = next((c for c in df_raw.columns if "qty" in c.lower() and "2024" in c), None)
    qty_2025 = next((c for c in df_raw.columns if "qty" in c.lower() and "2025" in c), None)

    df = df_raw.rename(columns={
        "Site": "Store",
        "Net Sale Amount - 2024": "Sales_LY",
        "Net Sale Amount - 2025": "Sales_CY",
        qty_2024: "Qty_LY",
        qty_2025: "Qty_CY"
    })

    store_agg = df.groupby("Store").agg(
        Sales_LY=("Sales_LY", "sum"),
        Sales_CY=("Sales_CY", "sum")
    ).reset_index()

    store_agg["YOY_Δ"] = store_agg["Sales_CY"] - store_agg["Sales_LY"]
    store_agg["YOY_%"] = store_agg["YOY_Δ"] / store_agg["Sales_LY"]

    total_ly = store_agg["Sales_LY"].sum()
    total_cy = store_agg["Sales_CY"].sum()
    net_yoy = total_cy - total_ly
    yoy_pct = (net_yoy / total_ly) if total_ly else 0

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Sales LY", f"₹{total_ly:,.0f}")
    c2.metric("Sales CY", f"₹{total_cy:,.0f}")
    c3.metric("Net YOY", f"₹{net_yoy:,.0f}")
    c4.metric("YOY %", f"{yoy_pct*100:.1f}%")

    fig = px.bar(
        store_agg.sort_values("YOY_Δ"),
        x="YOY_Δ",
        y="Store",
        orientation="h",
        title=f"LFL Store Impact – {period}",
        color=store_agg["YOY_Δ"] > 0,
        color_discrete_map={True: "green", False: "red"}
    )
    st.plotly_chart(fig, use_container_width=True)

    st.dataframe(store_agg, use_container_width=True)

# =====================================================
# 2️⃣ YOY OF HO
# =====================================================
elif view_mode == "YOY of HO":

    df = data_source["YOY OF HO"].copy()

    total_ly = df["Net Sale Amount - 2024"].sum()
    total_cy = df["Net Sale Amount - 2025"].sum()
    net_yoy = total_cy - total_ly

    c1, c2, c3 = st.columns(3)
    c1.metric("HO LY", f"₹{total_ly:,.0f}")
    c2.metric("HO CY", f"₹{total_cy:,.0f}")
    c3.metric("Net YOY", f"₹{net_yoy:,.0f}")

# =====================================================
# 3️⃣ CLOSED STORES
# =====================================================
elif view_mode == "Closed Stores":

    df = data_source["Closed Stores"].copy()

    lost = df["Net Sale Amount - 2024"].sum()
    st.metric(f"Revenue Lost ({period})", f"₹{lost:,.0f}")

    fig = px.bar(
        df.groupby("Site")["Net Sale Amount - 2024"].sum().reset_index(),
        x="Net Sale Amount - 2024",
        y="Site",
        orientation="h",
        title=f"Closed Store Impact – {period}"
    )
    st.plotly_chart(fig, use_container_width=True)

# =====================================================
# 4️⃣ NEW STORES
# =====================================================
elif view_mode == "New Stores":

    df = data_source["New Stores"].copy()

    total_sales = df["Net Sale Amount - 2025"].sum()
    avg_sales = df.groupby("Site")["Net Sale Amount - 2025"].sum().mean()

    c1, c2 = st.columns(2)
    c1.metric(f"New Store Sales ({period})", f"₹{total_sales:,.0f}")
    c2.metric("Avg per Store", f"₹{avg_sales:,.0f}")

    fig = px.bar(
        df.groupby("Site")["Net Sale Amount - 2025"].sum().reset_index(),
        x="Net Sale Amount - 2025",
        y="Site",
        orientation="h",
        title=f"New Store Contribution – {period}"
    )
    st.plotly_chart(fig, use_container_width=True)
