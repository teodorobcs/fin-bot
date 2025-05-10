"""
Unit-tests for app.chat.tools using pytest + unittest.mock.patch.
Each test stubs out requests.get so we don’t hit the real NetSuite API.
"""

from unittest.mock import patch
from requests.exceptions import RequestException
from app.chat import tools


# ───────────────────────── get_invoices ────────────────────────── #

@patch("app.chat.tools.requests.get")
def test_get_invoices_success(mock_get):
    mock_resp = mock_get.return_value
    mock_resp.status_code = 200
    mock_resp.json.return_value = [
        {"status": "Open", "amountRemaining": 1000.0}
    ]

    data = tools.get_invoices(status="Open")

    assert isinstance(data, list)
    assert data[0]["status"] == "Open"


@patch("app.chat.tools.requests.get")
def test_get_invoices_empty(mock_get):
    mock_resp = mock_get.return_value
    mock_resp.status_code = 200
    mock_resp.json.return_value = []

    data = tools.get_invoices()
    assert data == []


@patch("app.chat.tools.requests.get")
def test_get_invoices_failure(mock_get):
    mock_get.side_effect = RequestException("connection error")

    result = tools.get_invoices(status="Open")

    assert "error" in result
    assert result["status_code"] is None


# ───────────────────────── get_ar_balance ──────────────────────── #

@patch("app.chat.tools.requests.get")
def test_get_ar_balance_success(mock_get):
    mock_resp = mock_get.return_value
    mock_resp.status_code = 200
    mock_resp.json.return_value = {"subsidiary_totals": 5}

    data = tools.get_ar_balance(group_by="subsidiary")

    assert isinstance(data, dict)
    assert "subsidiary_totals" in data


@patch("app.chat.tools.requests.get")
def test_get_ar_balance_failure(mock_get):
    mock_get.side_effect = RequestException("API down")

    data = tools.get_ar_balance(group_by="customer")

    assert "error" in data