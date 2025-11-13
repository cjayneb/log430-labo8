"""
Tests for store manager, choreographed saga
SPDX - License - Identifier: LGPL - 3.0 - or -later
Auteurs : Gabriel C. Ullmann, Fabio Petrillo, 2025
"""

import json
from logger import Logger
import pytest
from store_manager import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_health(client):
    result = client.get('/health-check')
    assert result.status_code == 200
    assert result.get_json() == {'status':'ok'}

def test_saga(client):
    """Smoke test for complete saga"""
    logger = Logger.get_instance("test")
    
    # 1. Run order saga
    product_data = {
        "user_id": 1,
        "items": [{"product_id": 2, "quantity": 1}, {"product_id": 3, "quantity": 2}]
    }
    response = client.post('/orders',
                          data=json.dumps(product_data),
                          content_type='application/json')
    
    assert response.status_code == 201, f"Failed to create order: {response.get_json()}"
    order_id = response.get_json()['order_id']
    assert order_id > 0
    logger.debug(f"Created order with ID: {order_id}")
    
    # 2. Check if order really exists and whether it has a payment link
    response = client.get(f'/orders/{order_id}')
    assert response.status_code == 201, f"Failed to get order: {response.get_json()}"
    response = response.get_json()
    logger.debug(response)
    assert response["items"] is not None
    assert int(response["user_id"]) > 0
    assert float(response["total_amount"]) > 0
    assert "http" in response["payment_link"]
    logger.debug(f"Order data is correct")
    
    # NOTE: si nous le voulions, nous pourrions également écrire des tests pour vérifier si l'enregistrement Outbox a été créé