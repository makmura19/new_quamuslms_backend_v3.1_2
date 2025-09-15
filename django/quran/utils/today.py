from datetime import datetime, timedelta, timezone
from dateutil.relativedelta import relativedelta


def today(days=0, months=0):
    date = (
        datetime.now(timezone.utc)
        + timedelta(hours=7)
        + relativedelta(months=months, days=days)
    )
    date = date.strftime("%Y-%m-%d")
    date = datetime.strptime(date, "%Y-%m-%d")
    return date


def today_str(days=0, months=0):
    date = (
        datetime.now(timezone.utc)
        + timedelta(hours=7)
        + relativedelta(months=months, days=days)
    )
    date = date.strftime("%Y-%m-%d")
    return date


def today_date_format(days=0, months=0):
    date = (
        datetime.now(timezone.utc)
        + timedelta(hours=7)
        + relativedelta(months=months, days=days)
    )
    return date


def timestamp_int(date_value):
    if isinstance(date_value, str):
        date_obj = datetime.fromisoformat(date_value.replace("Z", "+00:00"))
        timestamp_ms = int(date_obj.timestamp() * 1000)
    else:
        timestamp_ms = date_value
    return timestamp_ms


def timestamp_to_date(timestamp):
    timestamp = timestamp_int(timestamp)
    second = timestamp / 1000
    return datetime.fromtimestamp(second, timezone.utc)


def timestamp_to_str_date(timestamp, format="%Y-%m-%d"):
    second = timestamp / 1000
    date = datetime.fromtimestamp(second, timezone.utc)
    date = date.strftime(format)
    return date


def days_name():
    day = datetime.now(timezone.utc) + timedelta(hours=7)
    day = day.strftime("%A")
    return indonesian_days.get(day)


def date_str():
    date = datetime.now(timezone.utc) + timedelta(hours=7)
    return date.strftime("%d-%m-%Y")


def time_str():
    date = datetime.now(timezone.utc) + timedelta(hours=7)
    return date.strftime("%H:%M")


def merge_date_time(date, time):
    datetime_obj = datetime.combine(date, time)
    return datetime_obj


def human_readable_time(seconds):
    if seconds < 60:
        return f"{seconds:.0f} detik"
    elif seconds < 3600:
        minutes = seconds // 60
        remaining_seconds = seconds % 60
        if remaining_seconds > 0:
            return f"{int(minutes)} menit {int(remaining_seconds)} detik"
        else:
            return f"{int(minutes)} menit"
    elif seconds < 86400:
        hours = seconds // 3600
        remaining_minutes = (seconds % 3600) // 60
        if remaining_minutes > 0:
            return f"{int(hours)} jam {int(remaining_minutes)} menit"
        else:
            return f"{int(hours)} jam"
    else:
        days = seconds // 86400
        remaining_hours = (seconds % 86400) // 3600
        if remaining_hours > 0:
            return f"{int(days)} hari {int(remaining_hours)} jam"
        else:
            return f"{int(days)} hari"


def normalize_date(date_str):
    formats = [
        "%Y-%m-%d",  # Format 2023-3-4
        "%d/%m/%Y",  # Format 28/12/2023
        "%d/%m/%y",  # Format 15/12/23
        "%y-%m-%d",  # Format 23-12-5
        "%y/%m/%d",  # Format 23/10/28
    ]

    for fmt in formats:
        try:
            date = datetime.strptime(date_str, fmt)
            # Return normalized date in YYYY-MM-DD format
            return date.strftime("%Y-%m-%d")
        except ValueError:
            continue

    # If none of the formats matched, return None
    return None


indonesian_months = [
    "Januari",
    "Februari",
    "Maret",
    "April",
    "Mei",
    "Juni",
    "Juli",
    "Agustus",
    "September",
    "Oktober",
    "November",
    "Desember",
]

indonesian_days = {
    "Monday": "Senin",
    "Tuesday": "Selasa",
    "Wednesday": "Rabu",
    "Thursday": "Kamis",
    "Friday": "Jumat",
    "Saturday": "Sabtu",
    "Sunday": "Minggu",
}
