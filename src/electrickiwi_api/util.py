"""Helpers for working with Electric Kiwi usage intervals."""

from datetime import date, datetime, time, timedelta, timezone
from typing import Union
from zoneinfo import ZoneInfo

NZ_TZ = ZoneInfo("Pacific/Auckland")


def interval_start(
    day: Union[date, str], interval: int, tz: ZoneInfo = NZ_TZ
) -> datetime:
    """Return the UTC start of a half-hourly usage interval.

    Interval N covers the (N-1)th half hour of *elapsed* time after local
    midnight. Adding a timedelta to an aware local datetime would do
    wall-clock arithmetic and break on DST transition days (which have 46
    or 50 intervals), so convert midnight to UTC before adding.
    """
    if isinstance(day, str):
        day = date.fromisoformat(day)
    midnight_utc = datetime.combine(day, time.min, tzinfo=tz).astimezone(timezone.utc)
    return midnight_utc + timedelta(minutes=30 * (interval - 1))
