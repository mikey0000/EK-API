from datetime import date, datetime, timezone

from electrickiwi_api.util import NZ_TZ, interval_start


def test_interval_one_is_local_midnight() -> None:
    start = interval_start("2026-06-16", 1)
    assert start.tzinfo == timezone.utc
    local = start.astimezone(NZ_TZ)
    assert (local.hour, local.minute) == (0, 0)


def test_interval_matches_time_label() -> None:
    # interval 9 carries the label "4:00 AM" in API responses
    local = interval_start(date(2026, 6, 16), 9).astimezone(NZ_TZ)
    assert (local.hour, local.minute) == (4, 0)


def test_spring_forward_day_has_46_intervals() -> None:
    # NZ clocks skip 2:00-3:00 AM on 2025-09-28; the day is 23 hours long
    day = date(2025, 9, 28)
    next_midnight = interval_start(day, 46) + (
        interval_start(day, 2) - interval_start(day, 1)
    )
    assert next_midnight == interval_start(date(2025, 9, 29), 1)
    local = interval_start(day, 5).astimezone(NZ_TZ)
    # the 5th half hour of elapsed time lands at 3:00 AM NZDT, not 2:00 AM
    assert (local.hour, local.minute) == (3, 0)


def test_fall_back_day_has_50_intervals() -> None:
    # NZ clocks repeat 2:00-3:00 AM on 2026-04-05; the day is 25 hours long
    day = date(2026, 4, 5)
    next_midnight = interval_start(day, 50) + (
        interval_start(day, 2) - interval_start(day, 1)
    )
    assert next_midnight == interval_start(date(2026, 4, 6), 1)


def test_intervals_are_half_hour_aligned_utc() -> None:
    for n in (1, 2, 47, 48):
        start = interval_start("2026-07-15", n)
        assert start.minute in (0, 30)
        assert start.second == 0
