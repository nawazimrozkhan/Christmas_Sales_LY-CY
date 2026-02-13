# 📊 Enhanced Sales Performance Dashboard

A comprehensive sales analytics platform built with Streamlit, featuring advanced visualizations, forecasting, and business intelligence capabilities.

## 🌟 Features

### 1. **📈 Advanced Analytics**
- Year-over-Year (YOY) performance comparison
- Like-to-Like store analysis
- Store-level and category-level breakdowns
- Historical data analysis
- Performance trend tracking

### 2. **📊 Rich Visualizations**
- Interactive bar charts and line graphs
- Donut charts for category distribution
- Heatmaps for store-category performance
- Geographic performance maps
- Time series comparisons

### 3. **🔮 Forecasting & Trends**
- 30-day sales forecasting using moving averages
- Daily, weekly, and monthly trend analysis
- Year-over-year trend overlays
- Seasonality pattern identification

### 4. **🗺️ Geographic Analysis**
- Interactive map with store locations
- Performance visualization by geography
- Size-based markers for sales volume
- Color-coded YOY performance indicators

### 5. **⚠️ Alerts & Insights**
- Customizable performance alerts
- Automatic identification of underperforming stores
- Top performer highlights
- AI-generated business insights
- Category performance breakdowns

### 6. **📊 Comparative Analysis**
- Multi-store comparison tools
- Side-by-side performance metrics
- Category performance across stores
- Time-series trend comparisons

### 7. **💾 Data Management**
- Upload CSV or Excel files
- Sample data generation for testing
- Data export to CSV/Excel
- Historical data retention
- Multiple filter options

### 8. **🎨 Enhanced UI/UX**
- Dark mode interface
- Responsive design
- Interactive filters and controls
- Tabbed navigation
- Custom date range selection
- Multi-select store and category filters

## 📋 Data Format

Your data file should include the following columns:

### Required Columns:
- `Date` - Transaction date (YYYY-MM-DD format)
- `Store` - Store name or identifier
- `Sales` - Sales amount (numeric)

### Optional Columns:
- `Category` - Product category (for category analysis)
- `Units_Sold` - Number of units sold
- `Latitude` - Store latitude (for geographic visualization)
- `Longitude` - Store longitude (for geographic visualization)

### Example Data Structure:
```csv
Date,Store,Category,Sales,Units_Sold,Latitude,Longitude
2024-01-01,MENS CLUB SHANKARPALLY,Shirts,25000,45,17.4523,78.1234
2024-01-01,MENS CLUB BHONGIR,Trousers,18000,32,17.3421,78.8765
```

## 🚀 Getting Started

### Option 1: Local Development

1. **Clone or download the files**
   ```bash
   # Make sure you have app.py and requirements.txt
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   streamlit run app.py
   ```

4. **Access the dashboard**
   - Open your browser to `http://localhost:8501`

### Option 2: Deploy to Streamlit Cloud

1. **Push to GitHub**
   ```bash
   git init
   git add app.py requirements.txt README.md
   git commit -m "Initial commit"
   git remote add origin YOUR_GITHUB_REPO_URL
   git push -u origin main
   ```

