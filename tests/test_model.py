import json
from pathlib import Path

import pytest

from electrickiwi_api.model import ConsumptionAverage, ConsumptionInsights

FIXTURE = Path(__file__).parent / "fixtures" / "consumption_insights.json"


@pytest.fixture(name="insights")
def insights_fixture() -> ConsumptionInsights:
    return ConsumptionInsights.from_dict(json.loads(FIXTURE.read_text()))


def test_parses_response_envelope(insights: ConsumptionInsights) -> None:
    assert insights.type == "consumption_averages"
    assert insights.range.group_by == "day"
    assert list(insights.usage) == ["2026-06-16", "2026-06-17", "2026-06-18"]
    assert insights.group_breakdown == ["2026-06-16", "2026-06-17", "2026-06-18"]


def test_parses_daily_usage(insights: ConsumptionInsights) -> None:
    day = insights.usage["2026-06-16"]
    assert day.date == "2026-06-16"
    assert day.status == "B"
    assert day.type == "A"
    assert day.usage_type == "tou_plus"
    assert day.solar_feed_in_tariffs is True
    assert day.consumption > 0
    assert day.total_charges_incl_gst > 0
    assert day.fixed_charges_incl_gst > 0
    assert insights.usage["2026-06-17"].status == "U"


def test_parses_intervals(insights: ConsumptionInsights) -> None:
    day = insights.usage["2026-06-16"]
    assert list(day.intervals) == list(range(1, 49))
    first = day.intervals[1]
    assert first.time == "12:00 AM"
    assert first.consumption == 0.0
    assert first.consumption_rate == 0.3312
    assert first.hop_best is False
    assert first.hop_interval is False
    assert sum(interval.consumption for interval in day.intervals.values()) == (
        pytest.approx(day.consumption, abs=0.5)
    )


def test_parses_feed_in_tariffs(insights: ConsumptionInsights) -> None:
    day = insights.usage["2026-06-16"]
    assert day.feed_in_tariffs is not None
    assert day.feed_in_tariffs.usage_type == "solar_tou_plus"
    assert list(day.feed_in_tariffs.intervals) == list(range(1, 49))
    first = day.feed_in_tariffs.intervals[1]
    assert first.generation == 0.01
    assert first.generation_rate == 0.115


def test_tolerates_missing_intervals() -> None:
    """Month-grouped responses may carry totals without interval data."""
    insights = ConsumptionInsights.from_dict(
        {
            "data": {
                "type": "consumption_averages",
                "range": {
                    "start_date": "2025-07-01",
                    "end_date": "2026-07-01",
                    "group_by": "month",
                },
                "group_breakdown": ["2025-07-01"],
                "usage": {
                    "2025-07-01": {
                        "consumption": "512.34",
                        "total_charges_incl_gst": "150.00",
                        "status": "B",
                    }
                },
            },
            "status": 1,
        }
    )
    month = insights.usage["2025-07-01"]
    assert month.consumption == 512.34
    assert month.intervals == {}
    assert month.feed_in_tariffs is None


def test_consumption_average_alias() -> None:
    assert ConsumptionAverage is ConsumptionInsights
