"""
Abstract base class defining the standard ERPClient interface.

All ERP integrations (e.g., NetSuite, SAP, QuickBooks) must inherit from this class
and implement the required sync methods to ensure a consistent data pipeline.
"""

from abc import ABC, abstractmethod

class ERPClient(ABC):
    """
    Base interface for ERP integrations.
    All methods must be implemented by subclasses to define how each data type is synced.
    """

    @abstractmethod
    def sync_account(self):
        """Sync chart of accounts or general ledger data from the ERP."""
        pass

    @abstractmethod
    def sync_customers(self):
        """Sync customer records from the ERP."""
        pass

    @abstractmethod
    def sync_employees(self):
        """Sync employee data from the ERP."""
        pass

    @abstractmethod
    def sync_invoices(self):
        """Sync invoice transactions from the ERP."""
        pass

    @abstractmethod
    def sync_subsidiaries(self):
        """Sync subsidiary or business unit structure from the ERP."""
        pass

    @abstractmethod
    def sync_vendor(self):
        """Sync vendor or supplier records from the ERP."""
        pass

    @abstractmethod
    def sync_all(self):
        """Run a full sync of all supported data types from the ERP."""
        pass