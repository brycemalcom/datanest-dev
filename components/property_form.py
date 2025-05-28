"""
Property Form component for reusable property input forms.
"""

import streamlit as st
from typing import Dict, Any, Optional, Tuple


class PropertyForm:
    """Reusable component for property address input forms."""
    
    def __init__(self):
        self.default_values = {
            "address": "531 NE Beck Rd",
            "city": "Belfair", 
            "state": "WA",
            "zip_code": "98528"
        }
    
    def render_form(self, form_key: str = "property_form") -> Tuple[bool, Dict[str, str]]:
        """Render a property input form and return submission status and data."""
        with st.form(form_key):
            col1, col2 = st.columns(2)
            
            with col1:
                address = st.text_input("Street Address", value=self.default_values["address"])
                city = st.text_input("City", value=self.default_values["city"])
            
            with col2:
                state = st.text_input("State", value=self.default_values["state"])
                zip_code = st.text_input("Zip Code", value=self.default_values["zip_code"])
            
            submitted = st.form_submit_button("Submit")
            
            form_data = {
                "address": address.strip(),
                "city": city.strip(),
                "state": state.strip().upper(),
                "zip_code": zip_code.strip()
            }
            
            return submitted, form_data 