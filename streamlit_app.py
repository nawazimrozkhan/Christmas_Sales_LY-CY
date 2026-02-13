import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from datetime import datetime, timedelta
import io

# Page configuration
st.set_page_config(
    page_title="Sales Performance Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better UI
st.markdown("""
    <style>
    .main {
        padding: 0rem 1rem;
    }
    .stMetric {
        background-color: #1e1e1e;
        padding: 15px;
        border-radius: 10px;
        border: 1px solid #333;
    }
    h1 {
        color: #ffffff;
        font-size: 2.5rem;
        font-weight: 700;
        margin-bottom: 1rem;
    }
    h2 {
        color: #ffffff;
        font-size: 1.8rem;
        margin-top: 2rem;
        margin-bottom: 1rem;
    }
    h3 {
        color: #cccccc;
        font-size: 1.4rem;
        margin-top: 1.5rem;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 24px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        padding: 0px 24px;
        background-color: #1e1e1e;
        border-radius: 5px;
    }
    </style>
    """, unsafe_allow_html=True)

# Initialize session state
if 'data' not in st.session_state:
    st.session_state.data = None

# Helper function to generate sample data
def generate_sample_data():
    """Generate sample sales data for demonstration"""
    np.random.seed(42)
    
    stores = [
        "MENS CLUB SHANKARPALLY",
        "MENS CLUB BHONGIR",
        "MENS CLUB KORUTLA STORE",
        "MENS CLUB BELLAMPALLY",
        "RAJ FASHIONS RETAIL LLP-NAGAKURNOOL",
        "DIAMOND JUBILEE FASHIONS-NALGONDA",
        "RAJ FASHIONS RETAIL LLP-M27 WARANGAL",
        "FASHION UNLIMITED -KODAD"
    ]
    
    categories = ["Shirts", "Trousers", "Shoes", "Accessories", "Suits", "Casual Wear"]
    
    dates = pd.date_range(start='2023-01-01', end='2024-12-31', freq='D')
    
    data = []
    for date in dates:
        for store in stores:
            for category in categories:
                # Generate realistic sales patterns
                base_sales = np.random.uniform(5000, 50000)
                
                # Add seasonality (higher sales in Dec, lower in summer)
                month_factor = 1.5 if date.month == 12 else (0.8 if date.month in [5, 6, 7] else 1.0)
                
                # Add some stores performing better
                store_factor = np.random.uniform(0.7, 1.3)
                
                # Year over year growth/decline
                year_factor = 1.1 if date.year == 2024 else 1.0
                
                sales = base_sales * month_factor * store_factor * year_factor
                
                data.append({
                    'Date': date,
                    'Store': store,
                    'Category': category,
                    'Sales': sales,
                    'Units_Sold': int(sales / np.random.uniform(200, 800)),
                    'Latitude': np.random.uniform(17.0, 18.5),
                    'Longitude': np.random.uniform(78.0, 80.0)
                })
    
    return pd.DataFrame(data)

# Sidebar
with st.sidebar:
    st.title("📊 Dashboard Controls")
    
    # Data Management Section
    st.header("🗂️ Data Management")
    
    uploaded_file = st.file_uploader(
        "Upload Sales Data (CSV/Excel)",
        type=['csv', 'xlsx', 'xls'],
        help="Upload your sales data file"
    )
    
    if uploaded_file is not None:
        try:
            if uploaded_file.name.endswith('.csv'):
                st.session_state.data = pd.read_csv(uploaded_file)
            else:
                st.session_state.data = pd.read_excel(uploaded_file)
            st.session_state.data['Date'] = pd.to_datetime(st.session_state.data['Date'])
            st.success("✅ Data uploaded successfully!")
        except Exception as e:
            st.error(f"Error loading file: {e}")
    
    # Use sample data button
    if st.button("📝 Use Sample Data"):
        with st.spinner("Generating sample data..."):
            st.session_state.data = generate_sample_data()
            st.success("✅ Sample data loaded!")
    
    st.divider()
    
    # Check if data is available
    if st.session_state.data is not None:
        df = st.session_state.data
        
        # View Mode Selection
        st.header("🎯 View Mode")
        analysis_type = st.radio(
            "Select Analysis",
            ["YOY – Like-to-Like Stores (LFL)", "YOY of HO", "Closed Stores", "New Stores"],
            index=0
        )
        
        st.divider()
        
        # Period Selection
        st.header("📅 Period Selection")
        
        period_type = st.radio(
            "Select Period Type",
            ["Predefined Periods", "Custom Date Range"],
            index=0
        )
        
        if period_type == "Predefined Periods":
            period = st.selectbox(
                "Select Period",
                ["Christmas (20-25 Dec)", "December Full Month", "January MTD", "Last 7 Days", "Last 30 Days", "Last Quarter"]
            )
        else:
            col1, col2 = st.columns(2)
            with col1:
                start_date = st.date_input("Start Date", df['Date'].min())
            with col2:
                end_date = st.date_input("End Date", df['Date'].max())
        
        st.divider()
        
        # Filters
        st.header("🔍 Filters")
        
        if 'Store' in df.columns:
            selected_stores = st.multiselect(
                "Select Stores",
                options=df['Store'].unique(),
                default=df['Store'].unique()
            )
        
        if 'Category' in df.columns:
            selected_categories = st.multiselect(
                "Select Categories",
                options=df['Category'].unique(),
                default=df['Category'].unique()
            )
        
        # Alert Threshold
        st.divider()
        st.header("⚠️ Alert Settings")
        alert_threshold = st.slider(
            "YOY Decline Alert (%)",
            min_value=-50,
            max_value=0,
            value=-10,
            help="Get alerts for stores with YOY decline below this threshold"
        )
        
        st.divider()
        
        # Export Options
        st.header("💾 Export Options")
        export_df = df.copy()
        
        if st.button("📥 Download CSV"):
            csv = export_df.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="Click to Download",
                data=csv,
                file_name=f"sales_data_{datetime.now().strftime('%Y%m%d')}.csv",
                mime="text/csv"
            )
        
        if st.button("📥 Download Excel"):
            buffer = io.BytesIO()
            with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
                export_df.to_excel(writer, index=False, sheet_name='Sales Data')
            st.download_button(
                label="Click to Download",
                data=buffer.getvalue(),
                file_name=f"sales_data_{datetime.now().strftime('%Y%m%d')}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
    else:
        st.warning("⚠️ Please upload data or use sample data to begin")

# Main Content
if st.session_state.data is not None:
    df = st.session_state.data.copy()
    
    # Apply filters
    if 'selected_stores' in locals():
        df = df[df['Store'].isin(selected_stores)]
    if 'selected_categories' in locals():
        df = df[df['Category'].isin(selected_categories)]
    
    # Apply date filters
    if period_type == "Custom Date Range":
        df = df[(df['Date'] >= pd.to_datetime(start_date)) & (df['Date'] <= pd.to_datetime(end_date))]
    else:
        # Implement predefined periods
        today = df['Date'].max()
        if period == "Christmas (20-25 Dec)":
            df = df[(df['Date'].dt.month == 12) & (df['Date'].dt.day >= 20) & (df['Date'].dt.day <= 25)]
        elif period == "December Full Month":
            df = df[df['Date'].dt.month == 12]
        elif period == "January MTD":
            df = df[(df['Date'].dt.month == 1) & (df['Date'] <= today)]
        elif period == "Last 7 Days":
            df = df[df['Date'] >= (today - timedelta(days=7))]
        elif period == "Last 30 Days":
            df = df[df['Date'] >= (today - timedelta(days=30))]
        elif period == "Last Quarter":
            df = df[df['Date'] >= (today - timedelta(days=90))]
    
    # Title
    st.title("📊 Sales Performance Dashboard")
    period_text = period if period_type == "Predefined Periods" else f"Custom: {start_date} to {end_date}"
    st.markdown(f"**{analysis_type}** | **{period_text}** — YOY Review")
    
    # Calculate KPIs
    current_year = df['Date'].dt.year.max()
    last_year = current_year - 1
    
    df_cy = df[df['Date'].dt.year == current_year]
    df_ly = df[df['Date'].dt.year == last_year]
    
    sales_cy = df_cy['Sales'].sum()
    sales_ly = df_ly['Sales'].sum()
    net_yoy = sales_cy - sales_ly
    yoy_percent = ((sales_cy - sales_ly) / sales_ly * 100) if sales_ly > 0 else 0
    
    # KPI Metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="💰 Sales LY",
            value=f"₹{sales_ly:,.0f}"
        )
    
    with col2:
        st.metric(
            label="💰 Sales CY",
            value=f"₹{sales_cy:,.0f}"
        )
    
    with col3:
        st.metric(
            label="📈 Net YOY",
            value=f"₹{net_yoy:,.0f}",
            delta=f"{yoy_percent:.1f}%"
        )
    
    with col4:
        st.metric(
            label="📊 YOY %",
            value=f"{yoy_percent:.1f}%",
            delta=f"{yoy_percent:.1f}%"
        )
    
    st.divider()
    
    # Tabs for different sections
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "🏪 Store Performance",
        "📦 Category Analysis",
        "📈 Trends & Forecasting",
        "🗺️ Geographic View",
        "⚠️ Alerts & Insights",
        "📊 Comparative Analysis"
    ])
    
    # Tab 1: Store Performance
    with tab1:
        st.header("Store Performance Analysis")
        
        # Calculate store-level YOY
        store_performance = []
        for store in df['Store'].unique():
            store_cy = df_cy[df_cy['Store'] == store]['Sales'].sum()
            store_ly = df_ly[df_ly['Store'] == store]['Sales'].sum()
            store_yoy = ((store_cy - store_ly) / store_ly * 100) if store_ly > 0 else 0
            
            store_performance.append({
                'Store': store,
                'Sales_CY': store_cy,
                'Sales_LY': store_ly,
                'YOY_%': store_yoy,
                'YOY_Positive': store_yoy >= 0
            })
        
        store_df = pd.DataFrame(store_performance)
        store_df = store_df.sort_values('YOY_%', ascending=True)
        
        # Store performance bar chart
        fig_stores = go.Figure()
        
        colors = ['green' if x else 'red' for x in store_df['YOY_Positive']]
        
        fig_stores.add_trace(go.Bar(
            y=store_df['Store'],
            x=store_df['YOY_%'],
            orientation='h',
            marker=dict(color=colors),
            text=store_df['YOY_%'].apply(lambda x: f"{x:.1f}%"),
            textposition='outside',
            hovertemplate='<b>%{y}</b><br>YOY: %{x:.1f}%<extra></extra>'
        ))
        
        fig_stores.update_layout(
            title=f"Store YOY Performance - {period_text}",
            xaxis_title="YOY %",
            yaxis_title="Store",
            height=max(400, len(store_df) * 40),
            showlegend=False,
            template="plotly_dark",
            xaxis=dict(zeroline=True, zerolinecolor='white', zerolinewidth=2)
        )
        
        st.plotly_chart(fig_stores, use_container_width=True)
        
        # Store details table
        st.subheader("📋 Store Details")
        
        store_display = store_df.copy()
        store_display['Sales_CY'] = store_display['Sales_CY'].apply(lambda x: f"₹{x:,.0f}")
        store_display['Sales_LY'] = store_display['Sales_LY'].apply(lambda x: f"₹{x:,.0f}")
        store_display['YOY_%'] = store_display['YOY_%'].apply(lambda x: f"{x:.1f}%")
        store_display = store_display.drop('YOY_Positive', axis=1)
        
        st.dataframe(store_display, use_container_width=True, hide_index=True)
    
    # Tab 2: Category Analysis
    with tab2:
        st.header("Category Performance Analysis")
        
        if 'Category' in df.columns:
            # Category sales breakdown
            col1, col2 = st.columns(2)
            
            with col1:
                category_sales = df_cy.groupby('Category')['Sales'].sum().sort_values(ascending=False)
                
                fig_category_pie = px.pie(
                    values=category_sales.values,
                    names=category_sales.index,
                    title=f"Category Sales Distribution ({current_year})",
                    template="plotly_dark",
                    hole=0.4
                )
                fig_category_pie.update_traces(textposition='inside', textinfo='percent+label')
                st.plotly_chart(fig_category_pie, use_container_width=True)
            
            with col2:
                # Category YOY comparison
                category_comparison = []
                for category in df['Category'].unique():
                    cat_cy = df_cy[df_cy['Category'] == category]['Sales'].sum()
                    cat_ly = df_ly[df_ly['Category'] == category]['Sales'].sum()
                    
                    category_comparison.append({
                        'Category': category,
                        f'{current_year}': cat_cy,
                        f'{last_year}': cat_ly
                    })
                
                cat_comp_df = pd.DataFrame(category_comparison)
                
                fig_category_bar = go.Figure()
                fig_category_bar.add_trace(go.Bar(
                    name=str(last_year),
                    x=cat_comp_df['Category'],
                    y=cat_comp_df[f'{last_year}'],
                    marker_color='lightblue'
                ))
                fig_category_bar.add_trace(go.Bar(
                    name=str(current_year),
                    x=cat_comp_df['Category'],
                    y=cat_comp_df[f'{current_year}'],
                    marker_color='darkblue'
                ))
                
                fig_category_bar.update_layout(
                    title="Category YOY Comparison",
                    xaxis_title="Category",
                    yaxis_title="Sales (₹)",
                    barmode='group',
                    template="plotly_dark",
                    height=400
                )
                
                st.plotly_chart(fig_category_bar, use_container_width=True)
            
            # Category performance by store - Heatmap
            st.subheader("Category Performance by Store")
            
            category_store = df_cy.groupby(['Store', 'Category'])['Sales'].sum().reset_index()
            category_store_pivot = category_store.pivot(index='Store', columns='Category', values='Sales').fillna(0)
            
            fig_heatmap = px.imshow(
                category_store_pivot,
                labels=dict(x="Category", y="Store", color="Sales (₹)"),
                title="Category Sales Heatmap by Store",
                aspect="auto",
                color_continuous_scale="Blues",
                template="plotly_dark"
            )
            
            fig_heatmap.update_xaxes(side="top")
            st.plotly_chart(fig_heatmap, use_container_width=True)
            
            # Category metrics table
            st.subheader("📊 Category Metrics")
            
            category_metrics = []
            for category in df['Category'].unique():
                cat_cy = df_cy[df_cy['Category'] == category]['Sales'].sum()
                cat_ly = df_ly[df_ly['Category'] == category]['Sales'].sum()
                cat_yoy = ((cat_cy - cat_ly) / cat_ly * 100) if cat_ly > 0 else 0
                
                if 'Units_Sold' in df.columns:
                    units = df_cy[df_cy['Category'] == category]['Units_Sold'].sum()
                else:
                    units = 0
                
                category_metrics.append({
                    'Category': category,
                    'Sales (₹)': f"₹{cat_cy:,.0f}",
                    'YOY %': f"{cat_yoy:.1f}%",
                    'Units Sold': f"{units:,}"
                })
            
            st.dataframe(pd.DataFrame(category_metrics), use_container_width=True, hide_index=True)
    
    # Tab 3: Trends & Forecasting
    with tab3:
        st.header("Sales Trends & Forecasting")
        
        # Daily trend
        daily_sales = df.groupby('Date')['Sales'].sum().reset_index()
        daily_sales = daily_sales.sort_values('Date')
        
        fig_trend = go.Figure()
        
        # Add CY line
        daily_cy = daily_sales[daily_sales['Date'].dt.year == current_year]
        fig_trend.add_trace(go.Scatter(
            x=daily_cy['Date'],
            y=daily_cy['Sales'],
            mode='lines',
            name=f'{current_year}',
            line=dict(color='blue', width=2)
        ))
        
        # Add LY line
        daily_ly = daily_sales[daily_sales['Date'].dt.year == last_year]
        daily_ly_copy = daily_ly.copy()
        daily_ly_copy['Date_Adjusted'] = daily_ly_copy['Date'] + pd.DateOffset(years=1)
        fig_trend.add_trace(go.Scatter(
            x=daily_ly_copy['Date_Adjusted'],
            y=daily_ly_copy['Sales'],
            mode='lines',
            name=f'{last_year}',
            line=dict(color='lightblue', width=2, dash='dash')
        ))
        
        fig_trend.update_layout(
            title="Daily Sales Trend - Year over Year",
            xaxis_title="Date",
            yaxis_title="Sales (₹)",
            template="plotly_dark",
            height=400,
            hovermode='x unified'
        )
        
        st.plotly_chart(fig_trend, use_container_width=True)
        
        # Weekly and Monthly aggregation
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📅 Weekly Performance")
            df_weekly = df.copy()
            df_weekly['Week'] = df_weekly['Date'].dt.to_period('W').astype(str)
            df_weekly['Year'] = df_weekly['Date'].dt.year
            weekly_sales = df_weekly.groupby(['Week', 'Year'])['Sales'].sum().reset_index()
            
            fig_weekly = px.line(
                weekly_sales,
                x='Week',
                y='Sales',
                color='Year',
                title="Weekly Sales Comparison",
                template="plotly_dark",
                markers=True
            )
            fig_weekly.update_xaxes(tickangle=45)
            fig_weekly.update_layout(height=350)
            st.plotly_chart(fig_weekly, use_container_width=True)
        
        with col2:
            st.subheader("📊 Monthly Performance")
            df_monthly = df.copy()
            df_monthly['Month'] = df_monthly['Date'].dt.to_period('M').astype(str)
            df_monthly['Year'] = df_monthly['Date'].dt.year
            monthly_sales = df_monthly.groupby(['Month', 'Year'])['Sales'].sum().reset_index()
            
            fig_monthly = px.bar(
                monthly_sales,
                x='Month',
                y='Sales',
                color='Year',
                title="Monthly Sales Comparison",
                template="plotly_dark",
                barmode='group'
            )
            fig_monthly.update_xaxes(tickangle=45)
            fig_monthly.update_layout(height=350)
            st.plotly_chart(fig_monthly, use_container_width=True)
        
        # Simple Forecasting
        st.subheader("🔮 Sales Forecast (Next 30 Days)")
        
        try:
            forecast_data = df_cy.groupby('Date')['Sales'].sum().sort_index()
            
            if len(forecast_data) > 7:
                # Simple moving average forecast
                last_date = forecast_data.index[-1]
                forecast_dates = pd.date_range(start=last_date + timedelta(days=1), periods=30, freq='D')
                
                # Use last 30 days average as forecast
                forecast_value = forecast_data.tail(30).mean()
                forecast_values = [forecast_value] * 30
                
                # Plot
                fig_forecast = go.Figure()
                
                # Historical data (last 60 days)
                historical = forecast_data.tail(60)
                fig_forecast.add_trace(go.Scatter(
                    x=historical.index,
                    y=historical.values,
                    mode='lines',
                    name='Actual Sales',
                    line=dict(color='blue', width=2)
                ))
                
                # Forecast
                fig_forecast.add_trace(go.Scatter(
                    x=forecast_dates,
                    y=forecast_values,
                    mode='lines',
                    name='Forecast',
                    line=dict(color='orange', width=2, dash='dash')
                ))
                
                fig_forecast.update_layout(
                    title="Sales Forecast - Next 30 Days",
                    xaxis_title="Date",
                    yaxis_title="Sales (₹)",
                    template="plotly_dark",
                    height=400,
                    hovermode='x unified'
                )
                
                st.plotly_chart(fig_forecast, use_container_width=True)
                
                st.info(f"📊 Forecasted average daily sales: ₹{forecast_value:,.0f}")
            else:
                st.warning("⚠️ Insufficient data for forecasting. Need at least 7 days of data.")
        except Exception as e:
            st.error(f"Error generating forecast: {e}")
    
    # Tab 4: Geographic View
    with tab4:
        st.header("Geographic Performance View")
        
        if 'Latitude' in df.columns and 'Longitude' in df.columns:
            # Store location map with performance
            store_geo = []
            for store in df['Store'].unique():
                store_data = df_cy[df_cy['Store'] == store]
                if len(store_data) > 0:
                    sales = store_data['Sales'].sum()
                    lat = store_data['Latitude'].iloc[0]
                    lon = store_data['Longitude'].iloc[0]
                    
                    # Calculate YOY
                    store_ly_sales = df_ly[df_ly['Store'] == store]['Sales'].sum()
                    yoy = ((sales - store_ly_sales) / store_ly_sales * 100) if store_ly_sales > 0 else 0
                    
                    store_geo.append({
                        'Store': store,
                        'Latitude': lat,
                        'Longitude': lon,
                        'Sales': sales,
                        'YOY_%': yoy,
                        'Size': sales / 10000
                    })
            
            geo_df = pd.DataFrame(store_geo)
            
            fig_map = px.scatter_mapbox(
                geo_df,
                lat='Latitude',
                lon='Longitude',
                size='Size',
                color='YOY_%',
                hover_name='Store',
                hover_data={
                    'Sales': ':,.0f',
                    'YOY_%': ':.1f',
                    'Latitude': False,
                    'Longitude': False,
                    'Size': False
                },
                color_continuous_scale=['red', 'yellow', 'green'],
                color_continuous_midpoint=0,
                zoom=7,
                height=600,
                title="Store Performance Map"
            )
            
            fig_map.update_layout(
                mapbox_style="carto-darkmatter",
                template="plotly_dark"
            )
            
            st.plotly_chart(fig_map, use_container_width=True)
            
            st.info("🗺️ Marker size represents sales volume. Color represents YOY performance (Red: Decline, Green: Growth)")
        else:
            st.warning("⚠️ Geographic data (Latitude/Longitude) not available in dataset")
            st.info("💡 Add 'Latitude' and 'Longitude' columns to your data to see geographic visualization")
    
    # Tab 5: Alerts & Insights
    with tab5:
        st.header("⚠️ Alerts & Business Insights")
        
        # Performance alerts
        underperforming = store_df[store_df['YOY_%'] < alert_threshold]
        
        if len(underperforming) > 0:
            st.error(f"🚨 **{len(underperforming)} store(s) below alert threshold ({alert_threshold}%)**")
            
            for idx, row in underperforming.iterrows():
                with st.expander(f"⚠️ {row['Store']} - YOY: {row['YOY_%']:.1f}%"):
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Sales CY", f"₹{row['Sales_CY']:,.0f}")
                    with col2:
                        st.metric("Sales LY", f"₹{row['Sales_LY']:,.0f}")
                    with col3:
                        st.metric("YOY Change", f"{row['YOY_%']:.1f}%")
                    
                    # Store-specific category insights
                    if 'Category' in df.columns:
                        store_data_cy = df_cy[df_cy['Store'] == row['Store']]
                        store_data_ly = df_ly[df_ly['Store'] == row['Store']]
                        
                        st.subheader("Category Performance")
                        cat_comparison = []
                        for cat in df['Category'].unique():
                            cat_cy = store_data_cy[store_data_cy['Category'] == cat]['Sales'].sum()
                            cat_ly = store_data_ly[store_data_ly['Category'] == cat]['Sales'].sum()
                            cat_yoy = ((cat_cy - cat_ly) / cat_ly * 100) if cat_ly > 0 else 0
                            
                            cat_comparison.append({
                                'Category': cat,
                                'CY': f"₹{cat_cy:,.0f}",
                                'LY': f"₹{cat_ly:,.0f}",
                                'YOY %': f"{cat_yoy:.1f}%"
                            })
                        
                        st.dataframe(pd.DataFrame(cat_comparison), use_container_width=True, hide_index=True)
        else:
            st.success(f"✅ All stores are performing above the alert threshold of {alert_threshold}%")
        
        st.divider()
        
        # Top performers
        st.subheader("🏆 Top Performing Stores")
        top_performers = store_df.nlargest(5, 'YOY_%')
        
        for idx, row in top_performers.iterrows():
            col1, col2, col3 = st.columns([3, 1, 1])
            with col1:
                st.write(f"**{row['Store']}**")
            with col2:
                st.write(f"₹{row['Sales_CY']:,.0f}")
            with col3:
                st.write(f"🔥 {row['YOY_%']:.1f}%")
        
        st.divider()
        
        # Business Insights
        st.subheader("💡 Key Insights")
        
        insights = []
        
        # Overall trend
        if yoy_percent > 0:
            insights.append(f"✅ Overall business is growing at {yoy_percent:.1f}% YOY")
        else:
            insights.append(f"⚠️ Overall business is declining at {abs(yoy_percent):.1f}% YOY")
        
        # Store performance spread
        best_store = store_df.iloc[-1]
        worst_store = store_df.iloc[0]
        insights.append(f"📊 Performance spread: {worst_store['YOY_%']:.1f}% to {best_store['YOY_%']:.1f}%")
        
        # Category insights
        if 'Category' in df.columns:
            category_yoy = []
            for category in df['Category'].unique():
                cat_cy = df_cy[df_cy['Category'] == category]['Sales'].sum()
                cat_ly = df_ly[df_ly['Category'] == category]['Sales'].sum()
                cat_yoy = ((cat_cy - cat_ly) / cat_ly * 100) if cat_ly > 0 else 0
                category_yoy.append({'Category': category, 'YOY': cat_yoy})
            
            cat_yoy_df = pd.DataFrame(category_yoy)
            best_category = cat_yoy_df.loc[cat_yoy_df['YOY'].idxmax()]
            worst_category = cat_yoy_df.loc[cat_yoy_df['YOY'].idxmin()]
            
            insights.append(f"📦 Best performing category: {best_category['Category']} ({best_category['YOY']:.1f}%)")
            insights.append(f"📦 Worst performing category: {worst_category['Category']} ({worst_category['YOY']:.1f}%)")
        
        for insight in insights:
            st.info(insight)
    
    # Tab 6: Comparative Analysis
    with tab6:
        st.header("📊 Comparative Analysis")
        
        # Store comparison selector
        st.subheader("Compare Stores")
        
        default_stores = list(df['Store'].unique())[:3] if len(df['Store'].unique()) >= 3 else list(df['Store'].unique())
        compare_stores = st.multiselect(
            "Select stores to compare",
            options=df['Store'].unique(),
            default=default_stores
        )
        
        if len(compare_stores) > 0:
            # Sales comparison
            comparison_data = []
            for store in compare_stores:
                store_cy = df_cy[df_cy['Store'] == store]['Sales'].sum()
                store_ly = df_ly[df_ly['Store'] == store]['Sales'].sum()
                
                comparison_data.append({
                    'Store': store,
                    'Current Year': store_cy,
                    'Last Year': store_ly
                })
            
            comp_df = pd.DataFrame(comparison_data)
            
            fig_comparison = go.Figure()
            fig_comparison.add_trace(go.Bar(
                name='Last Year',
                x=comp_df['Store'],
                y=comp_df['Last Year'],
                marker_color='lightblue'
            ))
            fig_comparison.add_trace(go.Bar(
                name='Current Year',
                x=comp_df['Store'],
                y=comp_df['Current Year'],
                marker_color='darkblue'
            ))
            
            fig_comparison.update_layout(
                title="Store Sales Comparison",
                xaxis_title="Store",
                yaxis_title="Sales (₹)",
                barmode='group',
                template="plotly_dark",
                height=400
            )
            
            st.plotly_chart(fig_comparison, use_container_width=True)
            
            # Time series comparison
            st.subheader("Sales Trend Comparison")
            
            trend_comparison = df[df['Store'].isin(compare_stores)].groupby(['Date', 'Store'])['Sales'].sum().reset_index()
            
            fig_trend_comp = px.line(
                trend_comparison,
                x='Date',
                y='Sales',
                color='Store',
                title="Daily Sales Trend by Store",
                template="plotly_dark",
                height=400
            )
            
            st.plotly_chart(fig_trend_comp, use_container_width=True)
            
            # Category performance comparison
            if 'Category' in df.columns:
                st.subheader("Category Performance Comparison")
                
                cat_store_comp = df_cy[df_cy['Store'].isin(compare_stores)].groupby(['Store', 'Category'])['Sales'].sum().reset_index()
                
                fig_cat_comp = px.bar(
                    cat_store_comp,
                    x='Category',
                    y='Sales',
                    color='Store',
                    title="Category Sales by Store",
                    barmode='group',
                    template="plotly_dark",
                    height=400
                )
                
                st.plotly_chart(fig_cat_comp, use_container_width=True)
        else:
            st.info("👆 Select stores to compare their performance")

