"""
Raw JSON View component for displaying API responses.
"""

import streamlit as st
import json
from typing import Dict, Any, Optional


class RawJsonView:
    """Component for displaying raw JSON data with formatting and download options."""
    
    def __init__(self):
        self.json_style = """
        <style>
        .json-container {
            background: #f8f9fa;
            border: 1px solid #e9ecef;
            border-radius: 0.5rem;
            padding: 1rem;
            margin: 1rem 0;
            font-family: 'Courier New', monospace;
            font-size: 0.9rem;
            max-height: 500px;
            overflow-y: auto;
        }
        .json-header {
            font-weight: bold;
            color: #495057;
            margin-bottom: 0.5rem;
            border-bottom: 1px solid #dee2e6;
            padding-bottom: 0.5rem;
        }
        </style>
        """
    
    def render(self, data: Dict[str, Any], title: str = "Raw JSON Response", 
               expandable: bool = True, download_filename: str = "response.json"):
        """Render the raw JSON view with optional expandable container."""
        # Apply custom CSS
        st.markdown(self.json_style, unsafe_allow_html=True)
        
        if expandable:
            with st.expander(f"🔍 {title}"):
                self._render_json_content(data, title, download_filename)
        else:
            st.subheader(f"🔍 {title}")
            self._render_json_content(data, title, download_filename)
    
    def _render_json_content(self, data: Dict[str, Any], title: str, download_filename: str):
        """Render the actual JSON content with controls."""
        # JSON display options
        col1, col2, col3 = st.columns([2, 1, 1])
        
        with col1:
            st.write(f"**{title}**")
        
        with col2:
            # Pretty print toggle
            pretty_print = st.checkbox("Pretty Print", value=True, key=f"pretty_{id(data)}")
        
        with col3:
            # Download button
            json_str = json.dumps(data, indent=2 if pretty_print else None)
            st.download_button(
                label="📥 Download",
                data=json_str,
                file_name=download_filename,
                mime="application/json",
                key=f"download_{id(data)}"
            )
        
        # Display JSON
        if pretty_print:
            st.json(data)
        else:
            # Display as code block for compact view
            json_str = json.dumps(data)
            st.code(json_str, language="json")
        
        # JSON statistics
        self._render_json_stats(data)
    
    def _render_json_stats(self, data: Dict[str, Any]):
        """Render statistics about the JSON data."""
        st.markdown("---")
        st.write("**JSON Statistics**")
        
        col1, col2, col3, col4 = st.columns(4)
        
        # Calculate statistics
        json_str = json.dumps(data)
        size_bytes = len(json_str.encode('utf-8'))
        
        # Count different data types
        stats = self._analyze_json_structure(data)
        
        with col1:
            st.metric("Size", f"{size_bytes:,} bytes")
        
        with col2:
            st.metric("Total Fields", stats['total_fields'])
        
        with col3:
            st.metric("Nested Objects", stats['nested_objects'])
        
        with col4:
            st.metric("Arrays", stats['arrays'])
    
    def _analyze_json_structure(self, data: Any, stats: Optional[Dict] = None) -> Dict[str, int]:
        """Recursively analyze JSON structure to gather statistics."""
        if stats is None:
            stats = {
                'total_fields': 0,
                'nested_objects': 0,
                'arrays': 0,
                'null_values': 0,
                'max_depth': 0
            }
        
        if isinstance(data, dict):
            stats['total_fields'] += len(data)
            if data:  # Non-empty dict
                stats['nested_objects'] += 1
            
            for value in data.values():
                self._analyze_json_structure(value, stats)
        
        elif isinstance(data, list):
            stats['arrays'] += 1
            for item in data:
                self._analyze_json_structure(item, stats)
        
        elif data is None:
            stats['null_values'] += 1
        
        return stats
    
    def render_compact(self, data: Dict[str, Any], max_lines: int = 10):
        """Render a compact view of JSON data with limited lines."""
        json_str = json.dumps(data, indent=2)
        lines = json_str.split('\n')
        
        if len(lines) <= max_lines:
            st.code(json_str, language="json")
        else:
            # Show first few lines with truncation indicator
            truncated_lines = lines[:max_lines]
            truncated_json = '\n'.join(truncated_lines)
            
            st.code(truncated_json + f"\n... ({len(lines) - max_lines} more lines)", language="json")
            
            # Option to expand
            if st.button("Show Full JSON", key=f"expand_{id(data)}"):
                st.code(json_str, language="json")
    
    def render_searchable(self, data: Dict[str, Any], title: str = "Searchable JSON"):
        """Render JSON with search functionality."""
        st.subheader(f"🔍 {title}")
        
        # Search input
        search_term = st.text_input("Search in JSON", placeholder="Enter search term...")
        
        if search_term:
            # Find matching paths
            matches = self._search_json(data, search_term.lower())
            
            if matches:
                st.success(f"Found {len(matches)} matches:")
                for path, value in matches:
                    st.write(f"**{path}:** {value}")
            else:
                st.warning("No matches found.")
        
        # Display full JSON
        st.json(data)
    
    def _search_json(self, data: Any, search_term: str, current_path: str = "") -> list:
        """Search for a term in JSON data and return matching paths."""
        matches = []
        
        if isinstance(data, dict):
            for key, value in data.items():
                new_path = f"{current_path}.{key}" if current_path else key
                
                # Check if key matches
                if search_term in key.lower():
                    matches.append((new_path, value))
                
                # Check if value matches (for string values)
                if isinstance(value, str) and search_term in value.lower():
                    matches.append((new_path, value))
                
                # Recursively search nested structures
                matches.extend(self._search_json(value, search_term, new_path))
        
        elif isinstance(data, list):
            for i, item in enumerate(data):
                new_path = f"{current_path}[{i}]"
                matches.extend(self._search_json(item, search_term, new_path))
        
        elif isinstance(data, str) and search_term in data.lower():
            matches.append((current_path, data))
        
        return matches
    
    def render_diff(self, data1: Dict[str, Any], data2: Dict[str, Any], 
                   title1: str = "Response 1", title2: str = "Response 2"):
        """Render a comparison view of two JSON responses."""
        st.subheader("🔄 JSON Comparison")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.write(f"**{title1}**")
            st.json(data1)
        
        with col2:
            st.write(f"**{title2}**")
            st.json(data2)
        
        # Basic comparison stats
        st.markdown("---")
        st.write("**Comparison Summary**")
        
        size1 = len(json.dumps(data1))
        size2 = len(json.dumps(data2))
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric(f"{title1} Size", f"{size1:,} bytes")
        
        with col2:
            st.metric(f"{title2} Size", f"{size2:,} bytes")
        
        with col3:
            diff = size2 - size1
            st.metric("Size Difference", f"{diff:+,} bytes") 