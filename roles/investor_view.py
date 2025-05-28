"""
Investor-specific dashboard view focusing on ROI, cash flow, and market analysis.
"""

import streamlit as st
import pandas as pd
from typing import Dict, Any, Optional


class InvestorView:
    """Dashboard view tailored for investors with focus on returns and market analysis."""
    
    def __init__(self):
        self.role = "Investor"
        self.primary_metrics = [
            "cap_rate",
            "cash_on_cash_return",
            "irr",
            "market_appreciation"
        ]
    
    def render_dashboard(self, property_data: Optional[Dict[str, Any]] = None):
        """Render the investor-specific dashboard layout."""
        st.header("📈 Investor Dashboard")
        st.subheader("ROI Analysis & Market Insights")
        
        # Investor-specific metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                label="Cap Rate",
                value="6.8%",
                delta="0.3%",
                help="Capitalization rate for the property"
            )
        
        with col2:
            st.metric(
                label="Cash-on-Cash",
                value="12.5%",
                delta="1.2%",
                help="Cash-on-cash return"
            )
        
        with col3:
            st.metric(
                label="IRR (5yr)",
                value="15.2%",
                delta="2.1%",
                help="Internal Rate of Return projection"
            )
        
        with col4:
            st.metric(
                label="Market Growth",
                value="8.3%",
                delta="YoY",
                help="Annual market appreciation"
            )
        
        # Investor-specific sections
        self._render_cash_flow_analysis()
        self._render_market_comparisons()
        self._render_investment_scenarios()
    
    def _render_cash_flow_analysis(self):
        """Render cash flow analysis section."""
        st.markdown("---")
        st.subheader("💰 Cash Flow Analysis")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.info("""
            **Monthly Cash Flow**
            - Rental Income: $3,200
            - Mortgage Payment: $2,100
            - Property Taxes: $350
            - Insurance: $150
            - Maintenance: $200
            - **Net Cash Flow: $400**
            """)
        
        with col2:
            # Placeholder for cash flow chart
            cash_flow_data = {
                "Month": ["Jan", "Feb", "Mar", "Apr", "May", "Jun"],
                "Income": [3200, 3200, 3200, 3200, 3200, 3200],
                "Expenses": [2800, 2950, 2750, 2800, 3100, 2800],
                "Net": [400, 250, 450, 400, 100, 400]
            }
            df = pd.DataFrame(cash_flow_data)
            st.line_chart(df.set_index("Month")[["Income", "Expenses", "Net"]])
    
    def _render_market_comparisons(self):
        """Render market comparison analysis."""
        st.markdown("---")
        st.subheader("🏘️ Market Comparisons")
        
        # Comparable properties table
        comp_data = {
            "Property": ["Subject", "Comp 1", "Comp 2", "Comp 3", "Market Avg"],
            "Price": ["$425,000", "$410,000", "$445,000", "$430,000", "$427,500"],
            "Cap Rate": ["6.8%", "6.5%", "7.1%", "6.9%", "6.8%"],
            "Price/SqFt": ["$285", "$275", "$295", "$288", "$286"],
            "Days on Market": ["N/A", "45", "32", "67", "48"]
        }
        
        df = pd.DataFrame(comp_data)
        st.dataframe(df, use_container_width=True, hide_index=True)
    
    def _render_investment_scenarios(self):
        """Render investment scenario modeling."""
        st.markdown("---")
        st.subheader("🎯 Investment Scenarios")
        
        # Investment scenario tabs
        tab1, tab2, tab3 = st.tabs(["Conservative", "Moderate", "Aggressive"])
        
        with tab1:
            st.write("**Conservative Scenario (3% appreciation)**")
            conservative_data = {
                "Year": [1, 2, 3, 4, 5],
                "Property Value": ["$425K", "$438K", "$451K", "$465K", "$479K"],
                "Annual Cash Flow": ["$4,800", "$4,944", "$5,092", "$5,245", "$5,402"],
                "Cumulative Return": ["1.1%", "4.3%", "7.8%", "11.6%", "15.7%"]
            }
            df = pd.DataFrame(conservative_data)
            st.dataframe(df, use_container_width=True, hide_index=True)
        
        with tab2:
            st.write("**Moderate Scenario (5% appreciation)**")
            moderate_data = {
                "Year": [1, 2, 3, 4, 5],
                "Property Value": ["$425K", "$446K", "$469K", "$492K", "$517K"],
                "Annual Cash Flow": ["$4,800", "$5,040", "$5,292", "$5,557", "$5,835"],
                "Cumulative Return": ["1.1%", "6.2%", "12.1%", "18.8%", "26.4%"]
            }
            df = pd.DataFrame(moderate_data)
            st.dataframe(df, use_container_width=True, hide_index=True)
        
        with tab3:
            st.write("**Aggressive Scenario (8% appreciation)**")
            aggressive_data = {
                "Year": [1, 2, 3, 4, 5],
                "Property Value": ["$425K", "$459K", "$496K", "$536K", "$579K"],
                "Annual Cash Flow": ["$4,800", "$5,184", "$5,599", "$6,047", "$6,531"],
                "Cumulative Return": ["1.1%", "9.1%", "18.7%", "30.2%", "44.1%"]
            }
            df = pd.DataFrame(aggressive_data)
            st.dataframe(df, use_container_width=True, hide_index=True)
    
    def get_role_config(self) -> Dict[str, Any]:
        """Get role-specific configuration."""
        return {
            "role": self.role,
            "primary_color": "#2ca02c",
            "focus_areas": ["ROI Analysis", "Cash Flow", "Market Trends"],
            "default_view": "cash_flow_analysis",
            "required_fields": ["cap_rate", "cash_flow", "market_data"]
        } 