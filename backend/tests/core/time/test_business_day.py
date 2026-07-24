from datetime import datetime, timezone

import pytest

from app.core.time import resolve_business_day_range


def test_scan_immediately_before_local_midnight_uses_previous_day() -> None:
    result = resolve_business_day_range(
        timezone_name="Asia/Amman",
        now_utc=datetime(
            2026,
            7,
            23,
            20,
            59,
            59,
            tzinfo=timezone.utc,
        ),
    )

    assert result.local_date == "2026-07-23"
    assert result.start_at_utc == datetime(
        2026,
        7,
        22,
        21,
        0,
        0,
        tzinfo=timezone.utc,
    )
    assert result.end_at_utc == datetime(
        2026,
        7,
        23,
        21,
        0,
        0,
        tzinfo=timezone.utc,
    )


def test_scan_exactly_at_local_midnight_uses_new_day() -> None:
    result = resolve_business_day_range(
        timezone_name="Asia/Amman",
        now_utc=datetime(
            2026,
            7,
            23,
            21,
            0,
            0,
            tzinfo=timezone.utc,
        ),
    )

    assert result.local_date == "2026-07-24"
    assert result.start_at_utc == datetime(
        2026,
        7,
        23,
        21,
        0,
        0,
        tzinfo=timezone.utc,
    )
    assert result.end_at_utc == datetime(
        2026,
        7,
        24,
        21,
        0,
        0,
        tzinfo=timezone.utc,
    )


def test_scan_immediately_after_local_midnight_uses_new_day() -> None:
    result = resolve_business_day_range(
        timezone_name="Asia/Amman",
        now_utc=datetime(
            2026,
            7,
            23,
            21,
            0,
            1,
            tzinfo=timezone.utc,
        ),
    )

    assert result.local_date == "2026-07-24"


def test_dst_spring_forward_day_has_23_utc_hours() -> None:
    result = resolve_business_day_range(
        timezone_name="America/New_York",
        now_utc=datetime(
            2026,
            3,
            8,
            16,
            0,
            0,
            tzinfo=timezone.utc,
        ),
    )

    assert result.local_date == "2026-03-08"
    assert (
        result.end_at_utc - result.start_at_utc
    ).total_seconds() == 23 * 60 * 60


def test_dst_fall_back_day_has_25_utc_hours() -> None:
    result = resolve_business_day_range(
        timezone_name="America/New_York",
        now_utc=datetime(
            2026,
            11,
            1,
            17,
            0,
            0,
            tzinfo=timezone.utc,
        ),
    )

    assert result.local_date == "2026-11-01"
    assert (
        result.end_at_utc - result.start_at_utc
    ).total_seconds() == 25 * 60 * 60


def test_naive_datetime_is_rejected() -> None:
    with pytest.raises(
        ValueError,
        match="now_utc must be timezone-aware",
    ):
        resolve_business_day_range(
            timezone_name="Asia/Amman",
            now_utc=datetime(2026, 7, 24, 0, 0, 0),
        )