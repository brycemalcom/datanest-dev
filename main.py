import streamlit as st
from utils.acumidata_client import AcumidataClient
from components.api_playground import APIPlayground
import pandas as pd
import io
import hashlib
import json
import os
from concurrent.futures import ThreadPoolExecutor, as_completed
import time

# Initialize session state
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'username' not in st.session_state:
    st.session_state.username = None

# Simple user database (in production, use a real database)
USER_DB_FILE = "users.json"

def load_users():
    """Load users from JSON file"""
    if os.path.exists(USER_DB_FILE):
        with open(USER_DB_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_users(users):
    """Save users to JSON file"""
    with open(USER_DB_FILE, 'w') as f:
        json.dump(users, f)

def hash_password(password):
    """Hash password using SHA256"""
    return hashlib.sha256(password.encode()).hexdigest()

def verify_password(password, hashed):
    """Verify password against hash"""
    return hash_password(password) == hashed

def login_form():
    """Display login form"""
    st.title("🔐 Login to Property Intelligence Dashboard")
    
    with st.form("login_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        login_button = st.form_submit_button("Login")
        
        if login_button:
            users = load_users()
            if username in users and verify_password(password, users[username]['password']):
                st.session_state.authenticated = True
                st.session_state.username = username
                st.success("Login successful!")
                st.rerun()
            else:
                st.error("Invalid username or password")
    
    st.markdown("---")
    st.subheader("Don't have an account?")
    if st.button("Sign Up"):
        st.session_state.show_signup = True
        st.rerun()

def signup_form():
    """Display signup form"""
    st.title("📝 Create Account")
    
    with st.form("signup_form"):
        username = st.text_input("Choose Username")
        email = st.text_input("Email")
        password = st.text_input("Choose Password", type="password")
        confirm_password = st.text_input("Confirm Password", type="password")
        signup_button = st.form_submit_button("Create Account")
        
        if signup_button:
            if not username or not email or not password:
                st.error("Please fill in all fields")
            elif password != confirm_password:
                st.error("Passwords don't match")
            elif len(password) < 6:
                st.error("Password must be at least 6 characters")
            else:
                users = load_users()
                if username in users:
                    st.error("Username already exists")
                else:
                    users[username] = {
                        'email': email,
                        'password': hash_password(password)
                    }
                    save_users(users)
                    st.success("Account created successfully! Please login.")
                    st.session_state.show_signup = False
                    st.rerun()
    
    if st.button("Back to Login"):
        st.session_state.show_signup = False
        st.rerun()

def logout():
    """Logout function"""
    st.session_state.authenticated = False
    st.session_state.username = None
    if 'show_signup' in st.session_state:
        del st.session_state.show_signup
    st.rerun()

# Authentication check
if not st.session_state.authenticated:
    if 'show_signup' in st.session_state and st.session_state.show_signup:
        signup_form()
    else:
        login_form()
    st.stop()

# Main app (only runs if authenticated)

st.set_page_config(page_title="Property Intelligence Dashboard", layout="centered")
st.markdown("""
<style>
.big-metric {
    font-size: 2.5rem;
    font-weight: bold;
    color: #2E8B57;
    margin-bottom: 0.5rem;
}
.metric-label {
    font-size: 1.1rem;
    color: #888;
    margin-bottom: 0.2rem;
}
.card {
    background: #f8f9fa;
    border-radius: 1rem;
    padding: 2rem 1.5rem 1.5rem 1.5rem;
    box-shadow: 0 2px 8px rgba(44,62,80,0.07);
    margin-bottom: 1.5rem;
}
</style>
""", unsafe_allow_html=True)

# Header with logout
col1, col2 = st.columns([3, 1])
with col1:
    st.title("🧠 Property Intelligence Dashboard")
    st.write(f"Welcome, {st.session_state.username}!")
with col2:
    st.write("")  # Add some spacing
    if st.button("Logout", type="secondary"):
        logout()

# Create tabs for different sections
tab1, tab2, tab3 = st.tabs(["🏠 Property Lookup", "📊 Batch Processing", "🔧 API Playground"])

with tab1:
    st.write("Enter a property address to get the latest valuation and comparables.")
    
    with st.form("lookup_form"):
        address = st.text_input("Street Address", "531 NE Beck Rd")
        city = st.text_input("City", "Belfair")
        state = st.text_input("State", "WA")
        zip_code = st.text_input("Zip Code", "98528")
        
        # Add report type selector
        report_type = st.selectbox(
            "Select Report Type",
            ["Get RELAR Full Report", "Get RELAR Simple Report", "Get Ranged Report"],
            help="Choose the type of valuation report you want to generate"
        )
        
        submitted = st.form_submit_button("Get Valuation")

    if submitted:
        with st.spinner("Fetching property data..."):
            client = AcumidataClient(environment="prod")
            
            # Map report types to API methods
            report_methods = {
                "Get RELAR Full Report": "get_valuation_advantage",
                "Get RELAR Simple Report": "get_valuation_simple",
                "Get Ranged Report": "get_valuation_ranged"
            }
            
            # Get the appropriate method based on selected report type
            method_name = report_methods[report_type]
            method = getattr(client, method_name)
            result = method(address, city, state, zip_code)
            
            if "error" in result:
                st.error(f"Error: {result['error']}")
            else:
                # Handle different response structures based on report type
                if report_type == "Get RELAR Full Report":
                    # Extract data from RELAR Full Report structure (correct paths from JSON)
                    search_data = result.get("searchData", {})
                    analysis = result.get("analysis", {})
                    metadata = result.get("metadata", {})
                    
                    # Property details from searchData
                    bedrooms = search_data.get("beds")
                    bathrooms = search_data.get("baths") 
                    year_built = search_data.get("yearBuilt")
                    home_size = search_data.get("size")  # Home size in sq ft
                    lot_size = search_data.get("lotSize")  # Lot size in sq ft
                    
                    # Valuation data from analysis.houseWorth.valuations.current
                    house_worth = analysis.get("houseWorth", {})
                    valuations = house_worth.get("valuations", {})
                    current_valuation = valuations.get("current", {})
                    
                    predicted_value = current_valuation.get("value")
                    confidence_score = current_valuation.get("confidence")
                    variance = current_valuation.get("variance")
                    
                    # PDF report link from metadata
                    pdf_link = metadata.get("reportPDFLink")
                    
                    # Convert string values to numbers if they exist
                    if predicted_value:
                        predicted_value = float(predicted_value)
                    if confidence_score:
                        confidence_score = float(confidence_score)
                    if variance:
                        variance = float(variance)
                    if home_size:
                        home_size = int(home_size)
                    if lot_size:
                        lot_size = int(lot_size)
                    
                    # Display property details
                    st.markdown('<div class="card">', unsafe_allow_html=True)
                    st.markdown('<div class="metric-label">Property Details</div>', unsafe_allow_html=True)
                    st.markdown(f'<div class="big-metric">{address}, {city}, {state} {zip_code}</div>', unsafe_allow_html=True)
                    if predicted_value:
                        st.markdown(f'<div class="big-metric">Estimated Value: ${predicted_value:,.0f}</div>', unsafe_allow_html=True)
                    st.markdown('</div>', unsafe_allow_html=True)

                    col1, col2, col3, col4 = st.columns(4)
                    with col1:
                        st.metric(label="Bedrooms", value=bedrooms if bedrooms else "N/A")
                    with col2:
                        st.metric(label="Bathrooms", value=bathrooms if bathrooms else "N/A")
                    with col3:
                        st.metric(label="Year Built", value=year_built if year_built else "N/A")
                    with col4:
                        if home_size:
                            st.metric(label="Home Size", value=f"{home_size:,} sq ft")
                        else:
                            st.metric(label="Home Size", value="N/A")

                    # Additional property details
                    if lot_size:
                        col1, col2 = st.columns([1, 3])
                        with col1:
                            st.metric(label="Lot Size", value=f"{lot_size:,} sq ft")

                    st.markdown("---")
                    st.subheader("Valuation Analysis 📊")
                    
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        if predicted_value:
                            st.metric(label="Current Value", value=f"${predicted_value:,.0f}")
                        else:
                            st.metric(label="Current Value", value="N/A")
                    with col2:
                        if confidence_score:
                            st.metric(label="Confidence Score", value=f"{confidence_score:.1f}%")
                        else:
                            st.metric(label="Confidence Score", value="N/A")
                    with col3:
                        if variance:
                            # Always show +/- for variance (positive or negative)
                            variance_sign = "+" if variance >= 0 else ""
                            st.metric(label="Variance", value=f"±${abs(variance):,.0f}", delta=f"{variance_sign}${variance:,.0f}")
                        else:
                            st.metric(label="Variance", value="N/A")
                    
                    # PDF Download Button
                    if pdf_link:
                        st.markdown("---")
                        st.subheader("📄 Report Download")
                        st.markdown(f"""
                        <a href="{pdf_link}" target="_blank" style="
                            display: inline-block;
                            background-color: #0066cc;
                            color: white;
                            padding: 0.5rem 1rem;
                            text-decoration: none;
                            border-radius: 0.5rem;
                            font-weight: bold;
                            margin: 0.5rem 0;
                        ">📥 Download PDF Report</a>
                        """, unsafe_allow_html=True)
                    
                elif report_type == "Get RELAR Simple Report":
                    # Extract data from RELAR Simple Report structure
                    prediction = result.get("prediction", {})
                    subject_parcel = result.get("subjectParcel", {})
                    structures = subject_parcel.get("structures", [])
                    metadata = result.get("metadata", {})
                    
                    # Valuation data from prediction
                    predicted_price = prediction.get("predictedPrice")
                    confidence_score = prediction.get("confidence")
                    price_low = prediction.get("priceLow")
                    price_high = prediction.get("priceHigh")
                    
                    # Property details from subjectParcel.structures[0]
                    if structures and len(structures) > 0:
                        structure = structures[0]
                        bedrooms = structure.get("bedrooms")
                        bathrooms = structure.get("bathrooms")
                        gla = structure.get("gla")  # Gross Living Area
                    else:
                        bedrooms = bathrooms = gla = None
                    
                    # PDF report link from metadata
                    pdf_link = metadata.get("reportPDFLink")
                    
                    # Convert string values to numbers if they exist
                    if predicted_price:
                        predicted_price = float(predicted_price)
                    if confidence_score:
                        confidence_score = float(confidence_score)
                    if price_low:
                        price_low = float(price_low)
                    if price_high:
                        price_high = float(price_high)
                    if gla:
                        gla = int(gla)
                    
                    # Display property details
                    st.markdown('<div class="card">', unsafe_allow_html=True)
                    st.markdown('<div class="metric-label">Property Details</div>', unsafe_allow_html=True)
                    st.markdown(f'<div class="big-metric">{address}, {city}, {state} {zip_code}</div>', unsafe_allow_html=True)
                    if predicted_price:
                        st.markdown(f'<div class="big-metric">Predicted Price: ${predicted_price:,.0f}</div>', unsafe_allow_html=True)
                    st.markdown('</div>', unsafe_allow_html=True)

                    # Property metrics (only 3 columns for Simple Report)
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric(label="Bedrooms", value=bedrooms if bedrooms is not None else "N/A")
                    with col2:
                        st.metric(label="Bathrooms", value=bathrooms if bathrooms is not None else "N/A")
                    with col3:
                        if gla is not None:
                            st.metric(label="Home Size", value=f"{gla:,} sq ft")
                        else:
                            st.metric(label="Home Size", value="N/A")

                    st.markdown("---")
                    st.subheader("Valuation Analysis 📊")
                    
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        if predicted_price:
                            st.metric(label="Predicted Price", value=f"${predicted_price:,.0f}")
                        else:
                            st.metric(label="Predicted Price", value="N/A")
                    with col2:
                        if confidence_score:
                            st.metric(label="Confidence Score", value=f"{confidence_score:.0f}%")
                        else:
                            st.metric(label="Confidence Score", value="N/A")
                    with col3:
                        if price_low and price_high:
                            # Use shorter format for price range to avoid cutoff
                            low_k = price_low / 1000
                            high_k = price_high / 1000
                            st.metric(label="Price Range", value=f"${low_k:.0f}K - ${high_k:.0f}K")
                        else:
                            st.metric(label="Price Range", value="N/A")
                    
                    # PDF Download Button
                    if pdf_link:
                        st.markdown("---")
                        st.subheader("📄 Report Download")
                        st.markdown(f"""
                        <a href="{pdf_link}" target="_blank" style="
                            display: inline-block;
                            background-color: #0066cc;
                            color: white;
                            padding: 0.5rem 1rem;
                            text-decoration: none;
                            border-radius: 0.5rem;
                            font-weight: bold;
                            margin: 0.5rem 0;
                        ">📥 Download PDF Report</a>
                        """, unsafe_allow_html=True)
                    
                elif report_type == "Get Ranged Report":
                    # Extract data from RELAR Ranged Report structure
                    prediction = result.get("prediction", {})
                    subject_parcel = result.get("subjectParcel", {})
                    structures = subject_parcel.get("structures", [])
                    metadata = result.get("metadata", {})
                    
                    # Valuation data from prediction (focus on range)
                    price_low = prediction.get("priceLow")
                    price_high = prediction.get("priceHigh")
                    confidence_score = prediction.get("confidence")
                    error_margin = prediction.get("error")
                    
                    # Property details from subjectParcel.structures[0]
                    if structures and len(structures) > 0:
                        structure = structures[0]
                        bedrooms = structure.get("bedrooms")
                        bathrooms = structure.get("bathrooms")
                        gla = structure.get("gla")  # Gross Living Area
                    else:
                        bedrooms = bathrooms = gla = None
                    
                    # PDF report link from metadata
                    pdf_link = metadata.get("reportPDFLink")
                    
                    # Convert string values to numbers if they exist
                    if price_low:
                        price_low = float(price_low)
                    if price_high:
                        price_high = float(price_high)
                    if confidence_score:
                        confidence_score = float(confidence_score)
                    if error_margin:
                        error_margin = float(error_margin)
                    if gla:
                        gla = int(gla)
                    
                    # Calculate midpoint for display
                    midpoint = None
                    if price_low and price_high:
                        midpoint = (price_low + price_high) / 2
                    
                    # Display property details
                    st.markdown('<div class="card">', unsafe_allow_html=True)
                    st.markdown('<div class="metric-label">Property Details</div>', unsafe_allow_html=True)
                    st.markdown(f'<div class="big-metric">{address}, {city}, {state} {zip_code}</div>', unsafe_allow_html=True)
                    if midpoint:
                        st.markdown(f'<div class="big-metric">Value Range: ${price_low:,.0f} - ${price_high:,.0f}</div>', unsafe_allow_html=True)
                    st.markdown('</div>', unsafe_allow_html=True)

                    # Property metrics (only 3 columns for Ranged Report)
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric(label="Bedrooms", value=bedrooms if bedrooms is not None else "N/A")
                    with col2:
                        st.metric(label="Bathrooms", value=bathrooms if bathrooms is not None else "N/A")
                    with col3:
                        if gla is not None:
                            st.metric(label="Home Size", value=f"{gla:,} sq ft")
                        else:
                            st.metric(label="Home Size", value="N/A")

                    st.markdown("---")
                    st.subheader("Valuation Range Analysis 📊")
                    
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        if price_low and price_high:
                            # Use shorter format for price range
                            low_k = price_low / 1000
                            high_k = price_high / 1000
                            st.metric(label="Value Range", value=f"${low_k:.0f}K - ${high_k:.0f}K")
                        else:
                            st.metric(label="Value Range", value="N/A")
                    with col2:
                        if confidence_score:
                            st.metric(label="Confidence Score", value=f"{confidence_score:.0f}%")
                        else:
                            st.metric(label="Confidence Score", value="N/A")
                    with col3:
                        if error_margin:
                            st.metric(label="Error Margin", value=f"±${error_margin/1000:.0f}K")
                        else:
                            st.metric(label="Error Margin", value="N/A")
                    
                    # PDF Download Button
                    if pdf_link:
                        st.markdown("---")
                        st.subheader("📄 Report Download")
                        st.markdown(f"""
                        <a href="{pdf_link}" target="_blank" style="
                            display: inline-block;
                            background-color: #0066cc;
                            color: white;
                            padding: 0.5rem 1rem;
                            text-decoration: none;
                            border-radius: 0.5rem;
                            font-weight: bold;
                            margin: 0.5rem 0;
                        ">📥 Download PDF Report</a>
                        """, unsafe_allow_html=True)
                    
                else:
                    # Use existing logic for other report types
                    details = result.get("Details", {})
                    property_valuation = details.get("PropertyValuation", {})
                    comps = details.get("ComparablePropertyListings", {}).get("Comparables", [])

                    estimated_value = property_valuation.get("EstimatedValue")
                    summary = details.get("PropertySummary", {})
                    
                    # PropertyBasics is nested inside PropertyDetails
                    property_details = details.get("PropertyDetails", {})
                    basics = property_details.get("PropertyBasics", {})
                    
                    # Get year built from PropertyBasics
                    year_built_actual = basics.get("YearBuiltActual") if basics else None
                    year_built_summary = summary.get("YearBuilt") if summary else None
                    year_built_valuation = property_valuation.get("YearBuilt") if property_valuation else None
                    
                    # Use the first available value and convert to string
                    if year_built_actual is not None:
                        year_built = str(year_built_actual)
                    elif year_built_summary is not None:
                        year_built = str(year_built_summary)
                    elif year_built_valuation is not None:
                        year_built = str(year_built_valuation)
                    else:
                        year_built = "N/A"
                        
                    beds = summary.get("Bedrooms", "N/A")
                    baths = summary.get("FullBaths", "N/A")

                    # Display property details
                    st.markdown('<div class="card">', unsafe_allow_html=True)
                    st.markdown('<div class="metric-label">Property Details</div>', unsafe_allow_html=True)
                    st.markdown(f'<div class="big-metric">{address}, {city}, {state} {zip_code}</div>', unsafe_allow_html=True)
                    if estimated_value:
                        st.markdown(f'<div class="big-metric">Estimated Value: ${estimated_value:,.2f}</div>', unsafe_allow_html=True)
                    st.markdown('</div>', unsafe_allow_html=True)

                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric(label="Beds", value=beds)
                    with col2:
                        st.metric(label="Baths", value=baths)
                    with col3:
                        st.metric(label="Year Built", value=year_built)

                    st.markdown("---")
                    st.subheader("Market Analysis 📊")
                    
                    # Get valuation range from PropertyValuation
                    valuation_low = property_valuation.get("ValuationRangeLow")
                    valuation_high = property_valuation.get("ValuationRangeHigh")
                    confidence_score = property_valuation.get("ConfidenceScore")
                    
                    # Display different metrics based on report type
                    if report_type == "Get Ranged Report":
                        col1, col2 = st.columns(2)
                        with col1:
                            if valuation_low:
                                st.metric(label="Valuation Low", value=f"${valuation_low:,.0f}")
                            else:
                                st.metric(label="Valuation Low", value="N/A")
                        with col2:
                            if valuation_high:
                                st.metric(label="Valuation High", value=f"${valuation_high:,.0f}")
                            else:
                                st.metric(label="Valuation High", value="N/A")
                    else:
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            if estimated_value:
                                st.metric(label="Estimated Value", value=f"${estimated_value:,.0f}")
                            else:
                                st.metric(label="Estimated Value", value="N/A")
                        with col2:
                            if confidence_score:
                                st.metric(label="Confidence Score", value=f"{confidence_score}/100")
                            else:
                                st.metric(label="Confidence Score", value="N/A")
                        with col3:
                            if valuation_low and valuation_high:
                                st.metric(label="Value Range", value=f"${valuation_low:,.0f} - ${valuation_high:,.0f}")
                            else:
                                st.metric(label="Value Range", value="N/A")
                    
                    if comps and report_type != "Get Ranged Report":
                        st.markdown("---")
                        st.subheader("Recent Comparable Sales 🏡")
                        comp_data = [{
                            "Address": f"{comp.get('Address', 'N/A')}, {comp.get('City', 'N/A')}, {comp.get('State', 'N/A')} {comp.get('Zip', 'N/A')}",
                            "Price": f"${float(comp.get('Price', 0)):,.0f}",
                            "Beds": comp.get("Bedrooms", "-"),
                            "Baths": comp.get("Bathrooms", "-"),
                            "Sq Ft": comp.get("SquareFeet", "-"),
                            "Year Built": comp.get("YearBuilt", "-"),
                            "Distance": f"{comp.get('Distance', '-')} mi"
                        } for comp in comps]
                        
                        if comp_data:
                            st.dataframe(pd.DataFrame(comp_data), use_container_width=True)
                        else:
                            st.info("No comparable properties found.")

                # Collapsible JSON/meta data section (only at the bottom)
                with st.expander("Show Full JSON Response"):
                    st.json(result)

with tab2:
    st.write("Upload a CSV file to process multiple properties at once.")
    
    # Add report type selector for batch processing
    batch_report_type = st.selectbox(
        "Select Report Type for Batch Processing",
        ["Get RELAR Full Report", "Get RELAR Simple Report", "Get Ranged Report"],
        help="Choose the type of valuation report for all properties in the CSV"
    )
    
    # Option to upload a CSV file
    uploaded_file = st.file_uploader("Upload a CSV file with columns: Address, City, State, Zipcode (or zip)", type="csv")

    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        # Normalize column names: lowercase and strip spaces
        df.columns = [col.strip().lower() for col in df.columns]
        st.write("Uploaded CSV:")
        st.dataframe(df)

        if st.button("Process CSV"):
            client = AcumidataClient(environment="prod")
            
            # Map report types to API methods
            report_methods = {
                "Get RELAR Full Report": "get_valuation_advantage",
                "Get RELAR Simple Report": "get_valuation_simple",
                "Get Ranged Report": "get_valuation_ranged"
            }
            
            method_name = report_methods[batch_report_type]
            method = getattr(client, method_name)

            # Add concurrent processing controls
            col1, col2 = st.columns(2)
            with col1:
                max_workers = st.slider("Concurrent Requests", min_value=1, max_value=10, value=5, 
                                      help="Number of simultaneous API calls")
            with col2:
                if len(df) > 1000:
                    st.warning(f"⚠️ Large dataset: {len(df)} properties. This may take 15-30 minutes.")
                    recommended_workers = min(3, max_workers)  # Be more conservative
                    st.info(f"💡 Recommended: Use {recommended_workers} concurrent requests for large batches")
                else:
                    st.info(f"📊 Processing {len(df)} properties")
            
            progress_bar = st.progress(0)
            status_text = st.empty()
            total_rows = len(df)
            completed_count = 0
            start_time = time.time()
            
            def process_single_property(row_data):
                """Process a single property and return the results"""
                index, row = row_data
                address = row['address']
                city = row['city']
                state = row['state']
                zip_code = str(row.get('zipcode', row.get('zip', '')))
                
                try:
                    result = method(address, city, state, zip_code)
                    return index, result, None
                except Exception as e:
                    return index, None, str(e)
            
            # Prepare data for concurrent processing
            row_data = [(index, row) for index, row in df.iterrows()]
            results = {}
            errors = {}
            
            # Process properties concurrently
            with ThreadPoolExecutor(max_workers=max_workers) as executor:
                # Submit all tasks
                future_to_index = {executor.submit(process_single_property, rd): rd[0] for rd in row_data}
                
                # Process completed tasks
                for future in as_completed(future_to_index):
                    index, result, error = future.result()
                    completed_count += 1
                    
                    if error:
                        errors[index] = error
                        if len(errors) <= 5:  # Only show first 5 errors to avoid spam
                            st.error(f"Error processing row {index + 1}: {error}")
                    else:
                        results[index] = result
                    
                    # Update progress
                    progress = completed_count / total_rows
                    progress_bar.progress(progress)
                    elapsed_time = time.time() - start_time
                    estimated_total = elapsed_time / progress if progress > 0 else 0
                    remaining_time = estimated_total - elapsed_time
                    
                    # Enhanced status for large datasets
                    rate = completed_count / elapsed_time if elapsed_time > 0 else 0
                    status_text.text(f"Processed {completed_count}/{total_rows} properties. "
                                   f"Rate: {rate:.1f}/sec, Elapsed: {elapsed_time:.1f}s, "
                                   f"Estimated remaining: {remaining_time:.1f}s")

            # Process results and add to DataFrame
            for index in range(total_rows):
                if index in results:
                    result = results[index]
                    
                    # Extract data based on report type (same logic as before)
                    if batch_report_type == "Get RELAR Full Report":
                        # Extract from RELAR Full Report structure
                        search_data = result.get("searchData", {})
                        analysis = result.get("analysis", {})
                        house_worth = analysis.get("houseWorth", {})
                        valuations = house_worth.get("valuations", {})
                        current_valuation = valuations.get("current", {})
                        metadata = result.get("metadata", {})
                        
                        # Property details
                        bedrooms = search_data.get("beds")
                        bathrooms = search_data.get("baths")
                        year_built = search_data.get("yearBuilt")
                        home_size = search_data.get("size")
                        lot_size = search_data.get("lotSize")
                        
                        # Valuation data
                        estimated_value = current_valuation.get("value")
                        confidence_score = current_valuation.get("confidence")
                        variance = current_valuation.get("variance")
                        
                        # PDF URL
                        pdf_url = metadata.get("reportPDFLink")
                        
                        # Convert strings to numbers
                        try:
                            estimated_value = float(estimated_value) if estimated_value else None
                            confidence_score = float(confidence_score) if confidence_score else None
                            variance = float(variance) if variance else None
                            home_size = int(home_size) if home_size else None
                            lot_size = int(lot_size) if lot_size else None
                        except (ValueError, TypeError):
                            pass
                        
                        # Add columns for Full Report
                        df.at[index, 'Bedrooms'] = bedrooms
                        df.at[index, 'Bathrooms'] = bathrooms
                        df.at[index, 'YearBuilt'] = year_built
                        df.at[index, 'HomeSize'] = home_size
                        df.at[index, 'LotSize'] = lot_size
                        df.at[index, 'EstimatedValue'] = estimated_value
                        df.at[index, 'ConfidenceScore'] = confidence_score
                        df.at[index, 'Variance'] = variance
                        # Add PDF link last
                        df.at[index, 'PDFReportLink'] = pdf_url
                        
                    elif batch_report_type in ["Get RELAR Simple Report", "Get Ranged Report"]:
                        # Extract from Simple/Ranged Report structure
                        prediction = result.get("prediction", {})
                        subject_parcel = result.get("subjectParcel", {})
                        structures = subject_parcel.get("structures", [])
                        metadata = result.get("metadata", {})
                        
                        # Property details
                        if structures and len(structures) > 0:
                            structure = structures[0]
                            bedrooms = structure.get("bedrooms")
                            bathrooms = structure.get("bathrooms")
                            gla = structure.get("gla")
                        else:
                            bedrooms = bathrooms = gla = None
                        
                        # Valuation data
                        predicted_price = prediction.get("predictedPrice") if batch_report_type == "Get RELAR Simple Report" else None
                        price_low = prediction.get("priceLow")
                        price_high = prediction.get("priceHigh")
                        confidence_score = prediction.get("confidence")
                        error_margin = prediction.get("error") if batch_report_type == "Get Ranged Report" else None
                        
                        # PDF URL
                        pdf_url = metadata.get("reportPDFLink")
                        
                        # Convert strings to numbers
                        try:
                            predicted_price = float(predicted_price) if predicted_price else None
                            price_low = float(price_low) if price_low else None
                            price_high = float(price_high) if price_high else None
                            confidence_score = float(confidence_score) if confidence_score else None
                            error_margin = float(error_margin) if error_margin else None
                            gla = int(gla) if gla else None
                        except (ValueError, TypeError):
                            pass
                        
                        # Add columns for Simple/Ranged Report
                        df.at[index, 'Bedrooms'] = bedrooms
                        df.at[index, 'Bathrooms'] = bathrooms
                        df.at[index, 'HomeSize'] = gla
                        df.at[index, 'PriceLow'] = price_low
                        df.at[index, 'PriceHigh'] = price_high
                        df.at[index, 'ConfidenceScore'] = confidence_score
                        
                        if batch_report_type == "Get RELAR Simple Report":
                            df.at[index, 'PredictedPrice'] = predicted_price
                        
                        if batch_report_type == "Get Ranged Report":
                            df.at[index, 'ErrorMargin'] = error_margin
                        
                        # Add PDF link last
                        df.at[index, 'PDFReportLink'] = pdf_url
                    else:
                        # Handle errors by setting all values to None/Error
                        if batch_report_type == "Get RELAR Full Report":
                            for col in ['Bedrooms', 'Bathrooms', 'YearBuilt', 'HomeSize', 'LotSize', 'EstimatedValue', 'ConfidenceScore', 'Variance', 'PDFReportLink']:
                                df.at[index, col] = "Error"
                        else:
                            for col in ['Bedrooms', 'Bathrooms', 'HomeSize', 'PriceLow', 'PriceHigh', 'ConfidenceScore', 'PDFReportLink']:
                                df.at[index, col] = "Error"
                            if batch_report_type == "Get RELAR Simple Report":
                                df.at[index, 'PredictedPrice'] = "Error"
                            if batch_report_type == "Get Ranged Report":
                                df.at[index, 'ErrorMargin'] = "Error"

            # Final completion message
            total_time = time.time() - start_time
            status_text.text(f"✅ Completed! Processed {total_rows} properties in {total_time:.1f} seconds "
                           f"({total_time/total_rows:.1f}s per property)")
            
            if errors:
                st.warning(f"⚠️ {len(errors)} properties had errors. Check the CSV for 'Error' values.")

            st.write("Enriched CSV:")
            st.dataframe(df)

            # Provide a download link for the enriched CSV
            csv = df.to_csv(index=False)
            filename = f"enriched_property_data_{batch_report_type.lower().replace(' ', '_').replace('get_', '')}.csv"
            st.download_button(
                label="Download Enriched CSV",
                data=csv,
                file_name=filename,
                mime="text/csv"
            )

with tab3:
    # Initialize and render the API Playground
    playground = APIPlayground()
    playground.render_playground()

def get_property_data(address, city, state, zip_code):
    client = AcumidataClient(environment="prod")
    result = client.get_property_valuation(address, city, state, zip_code)
    if "error" in result:
        return None, result["error"]
    try:
        details = result.get("Details", {})
        property_valuation = details.get("PropertyValuation", {})
        estimated_value = property_valuation.get("EstimatedValue")
        confidence_score = property_valuation.get("ConfidenceScore")
        range_low = property_valuation.get("ValuationRangeLow")
        range_high = property_valuation.get("ValuationRangeHigh")
        comps = details.get("ComparablePropertyListings", {}).get("Comparables", [])
        return {
            "estimated_value": estimated_value,
            "confidence_score": confidence_score,
            "range_low": range_low,
            "range_high": range_high,
            "comparables": comps
        }, None
    except Exception as e:
        return None, str(e) 