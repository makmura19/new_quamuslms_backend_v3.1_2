from datetime import datetime, timezone, date
from pytz import timezone as pytz_timezone, utc, UTC
from dateutil.parser import parse
from django.utils.timezone import is_naive


class DatetimeUtil:
    @staticmethod
    def to_utc(local_time, user_timezone="UTC"):
        """
        Mengonversi waktu lokal ke UTC.
        :param local_time: datetime objek atau string dalam format ISO 8601.
        :param user_timezone: Zona waktu lokal pengguna (default: "UTC").
        :return: datetime objek dalam UTC.
        """
        if isinstance(local_time, str):
            local_time = parse(
                local_time
            )  # Parse string ke datetime jika input adalah string

        if local_time.tzinfo is None:
            # Jika naive datetime, lokalisasi terlebih dahulu ke zona waktu pengguna
            user_tz = pytz_timezone(user_timezone)
            local_time = user_tz.localize(local_time)

        return local_time.astimezone(utc)

    @staticmethod
    def to_local(utc_time, user_timezone="Asia/Jakarta"):
        """
        Mengonversi waktu UTC ke zona waktu lokal pengguna.
        :param utc_time: datetime objek atau string dalam format ISO 8601.
        :param user_timezone: Zona waktu lokal pengguna (default: "Asia/Jakarta").
        :return: datetime objek dalam zona waktu lokal pengguna.
        """
        if isinstance(utc_time, str):
            utc_time = parse(
                utc_time
            )  # Parse string ke datetime jika input adalah string

        if utc_time.tzinfo is None:
            # Jika naive datetime, asumsikan sudah dalam UTC
            utc_time = utc_time.replace(tzinfo=timezone.utc)

        user_tz = pytz_timezone(user_timezone)
        return utc_time.astimezone(user_tz)

    @staticmethod
    def to_string(dt, format="%Y-%m-%dT%H:%M:%S%z"):
        """
        Mengonversi datetime objek ke string.
        :param dt: datetime objek.
        :param format: Format string untuk datetime (default: ISO 8601).
        :return: String representasi datetime.
        """
        if dt.tzinfo is None:
            raise ValueError(
                "Datetime harus memiliki informasi zona waktu (timezone-aware)."
            )
        return dt.strftime(format)

    @staticmethod
    def from_string(dt_str, format="%Y-%m-%dT%H:%M:%S%z"):
        """
        Mengonversi string ke datetime objek.
        :param dt_str: String representasi datetime.
        :param format: Format string untuk datetime (default: ISO 8601).
        :return: datetime objek.
        """
        try:
            return datetime.strptime(dt_str, format)
        except ValueError:
            # Gunakan dateutil.parser jika format tidak sesuai
            return parse(dt_str)

    @staticmethod
    def now_utc():
        """
        Mendapatkan waktu saat ini dalam UTC.
        :return: datetime objek dalam UTC.
        """
        return datetime.now(timezone.utc)

    @staticmethod
    def now_local(user_timezone="Asia/Jakarta"):
        """
        Mendapatkan waktu saat ini dalam zona waktu lokal pengguna.
        :param user_timezone: Zona waktu lokal pengguna (default: "Asia/Jakarta").
        :return: datetime objek dalam zona waktu lokal pengguna.
        """
        user_tz = pytz_timezone(user_timezone)
        return datetime.now(utc).astimezone(user_tz)

    @staticmethod
    def is_naive(dt):
        """
        Memeriksa apakah datetime objek naive (tidak memiliki informasi zona waktu).
        :param dt: datetime objek.
        :return: True jika naive, False jika timezone-aware.
        """
        return dt.tzinfo is None or dt.tzinfo.utcoffset(dt) is None

    @staticmethod
    def localize(dt, user_timezone="UTC"):
        """
        Melokalisasi naive datetime ke zona waktu tertentu.
        :param dt: datetime objek naive.
        :param user_timezone: Zona waktu untuk melokalisasi datetime (default: "UTC").
        :return: datetime objek dengan informasi zona waktu.
        """
        if not DatetimeUtil.is_naive(dt):
            raise ValueError(
                "Datetime sudah memiliki informasi zona waktu (timezone-aware)."
            )
        user_tz = pytz_timezone(user_timezone)
        return user_tz.localize(dt)

    @staticmethod
    def convert_dict_to_utc(data: dict, tz: str = "UTC", only_fields: list = None):
        """
        Mengonversi datetime pada dictionary `data` ke UTC berdasarkan zona waktu `tz`.
        - Jika `only_fields` diset, hanya field tersebut yang diproses.
        - Jika None, semua field dengan tipe datetime akan dikonversi.

        :param data: dict berisi data validasi
        :param tz: nama timezone (ex: 'Asia/Jakarta')
        :param only_fields: list nama field yang ingin dikonversi
        :return: dict baru dengan datetime dikonversi ke UTC
        """
        target_tz = pytz_timezone(tz)
        result = {}

        for k, v in data.items():
            should_convert = isinstance(v, datetime) and (
                only_fields is None or k in only_fields
            )

            if should_convert:
                if is_naive(v):
                    aware = target_tz.localize(v)
                else:
                    aware = v
                result[k] = aware.astimezone(UTC)
            else:
                result[k] = v

        return result

    @staticmethod
    def convert_local_datetimes_to_utc(
        data: dict, timezone_str="UTC", fields=[]
    ) -> dict:
        local_tz = pytz_timezone(timezone_str)

        def process(key_path, value):
            if isinstance(value, datetime) and key_path in fields:
                naive_dt = value.replace(tzinfo=None)
                local_date = local_tz.localize(naive_dt)
                return local_date.astimezone(UTC)
            elif isinstance(value, dict):
                return {
                    k: process(f"{key_path}.{k}" if key_path else k, v)
                    for k, v in value.items()
                }
            elif isinstance(value, list):
                return [process(key_path, item) for item in value]
            else:
                return value

        return process("", data)

    @staticmethod
    def count_age(value) -> int:
        if not value:
            return 0

        # Parse input ke datetime
        if isinstance(value, datetime):
            dob = value.date()
        elif isinstance(value, date):
            dob = value
        elif isinstance(value, str):
            try:
                dob = parse(value).date()
            except (ValueError, TypeError):
                return 0
        else:
            return 0

        today = date.today()
        age = today.year - dob.year

        # Koreksi jika belum ulang tahun tahun ini
        if (today.month, today.day) < (dob.month, dob.day):
            age -= 1

        return age
