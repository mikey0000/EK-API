import json
from datetime import date
from pathlib import Path
from urllib.parse import parse_qs, urlsplit

import pytest

from electrickiwi_api import ElectricKiwiApi
from electrickiwi_api.model import Service

FIXTURE = Path(__file__).parent / "fixtures" / "consumption_insights.json"


class FakeResponse:
    def __init__(self, payload: dict, status: int = 200) -> None:
        self._payload = payload
        self.status = status

    async def json(self) -> dict:
        return self._payload


class FakeAuth:
    """Stands in for AbstractAuth, recording the request it receives."""

    def __init__(self, payload: dict) -> None:
        self._payload = payload
        self.method = None
        self.url = None
        self.kwargs = None

    async def request(self, method: str, url: str, **kwargs) -> FakeResponse:
        self.method = method
        self.url = url
        self.kwargs = kwargs
        return FakeResponse(self._payload)


@pytest.fixture(name="api")
def api_fixture() -> ElectricKiwiApi:
    api = ElectricKiwiApi(FakeAuth(json.loads(FIXTURE.read_text())))
    api.customer_number = 12345678
    api.electricity = Service.from_dict(
        {
            "service": "electricity",
            "identifier": "0000111122WA3AB",
            "is_primary_service": True,
            "service_status": "Y",
        }
    )
    return api


async def test_get_consumption_insights_builds_query(api: ElectricKiwiApi) -> None:
    insights = await api.get_consumption_insights(
        date(2026, 6, 16), date(2026, 7, 16)
    )

    assert api.auth.method == "get"
    split = urlsplit(api.auth.url)
    assert split.path == "/power/usage/v1/insights/12345678/0000111122WA3AB"
    assert parse_qs(split.query) == {
        "start_date": ["2026-06-16"],
        "end_date": ["2026-07-16"],
        "group_by": ["day"],
    }
    assert api.auth.kwargs == {}
    assert "2026-06-16" in insights.usage


async def test_get_consumption_insights_group_by_month(api: ElectricKiwiApi) -> None:
    await api.get_consumption_insights("2025-07-16", "2026-07-16", group_by="month")

    query = parse_qs(urlsplit(api.auth.url).query)
    assert query["group_by"] == ["month"]
    assert query["start_date"] == ["2025-07-16"]


async def test_get_consumption_averages_deprecated(api: ElectricKiwiApi) -> None:
    with pytest.deprecated_call():
        await api.get_consumption_averages("2026-06-16", "2026-07-16")

    query = parse_qs(urlsplit(api.auth.url).query)
    assert query["group_by"] == ["week"]
