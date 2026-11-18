import pytest
import requests


@pytest.mark.api
def test_demo_application_is_served(app_base_url):
    response = requests.get(app_base_url, timeout=5)
    assert response.status_code == 200
    assert "SocioLedger Demo ERP" in response.text
