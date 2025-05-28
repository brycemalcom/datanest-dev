"""
Role-based dashboard views for different user types.
"""

from .lender_view import LenderView
from .investor_view import InvestorView
from .asset_manager_view import AssetManagerView

__all__ = ['LenderView', 'InvestorView', 'AssetManagerView'] 