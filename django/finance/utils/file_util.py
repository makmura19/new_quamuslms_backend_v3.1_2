import json
import os


class FileUtil:
    @staticmethod
    def read_json_file(file_path):
        """
        Membaca file JSON dan mengembalikan kontennya sebagai dictionary.
        :param file_path: Path lengkap ke file JSON.
        :return: Dictionary yang berisi data dari file JSON.
        :raises FileNotFoundError: Jika file tidak ditemukan.
        :raises json.JSONDecodeError: Jika file bukan JSON yang valid.
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File tidak ditemukan: {file_path}")

        try:
            with open(file_path, "r", encoding="utf-8") as file:
                return json.load(file)
        except json.JSONDecodeError as e:
            raise ValueError(f"File JSON tidak valid: {e}") from e

    @staticmethod
    def write_file(file_path, data, mode="w", encoding="utf-8"):
        """
        Menulis data ke file.
        :param file_path: Path lengkap ke file yang akan ditulis.
        :param data: Data yang akan ditulis (string atau bytes).
        :param mode: Mode penulisan ('w' untuk teks, 'wb' untuk biner, dll.).
        :param encoding: Encoding untuk file teks (default: utf-8).
        :raises IOError: Jika terjadi kesalahan saat menulis file.
        """
        try:
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            if "b" in mode:
                with open(file_path, mode) as file:
                    file.write(data)
            else:
                with open(file_path, mode, encoding=encoding) as file:
                    file.write(data)
        except IOError as e:
            raise IOError(f"Gagal menulis file: {e}") from e
