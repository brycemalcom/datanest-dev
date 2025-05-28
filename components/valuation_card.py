"""
Valuation Card component for displaying property valuation data.
"""

import streamlit as st
import pandas as pd
from typing import Dict, Any, Optional


class ValuationCard:
    """Reusable component for displaying property valuation information."""
    
    def __init__(self):
        self.card_style = """
        <style>
        .valuation-card {
            background: #f8f9fa;
            border-radius: 1rem;
            padding: 2rem 1.5rem 1.5rem 1.5rem;
            box-shadow: 0 2px 8px rgba(44,62,80,0.07);
            margin-bottom: 1.5rem;
        }
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
        </style>
        """
    
    def render(self, valuation_data: Dict[str, Any], property_address: str = ""):
        """Render the valuation card with property data."""
        # Apply custom CSS
        st.markdown(self.card_style, unsafe_allow_html=True)
        
        # Extract valuation information
        details = valuation_data.get("Details", {})
        property_valuation = details.get("PropertyValuation", {})
        property_summary = details.get("PropertySummary", {})
        property_details = details.get("PropertyDetails", {})
        basics = property_details.get("PropertyBasics", {}) if property_details else {}
        
        # Main valuation card
        st.markdown('<div class="valuation-card">', unsafe_allow_html=True)
        st.markdown('<div class="metric-label">Property Valuation</div>', unsafe_allow_html=True)
        
        if property_address:
            st.markdown(f'<div class="big-metric">{property_address}</div>', unsafe_allow_html=True)
        
        estimated_value = property_valuation.get("EstimatedValue")
        if estimated_value:
            st.markdown(f'<div class="big-metric">Estimated Value: ${estimated_value:,.2f}</div>', unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Property details metrics
        self._render_property_metrics(property_summary, basics, property_valuation)
        
        # Valuation range and confidence
        self._render_valuation_metrics(property_valuation)
        
        # Comparable properties
        comps = details.get("ComparablePropertyListings", {}).get("Comparables", [])
        if comps:
            self._render_comparables(comps)
    
    def _render_property_metrics(self, summary: Dict, basics: Dict, valuation: Dict):
        """Render basic property metrics."""
        col1, col2, col3 = st.columns(3)
        
        # Get year built from multiple sources
        year_built = self._get_year_built(summary, basics, valuation)
        beds = summary.get("Bedrooms", "N/A")
        baths = summary.get("FullBaths", "N/A")
        
        with col1:
            st.metric(label="Bedrooms", value=beds)
        with col2:
            st.metric(label="Bathrooms", value=baths)
        with col3:
            st.metric(label="Year Built", value=year_built)
    
    def _render_valuation_metrics(self, property_valuation: Dict):
        """Render valuation-specific metrics."""
        st.markdown("---")
        st.subheader("Valuation Analysis 📊")
        
        col1, col2, col3 = st.columns(3)
        
        confidence_score = property_valuation.get("ConfidenceScore")
        valuation_low = property_valuation.get("ValuationRangeLow")
        valuation_high = property_valuation.get("ValuationRangeHigh")
        
        with col1:
            if confidence_score:
                st.metric(
                    label="Confidence Score",
                    value=f"{confidence_score}/100",
                    help="Confidence level of the valuation estimate"
                )
            else:
                st.metric(label="Confidence Score", value="N/A")
        
        with col2:
            if valuation_low:
                st.metric(
                    label="Valuation Low",
                    value=f"${valuation_low:,.0f}",
                    help="Lower bound of valuation range"
                )
            else:
                st.metric(label="Valuation Low", value="N/A")
        
        with col3:
            if valuation_high:
                st.metric(
                    label="Valuation High",
                    value=f"${valuation_high:,.0f}",
                    help="Upper bound of valuation range"
                )
            else:
                st.metric(label="Valuation High", value="N/A")
    
    def _render_comparables(self, comps: list):
        """Render comparable properties section."""
        st.markdown("---")
        st.subheader("Recent Comparable Sales 🏡")
        
        if not comps:
            st.info("No comparable properties found.")
            return
        
        # Calculate average price from comparables
        prices = [float(prop.get("Price", 0)) for prop in comps if prop.get("Price")]
        if prices:
            avg_price = sum(prices) / len(prices)
            col1, col2 = st.columns(2)
            
            with col1:
                st.metric(
                    label="Average Comp Price",
                    value=f"${avg_price:,.0f}",
                    help="Average price of comparable properties"
                )
            
            with col2:
                st.metric(
                    label="Number of Comps",
                    value=len(comps),
                    help="Total number of comparable properties found"
                )
        
        # Comparables table
        comp_data = []
        for comp in comps[:5]:  # Show top 5 comparables
            comp_data.append({
                "Address": f"{comp.get('Address', 'N/A')}, {comp.get('City', 'N/A')}, {comp.get('State', 'N/A')} {comp.get('Zip', 'N/A')}",
                "Price": f"${float(comp.get('Price', 0)):,.0f}" if comp.get('Price') else "N/A",
                "Beds": comp.get("Bedrooms", "-"),
                "Baths": comp.get("Baths", "-"),
                "Sqft": comp.get("BuildingSqft", "-"),
                "Year Built": comp.get("YearBuilt", "-"),
                "Distance": f"{comp.get('Distance', '-')} mi"
            })
        
        if comp_data:
            df = pd.DataFrame(comp_data)
            st.dataframe(df, use_container_width=True, hide_index=True)
    
    def _get_year_built(self, summary: Dict, basics: Dict, valuation: Dict) -> str:
        """Get year built from multiple possible sources."""
        year_built_actual = basics.get("YearBuiltActual") if basics else None
        year_built_summary = summary.get("YearBuilt") if summary else None
        year_built_valuation = valuation.get("YearBuilt") if valuation else None
        
        # Use the first available value and convert to string
        if year_built_actual is not None:
            return str(year_built_actual)
        elif year_built_summary is not None:
            return str(year_built_summary)
        elif year_built_valuation is not None:
            return str(year_built_valuation)
        else:
            return "N/A"
    
    def render_compact(self, valuation_data: Dict[str, Any], property_address: str = ""):
        """Render a compact version of the valuation card."""
        details = valuation_data.get("Details", {})
        property_valuation = details.get("PropertyValuation", {})
        
        estimated_value = property_valuation.get("EstimatedValue")
        confidence_score = property_valuation.get("ConfidenceScore")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if estimated_value:
                st.metric("Estimated Value", f"${estimated_value:,.2f}")
            else:
                st.metric("Estimated Value", "N/A")
        
        with col2:
            if confidence_score:
                st.metric("Confidence", f"{confidence_score}/100")
            else:
                st.metric("Confidence", "N/A") 