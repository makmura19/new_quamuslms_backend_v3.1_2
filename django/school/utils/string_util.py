import random
import string
from datetime import datetime, date
from dateutil import parser


class StringUtil:

    @staticmethod
    def generate_code(pattern_str, exclude_char=None, exclude_numeric=None):
        if exclude_char is None:
            exclude_char = ""
        if exclude_numeric is None:
            exclude_numeric = ""

        characters = "".join(c for c in string.ascii_letters if c not in exclude_char)
        numerics = "".join(n for n in string.digits if n not in exclude_numeric)

        if not characters or not numerics:
            raise ValueError("Character or numeric pool is empty after exclusions.")

        result = []
        for idx, char in enumerate(pattern_str):
            if char == "c":
                result.append(random.choice(characters))
            elif char == "n":
                if idx == 0:
                    # angka pertama tidak boleh 0
                    numerics_no_zero = numerics.replace("0", "")
                    if not numerics_no_zero:
                        raise ValueError(
                            "No non-zero digit available for first numeric."
                        )
                    result.append(random.choice(numerics_no_zero))
                else:
                    result.append(random.choice(numerics))
            else:
                raise ValueError(
                    "Invalid pattern character. Use 'c' for character and 'n' for numeric."
                )

        return "".join(result)

    @staticmethod
    def get_initial(name):
        if not name:
            return ""
        parts = name.strip().split()
        initials = "".join([p[0] for p in parts if p])
        return initials.lower()

    @staticmethod
    def mask(number: str, pattern: str):
        """
        Usage
        mask(donor_no, "###-##-##")
        """
        number = str(number)
        result = []
        idx = 0

        for ch in pattern:
            if ch == "#":
                if idx < len(number):
                    result.append(number[idx])
                    idx += 1
                else:
                    result.append("")
            else:
                result.append(ch)

        return "".join(result)

    @staticmethod
    def format_date(value, output_format: str = "%d-%m-%Y") -> str:
        if not value:
            return ""

        if isinstance(value, (datetime, date)):
            dt = value
        else:
            try:
                dt = parser.parse(str(value))
            except (ValueError, TypeError):
                return ""

        return dt.strftime(output_format)

    @staticmethod
    def format_date_long(dt):
        bulan_map = {
            1: "Januari",
            2: "Februari",
            3: "Maret",
            4: "April",
            5: "Mei",
            6: "Juni",
            7: "Juli",
            8: "Agustus",
            9: "September",
            10: "Oktober",
            11: "November",
            12: "Desember",
        }
        if isinstance(dt, str):
            try:
                dt = parser.parse(dt)
            except (ValueError, TypeError):
                return ""

        if isinstance(dt, date) and not isinstance(dt, datetime):
            dt = datetime(dt.year, dt.month, dt.day)
        return f"{dt.day} {bulan_map[dt.month]} {dt.year}"

    @staticmethod
    def format_time(dt):
        if isinstance(dt, str):
            try:
                dt = parser.parse(dt)
            except (ValueError, TypeError):
                return ""

        if isinstance(dt, date) and not isinstance(dt, datetime):
            dt = datetime(dt.year, dt.month, dt.day)
        return dt.strftime("%H:%M")

    @staticmethod
    def format_address(address):
        output = f"{address.get('street')} Ds. {address.get('village')} Kec. {address.get('district')} {address.get('city')}, {address.get('province')} {address.get('zipcode')}"
        return output
