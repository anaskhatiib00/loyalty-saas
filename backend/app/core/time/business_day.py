from dataclasses import dataclass
from datetime import datetime, time, timedelta, timezone
from zoneinfo import ZoneInfo


@dataclass(frozen=True, slots=True)
class BusinessDayRange:
    """
    UTC boundaries representing one local business calendar day.

    The range is half-open:

        start_at_utc <= timestamp < end_at_utc

    This prevents overlap between consecutive business days.
    """

    start_at_utc: datetime
    end_at_utc: datetime
    local_date: str
    timezone_name: str


def resolve_business_day_range(
    *,
    timezone_name: str,
    now_utc: datetime | None = None,
) -> BusinessDayRange:
    """
    Resolve the current local business day and return its UTC boundaries.

    Scans and activities remain stored in UTC. The business timezone is used
    only to determine which local calendar day each timestamp belongs to.
    """
    business_timezone = ZoneInfo(timezone_name)

    effective_now_utc = now_utc or datetime.now(timezone.utc)

    if effective_now_utc.tzinfo is None:
        raise ValueError("now_utc must be timezone-aware")

    effective_now_utc = effective_now_utc.astimezone(timezone.utc)
    local_now = effective_now_utc.astimezone(business_timezone)

    local_start = datetime.combine(
        local_now.date(),
        time.min,
        tzinfo=business_timezone,
    )

    local_end = datetime.combine(
       local_now.date() + timedelta(days=1),
       time.min,
       tzinfo=business_timezone,
    )

    return BusinessDayRange(
        start_at_utc=local_start.astimezone(timezone.utc),
        end_at_utc=local_end.astimezone(timezone.utc),
        local_date=local_now.date().isoformat(),
        timezone_name=timezone_name,
    )