import os
import re
from django.conf import settings
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile


class FileUploadUtil:

    @staticmethod
    def clean_filename(filename):
        name, ext = os.path.splitext(filename)
        name = re.sub(r"\bat\s+\d{2}\.\d{2}\.\d{2}", "", name, flags=re.IGNORECASE)
        name = name.replace(" ", "_")
        name = re.sub(r"[^\w\-]+", "", name)
        clean_name = name.lower()
        return f"{clean_name}{ext.lower()}"

    @staticmethod
    def readable_size(num_bytes):
        for unit in ["B", "KB", "MB", "GB", "TB"]:
            if num_bytes < 1024.0:
                return f"{num_bytes:.1f}{unit}"
            num_bytes /= 1024.0
        return f"{num_bytes:.1f}PB"

    @staticmethod
    def save_file(file, folder=""):
        if not file:
            return None

        try:
            original_name = file.name
            cleaned_name = FileUploadUtil.clean_filename(original_name)

            folder_path = os.path.join(folder)
            file_root, file_ext = os.path.splitext(cleaned_name)
            file_path = os.path.join(folder_path, cleaned_name)

            index = 1
            while default_storage.exists(file_path):
                new_filename = f"{file_root}_{index}{file_ext}"
                file_path = os.path.join(folder_path, new_filename)
                index += 1

            file_content = file.read()
            size_in_bytes = len(file_content)
            saved_path = default_storage.save(file_path, ContentFile(file_content))
            return (
                f"{settings.REPO_BASE_URL}/media/{saved_path}",
                size_in_bytes,
                FileUploadUtil.readable_size(size_in_bytes),
            )
        except Exception as e:
            print(f"❌ Gagal menyimpan file: {str(e)}")
            return None

    @staticmethod
    def delete_file(relative_path):
        """
        Hapus file dari MEDIA_ROOT jika ada.
        :param relative_path: path relatif dari MEDIA_ROOT (contoh: "surat/abc.pdf")
        """
        if not relative_path:
            return False

        absolute_path = os.path.join(settings.MEDIA_ROOT, relative_path)
        if os.path.isfile(absolute_path):
            try:
                os.remove(absolute_path)
                return True
            except Exception as e:
                print(f"❌ Gagal menghapus file: {str(e)}")
        return False

    @staticmethod
    def get_full_path(relative_path):
        """
        Kembalikan path absolut dari file di media.
        :param relative_path: "surat/abc.pdf"
        :return: "/var/www/project/media/surat/abc.pdf"
        """
        return (
            os.path.join(settings.MEDIA_ROOT, relative_path) if relative_path else None
        )
