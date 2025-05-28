"""
Parser utilities for processing API responses and data transformation.
"""

from typing import Dict, Any, Optional, List


class PropertyDataParser:
    """Parser for property data from various API endpoints."""
    
    @staticmethod
    def extract_valuation_summary(api_response: Dict[str, Any]) -> Dict[str, Any]:
        """Extract key valuation metrics from API response."""
        details = api_response.get("Details", {})
        property_valuation = details.get("PropertyValuation", {})
        property_summary = details.get("PropertySummary", {})
        
        return {
            "estimated_value": property_valuation.get("EstimatedValue"),
            "confidence_score": property_valuation.get("ConfidenceScore"),
            "valuation_range_low": property_valuation.get("ValuationRangeLow"),
            "valuation_range_high": property_valuation.get("ValuationRangeHigh"),
            "bedrooms": property_summary.get("Bedrooms"),
            "bathrooms": property_summary.get("FullBaths"),
            "year_built": property_summary.get("YearBuilt")
        }
    
    @staticmethod
    def extract_comparables(api_response: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Extract comparable properties from API response."""
        details = api_response.get("Details", {})
        comps_data = details.get("ComparablePropertyListings", {})
        comparables = comps_data.get("Comparables", [])
        
        processed_comps = []
        for comp in comparables:
            processed_comps.append({
                "address": comp.get("Address"),
                "city": comp.get("City"),
                "state": comp.get("State"),
                "zip": comp.get("Zip"),
                "price": comp.get("Price"),
                "bedrooms": comp.get("Bedrooms"),
                "bathrooms": comp.get("Baths"),
                "sqft": comp.get("BuildingSqft"),
                "year_built": comp.get("YearBuilt"),
                "distance": comp.get("Distance")
            })
        
        return processed_comps
    
    @staticmethod
    def calculate_comp_statistics(comparables: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Calculate statistics from comparable properties."""
        if not comparables:
            return {}
        
        prices = [float(comp.get("price", 0)) for comp in comparables if comp.get("price")]
        distances = [float(comp.get("distance", 0)) for comp in comparables if comp.get("distance")]
        
        stats = {
            "total_comps": len(comparables),
            "avg_price": sum(prices) / len(prices) if prices else 0,
            "min_price": min(prices) if prices else 0,
            "max_price": max(prices) if prices else 0,
            "avg_distance": sum(distances) / len(distances) if distances else 0
        }
        
        return stats 