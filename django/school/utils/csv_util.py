import csv
import io


class CsvUtils:
    @staticmethod
    def read(file, delimiter=","):
        decoded_file = io.TextIOWrapper(file.file, encoding="utf-8")
        reader = csv.DictReader(decoded_file, delimiter=delimiter)
        data = [row for row in reader]
        return data
