import os
import math
import uuid
import logging
import requests
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.utils.text import get_valid_filename
from django.core.files.uploadedfile import (
    UploadedFile,
    InMemoryUploadedFile,
    TemporaryUploadedFile,
)
from typing import Dict, List, Union

logger = logging.getLogger(__name__)


class FileStorageUtil:

    AWS_BUCKET_URL = "https://quamus-lms-s3.s3.ap-southeast-3.amazonaws.com/"
    MAX_FILE_SIZE = 50 * 1024 * 1024
    ALLOWED_EXTENSIONS = [
        ".jpg",
        ".jpeg",
        ".png",
        ".webp",
        ".pdf",
        ".doc",
        ".docx",
        ".xls",
        ".xlsx",
        ".txt",
    ]

    # @staticmethod
    # def upload_aws(
    #     files,
    #     folder: str,
    # ) -> List[str]:
    #     """
    #     Mengunggah file ke AWS S3.

    #     Args:
    #         - files (Union[List[InMemoryUploadedFile], Dict[str, InMemoryUploadedFile]]): List atau Dict berisi file yang akan diunggah.
    #         - folder (str): Nama folder tempat file akan disimpan.

    #     Returns:
    #         - List[str]: List URL file yang berhasil diunggah.

    #     **Contoh Penggunaan:**
    #     ```python
    #     files = {"file1": uploaded_file_1, "file2": uploaded_file_2}
    #     result = FileStorageUtil.upload_aws(files, "uploads")
    #     # Output (contoh): ["https://s3.amazonaws.com/your-bucket/uploads/abc123.jpg"]
    #     ```
    #     """
    #     print("files", files.values())
    #     if not files:
    #         return []

    #     if isinstance(files, dict):
    #         files = list(files.values())

    #     if not all(isinstance(file, InMemoryUploadedFile) for file in files):
    #         logger.error(
    #             "ERROR: Semua file yang diunggah harus berupa `InMemoryUploadedFile`."
    #         )
    #         return []

    #     urls = []
    #     for file in files:
    #         if file.size > FileStorageUtil.MAX_FILE_SIZE:
    #             logger.warning(f"File {file.name} terlalu besar dan diabaikan.")
    #             continue

    #         _id = str(uuid.uuid4())
    #         ext = os.path.splitext(get_valid_filename(file.name))[1].lower()
    #         url_file = f"{folder}/{_id}{ext}"
    #         url = f"{FileStorageUtil.AWS_BUCKET_URL}{url_file}"

    #         try:
    #             default_storage.save(url_file, file)
    #             urls.append(url)
    #         except Exception as e:
    #             logger.error(f"Gagal mengunggah {file.name}: {e}")

    #     return urls

    # @staticmethod
    # def upload_aws(
    #     files,
    #     folder: str,
    # ) -> List[str]:
    #     if not files:
    #         return []

    #     print("files", files, type(files))
    #     if isinstance(files, (InMemoryUploadedFile, TemporaryUploadedFile)):
    #         files = [files]
    #     elif isinstance(files, dict):
    #         files = list(files.values())
    #     elif not isinstance(files, list):
    #         logger.error("ERROR: Tipe file tidak dikenali.")
    #         return []

    #     files = [f for f in files if isinstance(f, InMemoryUploadedFile)]

    #     urls = []
    #     for file in files:
    #         if file.size > FileStorageUtil.MAX_FILE_SIZE:
    #             logger.warning(f"File {file.name} terlalu besar dan diabaikan.")
    #             continue

    #         try:
    #             _id = str(uuid.uuid4())
    #             ext = os.path.splitext(get_valid_filename(file.name))[1].lower()
    #             url_file = f"{folder}/{_id}{ext}"
    #             url = f"{FileStorageUtil.AWS_BUCKET_URL}{url_file}"

    #             default_storage.save(url_file, file)
    #             urls.append(url)
    #         except Exception as e:
    #             logger.error(f"Gagal mengunggah {file.name}: {e}")

    #     return urls

    @staticmethod
    def upload_aws(
        files,
        folder: str,
    ) -> List[str]:
        if not files:
            logger.warning("Tidak ada file yang dikirim.")
            return []

        if isinstance(files, UploadedFile):
            files = [files]
        elif isinstance(files, dict):
            files = list(files.values())
        elif not isinstance(files, list):
            logger.error(f"ERROR: Tipe file tidak dikenali. type={type(files)}")
            return []

        # Filter hanya UploadedFile
        files = [f for f in files if isinstance(f, UploadedFile)]
        if not files:
            logger.warning("Tidak ada file yang valid untuk diunggah.")
            return []

        urls = []

        for file in files:
            try:
                if file.size > FileStorageUtil.MAX_FILE_SIZE:
                    logger.warning(
                        f"File {file.name} terlalu besar ({file.size} bytes) dan diabaikan."
                    )
                    continue

                ext = os.path.splitext(get_valid_filename(file.name))[1].lower()
                if ext not in FileStorageUtil.ALLOWED_EXTENSIONS:
                    logger.warning(
                        f"Ekstensi file {file.name} ({ext}) tidak diizinkan."
                    )
                    continue

                _id = str(uuid.uuid4())
                url_file = f"{folder}/{_id}{ext}"
                url = f"{FileStorageUtil.AWS_BUCKET_URL}{url_file}"

                default_storage.save(url_file, file)
                urls.append(url)
                logger.info(f"Berhasil unggah: {file.name} → {url}")
            except Exception as e:
                logger.error(f"Gagal mengunggah file {file.name}: {e}")

        return urls

    @staticmethod
    def upload_link(
        url: Union[str, List[str]], folder: str, max_file_size: int = 100 * 1024 * 1024
    ) -> Union[str, List[str]]:
        """
        Mengunggah file dari satu URL atau daftar URL ke AWS S3 dan mengembalikan URL hasil upload.

        :param url: URL atau list URL file yang ingin diunggah
        :param folder: Folder tujuan di bucket
        :param max_file_size: Ukuran maksimum file (default: 30MB)
        :return: URL hasil upload ke S3 (str atau List[str])
        """

        def upload_single(u: str) -> str:
            try:
                response = requests.get(u, stream=True)
                response.raise_for_status()

                content = response.content
                if len(content) > max_file_size:
                    raise ValueError(f"Ukuran file dari {u} melebihi batas maksimum.")

                filename = os.path.basename(u.split("?")[0])
                filename = get_valid_filename(filename)
                ext = os.path.splitext(filename)[1].lower()

                file_id = str(uuid.uuid4())
                url_path = f"{folder}/{file_id}{ext}"
                s3_url = f"{FileStorageUtil.AWS_BUCKET_URL}{url_path}"

                default_storage.save(url_path, ContentFile(content))
                return s3_url

            except Exception as e:
                logger.error(f"Gagal upload dari URL: {u}, error: {e}")
                raise

        if isinstance(url, str):
            return upload_single(url)
        elif isinstance(url, list):
            return [upload_single(u) for u in url if isinstance(u, str)]
        else:
            raise TypeError("Parameter `url` harus berupa string atau list of string.")

    @staticmethod
    def upload_file(
        field: str,
        data: Dict[
            str,
            Union[
                InMemoryUploadedFile,
                List[InMemoryUploadedFile],
                Dict[str, InMemoryUploadedFile],
            ],
        ],
        folder: str,
    ) -> None:
        """
        Mengunggah file dari field tertentu dalam data request.

        Args:
            - field (str): Nama field dalam request yang berisi file.
            - data (Dict): Dictionary yang berisi data request.
            - folder (str): Nama folder tempat file akan disimpan.

        Returns:
            - None: Mengubah `data[field]` menjadi list URL file yang berhasil diunggah.

        **Contoh Penggunaan:**
        ```python
        request_data = {"profile_picture": uploaded_file}
        FileStorageUtil.upload_file("profile_picture", request_data, "profiles")
        # request_data["profile_picture"] akan berisi URL dari file yang diunggah.
        ```
        """
        if field not in data or data[field] is None:
            logger.warning(f"WARNING: Tidak ada file untuk `{field}`.")
            return

        files = data[field]

        if isinstance(files, InMemoryUploadedFile):
            files = [files]

        if not isinstance(files, (list, dict)):
            logger.error(
                f"ERROR: `{field}` harus berupa list atau dict `InMemoryUploadedFile`, bukan `{type(files).__name__}`."
            )
            return

        data[field] = FileStorageUtil.upload_aws(files, folder)

    @staticmethod
    def upload_repository(
        _id: str, files: List[InMemoryUploadedFile], folder: str
    ) -> List[str]:
        """
        Mengunggah file dengan nama tetap berdasarkan ID tertentu.

        Args:
            - _id (str): ID yang akan digunakan sebagai nama file.
            - files (List[InMemoryUploadedFile]): List file yang akan diunggah.
            - folder (str): Nama folder tempat file akan disimpan.

        Returns:
            - List[str]: List URL file yang berhasil diunggah.

        **Contoh Penggunaan:**
        ```python
        files = [uploaded_file_1, uploaded_file_2]
        result = FileStorageUtil.upload_repository("12345", files, "repository")
        # Output (contoh): ["https://s3.amazonaws.com/your-bucket/repository/12345.jpg"]
        ```
        """
        if not files:
            return []

        urls = []
        for file in files:
            if file.size > FileStorageUtil.MAX_FILE_SIZE:
                logger.warning(f"File {file.name} terlalu besar dan diabaikan.")
                continue  # Lewati file yang terlalu besar

            ext = os.path.splitext(get_valid_filename(file.name))[1].lower()
            url_file = f"{folder}/{_id}{ext}"
            url = f"{FileStorageUtil.AWS_BUCKET_URL}{url_file}"

            try:
                default_storage.save(url_file, file)
                urls.append(url)
            except Exception as e:
                logger.error(f"Gagal mengunggah {file.name}: {e}")

        return urls

    @staticmethod
    def delete_files(file_urls: List[str]) -> None:
        """
        Menghapus file dari AWS S3 berdasarkan URL.

        Args:
            - file_urls (List[str]): List URL file yang akan dihapus.

        Returns:
            - None

        **Contoh Penggunaan:**
        ```python
        urls = [
            "https://s3.amazonaws.com/your-bucket/uploads/file1.jpg",
            "https://s3.amazonaws.com/your-bucket/uploads/file2.png"
        ]
        FileStorageUtil.delete_files(urls)
        # Output: File uploads/file1.jpg berhasil dihapus.
        ```
        """
        if not file_urls:
            return

        for url in file_urls:
            try:
                existing_file = url.replace(FileStorageUtil.AWS_BUCKET_URL, "")
                if default_storage.exists(existing_file):
                    default_storage.delete(existing_file)
                    logger.info(f"File {existing_file} berhasil dihapus.")
                else:
                    logger.warning(f"File {existing_file} tidak ditemukan.")
            except Exception as e:
                logger.error(f"Gagal menghapus file {url}: {e}")

    @staticmethod
    def update_file(
        _id: str, files: List[InMemoryUploadedFile], folder: str
    ) -> List[str]:
        """
        Memperbarui file dengan nama tetap berdasarkan ID tertentu.

        Args:
            - _id (str): ID yang digunakan sebagai nama file.
            - files (List[InMemoryUploadedFile]): List file yang akan diperbarui.
            - folder (str): Nama folder tempat file akan disimpan.

        Returns:
            - List[str]: List URL file yang berhasil diperbarui.

        **Contoh Penggunaan:**
        ```python
        files = [uploaded_file_1, uploaded_file_2]
        result = FileStorageUtil.update_file("12345", files, "repository")
        # Output (contoh): ["https://s3.amazonaws.com/your-bucket/repository/12345.jpg"]
        ```
        """
        if not files:
            return []

        urls = []
        for file in files:
            if file.size > FileStorageUtil.MAX_FILE_SIZE:
                logger.warning(f"File {file.name} terlalu besar dan diabaikan.")
                continue  # Lewati file yang terlalu besar

            ext = os.path.splitext(get_valid_filename(file.name))[1].lower()
            url_file = f"{folder}/{_id}{ext}"
            url = f"{FileStorageUtil.AWS_BUCKET_URL}{url_file}"

            try:
                default_storage.save(url_file, file)
                urls.append(url)
            except Exception as e:
                logger.error(f"Gagal memperbarui {file.name}: {e}")

        return urls

    @staticmethod
    def get_proper_file_size(size_in_bytes: int) -> str:
        """
        Mengonversi ukuran file dari bytes ke KB, MB, GB, dll.

        Args:
            - size_in_bytes (int): Ukuran file dalam byte.

        Returns:
            - str: Ukuran file yang telah dikonversi ke satuan yang lebih mudah dibaca.

        **Contoh Penggunaan:**
        ```python
        result = FileStorageUtil.get_proper_file_size(1048576)
        # Output (contoh): "1 MB"
        ```
        """
        if size_in_bytes == 0:
            return "0B"
        size_name = ("B", "KB", "MB", "GB", "TB", "PB")
        i = int(math.floor(math.log(size_in_bytes, 1024)))
        p = math.pow(1024, i)
        s = round(size_in_bytes / p, 2)
        return f"{s} {size_name[i]}"

    @staticmethod
    def file_exists(file_url: str) -> bool:
        """
        Mengecek apakah file ada di AWS S3 berdasarkan URL.

        Args:
            - file_url (str): URL file yang akan diperiksa.

        Returns:
            - bool: True jika file ada, False jika tidak.

        **Contoh Penggunaan:**
        ```python
        result = FileStorageUtil.file_exists("https://s3.amazonaws.com/your-bucket/uploads/file.jpg")
        # Output (contoh): True
        ```
        """
        file_path = file_url.replace(FileStorageUtil.AWS_BUCKET_URL, "")
        return default_storage.exists(file_path)
