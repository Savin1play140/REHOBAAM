from datetime import date, datetime
from zoneinfo import ZoneInfo

def date_now():
    """
    Get actually date
    """
    return date.today()

def time_now():
    """
    Get actually time
    """
    return datetime.now().time().strftime("%H:%M:%S")

def time_in_zone(tz: str) -> str:
    """Время в указанной временной зоне, например 'Europe/Moscow'"""
    return datetime.now(ZoneInfo(tz)).strftime("%H:%M:%S")

def days_until(target: date) -> int:
    """Сколько дней до даты"""
    return (target - date.today()).days

def date_add(days: int = 0, weeks: int = 0, months: int = 0) -> date:
    """Дата через N дней/недель/месяцев"""
    from dateutil.relativedelta import relativedelta
    return date.today() + relativedelta(days=days, weeks=weeks, months=months)

def is_weekend() -> bool:
    return date.today().weekday() >= 5

def is_leap_year(year: int | None = None) -> bool:
    import calendar
    return calendar.isleap(year or date.today().year)

def parse_date(s: str, fmt: str = "%d.%m.%Y") -> date:
    return datetime.strptime(s, fmt).date()

def parse_date_auto(s: str) -> date:
    """Автоматический парсинг ('2025-06-27', '27.06.2025' и т.д.)"""
    from dateutil.parser import parse
    return parse(s).date()

def timestamp_now() -> float:
    return datetime.now().timestamp()

def from_timestamp(ts: float) -> datetime:
    return datetime.fromtimestamp(ts)
