from rest_framework import serializers
from enum import Enum
import os
import mimetypes
import re


class PhoneNumberField(serializers.CharField):
    def to_internal_value(self, data):
        if not isinstance(data, str):
            raise serializers.ValidationError("Nomor telepon harus berupa string.")

        if re.match(r"^08\d{8,12}$", data):
            return "62" + data[1:]
        elif re.match(r"^628\d{8,12}$", data):
            return data
        else:
            raise serializers.ValidationError("Format nomor telepon tidak valid.")

    def to_representation(self, value):
        return value


class CharField(serializers.CharField):
    def __init__(
        self,
        required=True,
        allow_blank=False,
        allow_null=False,
        blank_to_null=False,
        **kwargs,
    ):
        self.allow_null = allow_null
        self.blank_to_null = blank_to_null

        super().__init__(required=required, allow_blank=allow_blank, **kwargs)

    def to_internal_value(self, data):
        if data is None:
            if self.allow_null:
                return None
            raise serializers.ValidationError("Field ini tidak boleh bernilai null.")

        if isinstance(data, str) and data.strip() == "":
            if self.blank_to_null:
                return None
            if not self.allow_blank:
                raise serializers.ValidationError("Field ini tidak boleh kosong.")
            return ""

        return super().to_internal_value(data)


class DateTimeField(serializers.DateTimeField):
    def __init__(
        self,
        required=True,
        allow_null=False,
        blank_to_null=True,
        input_formats=None,
        **kwargs,
    ):
        self.blank_to_null = blank_to_null
        if input_formats is None:
            input_formats = ["%Y-%m-%d", "%Y-%m-%dT%H:%M:%SZ"]
        super().__init__(
            required=required,
            allow_null=allow_null,
            input_formats=input_formats,
            **kwargs,
        )

    def to_internal_value(self, value):
        if isinstance(value, dict) and getattr(self, "field_name", None):
            value = value.get(self.field_name, value)

        if value is None:
            if self.allow_null:
                return None
            raise serializers.ValidationError("Field ini tidak boleh bernilai null.")

        if isinstance(value, str) and value.strip() == "":
            if self.blank_to_null:
                if self.allow_null:
                    return None

                raise serializers.ValidationError(
                    "Field ini tidak boleh bernilai null."
                )

            raise serializers.ValidationError(
                "Format tanggal/waktu tidak valid atau kosong."
            )

        return super().to_internal_value(value)


class FileField(serializers.FileField):
    def __init__(self, required=True, allowed_types=None, max_size_mb=None, **kwargs):
        self.allowed_types = allowed_types or []
        self.max_size_mb = max_size_mb
        super().__init__(required=required, **kwargs)

    def to_internal_value(self, data):
        file = super().to_internal_value(data)

        # Ambil ekstensi & MIME type
        ext = os.path.splitext(file.name)[1].lower()
        mime_type, _ = mimetypes.guess_type(file.name)

        # 1. Validasi ekstensi
        if self.allowed_types:
            allowed_exts = [
                e.value if isinstance(e, Enum) else str(e) for e in self.allowed_types
            ]
            if ext not in allowed_exts:
                raise serializers.ValidationError(
                    f"Tipe file '{ext}' tidak diizinkan. "
                    f"Hanya boleh: {', '.join(allowed_exts)}"
                )

        if mime_type is None and self.allowed_types:
            raise serializers.ValidationError(
                "Tidak dapat menentukan MIME type file. Pastikan file valid."
            )

        if self.max_size_mb is not None:
            max_bytes = self.max_size_mb * 1024 * 1024
            if file.size > max_bytes:
                raise serializers.ValidationError(
                    f"Ukuran file maksimal {self.max_size_mb}MB. "
                    f"File yang diunggah {file.size / (1024*1024):.2f}MB."
                )

        return file


class FILETYPE(str, Enum):
    # Dokumen
    PDF = ".pdf"
    DOC = ".doc"
    DOCX = ".docx"
    XLS = ".xls"
    XLSX = ".xlsx"
    PPT = ".ppt"
    PPTX = ".pptx"
    TXT = ".txt"
    CSV = ".csv"

    # Gambar
    JPG = ".jpg"
    JPEG = ".jpeg"
    PNG = ".png"
    GIF = ".gif"
    BMP = ".bmp"
    WEBP = ".webp"
    SVG = ".svg"

    # Audio
    MP3 = ".mp3"
    WAV = ".wav"
    OGG = ".ogg"
    M4A = ".m4a"

    # Video
    MP4 = ".mp4"
    AVI = ".avi"
    MKV = ".mkv"
    MOV = ".mov"

    # Arsip
    ZIP = ".zip"
    RAR = ".rar"
    TAR = ".tar"
    GZ = ".gz"


# ==== FILETYPEGROUP ====
class FILETYPEGROUP:
    IMAGE = [
        FILETYPE.JPG,
        FILETYPE.JPEG,
        FILETYPE.PNG,
        FILETYPE.GIF,
        FILETYPE.BMP,
        FILETYPE.WEBP,
        FILETYPE.SVG,
    ]

    DOCUMENT = [
        FILETYPE.PDF,
        FILETYPE.DOC,
        FILETYPE.DOCX,
        FILETYPE.XLS,
        FILETYPE.XLSX,
        FILETYPE.PPT,
        FILETYPE.PPTX,
        FILETYPE.TXT,
        FILETYPE.CSV,
    ]

    AUDIO = [FILETYPE.MP3, FILETYPE.WAV, FILETYPE.OGG, FILETYPE.M4A]

    VIDEO = [FILETYPE.MP4, FILETYPE.AVI, FILETYPE.MKV, FILETYPE.MOV]

    ARCHIVE = [FILETYPE.ZIP, FILETYPE.RAR, FILETYPE.TAR, FILETYPE.GZ]


# ==== CONTOH PENGGUNAAN DI SERIALIZER ====
"""
class MySerializer(serializers.Serializer):
    file = CustomFileField(
        required=True,
        allowed_types=[FILETYPE.PDF, *FILETYPEGROUP.IMAGE],
        max_size_mb=15,
    )
"""
