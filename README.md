# 🧠 Property Intelligence Dashboard

A comprehensive property analysis and API testing platform built with Streamlit, featuring role-based dashboards and a complete Acumidata API testing playground.

## 🚀 Features

### 🏠 Property Analysis
- **Single Property Lookup** - Get detailed valuations, comparables, and market analysis
- **Batch Processing** - Upload CSV files for bulk property analysis
- **Multiple Valuation Models** - Quantarium, RELAR, and specialized reports

### 🔧 API Testing Playground
- **17 Live Endpoints** across 6 categories (Valuation, Comparables, Equity, Monitoring, Title, MLS/Listings)
- **Smart Form Detection** - Automatically shows appropriate input fields for each endpoint
- **Environment Switching** - Test on UAT or Production environments
- **Response Analysis** - Formatted summaries, raw JSON, and response statistics
- **Download Capabilities** - Export API responses as JSON files

### 👥 Role-Based Views (Planned)
- **Lender View** - Risk assessment, LTV ratios, compliance checking
- **Investor View** - ROI analysis, cash flow projections, investment scenarios  
- **Asset Manager View** - Portfolio management, operational metrics

## 📊 Supported API Endpoints

### Valuation Services (6 endpoints)
- Property Valuation (Full Report) - Quantarium comprehensive analysis
- RELAR Full Report - Complete RELAR property analysis
- RELAR Simple Report - Simplified valuation
- RELAR Ranged Report - Value range analysis
- Quantarium Collateral - Lending-focused reports
- QVM Simple - Quick estimates

### Comparable Properties (3 endpoints)
- Standard Comps - RELAR comparable properties
- Radius Search - Properties within specified distance
- Polygon Search - Custom geographic area analysis

### Additional Services
- **Equity Calculator** - Property equity analysis
- **Property Monitoring** - Portfolio tracking setup
- **Title Reports** - Comprehensive title information
- **MLS/Listings** - Property listings, delta reports, and data feeds

## 🛠️ Project Structure

```
datanest-dev/
├── main.py                 # Main Streamlit application
├── utils/
│   ├── acumidata_client.py # API client with 17 endpoints
│   ├── parser.py           # Data processing utilities
│   └── env_loader.py       # Environment management
├── components/
│   ├── api_playground.py   # Complete API testing interface
│   ├── valuation_card.py   # Property display components
│   ├── raw_json_view.py    # JSON response viewer
│   └── property_form.py    # Reusable input forms
├── roles/
│   ├── lender_view.py      # Lender-specific dashboard
│   ├── investor_view.py    # Investor analysis tools
│   └── asset_manager_view.py # Portfolio management
├── api_tools/
│   └── endpoint_explorer.py # API discovery tools
└── api_docs/
    └── acumidata_swagger.json # Complete API documentation
```

## 🔧 Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/brycemalcom/datanest-dev.git
   cd datanest-dev
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   venv\Scripts\activate  # Windows
   # source venv/bin/activate  # macOS/Linux
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   Create a `.env` file with your API keys:
   ```
   ACUMIDATA_UAT_KEY=your_uat_api_key
   ACUMIDATA_PROD_KEY=your_production_api_key
   ```

5. **Run the application**
   ```bash
   streamlit run main.py
   ```

## 🎯 Usage

### Property Lookup
1. Navigate to the **Property Lookup** tab
2. Enter property address details
3. Click "Get Valuation" for comprehensive analysis

### API Testing
1. Go to the **API Playground** tab
2. Select your environment (UAT/PROD)
3. Choose an endpoint category and specific endpoint
4. Fill in the appropriate form fields
5. View results in Summary, Raw JSON, or Stats tabs

### Batch Processing
1. Use the **Batch Processing** tab
2. Upload a CSV with columns: address, city, state, zip
3. Process multiple properties simultaneously
4. Download enriched results

## 🔑 API Categories

- **Valuation** - Property value estimates and analysis
- **Comparables** - Similar property data and market analysis
- **Equity** - Property equity calculations
- **Monitoring** - Portfolio tracking and alerts
- **Title** - Property ownership and legal information
- **MLS/Listings** - Real estate listing data and feeds

## 🌟 Key Features

- **100% Acumidata API Coverage** - All property address-based endpoints
- **Intelligent Form Handling** - 5 different form types for different endpoint needs
- **Response Intelligence** - Smart parsing and display of API responses
- **Environment Management** - Seamless switching between UAT and Production
- **Export Capabilities** - Download responses and processed data
- **User Authentication** - Secure login and session management

## 🚧 Development Roadmap

- [ ] Implement role-based dashboard views
- [ ] Add data visualization and charting
- [ ] Integrate mapping and geographic analysis
- [ ] Build automated reporting features
- [ ] Add portfolio management tools
- [ ] Implement advanced filtering and search

## 📝 License

This project is licensed under the MIT License.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

---

**Built with ❤️ using Streamlit and the Acumidata API**
