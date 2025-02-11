"""httpx предоставляет асинхронного клиента для тестов"""
from datetime import datetime
from httpx import AsyncClient
import pytest

@pytest.mark.asyncio(scope="session")
async def test_get_reports(auth_ac: AsyncClient):
    response = await auth_ac.get("/reports/", params={'date_from': datetime.strptime('2025-01-30', '%Y-%m-%d'),
                                                      'date_to': datetime.strptime('2025-02-28', '%Y-%m-%d')})
    assert response.status_code == 200
    assert response.json() == {"count_done_status": 2,
                               "count_pending_status": 2,
                               "count_in progress_status": 1,
                               "count_skip_status": 1}