2. **Deploy on Streamlit Cloud**
   - Go to [share.streamlit.io](https://share.streamlit.io)
   - Click "New app"
   - Select your repository
   - Set main file path to `app.py`
   - Click "Deploy"

### Option 3: Update Existing Streamlit App

If you already have a Streamlit app running:

1. **Replace your existing files**
   - Replace your current `app.py` with the new one
   - Replace your current `requirements.txt` with the new one

2. **Commit and push changes**
   ```bash
   git add app.py requirements.txt
   git commit -m "Update to enhanced dashboard"
   git push origin main
   ```

3. **Streamlit Cloud will automatically redeploy**

## 🎯 Usage Guide

### 1. **Loading Data**
- Click "Upload Sales Data" in the sidebar
- OR click "Use Sample Data" to try the demo
- Supported formats: CSV, XLSX, XLS

### 2. **Selecting Analysis Type**
- YOY – Like-to-Like Stores (LFL)
- YOY of HO
- Closed Stores
- New Stores

### 3. **Choosing Time Periods**
**Predefined Periods:**
- Christmas (20-25 Dec)
- December Full Month
- January MTD
- Last 7 Days
- Last 30 Days
- Last Quarter

**Custom Date Range:**
- Select any start and end date

### 4. **Applying Filters**
- Select specific stores
- Filter by product categories
- Set alert thresholds

### 5. **Exploring Tabs**
- **🏪 Store Performance** - Individual store metrics and rankings
- **📦 Category Analysis** - Product category breakdowns
- **📈 Trends & Forecasting** - Historical trends and predictions
- **🗺️ Geographic View** - Map-based performance visualization
- **⚠️ Alerts & Insights** - Warnings and key findings
- **📊 Comparative Analysis** - Multi-store comparisons

### 6. **Exporting Data**
- Click "Download CSV" or "Download Excel" in sidebar
- All current filters and selections are applied to exports

## 🔧 Customization

### Modifying Alert Thresholds
Adjust the YOY Decline Alert slider in the sidebar (default: -10%)

### Adding New Metrics
Edit the `app.py` file to add custom calculations in the KPI section

### Changing Color Schemes
Modify the Plotly theme in the chart configurations:
```python
template="plotly_dark"  # Change to "plotly", "plotly_white", etc.
```

### Adding More Period Options
Edit the period selection in the sidebar section

## 📊 Key Metrics Explained

### Sales LY (Last Year)
Total sales from the same period in the previous year

### Sales CY (Current Year)
Total sales from the current period

### Net YOY
Absolute difference between current year and last year sales

### YOY %
Percentage change from last year to current year:
```
YOY % = ((Sales CY - Sales LY) / Sales LY) × 100
```

## 🛠️ Technical Stack

- **Framework**: Streamlit 1.31.0
- **Data Processing**: Pandas 2.2.0
- **Visualizations**: Plotly 5.18.0
- **Calculations**: NumPy 1.26.3
- **Excel Support**: OpenPyXL 3.1.2

## 📝 Tips & Best Practices

1. **Data Quality**: Ensure dates are in consistent format
2. **Performance**: Filter data for faster rendering with large datasets
3. **Comparisons**: Use the comparison tab for store benchmarking
4. **Exports**: Export filtered data for offline analysis
5. **Alerts**: Set realistic thresholds based on business context

## 🐛 Troubleshooting

### Issue: Charts not loading
**Solution**: Check if your data has the required columns (Date, Store, Sales)

### Issue: Date filtering not working
**Solution**: Ensure Date column is in proper datetime format

### Issue: Map not showing
**Solution**: Add Latitude and Longitude columns to your data

### Issue: Upload fails
**Solution**: Verify your file format (CSV/XLSX) and column names

## 🎉 All Features Implemented

- ✅ Product category performance tracking
- ✅ Daily/weekly/monthly trend charts
- ✅ Sales forecasting (30 days)
- ✅ Geographic maps with store performance
- ✅ Time series trends with year-over-year overlay
- ✅ Comparative bar charts and visualizations
- ✅ Performance heatmaps
- ✅ Data export to CSV and Excel
- ✅ Custom date range selection
- ✅ Advanced filtering (stores, categories)
- ✅ Performance alerts for underperforming stores
- ✅ Store comparison tool with multiple metrics
- ✅ Interactive filters and controls
- ✅ Mobile-responsive design
- ✅ Dark theme with custom styling
- ✅ Upload functionality for CSV/Excel
- ✅ Sample data generation for testing
- ✅ Historical data analysis across years
- ✅ Drill-down capabilities in alerts section
- ✅ Multi-tab navigation for organized insights

---

**Built with ❤️ for data-driven decision making**
