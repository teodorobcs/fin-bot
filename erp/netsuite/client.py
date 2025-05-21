"""
NetSuiteClient implements the ERPClient interface for NetSuite.

Each method wraps around the NetSuite-specific sync logic for its respective data type.
This client is used by the system to trigger syncs without knowing the ERP-specific implementation.
"""

from erp.base import ERPClient
from sync.sync_all import (
    sync_all,
    sync_vendor,
    sync_invoices,
    sync_employees,
    sync_subsidiaries,
    sync_account,
    sync_customer,
)

class NetSuiteClient(ERPClient):
    """
    Adapter for NetSuite ERP system.
    Provides concrete implementations of the ERPClient sync interface using NetSuite-specific logic.
    """

    def sync_account(self):
        """
        Trigger NetSuite sync for chart of accounts or GL data.
        """
        return sync_account()

    def sync_customers(self):
        """
        Trigger NetSuite sync for customer records.
        """
        return sync_customer()

    def sync_employees(self):
        """
        Trigger NetSuite sync for employee records.
        """
        return sync_employees()

    def sync_invoices(self):
        """
        Trigger NetSuite sync for invoice transactions.
        """
        return sync_invoices()

    def sync_subsidiaries(self):
        """
        Trigger NetSuite sync for subsidiaries or business units.
        """
        return sync_subsidiaries()

    def sync_vendor(self):
        """
        Trigger NetSuite sync for vendor or supplier records.
        """
        return sync_vendor()

    def sync_all(self):
        """
        Trigger a full NetSuite data sync for all available data points.
        """
        return sync_all()