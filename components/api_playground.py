"""
API Testing Playground component for testing Acumidata endpoints.
"""

import streamlit as st
import json
from typing import Dict, Any, Optional
from utils.acumidata_client import AcumidataClient


class APIPlayground:
    """Interactive API testing playground for Acumidata endpoints."""
    
    def __init__(self):
        self.endpoints = {
            "valuation_estimate": {
                "name": "Property Valuation (Full Report)",
                "endpoint": "/api/Valuation/estimate",
                "description": "Get comprehensive property valuation with Quantarium Full Report",
                "method": "get_property_valuation",
                "category": "Valuation"
            },
            "valuation_advantage": {
                "name": "RELAR Full Report",
                "endpoint": "/api/Valuation/advantage",
                "description": "Get RELAR Full Report with comprehensive property analysis",
                "method": "get_valuation_advantage",
                "category": "Valuation"
            },
            "valuation_simple": {
                "name": "RELAR Simple Report",
                "endpoint": "/api/Valuation/simple",
                "description": "Get RELAR Simple Valuation Report",
                "method": "get_valuation_simple",
                "category": "Valuation"
            },
            "valuation_ranged": {
                "name": "RELAR Ranged Report",
                "endpoint": "/api/Valuation/ranged",
                "description": "Get RELAR Ranged Valuation Report",
                "method": "get_valuation_ranged",
                "category": "Valuation"
            },
            "valuation_collateral": {
                "name": "Quantarium Collateral",
                "endpoint": "/api/Valuation/collateral",
                "description": "Get Quantarium Collateral Report for lending purposes",
                "method": "get_valuation_collateral",
                "category": "Valuation"
            },
            "valuation_qvm_simple": {
                "name": "QVM Simple Valuation",
                "endpoint": "/api/Valuation/qvmsimple",
                "description": "Get Quantarium QVM simple valuation data",
                "method": "get_qvm_simple",
                "category": "Valuation"
            },
            "comps_advantage": {
                "name": "Property Comps (Advantage)",
                "endpoint": "/api/Comps/advantage",
                "description": "Get RELAR comparable properties data",
                "method": "get_property_advantage",
                "category": "Comparables"
            },
            "comps_radius": {
                "name": "Property Comps (Radius)",
                "endpoint": "/api/Comps/advantageradius",
                "description": "Get comparable properties within specified radius",
                "method": "get_comps_advantage_radius",
                "category": "Comparables"
            },
            "comps_polygon": {
                "name": "Property Comps (Polygon)",
                "endpoint": "/api/Comps/advantagepolygon",
                "description": "Get comparable properties within a custom polygon area",
                "method": "get_comps_advantage_polygon",
                "category": "Comparables",
                "special_form": "polygon_based"
            },
            "equity_advantage": {
                "name": "Equity Calculator",
                "endpoint": "/api/Equity/advantage",
                "description": "Get equity calculator report for property",
                "method": "get_equity_advantage",
                "category": "Equity"
            },
            "monitors_advantage": {
                "name": "Property Monitoring",
                "endpoint": "/api/Monitors/advantage",
                "description": "Create monitoring portfolio for property",
                "method": "get_monitors_advantage",
                "category": "Monitoring"
            },
            "title_advantage": {
                "name": "Title Report",
                "endpoint": "/api/Title/advantage",
                "description": "Get comprehensive title report for property",
                "method": "get_title_advantage",
                "category": "Title"
            },
            "parcels_detail": {
                "name": "Simple Parcel Details",
                "endpoint": "/api/Parcels/detail",
                "description": "Get simple parcel details for a property",
                "method": "get_parcels_detail",
                "category": "Parcels"
            },
            "listings_property": {
                "name": "Listings by Property",
                "endpoint": "/api/Listings/{product}",
                "description": "Create listing order for specific property",
                "method": "get_listings_by_property",
                "category": "MLS/Listings"
            },
            "listings_delta_zip": {
                "name": "Listings Delta (Zip)",
                "endpoint": "/api/Listings/delta-zip",
                "description": "Get listings delta report by zip code",
                "method": "get_listings_delta_zip",
                "category": "MLS/Listings",
                "special_form": "zip_based"
            },
            "listings_delta_fips": {
                "name": "Listings Delta (FIPS)",
                "endpoint": "/api/Listings/delta-fips",
                "description": "Get listings delta report by FIPS code",
                "method": "get_listings_delta_fips",
                "category": "MLS/Listings",
                "special_form": "fips_based"
            },
            "listings_feed": {
                "name": "MLS Data Feed",
                "endpoint": "/api/Listings/feed",
                "description": "Get MLS data feed by state and timestamp",
                "method": "get_listings_feed",
                "category": "MLS/Listings",
                "special_form": "state_based"
            },
            "listings_feed_enhanced": {
                "name": "MLS Data Feed (Enhanced)",
                "endpoint": "/api/Listings/feed",
                "description": "Get MLS data feed with pagination and transaction control",
                "method": "get_listings_feed_enhanced",
                "category": "MLS/Listings",
                "special_form": "enhanced_state_based"
            }
        }
    
    def render_playground(self):
        """Render the complete API testing playground."""
        st.header("🔧 API Testing Playground")
        st.write("Test Acumidata endpoints with live property data")
        
        # Environment selection
        col1, col2 = st.columns([1, 3])
        with col1:
            environment = st.selectbox(
                "Environment",
                ["uat", "prod"],
                help="Select API environment (UAT for testing, PROD for live data)"
            )
        
        with col2:
            env_color = "🟢" if environment == "prod" else "🟡"
            st.info(f"{env_color} Using **{environment.upper()}** environment")
        
        # Endpoint selection
        st.markdown("---")
        st.subheader("📡 Select Endpoint")
        
        # Group endpoints by category
        categories = {}
        for key, endpoint in self.endpoints.items():
            category = endpoint["category"]
            if category not in categories:
                categories[category] = []
            categories[category].append((key, endpoint))
        
        # Create tabs for each category
        tab_names = list(categories.keys())
        tabs = st.tabs(tab_names)
        
        selected_endpoint = None
        selected_key = None
        
        for i, (category, endpoints) in enumerate(categories.items()):
            with tabs[i]:
                for key, endpoint in endpoints:
                    if st.button(
                        f"**{endpoint['name']}**\n{endpoint['description']}", 
                        key=f"btn_{key}",
                        use_container_width=True
                    ):
                        selected_endpoint = endpoint
                        selected_key = key
                        st.session_state.selected_endpoint = key
        
        # Use session state to maintain selection
        if 'selected_endpoint' in st.session_state:
            selected_key = st.session_state.selected_endpoint
            selected_endpoint = self.endpoints[selected_key]
        
        if selected_endpoint:
            st.markdown("---")
            self._render_endpoint_tester(selected_endpoint, selected_key, environment)
    
    def _render_endpoint_tester(self, endpoint_info: Dict[str, str], endpoint_key: str, environment: str):
        """Render the endpoint testing interface."""
        st.subheader(f"🎯 Testing: {endpoint_info['name']}")
        
        # Endpoint details
        col1, col2 = st.columns(2)
        with col1:
            st.info(f"**Endpoint:** `{endpoint_info['endpoint']}`")
        with col2:
            st.info(f"**Category:** {endpoint_info['category']}")
        
        st.write(endpoint_info['description'])
        
        # Property input form
        special_form = endpoint_info.get("special_form")
        
        if special_form == "zip_based":
            self._render_zip_based_form(endpoint_info, endpoint_key, environment)
        elif special_form == "state_based":
            self._render_state_based_form(endpoint_info, endpoint_key, environment)
        elif special_form == "enhanced_state_based":
            self._render_enhanced_state_based_form(endpoint_info, endpoint_key, environment)
        elif special_form == "polygon_based":
            self._render_polygon_based_form(endpoint_info, endpoint_key, environment)
        elif special_form == "fips_based":
            self._render_fips_based_form(endpoint_info, endpoint_key, environment)
        else:
            self._render_standard_property_form(endpoint_info, endpoint_key, environment)
    
    def _render_standard_property_form(self, endpoint_info: Dict[str, str], endpoint_key: str, environment: str):
        """Render the standard property address form."""
        st.markdown("### 🏠 Property Information")
        
        with st.form(f"api_test_form_{endpoint_key}"):
            col1, col2 = st.columns(2)
            
            with col1:
                address = st.text_input("Street Address", value="531 NE Beck Rd")
                city = st.text_input("City", value="Belfair")
            
            with col2:
                state = st.text_input("State", value="WA")
                zip_code = st.text_input("Zip Code", value="98528")
            
            # Special parameters for specific endpoints
            extra_params = {}
            if endpoint_key == "comps_radius":
                radius = st.selectbox("Search Radius (miles)", ["0.25", "0.5", "1.0", "2.0", "5.0"], index=1)
                extra_params["radius"] = radius
            elif endpoint_key == "listings_property":
                product = st.selectbox("Product Type", ["advantage", "standard", "premium"], index=0)
                extra_params["product"] = product
            
            submitted = st.form_submit_button("🚀 Test Endpoint", type="primary")
        
        if submitted:
            self._execute_standard_api_test(endpoint_info, address, city, state, zip_code, environment, extra_params)
    
    def _render_zip_based_form(self, endpoint_info: Dict[str, str], endpoint_key: str, environment: str):
        """Render form for zip-based endpoints."""
        st.markdown("### 📮 Zip Code Information")
        
        with st.form(f"api_test_form_{endpoint_key}"):
            zip_codes = st.text_input("Zip Codes (comma-separated)", value="98528,98027,98004", 
                                     help="Enter one or more zip codes separated by commas")
            
            col1, col2 = st.columns(2)
            with col1:
                start_date = st.date_input("Start Date (optional)", value=None)
                ref_id = st.text_input("Reference ID (optional)", value="")
            
            with col2:
                end_date = st.date_input("End Date (optional)", value=None)
                statuses = st.text_input("Statuses (optional)", value="", 
                                        help="e.g., Active,Pending,Sold")
            
            submitted = st.form_submit_button("🚀 Test Endpoint", type="primary")
        
        if submitted:
            extra_params = {
                "zip_codes": zip_codes,
                "start_date": start_date.isoformat() if start_date else None,
                "end_date": end_date.isoformat() if end_date else None,
                "statuses": statuses if statuses else None,
                "ref_id": ref_id if ref_id else None
            }
            self._execute_zip_based_api_test(endpoint_info, environment, extra_params)
    
    def _render_state_based_form(self, endpoint_info: Dict[str, str], endpoint_key: str, environment: str):
        """Render form for state-based endpoints."""
        st.markdown("### 🗺️ State and Timestamp Information")
        
        with st.form(f"api_test_form_{endpoint_key}"):
            col1, col2 = st.columns(2)
            
            with col1:
                state = st.selectbox("State", ["FL", "CA", "TX", "NY", "WA", "Other"], index=4)
                if state == "Other":
                    state = st.text_input("Enter State Code", value="")
                
                extract_type = st.selectbox("Extract Type (optional)", ["", "full", "delta"], index=0)
            
            with col2:
                start_timestamp = st.number_input("Start Timestamp (EPOCH)", value=1710720000, 
                                                help="EPOCH timestamp, e.g., 1710720000 for 03/18/2024")
                end_timestamp = st.number_input("End Timestamp (EPOCH, optional)", value=0, 
                                              help="Leave as 0 for no end timestamp")
            
            submitted = st.form_submit_button("🚀 Test Endpoint", type="primary")
        
        if submitted:
            extra_params = {
                "state": state,
                "start_timestamp": int(start_timestamp) if start_timestamp else None,
                "end_timestamp": int(end_timestamp) if end_timestamp and end_timestamp > 0 else None,
                "extract_type": extract_type if extract_type else None
            }
            self._execute_state_based_api_test(endpoint_info, environment, extra_params)
    
    def _render_enhanced_state_based_form(self, endpoint_info: Dict[str, str], endpoint_key: str, environment: str):
        """Render form for enhanced state-based endpoints with pagination."""
        st.markdown("### 🗺️ Enhanced State and Feed Information")
        
        with st.form(f"api_test_form_{endpoint_key}"):
            col1, col2 = st.columns(2)
            
            with col1:
                state = st.selectbox("State", ["FL", "CA", "TX", "NY", "WA", "Other"], index=4)
                if state == "Other":
                    state = st.text_input("Enter State Code", value="")
                
                page_size = st.number_input("Page Size", min_value=1, max_value=1000, value=100, 
                                          help="Number of records per page")
            
            with col2:
                start_timestamp = st.number_input("Start Timestamp (EPOCH)", value=1710720000, 
                                                help="EPOCH timestamp, e.g., 1710720000 for 03/18/2024")
                end_timestamp = st.number_input("End Timestamp (EPOCH, optional)", value=0, 
                                              help="Leave as 0 for no end timestamp")
            
            col1, col2 = st.columns(2)
            with col1:
                extract_type = st.selectbox("Extract Type (optional)", ["", "full", "delta"], index=0)
            
            with col2:
                transaction_id = st.number_input("Transaction ID (optional)", value=0, 
                                               help="Required when extract type is null")
            
            submitted = st.form_submit_button("🚀 Test Endpoint", type="primary")
        
        if submitted:
            extra_params = {
                "state": state,
                "page_size": int(page_size),
                "start_timestamp": int(start_timestamp) if start_timestamp else None,
                "end_timestamp": int(end_timestamp) if end_timestamp and end_timestamp > 0 else None,
                "extract_type": extract_type if extract_type else None,
                "transaction_id": int(transaction_id) if transaction_id and transaction_id > 0 else None
            }
            self._execute_enhanced_state_based_api_test(endpoint_info, environment, extra_params)
    
    def _render_polygon_based_form(self, endpoint_info: Dict[str, str], endpoint_key: str, environment: str):
        """Render form for polygon-based endpoints."""
        st.markdown("### 🗺️ Property and Polygon Information")
        
        with st.form(f"api_test_form_{endpoint_key}"):
            # Property address fields
            col1, col2 = st.columns(2)
            with col1:
                address = st.text_input("Street Address", value="531 NE Beck Rd")
                city = st.text_input("City", value="Belfair")
            
            with col2:
                state = st.text_input("State", value="WA")
                zip_code = st.text_input("Zip Code", value="98528")
            
            # Polygon and additional parameters
            polygon = st.text_area("Polygon Coordinates", 
                                  value="47.6062,-122.3321,47.2529,-122.7414,47.2529,-121.7414,47.6062,-121.3321", 
                                  help="Enter polygon coordinates as comma-separated lat,lon pairs")
            
            col1, col2, col3 = st.columns(3)
            with col1:
                land_use = st.selectbox("Land Use (optional)", ["", "SFR", "CONDO", "TOWNHOUSE", "FARM", "MOBILE"], index=0)
            
            with col2:
                date = st.date_input("Date (optional)", value=None)
            
            with col3:
                include_birdseye = st.selectbox("Include Birdseye", ["", "true", "false"], index=0)
            
            submitted = st.form_submit_button("🚀 Test Endpoint", type="primary")
        
        if submitted:
            extra_params = {
                "polygon": polygon,
                "land_use": land_use if land_use else None,
                "date": date.isoformat() if date else None,
                "include_birdseye": include_birdseye if include_birdseye else None
            }
            self._execute_polygon_based_api_test(endpoint_info, address, city, state, zip_code, environment, extra_params)
    
    def _render_fips_based_form(self, endpoint_info: Dict[str, str], endpoint_key: str, environment: str):
        """Render form for FIPS-based endpoints."""
        st.markdown("### 🗺️ FIPS Information")
        
        with st.form(f"api_test_form_{endpoint_key}"):
            fips_codes = st.text_input("FIPS Codes (comma-separated)", value="16000US06075,16000US06085", 
                                     help="Enter one or more FIPS codes separated by commas")
            
            col1, col2 = st.columns(2)
            with col1:
                start_date = st.date_input("Start Date (optional)", value=None)
                ref_id = st.text_input("Reference ID (optional)", value="")
            
            with col2:
                end_date = st.date_input("End Date (optional)", value=None)
                statuses = st.text_input("Statuses (optional)", value="", 
                                        help="e.g., Active,Pending,Sold")
            
            submitted = st.form_submit_button("🚀 Test Endpoint", type="primary")
        
        if submitted:
            extra_params = {
                "fips_codes": fips_codes,
                "start_date": start_date.isoformat() if start_date else None,
                "end_date": end_date.isoformat() if end_date else None,
                "statuses": statuses if statuses else None,
                "ref_id": ref_id if ref_id else None
            }
            self._execute_fips_based_api_test(endpoint_info, environment, extra_params)
    
    def _execute_standard_api_test(self, endpoint_info: Dict[str, str], address: str, city: str, 
                                 state: str, zip_code: str, environment: str, extra_params: Dict = None):
        """Execute the standard API test and display results."""
        if not all([address, city, state, zip_code]):
            st.error("Please fill in all required fields")
            return
        
        method_name = endpoint_info['method']
        
        with st.spinner(f"Calling {endpoint_info['name']} endpoint..."):
            try:
                # Initialize client
                client = AcumidataClient(environment=environment)
                
                # Get the method from the client
                method = getattr(client, method_name)
                
                # Call the method with appropriate parameters
                if extra_params and "radius" in extra_params:
                    result = method(address, city, state, zip_code, extra_params["radius"])
                elif extra_params and "product" in extra_params:
                    result = method(address, city, state, zip_code, extra_params["product"])
                else:
                    result = method(address, city, state, zip_code)
                
                # Display results
                self._display_api_results(result, endpoint_info, f"{address}, {city}, {state} {zip_code}")
                
            except AttributeError as e:
                # Check if it's actually a missing method or something else
                if f"'{method_name}'" in str(e) and "object has no attribute" in str(e):
                    st.error(f"Method {method_name} not implemented in AcumidataClient")
                else:
                    st.error(f"AttributeError during execution: {str(e)}")
                    st.write("**Debug Info:**")
                    st.write(f"- Method name: {method_name}")
                    st.write(f"- Method exists: {hasattr(client, method_name)}")
                    if hasattr(client, method_name):
                        st.write("✅ Method found - error likely in result processing")
                        # Try to show partial results if API call succeeded
                        try:
                            method = getattr(client, method_name)
                            result = method(address, city, state, zip_code)
                            st.write("✅ API call succeeded, showing raw result:")
                            st.json(result)
                        except Exception as api_error:
                            st.write(f"❌ API call failed: {api_error}")
            except Exception as e:
                st.error(f"Error calling API: {str(e)}")
    
    def _execute_zip_based_api_test(self, endpoint_info: Dict[str, str], environment: str, extra_params: Dict):
        """Execute zip-based API test."""
        if not extra_params.get("zip_codes"):
            st.error("Please provide at least one zip code")
            return
        
        method_name = endpoint_info['method']
        
        with st.spinner(f"Calling {endpoint_info['name']} endpoint..."):
            try:
                client = AcumidataClient(environment=environment)
                method = getattr(client, method_name)
                
                # Call method with zip-based parameters
                result = method(
                    extra_params["zip_codes"],
                    extra_params.get("start_date"),
                    extra_params.get("end_date"),
                    extra_params.get("statuses"),
                    extra_params.get("ref_id")
                )
                
                self._display_api_results(result, endpoint_info, f"Zip Codes: {extra_params['zip_codes']}")
                
            except AttributeError:
                st.error(f"Method {method_name} not implemented in AcumidataClient")
            except Exception as e:
                st.error(f"Error calling API: {str(e)}")
    
    def _execute_state_based_api_test(self, endpoint_info: Dict[str, str], environment: str, extra_params: Dict):
        """Execute state-based API test."""
        if not extra_params.get("state"):
            st.error("Please provide a state code")
            return
        
        method_name = endpoint_info['method']
        
        with st.spinner(f"Calling {endpoint_info['name']} endpoint..."):
            try:
                client = AcumidataClient(environment=environment)
                method = getattr(client, method_name)
                
                # Call method with state-based parameters
                result = method(
                    extra_params["state"],
                    extra_params.get("start_timestamp"),
                    extra_params.get("end_timestamp"),
                    extra_params.get("extract_type")
                )
                
                self._display_api_results(result, endpoint_info, f"State: {extra_params['state']}")
                
            except AttributeError:
                st.error(f"Method {method_name} not implemented in AcumidataClient")
            except Exception as e:
                st.error(f"Error calling API: {str(e)}")
    
    def _execute_polygon_based_api_test(self, endpoint_info: Dict[str, str], address: str, city: str, 
                                       state: str, zip_code: str, environment: str, extra_params: Dict):
        """Execute polygon-based API test."""
        if not all([address, city, state, zip_code]):
            st.error("Please fill in all required property address fields")
            return
        
        if not extra_params.get("polygon"):
            st.error("Please provide polygon coordinates")
            return
        
        method_name = endpoint_info['method']
        
        with st.spinner(f"Calling {endpoint_info['name']} endpoint..."):
            try:
                client = AcumidataClient(environment=environment)
                method = getattr(client, method_name)
                
                # Call method with polygon-based parameters
                result = method(
                    address, city, state, zip_code,
                    extra_params["polygon"],
                    extra_params.get("land_use"),
                    extra_params.get("date"),
                    extra_params.get("include_birdseye")
                )
                
                self._display_api_results(result, endpoint_info, f"{address}, {city}, {state} {zip_code} (Polygon)")
                
            except AttributeError:
                st.error(f"Method {method_name} not implemented in AcumidataClient")
            except Exception as e:
                st.error(f"Error calling API: {str(e)}")
    
    def _execute_fips_based_api_test(self, endpoint_info: Dict[str, str], environment: str, extra_params: Dict):
        """Execute FIPS-based API test."""
        if not extra_params.get("fips_codes"):
            st.error("Please provide at least one FIPS code")
            return
        
        method_name = endpoint_info['method']
        
        with st.spinner(f"Calling {endpoint_info['name']} endpoint..."):
            try:
                client = AcumidataClient(environment=environment)
                method = getattr(client, method_name)
                
                # Call method with FIPS-based parameters
                result = method(
                    extra_params["fips_codes"],
                    extra_params.get("start_date"),
                    extra_params.get("end_date"),
                    extra_params.get("statuses"),
                    extra_params.get("ref_id")
                )
                
                self._display_api_results(result, endpoint_info, f"FIPS Codes: {extra_params['fips_codes']}")
                
            except AttributeError:
                st.error(f"Method {method_name} not implemented in AcumidataClient")
            except Exception as e:
                st.error(f"Error calling API: {str(e)}")
    
    def _execute_enhanced_state_based_api_test(self, endpoint_info: Dict[str, str], environment: str, extra_params: Dict):
        """Execute enhanced state-based API test."""
        if not extra_params.get("state"):
            st.error("Please provide a state code")
            return
        
        method_name = endpoint_info['method']
        
        with st.spinner(f"Calling {endpoint_info['name']} endpoint..."):
            try:
                client = AcumidataClient(environment=environment)
                method = getattr(client, method_name)
                
                # Call method with enhanced state-based parameters
                result = method(
                    extra_params["state"],
                    extra_params.get("page_size", 100),
                    extra_params.get("start_timestamp"),
                    extra_params.get("end_timestamp"),
                    extra_params.get("extract_type"),
                    extra_params.get("transaction_id")
                )
                
                self._display_api_results(result, endpoint_info, f"State: {extra_params['state']} (Enhanced)")
                
            except AttributeError:
                st.error(f"Method {method_name} not implemented in AcumidataClient")
            except Exception as e:
                st.error(f"Error calling API: {str(e)}")
    
    def _display_api_results(self, result: Dict[str, Any], endpoint_info: Dict[str, str], query_info: str):
        """Display API results in formatted and raw views."""
        st.markdown("---")
        st.subheader("📊 API Response")
        
        if "error" in result:
            st.error(f"API Error: {result['error']}")
            return
        
        # Query info header
        st.success(f"✅ Successfully retrieved data for: **{query_info}**")
        
        # Check if result has meaningful data
        details = result.get("Details")
        metadata = result.get("MetaData") 
        
        if details is None and metadata is None:
            st.warning("⚠️ API returned successful response but with no data (NULL values)")
            st.info("This might indicate:")
            st.write("- Property not found in database")
            st.write("- Invalid address or location")
            st.write("- Service temporarily unavailable for this property")
            st.write("- Insufficient data available for this property")
        
        # Create tabs for different views
        tab1, tab2, tab3 = st.tabs(["📋 Summary", "🔍 Raw JSON", "📈 Response Stats"])
        
        with tab1:
            self._render_formatted_summary(result, endpoint_info)
        
        with tab2:
            self._render_raw_json(result, endpoint_info)
        
        with tab3:
            self._render_response_stats(result)
    
    def _render_formatted_summary(self, result: Dict[str, Any], endpoint_info: Dict[str, str]):
        """Render a formatted summary based on endpoint type."""
        st.write("**Key Information**")
        
        # Check if we have valid details
        details = result.get("Details")
        if details is None:
            st.info("No detailed information available - API returned NULL data")
            return
        
        category = endpoint_info['category']
        
        if category == "Valuation":
            self._render_valuation_summary(result)
        elif category == "Comparables":
            self._render_comps_summary(result)
        elif category == "Equity":
            self._render_equity_summary(result)
        elif category == "Monitoring":
            self._render_monitoring_summary(result)
        elif category == "Title":
            self._render_title_summary(result)
        elif category == "MLS/Listings":
            self._render_listings_summary(result)
        elif category == "Parcels":
            self._render_parcels_summary(result)
        else:
            # Generic display
            if isinstance(details, dict):
                for key, value in details.items():
                    if isinstance(value, dict) and len(str(value)) < 200:
                        st.write(f"**{key.replace('_', ' ').title()}:** {value}")
            else:
                st.write("Details data is not in expected format")
    
    def _render_valuation_summary(self, result: Dict[str, Any]):
        """Render valuation-specific summary."""
        details = result.get("Details")
        if not details or not isinstance(details, dict):
            st.info("No valuation details available")
            return
            
        property_valuation = details.get("PropertyValuation", {})
        property_summary = details.get("PropertySummary", {})
        
        if property_valuation and isinstance(property_valuation, dict):
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
        
        if property_summary and isinstance(property_summary, dict):
            st.write("**Property Details:**")
            col1, col2, col3 = st.columns(3)
            
            with col1:
                beds = property_summary.get("Bedrooms", "N/A")
                st.write(f"Bedrooms: {beds}")
            
            with col2:
                baths = property_summary.get("FullBaths", "N/A")
                st.write(f"Bathrooms: {baths}")
            
            with col3:
                year_built = property_summary.get("YearBuilt", "N/A")
                st.write(f"Year Built: {year_built}")
        
        if not property_valuation and not property_summary:
            st.info("No specific valuation or property summary data found in response")
    
    def _render_comps_summary(self, result: Dict[str, Any]):
        """Render comparables-specific summary."""
        details = result.get("Details")
        if not details or not isinstance(details, dict):
            st.info("No comparables details available")
            return
            
        comp_listings = details.get("ComparablePropertyListings")
        if not comp_listings or not isinstance(comp_listings, dict):
            st.info("No comparable property listings found")
            return
            
        comps = comp_listings.get("Comparables", [])
        
        if comps and isinstance(comps, list):
            st.write(f"**Found {len(comps)} comparable properties**")
            
            # Calculate statistics
            prices = [float(comp.get("Price", 0)) for comp in comps if comp.get("Price")]
            if prices:
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    avg_price = sum(prices) / len(prices)
                    st.metric("Average Price", f"${avg_price:,.0f}")
                
                with col2:
                    st.metric("Price Range", f"${min(prices):,.0f} - ${max(prices):,.0f}")
                
                with col3:
                    distances = [float(comp.get("Distance", 0)) for comp in comps if comp.get("Distance")]
                    if distances:
                        avg_distance = sum(distances) / len(distances)
                        st.metric("Avg Distance", f"{avg_distance:.1f} mi")
            
            # Show top 3 comps
            st.write("**Top Comparable Properties:**")
            for i, comp in enumerate(comps[:3]):
                with st.expander(f"Comp {i+1}: {comp.get('Address', 'N/A')}"):
                    col1, col2 = st.columns(2)
                    with col1:
                        st.write(f"Price: ${float(comp.get('Price', 0)):,.0f}")
                        st.write(f"Beds: {comp.get('Bedrooms', 'N/A')}")
                        st.write(f"Baths: {comp.get('Baths', 'N/A')}")
                    with col2:
                        st.write(f"Sqft: {comp.get('BuildingSqft', 'N/A')}")
                        st.write(f"Year: {comp.get('YearBuilt', 'N/A')}")
                        st.write(f"Distance: {comp.get('Distance', 'N/A')} mi")
        else:
            st.info("No comparable properties found")
    
    def _render_equity_summary(self, result: Dict[str, Any]):
        """Render equity-specific summary."""
        details = result.get("Details", {})
        if details:
            st.write("**Equity Analysis Results:**")
            # Add specific equity parsing based on actual response structure
            st.json(details)
    
    def _render_monitoring_summary(self, result: Dict[str, Any]):
        """Render monitoring-specific summary."""
        details = result.get("Details", {})
        if details:
            st.write("**Monitoring Setup Results:**")
            # Add specific monitoring parsing based on actual response structure
            st.json(details)
    
    def _render_title_summary(self, result: Dict[str, Any]):
        """Render title-specific summary."""
        details = result.get("Details", {})
        if details:
            st.write("**Title Report Summary:**")
            
            # Look for common title report fields
            title_info = details.get("TitleInformation", {})
            property_info = details.get("PropertyInformation", {})
            
            if title_info:
                col1, col2 = st.columns(2)
                
                with col1:
                    owner = title_info.get("Owner", "N/A")
                    st.write(f"**Owner:** {owner}")
                    
                    deed_type = title_info.get("DeedType", "N/A")
                    st.write(f"**Deed Type:** {deed_type}")
                
                with col2:
                    recording_date = title_info.get("RecordingDate", "N/A")
                    st.write(f"**Recording Date:** {recording_date}")
                    
                    legal_description = title_info.get("LegalDescription", "N/A")
                    if len(str(legal_description)) < 100:
                        st.write(f"**Legal Description:** {legal_description}")
            
            if property_info:
                st.write("**Property Information:**")
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    parcel_id = property_info.get("ParcelId", "N/A")
                    st.write(f"Parcel ID: {parcel_id}")
                
                with col2:
                    assessed_value = property_info.get("AssessedValue", "N/A")
                    if assessed_value != "N/A":
                        st.write(f"Assessed Value: ${assessed_value:,.0f}")
                    else:
                        st.write(f"Assessed Value: {assessed_value}")
                
                with col3:
                    land_use = property_info.get("LandUse", "N/A")
                    st.write(f"Land Use: {land_use}")
            
            # Show any liens or encumbrances
            liens = details.get("Liens", [])
            if liens:
                st.write(f"**Found {len(liens)} liens/encumbrances**")
                for i, lien in enumerate(liens[:3]):
                    with st.expander(f"Lien {i+1}"):
                        st.json(lien)
        else:
            st.info("No detailed title information available in response")

    def _render_parcels_summary(self, result: Dict[str, Any]):
        """Render parcels-specific summary."""
        parcel_details = result.get("parcelDetails", [])
        metadata = result.get("metadata", {})
        
        if metadata:
            st.write("**Request Summary:**")
            col1, col2, col3 = st.columns(3)
            
            with col1:
                parcel_count = metadata.get("parcelCount", 0)
                st.metric("Total Parcels", parcel_count)
            
            with col2:
                valid_address_count = metadata.get("validAddressCount", 0)
                st.metric("Valid Addresses", valid_address_count)
            
            with col3:
                invalid_address_count = metadata.get("inValidAddressCount", 0)
                st.metric("Invalid Addresses", invalid_address_count)
        
        if parcel_details and len(parcel_details) > 0:
            st.write(f"**Found {len(parcel_details)} parcel(s)**")
            
            for i, parcel in enumerate(parcel_details):
                with st.expander(f"Parcel {i+1}: {parcel.get('streetAddress', 'N/A')}"):
                    # Basic property information
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.write("**Property Details:**")
                        st.write(f"**Address:** {parcel.get('streetAddress', 'N/A')}")
                        st.write(f"**City:** {parcel.get('city', 'N/A')}")
                        st.write(f"**State:** {parcel.get('stateProvince', 'N/A')}")
                        st.write(f"**ZIP:** {parcel.get('postalCode', 'N/A')}")
                        st.write(f"**County:** {parcel.get('county', 'N/A')}")
                        st.write(f"**APN:** {parcel.get('apn', 'N/A')}")
                    
                    with col2:
                        st.write("**Property Characteristics:**")
                        st.write(f"**Square Feet:** {parcel.get('sqFt', 'N/A'):,}" if parcel.get('sqFt') else "**Square Feet:** N/A")
                        st.write(f"**Bedrooms:** {parcel.get('bedrooms', 'N/A')}")
                        st.write(f"**Bathrooms:** {parcel.get('bathrooms', 'N/A')}")
                        st.write(f"**Year Built:** {parcel.get('yearBuilt', 'N/A')}")
                        st.write(f"**Lot Size:** {parcel.get('lotSize', 'N/A')}")
                        st.write(f"**Property Type:** {parcel.get('propertyType', 'N/A')}")
                    
                    # Financial information
                    if any(parcel.get(key) for key in ['lastSalePrice', 'lastSaleDate', 'taxAssessedValue']):
                        st.write("**Financial Information:**")
                        col1, col2, col3 = st.columns(3)
                        
                        with col1:
                            last_sale_price = parcel.get('lastSalePrice')
                            if last_sale_price:
                                st.write(f"**Last Sale Price:** ${float(last_sale_price):,.0f}")
                            else:
                                st.write("**Last Sale Price:** N/A")
                        
                        with col2:
                            last_sale_date = parcel.get('lastSaleDate')
                            st.write(f"**Last Sale Date:** {last_sale_date or 'N/A'}")
                        
                        with col3:
                            tax_assessed_value = parcel.get('taxAssessedValue')
                            if tax_assessed_value:
                                st.write(f"**Tax Assessed Value:** ${float(tax_assessed_value):,.0f}")
                            else:
                                st.write("**Tax Assessed Value:** N/A")
                    
                    # Location information
                    if parcel.get('latitude') and parcel.get('longitude'):
                        st.write("**Location:**")
                        st.write(f"**Coordinates:** {parcel.get('latitude')}, {parcel.get('longitude')}")
                    
                    # Additional details in an expandable section
                    with st.expander("Additional Details"):
                        additional_fields = {
                            'legal_Desc': 'Legal Description',
                            'zoning': 'Zoning',
                            'landUse': 'Land Use',
                            'fireplace': 'Fireplace',
                            'pool': 'Pool',
                            'gla': 'Gross Living Area',
                            'data_last_update': 'Data Last Updated'
                        }
                        
                        for field, label in additional_fields.items():
                            value = parcel.get(field)
                            if value:
                                st.write(f"**{label}:** {value}")
        
        elif parcel_details is not None and len(parcel_details) == 0:
            st.warning("No parcel details found for the provided address")
        else:
            st.info("No parcel details available in response")

    def _render_listings_summary(self, result: Dict[str, Any]):
        """Render listings-specific summary."""
        details = result.get("Details")
        
        if not details or not isinstance(details, dict):
            st.info("No listings details available")
            return
        
        # Check for listings array
        listings = details.get("Listings", [])
        properties = details.get("Properties", [])
        
        if listings and isinstance(listings, list):
            st.write(f"**Found {len(listings)} listings**")
            
            # Calculate statistics
            active_listings = [l for l in listings if l.get("Status", "").lower() == "active"]
            pending_listings = [l for l in listings if l.get("Status", "").lower() == "pending"]
            sold_listings = [l for l in listings if l.get("Status", "").lower() == "sold"]
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("Active Listings", len(active_listings))
            
            with col2:
                st.metric("Pending Listings", len(pending_listings))
            
            with col3:
                st.metric("Sold Listings", len(sold_listings))
            
            # Price statistics
            prices = [float(l.get("ListPrice", 0)) for l in listings if l.get("ListPrice")]
            if prices:
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    avg_price = sum(prices) / len(prices)
                    st.metric("Average Price", f"${avg_price:,.0f}")
                
                with col2:
                    st.metric("Price Range", f"${min(prices):,.0f} - ${max(prices):,.0f}")
                
                with col3:
                    median_price = sorted(prices)[len(prices)//2]
                    st.metric("Median Price", f"${median_price:,.0f}")
            
            # Show sample listings
            st.write("**Sample Listings:**")
            for i, listing in enumerate(listings[:5]):
                with st.expander(f"Listing {i+1}: {listing.get('Address', 'N/A')}"):
                    col1, col2 = st.columns(2)
                    with col1:
                        st.write(f"Price: ${float(listing.get('ListPrice', 0)):,.0f}")
                        st.write(f"Status: {listing.get('Status', 'N/A')}")
                        st.write(f"Beds: {listing.get('Bedrooms', 'N/A')}")
                    with col2:
                        st.write(f"Baths: {listing.get('Bathrooms', 'N/A')}")
                        st.write(f"Sqft: {listing.get('SquareFeet', 'N/A')}")
                        st.write(f"List Date: {listing.get('ListDate', 'N/A')}")
        
        elif properties and isinstance(properties, list):
            st.write(f"**Found {len(properties)} properties**")
            # Handle properties array similar to listings
            for i, prop in enumerate(properties[:3]):
                with st.expander(f"Property {i+1}"):
                    st.json(prop)
        
        else:
            # Check for other data structures
            data_keys = [k for k in details.keys() if isinstance(details[k], list) and details[k]]
            if data_keys:
                st.write("**Available Data:**")
                for key in data_keys:
                    data_list = details[key]
                    st.write(f"- {key.replace('_', ' ').title()}: {len(data_list)} items")
                    
                    if len(data_list) > 0 and isinstance(data_list[0], dict):
                        with st.expander(f"Sample {key} data"):
                            st.json(data_list[0])
            else:
                st.write("**Response Summary:**")
                for key, value in details.items():
                    if not isinstance(value, (list, dict)) or len(str(value)) < 100:
                        st.write(f"**{key.replace('_', ' ').title()}:** {value}")
    
    def _render_raw_json(self, result: Dict[str, Any], endpoint_info: Dict[str, str]):
        """Render the raw JSON response."""
        st.write("**Complete API Response**")
        
        # JSON display options
        col1, col2 = st.columns([3, 1])
        
        with col2:
            # Download button
            json_str = json.dumps(result, indent=2)
            st.download_button(
                label="📥 Download JSON",
                data=json_str,
                file_name=f"{endpoint_info['name'].lower().replace(' ', '_')}_response.json",
                mime="application/json"
            )
        
        # Display JSON
        st.json(result)
    
    def _render_response_stats(self, result: Dict[str, Any]):
        """Render response statistics."""
        st.write("**Response Statistics**")
        
        # Basic response stats
        col1, col2, col3 = st.columns(3)
        
        with col1:
            response_size = len(json.dumps(result))
            st.metric("Response Size", f"{response_size:,} bytes")
        
        with col2:
            details = result.get("Details")
            if details and isinstance(details, dict):
                field_count = len(details)
            else:
                field_count = 0
            st.metric("Data Fields", field_count)
        
        with col3:
            # Count nested objects
            nested_count = 0
            if details and isinstance(details, dict):
                nested_count = sum(1 for v in details.values() if isinstance(v, dict))
            st.metric("Nested Objects", nested_count)
        
        # Response structure
        if isinstance(result, dict):
            st.write("**Response Structure:**")
            structure = self._analyze_structure(result)
            st.code(structure, language="text")
    
    def _analyze_structure(self, data: Any, prefix: str = "", max_depth: int = 3) -> str:
        """Analyze and display the structure of the response."""
        if max_depth <= 0:
            return f"{prefix}... (truncated)"
        
        structure = ""
        
        if isinstance(data, dict):
            for key, value in data.items():
                if isinstance(value, dict):
                    structure += f"{prefix}{key}/ (object)\n"
                    structure += self._analyze_structure(value, prefix + "  ", max_depth - 1)
                elif isinstance(value, list):
                    structure += f"{prefix}{key}[] (array, {len(value)} items)\n"
                    if value and max_depth > 1:
                        structure += self._analyze_structure(value[0], prefix + "  ", max_depth - 1)
                else:
                    value_type = type(value).__name__
                    structure += f"{prefix}{key} ({value_type})\n"
        
        return structure 