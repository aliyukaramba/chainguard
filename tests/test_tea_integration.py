"""Unit tests for Tea Protocol integration."""
import pytest
from chainguard.tea_integration import TeaProtocolClient

def test_tea_client_init():
    """Test TeaProtocolClient initialization."""
    client = TeaProtocolClient()
    assert client.config is not None

def test_get_package_metadata():
    """Test fetching package metadata."""
    client = TeaProtocolClient()
    metadata = client.get_package_metadata("requests")
    assert "teaRank" in metadata
    assert "dependencies" in metadata