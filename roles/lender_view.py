"""
Lender-specific dashboard view focusing on risk assessment and loan metrics.
"""

import streamlit as st
import pandas as pd
from typing import Dict, Any, Optional


class LenderView:
    """Dashboard view tailored for lenders with focus on risk assessment."""
    
    def __init__(self):
        self.role = "Lender"
        self.primary_metrics = [
            "loan_to_value_ratio",
            "debt_service_coverage",
            "property_condition_score",
            "market_risk_score"
        ]
    
    def render_dashboard(self, property_data: Optional[Dict[str, Any]] = None):
        """Render the lender-specific dashboard layout."""
        st.header("🏦 Lender Dashboard")
        st.subheader("Risk Assessment & Loan Metrics")
        
        # Lender-specific metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                label="LTV Ratio",
                value="75%",
                delta="-5%",
                help="Loan-to-Value ratio for risk assessment"
            )
        
        with col2:
            st.metric(
                label="DSCR",
                value="1.25",
                delta="0.15",
                help="Debt Service Coverage Ratio"
            )
        
        with col3:
            st.metric(
                label="Risk Score",
                value="B+",
                delta="Stable",
                help="Overall property risk assessment"
            )
        
        with col4:
            st.metric(
                label="Market Trend",
                value="↗️ Rising",
                delta="2.3%",
                help="Local market trend indicator"
            )
        
        # Lender-specific sections
        self._render_risk_analysis()
        self._render_loan_scenarios()
        self._render_compliance_check()
    
    def _render_risk_analysis(self):
        """Render risk analysis section."""
        st.markdown("---")
        st.subheader("📊 Risk Analysis")
        
        # Placeholder for risk analysis charts
        col1, col2 = st.columns(2)
        
        with col1:
            st.info("**Market Risk Factors**\n- Property type: Single Family\n- Location score: 8.5/10\n- Market volatility: Low")
        
        with col2:
            st.info("**Property Risk Factors**\n- Condition score: 7.8/10\n- Age: 15 years\n- Maintenance history: Good")
    
    def _render_loan_scenarios(self):
        """Render loan scenario modeling."""
        st.markdown("---")
        st.subheader("💰 Loan Scenarios")
        
        # Placeholder loan scenario table
        scenarios_data = {
            "Scenario": ["Conservative", "Standard", "Aggressive"],
            "LTV": ["70%", "80%", "90%"],
            "Interest Rate": ["6.5%", "7.0%", "7.5%"],
            "Monthly Payment": ["$2,850", "$3,200", "$3,650"],
            "Risk Level": ["Low", "Medium", "High"]
        }
        
        df = pd.DataFrame(scenarios_data)
        st.dataframe(df, use_container_width=True, hide_index=True)
    
    def _render_compliance_check(self):
        """Render compliance and regulatory checks."""
        st.markdown("---")
        st.subheader("✅ Compliance Check")
        
        compliance_items = [
            ("Appraisal Requirements", "✅ Completed"),
            ("Income Verification", "✅ Verified"),
            ("Credit Score Check", "✅ 750+"),
            ("Debt-to-Income Ratio", "✅ 28%"),
            ("Property Insurance", "⏳ Pending"),
            ("Title Search", "✅ Clear")
        ]
        
        for item, status in compliance_items:
            col1, col2 = st.columns([3, 1])
            with col1:
                st.write(item)
            with col2:
                st.write(status)
    
    def get_role_config(self) -> Dict[str, Any]:
        """Get role-specific configuration."""
        return {
            "role": self.role,
            "primary_color": "#1f77b4",
            "focus_areas": ["Risk Assessment", "Loan Metrics", "Compliance"],
            "default_view": "risk_analysis",
            "required_fields": ["ltv_ratio", "dscr", "credit_score"]
        } 