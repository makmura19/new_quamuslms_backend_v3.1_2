import openpyxl
from reportlab.platypus import (
    SimpleDocTemplate,
    Table,
    TableStyle,
    Paragraph,
    PageBreak,
    Spacer,
)
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from reportlab.pdfgen import canvas
from reportlab.lib.units import cm
from io import BytesIO
from datetime import datetime
from django.http import HttpResponse


class PdfTableHelper:
    def __init__(
        self,
        data,
        setting=None,
        filename="report",
        title=None,
        options=None,
    ):
        self.data = data
        self.setting = setting or []
        self.filename = f"{filename}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        self.title = title
        self.options = options or []

        self.buffer = BytesIO()
        self.styles = getSampleStyleSheet()
        self.story = []

        self._generate()

    def _add_summary_row(self, data, setting):
        headers = data[0]
        values = data[1:]

        has_summary = any(any(k in s for k in ["sum", "avg", "count"]) for s in setting)
        if not has_summary:
            return data

        summary_row = []
        for idx, col_setting in enumerate(setting):
            parts = col_setting.split()
            col_data = [row[idx] for row in values]

            if any(k in parts for k in ["sum", "avg", "count"]):
                numeric_values = []
                for val in col_data:
                    try:
                        numeric_values.append(int(str(val).replace(".", "")))
                    except:
                        numeric_values.append(0)

                if "sum" in parts:
                    value = sum(numeric_values)
                elif "avg" in parts:
                    value = (
                        round(sum(numeric_values) / len(numeric_values))
                        if numeric_values
                        else 0
                    )
                elif "count" in parts:
                    value = len(numeric_values)
                else:
                    value = ""

                summary_row.append(f"{value:,}".replace(",", "."))
            else:
                summary_row.append("")

        return data + [summary_row]

    def _generate(self):
        doc = SimpleDocTemplate(
            self.buffer,
            pagesize=A4,
            rightMargin=2 * cm,
            leftMargin=2 * cm,
            topMargin=(2.5 + (len(self.options) * 0.5)) * cm,
            bottomMargin=2 * cm,
        )

        table_data = [self.data[0]]
        for row in self.data[1:]:
            formatted_row = []
            for idx, val in enumerate(row):
                parts = self.setting[idx].split() if idx < len(self.setting) else []
                if "date" in parts and isinstance(val, str):
                    try:
                        dt = datetime.strptime(val, "%Y-%m-%d")
                        val = dt.strftime("%d-%m-%Y")
                    except:
                        pass
                elif "number" in parts:
                    try:
                        val = f"{int(val):,}".replace(",", ".")
                    except:
                        pass
                formatted_row.append(val)
            table_data.append(formatted_row)
        table_data = self._add_summary_row(table_data, self.setting)
        table_style = [
            ("GRID", (0, 0), (-1, -1), 0.5, colors.black),
            ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ]

        col_widths = []
        for col_idx, s in enumerate(self.setting):
            parts = s.split()
            width = 3 * cm
            align = TA_LEFT
            for p in parts:
                if p.startswith("w-"):
                    width = int(p.replace("w-", "")) * 0.25 * cm
                elif p == "text-center":
                    align = TA_CENTER
                elif p == "text-right":
                    align = TA_RIGHT
            col_widths.append(width)
            table_style.append(
                (
                    "ALIGN",
                    (col_idx, 1),
                    (col_idx, -1),
                    {TA_LEFT: "LEFT", TA_CENTER: "CENTER", TA_RIGHT: "RIGHT"}[align],
                )
            )
            table_style.append(("ALIGN", (col_idx, 0), (col_idx, 0), "CENTER"))

        if any(any(k in s for k in ["sum", "avg", "count"]) for s in self.setting):
            summary_row_index = len(table_data) - 1
            table_style.append(
                (
                    "FONTNAME",
                    (0, summary_row_index),
                    (-1, summary_row_index),
                    "Helvetica-Bold",
                )
            )
        table = Table(table_data, colWidths=col_widths, repeatRows=1, hAlign="LEFT")
        table.setStyle(TableStyle(table_style))
        self.story.append(table)

        def header_footer(canvas, doc):
            canvas.saveState()
            canvas.setFont("Helvetica", 8)

            canvas.drawString(
                doc.leftMargin,
                A4[1] - 1.5 * cm,
                f"Dicetak: {datetime.now().strftime('%d-%m-%Y %H:%M')}",
            )

            canvas.drawRightString(
                A4[0] - doc.rightMargin, 1.5 * cm, f"Halaman {doc.page}"
            )
            y_position = A4[1] - 2.2 * cm

            if self.title:
                title_style = ParagraphStyle(
                    name="Title",
                    parent=self.styles["Heading2"],
                    alignment=TA_CENTER,
                )
                title_para = Paragraph(self.title, title_style)
                w, h = title_para.wrap(doc.width, doc.topMargin)
                title_para.drawOn(canvas, doc.leftMargin, y_position)
                y_position -= h + 6

            if self.options:
                option_style = ParagraphStyle(
                    name="Option",
                    parent=self.styles["Normal"],
                    fontSize=10,
                    italic=True,
                    alignment=TA_LEFT,
                )
                for opt in self.options:
                    para = Paragraph(opt, option_style)
                    w, h = para.wrap(doc.width, doc.topMargin)
                    para.drawOn(canvas, doc.leftMargin, y_position)
                    y_position -= h

            canvas.restoreState()

        doc.build(self.story, onFirstPage=header_footer, onLaterPages=header_footer)

    @property
    def response(self) -> HttpResponse:
        self.buffer.seek(0)
        response = HttpResponse(self.buffer, content_type="application/pdf")
        response["Content-Disposition"] = f'inline; filename="{self.filename}"'
        return response


"""
## Example Data
data = [
    ["No", "Nama", "Tanggal Lahir", "Gaji"],
    ["1", "Joe", "1988-04-24", 250000],
    ["2", "Daisy", "1984-04-24", 150000],
]


setting = [
    "w-4 text-center",
    "w-20",
    "w-14 date text-center",
    "w-10 text-right number sum",
]

### Example Usage
response_type = query_params.get("response_type")
if response_type in ["xlsx", "pdf"]:
    export_data = [["No", "Nama"]]
    export_setting = ["w-5 text-center", "w-40"]
    for idx, item in enumerate(result["data"], start=1):
        export_data.append([idx, item.get("name", "")])

    export_kwargs = {
        "data": export_data,
        "setting": export_setting,
        "filename": "author_grade",
        "title": "Data Author Grade",
    }

    if response_type == "pdf":
        export_kwargs["options"] = ["Cluster: Sinom", "Blok: B1"]

    helper_class = {
        "xlsx": OpenpxlHelper,
        "pdf": PdfTableHelper,
    }.get(response_type)

    return helper_class(**export_kwargs).response
"""
