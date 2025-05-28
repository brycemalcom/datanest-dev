"""
API Endpoint Explorer for testing and debugging property data endpoints.
"""

import streamlit as st
import json
from typing import Dict, Any, Optional, List
from utils.acumidata_client import AcumidataClient


class EndpointExplorer:
    """Interactive API endpoint testing playground."""
    
    def __init__(self):
        self.client = None
        self.available_endpoints = {
            "valuation": {
                "name": "Property Valuation",
                "endpoint": "api/Valuation/estimate",
                "description": "Get comprehensive property valuation with comparables",
                "method": "get_property_valuation"
            },
            "qvm_simple": {
                "name": "QVM Simple Valuation",
                "endpoint": "api/Valuation/qvmsimple",
                "description": "Get Quantarium QVM valuation data",
                "method": "get_qvm_simple"
            },
            "advantage": {
                "name": "Property Advantage",
                "endpoint": "api/Comps/advantage",
                "description": "Get rich property and comparable data",
                "method": "get_property_advantage"
            },
            "equity": {
                "name": "Equity Analysis",
                "endpoint": "api/Equity/analysis",
                "description": "Property equity and ownership analysis",
                "method": "get_equity_analysis",
                "status": "Coming Soon"
            },
            "monitoring": {
                "name": "Property Monitoring",
                "endpoint": "api/Monitor/alerts",
                "description": "Property value and market monitoring",
                "method": "get_monitoring_data",
                "status": "Coming Soon"
            }
        }
    
    def render_explorer(self):
        """Render the API endpoint explorer interface."""
        st.header("🔧 API Endpoint Explorer")
        st.subheader("Test and explore property data endpoints")
        
        # Environment selection
        col1, col2 = st.columns([1, 3])
        with col1:
            environment = st.selectbox(
                "Environment",
                ["prod", "uat"],
                help="Select API environment"
            )
        
        with col2:
            st.info(f"Using {environment.upper()} environment")
        
        # Initialize client
        self.client = AcumidataClient(environment=environment)
        
        # Endpoint selection
        st.markdown("---")
        st.subheader("📡 Select Endpoint")
        
        endpoint_key = st.selectbox(
            "Choose an endpoint to test",
            options=list(self.available_endpoints.keys()),
            format_func=lambda x: f"{self.available_endpoints[x]['name']} - {self.available_endpoints[x]['description']}"
        )
        
        endpoint_info = self.available_endpoints[endpoint_key]
        
        # Display endpoint information
        col1, col2 = st.columns(2)
        with col1:
            st.info(f"**Endpoint:** `{endpoint_info['endpoint']}`")
        with col2:
            status = endpoint_info.get('status', 'Available')
            if status == 'Available':
                st.success(f"**Status:** {status}")
            else:
                st.warning(f"**Status:** {status}")
        
        # Property input form
        st.markdown("---")
        st.subheader("🏠 Property Information")
        
        with st.form("property_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                address = st.text_input("Street Address", value="531 NE Beck Rd")
                city = st.text_input("City", value="Belfair")
            
            with col2:
                state = st.text_input("State", value="WA")
                zip_code = st.text_input("Zip Code", value="98528")
            
            submit_button = st.form_submit_button("🚀 Test Endpoint")
        
        # Execute API call
        if submit_button:
            if endpoint_info.get('status') == 'Coming Soon':
                st.warning("This endpoint is not yet implemented.")
                return
            
            self._execute_api_call(endpoint_key, address, city, state, zip_code)
    
    def _execute_api_call(self, endpoint_key: str, address: str, city: str, state: str, zip_code: str):
        """Execute the API call and display results."""
        endpoint_info = self.available_endpoints[endpoint_key]
        method_name = endpoint_info['method']
        
        with st.spinner(f"Calling {endpoint_info['name']} endpoint..."):
            try:
                # Get the method from the client
                method = getattr(self.client, method_name)
                result = method(address, city, state, zip_code)
                
                # Display results
                self._display_results(result, endpoint_info)
                
            except AttributeError:
                st.error(f"Method {method_name} not implemented in AcumidataClient")
            except Exception as e:
                st.error(f"Error calling API: {str(e)}")
    
    def _display_results(self, result: Dict[str, Any], endpoint_info: Dict[str, str]):
        """Display API results in formatted and raw views."""
        st.markdown("---")
        st.subheader("📊 API Response")
        
        if "error" in result:
            st.error(f"API Error: {result['error']}")
            return
        
        # Create tabs for different views
        tab1, tab2, tab3 = st.tabs(["📋 Formatted View", "🔍 Raw JSON", "📈 Key Metrics"])
        
        with tab1:
            self._render_formatted_view(result, endpoint_info)
        
        with tab2:
            self._render_raw_json(result)
        
        with tab3:
            self._render_key_metrics(result, endpoint_info)
    
    def _render_formatted_view(self, result: Dict[str, Any], endpoint_info: Dict[str, str]):
        """Render a formatted, user-friendly view of the API response."""
        st.write("**Formatted Response Data**")
        
        # Extract key information based on endpoint type
        details = result.get("Details", {})
        
        if "valuation" in endpoint_info['endpoint'].lower():
            self._render_valuation_formatted(details)
        elif "advantage" in endpoint_info['endpoint'].lower():
            self._render_advantage_formatted(details)
        else:
            # Generic formatting
            for key, value in details.items():
                if isinstance(value, dict):
                    st.subheader(key.replace("_", " ").title())
                    st.json(value)
                else:
                    st.write(f"**{key}:** {value}")
    
    def _render_valuation_formatted(self, details: Dict[str, Any]):
        """Render formatted valuation data."""
        property_valuation = details.get("PropertyValuation", {})
        property_summary = details.get("PropertySummary", {})
        
        if property_valuation:
            col1, col2, col3 = st.columns(3)
            
            with col1:
                estimated_value = property_valuation.get("EstimatedValue")
                if estimated_value:
                    st.metric("Estimated Value", f"${estimated_value:,.2f}")
            
            with col2:
                confidence = property_valuation.get("ConfidenceScore")
                if confidence:
                    st.metric("Confidence Score", f"{confidence}/100")
            
            with col3:
                range_low = property_valuation.get("ValuationRangeLow")
                range_high = property_valuation.get("ValuationRangeHigh")
                if range_low and range_high:
                    st.metric("Valuation Range", f"${range_low:,.0f} - ${range_high:,.0f}")
        
        if property_summary:
            st.subheader("Property Summary")
            col1, col2, col3 = st.columns(3)
            
            with col1:
                beds = property_summary.get("Bedrooms", "N/A")
                st.write(f"**Bedrooms:** {beds}")
            
            with col2:
                baths = property_summary.get("FullBaths", "N/A")
                st.write(f"**Bathrooms:** {baths}")
            
            with col3:
                year_built = property_summary.get("YearBuilt", "N/A")
                st.write(f"**Year Built:** {year_built}")
    
    def _render_advantage_formatted(self, details: Dict[str, Any]):
        """Render formatted advantage data."""
        comps = details.get("ComparablePropertyListings", {}).get("Comparables", [])
        
        if comps:
            st.subheader("Comparable Properties")
            comp_data = []
            
            for comp in comps[:5]:  # Show top 5 comps
                comp_data.append({
                    "Address": f"{comp.get('Address', 'N/A')}, {comp.get('City', 'N/A')}",
                    "Price": f"${float(comp.get('Price', 0)):,.0f}" if comp.get('Price') else "N/A",
                    "Beds": comp.get("Bedrooms", "N/A"),
                    "Baths": comp.get("Baths", "N/A"),
                    "Sqft": comp.get("BuildingSqft", "N/A"),
                    "Distance": f"{comp.get('Distance', 'N/A')} mi"
                })
            
            if comp_data:
                import pandas as pd
                df = pd.DataFrame(comp_data)
                st.dataframe(df, use_container_width=True, hide_index=True)
    
    def _render_raw_json(self, result: Dict[str, Any]):
        """Render the raw JSON response."""
        st.write("**Raw JSON Response**")
        st.json(result)
        
        # Add download button for JSON
        json_str = json.dumps(result, indent=2)
        st.download_button(
            label="📥 Download JSON",
            data=json_str,
            file_name="api_response.json",
            mime="application/json"
        )
    
    def _render_key_metrics(self, result: Dict[str, Any], endpoint_info: Dict[str, str]):
        """Render key metrics and statistics from the response."""
        st.write("**Response Statistics**")
        
        # Basic response stats
        col1, col2, col3 = st.columns(3)
        
        with col1:
            response_size = len(json.dumps(result))
            st.metric("Response Size", f"{response_size:,} bytes")
        
        with col2:
            details = result.get("Details", {})
            field_count = len(details)
            st.metric("Data Fields", field_count)
        
        with col3:
            # Count nested objects
            nested_count = sum(1 for v in details.values() if isinstance(v, dict))
            st.metric("Nested Objects", nested_count)
        
        # Endpoint-specific metrics
        if "valuation" in endpoint_info['endpoint'].lower():
            self._render_valuation_metrics(result)
    
    def _render_valuation_metrics(self, result: Dict[str, Any]):
        """Render valuation-specific metrics."""
        details = result.get("Details", {})
        comps = details.get("ComparablePropertyListings", {}).get("Comparables", [])
        
        if comps:
            st.subheader("Comparable Analysis")
            
            # Calculate comp statistics
            prices = [float(comp.get("Price", 0)) for comp in comps if comp.get("Price")]
            distances = [float(comp.get("Distance", 0)) for comp in comps if comp.get("Distance")]
            
            if prices:
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    avg_price = sum(prices) / len(prices)
                    st.metric("Avg Comp Price", f"${avg_price:,.0f}")
                
                with col2:
                    st.metric("Price Range", f"${min(prices):,.0f} - ${max(prices):,.0f}")
                
                with col3:
                    if distances:
                        avg_distance = sum(distances) / len(distances)
                        st.metric("Avg Distance", f"{avg_distance:.1f} mi") 