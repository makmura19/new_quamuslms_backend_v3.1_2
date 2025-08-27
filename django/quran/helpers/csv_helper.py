import csv
from io import StringIO
from django.http import HttpResponse
from datetime import datetime


class CsvHelper:
    def __init__(self, data, filename="export", setting=None, title=None):
        self.data = data
        self.filename = f"{filename}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"

    @property
    def response(self) -> HttpResponse:
        buffer = StringIO()
        writer = csv.writer(buffer, delimiter=";")

        for row in self.data:
            writer.writerow(row)

        buffer.seek(0)
        response = HttpResponse(buffer.getvalue(), content_type="text/csv")
        response["Content-Disposition"] = f'attachment; filename="{self.filename}"'
        return response
