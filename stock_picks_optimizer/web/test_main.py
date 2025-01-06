from fastapi.testclient import TestClient
from stock_picks_optimizer.web.main import app

client = TestClient(app)


def test_index_when_stock_groups_available_should_return_stock_groups():
    response = client.get("/")
    assert response.status_code == 200
