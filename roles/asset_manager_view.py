"""
Asset Manager-specific dashboard view focusing on portfolio management and operational metrics.
"""

import streamlit as st
import pandas as pd
from typing import Dict, Any, Optional


class AssetManagerView:
    """Dashboard view tailored for asset managers with focus on portfolio and operations."""
    
    def __init__(self):
        self.role = "Asset Manager"
        self.primary_metrics = [
            "portfolio_value",
            "occupancy_rate",
            "noi_growth",
            "maintenance_ratio"
        ]
    
    def render_dashboard(self, property_data: Optional[Dict[str, Any]] = None):
        """Render the asset manager-specific dashboard layout."""
        st.header("🏢 Asset Manager Dashboard")
        st.subheader("Portfolio Management & Operations")
        
        # Asset manager-specific metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                label="Portfolio Value",
                value="$12.5M",
                delta="$850K",
                help="Total portfolio value"
            )
        
        with col2:
            st.metric(
                label="Occupancy Rate",
                value="94.2%",
                delta="2.1%",
                help="Portfolio-wide occupancy rate"
            )
        
        with col3:
            st.metric(
                label="NOI Growth",
                value="7.8%",
                delta="YoY",
                help="Net Operating Income growth"
            )
        
        with col4:
            st.metric(
                label="Maintenance Ratio",
                value="12.3%",
                delta="-1.2%",
                help="Maintenance costs as % of revenue"
            )
        
        # Asset manager-specific sections
        self._render_portfolio_overview()
        self._render_operational_metrics()
        self._render_maintenance_tracking()
    
    def _render_portfolio_overview(self):
        """Render portfolio overview section."""
        st.markdown("---")
        st.subheader("📊 Portfolio Overview")
        
        # Portfolio composition
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**Property Types**")
            property_types = {
                "Single Family": 45,
                "Multi-Family": 25,
                "Commercial": 20,
                "Mixed Use": 10
            }
            st.bar_chart(property_types)
        
        with col2:
            st.write("**Geographic Distribution**")
            geographic_data = {
                "Region": ["Seattle Metro", "Tacoma", "Spokane", "Bellingham", "Other"],
                "Properties": [35, 20, 15, 12, 18],
                "Value ($M)": [6.2, 2.8, 1.9, 1.1, 0.5]
            }
            df = pd.DataFrame(geographic_data)
            st.dataframe(df, use_container_width=True, hide_index=True)
    
    def _render_operational_metrics(self):
        """Render operational metrics section."""
        st.markdown("---")
        st.subheader("⚙️ Operational Metrics")
        
        # Key operational indicators
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.info("""
            **Leasing Metrics**
            - Avg Days to Lease: 28
            - Renewal Rate: 87%
            - Rent Growth: 5.2%
            - Vacancy Loss: 2.1%
            """)
        
        with col2:
            st.info("""
            **Financial Performance**
            - Total Revenue: $2.1M
            - Operating Expenses: $1.3M
            - NOI: $800K
            - EBITDA Margin: 38%
            """)
        
        with col3:
            st.info("""
            **Tenant Satisfaction**
            - Response Rate: 92%
            - Satisfaction Score: 4.2/5
            - Complaints: 12 (down 25%)
            - Retention Rate: 89%
            """)
    
    def _render_maintenance_tracking(self):
        """Render maintenance and capital expenditure tracking."""
        st.markdown("---")
        st.subheader("🔧 Maintenance & CapEx Tracking")
        
        # Maintenance requests and spending
        tab1, tab2, tab3 = st.tabs(["Active Requests", "Spending Analysis", "Preventive Schedule"])
        
        with tab1:
            st.write("**Active Maintenance Requests**")
            maintenance_data = {
                "Property": ["123 Main St", "456 Oak Ave", "789 Pine Rd", "321 Elm St"],
                "Issue": ["HVAC Repair", "Plumbing Leak", "Roof Inspection", "Electrical"],
                "Priority": ["High", "Medium", "Low", "High"],
                "Status": ["In Progress", "Scheduled", "Pending", "Assigned"],
                "Days Open": [3, 7, 12, 1]
            }
            df = pd.DataFrame(maintenance_data)
            st.dataframe(df, use_container_width=True, hide_index=True)
        
        with tab2:
            st.write("**Monthly Maintenance Spending**")
            spending_data = {
                "Month": ["Jan", "Feb", "Mar", "Apr", "May", "Jun"],
                "Routine": [15000, 12000, 18000, 14000, 16000, 13000],
                "Emergency": [8000, 5000, 12000, 3000, 7000, 4000],
                "CapEx": [25000, 0, 45000, 15000, 0, 30000]
            }
            df = pd.DataFrame(spending_data)
            st.line_chart(df.set_index("Month"))
        
        with tab3:
            st.write("**Preventive Maintenance Schedule**")
            schedule_data = {
                "Task": ["HVAC Service", "Roof Inspection", "Fire Safety Check", "Landscaping"],
                "Frequency": ["Quarterly", "Bi-Annual", "Annual", "Monthly"],
                "Last Completed": ["2024-03-15", "2024-01-20", "2023-12-10", "2024-05-25"],
                "Next Due": ["2024-06-15", "2024-07-20", "2024-12-10", "2024-06-25"],
                "Status": ["Scheduled", "Overdue", "Upcoming", "Completed"]
            }
            df = pd.DataFrame(schedule_data)
            st.dataframe(df, use_container_width=True, hide_index=True)
    
    def get_role_config(self) -> Dict[str, Any]:
        """Get role-specific configuration."""
        return {
            "role": self.role,
            "primary_color": "#ff7f0e",
            "focus_areas": ["Portfolio Management", "Operations", "Maintenance"],
            "default_view": "portfolio_overview",
            "required_fields": ["portfolio_data", "occupancy_rates", "maintenance_logs"]
        } 