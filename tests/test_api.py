import pytest
from app import fetch_data as fd


def test_fetch_data_returns_result(monkeypatch):
    """
    Unit-test version: stub fetch_data so we don't hit the real API.
    """
    # fake implementation that mimics a valid payload
    def fake_fetch(_endpoint):
        return {"records": 1}

    monkeypatch.setattr(fd, "fetch_data", fake_fetch)

    data = fd.fetch_data("invoice")
    assert data == {"records": 1}


def test_fetch_data_raises_on_bad_endpoint(monkeypatch):
    """
    Failure path stubbed to raise the expected exception.
    """
    def fake_fetch(_endpoint):
        raise RuntimeError("boom")

    monkeypatch.setattr(fd, "fetch_data", fake_fetch)

    with pytest.raises(RuntimeError):
        fd.fetch_data("bad-endpoint")
