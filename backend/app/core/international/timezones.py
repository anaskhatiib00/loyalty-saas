from functools import lru_cache
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError


def normalize_timezone_name(timezone_name: str) -> str:
    return timezone_name.strip()


@lru_cache(maxsize=512)
def is_valid_timezone(timezone_name: str) -> bool:
    normalized_timezone_name = normalize_timezone_name(timezone_name)

    if not normalized_timezone_name:
        return False

    try:
        ZoneInfo(normalized_timezone_name)
    except ZoneInfoNotFoundError:
        return False

    return True