else:
    # Welcome screen
    st.title("📊 Sales Performance Dashboard")
    st.markdown("### Welcome to your enhanced sales analytics platform!")
    
    st.markdown("""
    #### 🚀 Features Available:
    
    **📈 Analytics & Insights**
    - YOY performance analysis
    - Store-level comparisons
    - Category performance tracking
    - Sales trend analysis
    
    **📊 Visualizations**
    - Interactive charts and graphs
    - Geographic performance maps
    - Heatmaps and trends
    - Forecasting capabilities
    
    **⚙️ Advanced Features**
    - Custom date ranges
    - Multiple filter options
    - Export to CSV/Excel
    - Performance alerts
    - Comparative analysis
    
    **💾 Data Management**
    - Upload CSV or Excel files
    - Use sample data for testing
    - Historical data analysis
    
    #### 🎯 Getting Started:
    1. Use the sidebar to upload your data or load sample data
    2. Select your preferred analysis view
    3. Choose time periods and apply filters
    4. Explore different tabs for detailed insights
    
    #### 📋 Data Format:
    Your data should include these columns:
    - `Date` - Transaction date
    - `Store` - Store name
    - `Sales` - Sales amount
    - `Category` (optional) - Product category
    - `Units_Sold` (optional) - Quantity sold
    - `Latitude`, `Longitude` (optional) - For geographic view
    """)
    
    st.info("👈 **Get started by uploading your data or using sample data from the sidebar!**")
