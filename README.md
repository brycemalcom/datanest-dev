# DataNest Dev - Property Valuation Dashboard

A modular Streamlit application for property valuation analysis with role-based dashboards and API testing capabilities.

## 🏗️ Project Structure

```
datanest-dev/
├── main.py                 # Main Streamlit application entry point
├── requirements.txt        # Python dependencies
├── .gitignore             # Git ignore rules
├── users.json             # User authentication data
├── README.md              # This file
│
├── roles/                 # Role-based dashboard views
│   ├── __init__.py
│   ├── lender_view.py     # Lender-specific dashboard
│   ├── investor_view.py   # Investor-specific dashboard
│   └── asset_manager_view.py  # Asset manager dashboard
│
├── api_tools/             # API testing and exploration
│   ├── __init__.py
│   └── endpoint_explorer.py  # Interactive API testing playground
│
├── components/            # Reusable UI components
│   ├── __init__.py
│   ├── valuation_card.py  # Property valuation display component
│   ├── raw_json_view.py   # JSON response viewer
│   └── property_form.py   # Reusable property input forms
│
└── utils/                 # Utility modules
    ├── __init__.py
    ├── acumidata_client.py    # API client for property data
    ├── parser.py              # Data parsing utilities
    └── env_loader.py          # Environment configuration loader
```

## 🚀 Features

### Core Functionality
- **Property Valuation**: Get comprehensive property valuations with comparables
- **CSV Bulk Processing**: Upload and process multiple properties at once
- **User Authentication**: Secure login/signup system
- **Role-Based Views**: Different dashboards for Lenders, Investors, and Asset Managers

### API Testing Playground
- **Endpoint Explorer**: Test different API endpoints interactively
- **Environment Switching**: Toggle between UAT and Production environments
- **Response Analysis**: View formatted data, raw JSON, and key metrics
- **Download Capabilities**: Export API responses as JSON files

### Role-Based Dashboards

#### 🏦 Lender View
- Risk assessment metrics (LTV, DSCR, Risk Score)
- Loan scenario modeling
- Compliance checking
- Market trend analysis

#### 📈 Investor View
- ROI analysis (Cap Rate, Cash-on-Cash, IRR)
- Cash flow projections
- Market comparisons
- Investment scenario modeling

#### 🏢 Asset Manager View
- Portfolio overview and composition
- Operational metrics and KPIs
- Maintenance tracking and scheduling
- Geographic distribution analysis

## 🛠️ Installation & Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd datanest-dev
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   Create a `.env` file in the root directory:
   ```env
   ACUMIDATA_UAT_KEY=your_uat_api_key
   ACUMIDATA_PROD_KEY=your_prod_api_key
   ```

5. **Run the application**
   ```bash
   streamlit run main.py
   ```

## 📋 Usage

### Basic Property Lookup
1. Log in or create an account
2. Enter property details (address, city, state, zip)
3. Click "Get Valuation" to retrieve property data
4. View formatted results with comparables

### API Testing
1. Navigate to the API Explorer section
2. Select an endpoint to test
3. Choose environment (UAT/Production)
4. Enter property information
5. View results in multiple formats

### Role-Based Analysis
1. Select your role (Lender/Investor/Asset Manager)
2. Access role-specific metrics and analysis
3. Use specialized tools for your workflow

### Bulk Processing
1. Prepare a CSV file with columns: address, city, state, zip
2. Upload the file using the CSV uploader
3. Process all properties and download enriched results

## 🔧 Configuration

### Environment Variables
- `ACUMIDATA_UAT_KEY`: API key for UAT environment
- `ACUMIDATA_PROD_KEY`: API key for Production environment
- `DEBUG`: Enable debug mode (True/False)
- `LOG_LEVEL`: Logging level (INFO, DEBUG, WARNING, ERROR)

### API Endpoints
The application supports multiple Acumidata API endpoints:
- **Property Valuation**: `/api/Valuation/estimate`
- **QVM Simple**: `/api/Valuation/qvmsimple`
- **Property Advantage**: `/api/Comps/advantage`
- **Equity Analysis**: `/api/Equity/analysis` (Coming Soon)
- **Property Monitoring**: `/api/Monitor/alerts` (Coming Soon)

## 🧩 Modular Architecture

### Components
Reusable UI components for consistent interface:
- `ValuationCard`: Property valuation display
- `RawJsonView`: JSON response viewer with download
- `PropertyForm`: Standardized property input forms

### Roles
Role-specific dashboard implementations:
- `LenderView`: Risk-focused metrics and compliance
- `InvestorView`: ROI analysis and market insights
- `AssetManagerView`: Portfolio and operational management

### Utils
Utility modules for core functionality:
- `AcumidataClient`: API communication layer
- `PropertyDataParser`: Response data processing
- `EnvLoader`: Configuration management

## 🔒 Security

- User authentication with hashed passwords
- Environment variable protection for API keys
- Secure session management
- Input validation and sanitization

## 📈 Development Roadmap

- [ ] Add more API endpoints (Equity, Monitoring)
- [ ] Implement database integration
- [ ] Add data visualization charts
- [ ] Create export/reporting features
- [ ] Implement user role permissions
- [ ] Add property comparison tools

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 📞 Support

For questions or support, please contact the development team or create an issue in the repository. 