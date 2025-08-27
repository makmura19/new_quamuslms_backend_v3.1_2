from reportlab.lib.pagesizes import A4, portrait
from reportlab.platypus import (
    BaseDocTemplate,
    PageTemplate,
    Frame,
    Table,
    Spacer,
    PageBreak,
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from io import BytesIO
from reportlab.lib import colors
from utils.reportlab_util import ReportLabUtil, NumberedCanvas, EnumTableStyle
from utils.string_util import StringUtil
from utils.datetime_util import DatetimeUtil
from constants.timezone import Timezone


class Report:
    def __init__(self, data):
        self.data = data
        self.gender_map = {"male": "Laki-laki", "female": "Perempuan"}
        self.reportlab_util = ReportLabUtil()
        self.p = self.reportlab_util.paragraph
        self.l = self.reportlab_util.list_paragraph
        self.buffer = BytesIO()
        self.page_width, self.page_height = portrait(A4)
        self.doc = BaseDocTemplate(
            self.buffer,
            pagesize=portrait(A4),
            leftMargin=30,
            rightMargin=30,
            topMargin=130,
            bottomMargin=30,
        )
        self.page_width_clean = (
            self.page_width - self.doc.leftMargin - self.doc.rightMargin
        )
        self.page_height_clean = (
            self.page_height - self.doc.topMargin - self.doc.bottomMargin
        )
        self.frame = Frame(
            self.doc.leftMargin,
            self.doc.bottomMargin,
            self.doc.width,
            self.doc.height,
            id="normal",
        )
        self.template = PageTemplate(
            id="main", frames=[self.frame], onPage=self.on_page
        )
        self.doc.addPageTemplates([self.template])

        self.styles = getSampleStyleSheet()
        self.normal = self.styles["Normal"]
        self.centered_bold = ParagraphStyle(
            "centered_bold", parent=self.normal, alignment=1, fontName="Helvetica-Bold"
        )
        self.centered_italic = ParagraphStyle(
            "centered_italic",
            parent=self.normal,
            alignment=1,
            fontName="Helvetica-Oblique",
        )
        self.italic = ParagraphStyle(
            "italic", parent=self.normal, fontName="Helvetica-Oblique"
        )
        self.elements = []
        self.elements.append(
            self.p(
                "FORMULIR INFORMASI MEDIS PENDONOR MATA",
                "center bold text-[12] mb-10 font-helvetica",
            )
        )
        self.table()
        self.doc.build(self.elements, canvasmaker=NumberedCanvas)
        self.buffer.seek(0)
        self.pdf_bytes = self.buffer.getvalue()
        self.response = {"type": "pdf", "buffer": BytesIO(self.pdf_bytes)}

    def on_page(self, canvas, doc):
        logo_url = "https://quamus-s3.s3.ap-southeast-3.amazonaws.com/logo/Rscm_new.png"

        logo_cell = Table(
            [[self.reportlab_util.image(logo_url, 160)]],
            style=[(EnumTableStyle.LEFTPADDING, (0, 0), (-1, -1), 0)],
            hAlign="LEFT",
        )

        box_data = [
            [self.p("Data Calon Donor Mata", "center bold"), ""],
            [
                self.p("NRM"),
                self.p(f": {StringUtil.mask(self.donor.get('donor_no'),'###-##-##')}"),
            ],
            [self.p("Nama"), self.p(f": {self.donor.get('name')}")],
            [
                self.p("Jenis Kelamin"),
                self.p(f": {self.gender_map.get(self.donor.get('gender'))}"),
            ],
            [
                self.p("Tanggal Lahir"),
                self.p(f": {StringUtil.format_date(self.donor.get('birth_date'))}"),
            ],
        ]

        box_table = Table(
            box_data,
            colWidths=[80, 160],
            style=[
                (EnumTableStyle.BOX, (0, 0), (-1, -1), 0.5, colors.black),
                (EnumTableStyle.SPAN, (0, 0), (1, 0)),
            ],
            hAlign="RIGHT",
            cornerRadii=[5, 5, 5, 5],
            rowHeights=16,
        )

        layout_table = Table(
            [[logo_cell, box_table]],
            colWidths=[262, 262],
            style=[
                (EnumTableStyle.ALIGN, (1, 0), (1, 0), EnumTableStyle.RIGHT),
                (EnumTableStyle.VALIGN, (0, 0), (-1, -1), EnumTableStyle.TOP),
            ],
            hAlign="LEFT",
        )

        w, h = layout_table.wrap(doc.width, doc.topMargin)
        layout_table.drawOn(canvas, doc.leftMargin, doc.height + doc.topMargin - h)

    def table(self):
        table_data = [
            [self.p("IDENTITAS PENDONOR MATA", "center bold"), ""],
            [
                self.p("Nomor rekam medis"),
                self.p("123-45-67"),
            ],
        ]
        table = Table(
            table_data,
            colWidths=[200, 335],
            style=[
                (EnumTableStyle.GRID, (0, 0), (-1, -1), 0.5, colors.black),
                (EnumTableStyle.SPAN, (0, 0), (1, 0)),
                (EnumTableStyle.TOPPADDING, (0, 0), (-1, -1), 2),
                (EnumTableStyle.BOTTOMPADDING, (0, 0), (-1, -1), 2),
            ],
            hAlign=EnumTableStyle.LEFT,
        )
        self.elements.append(table)

    def table_check(self):
        disease = {
            "ensefalitis": "Ensefalitis",
            "creutzfeld": "Creutzfeld/Jacob Disease",
        }
        table_data = [
            [
                self.reportlab_util.checkbox(
                    is_check=self.data.get("neurological_disorder").get("ensefalitis"),
                    text=disease["ensefalitis"],
                ),
                self.reportlab_util.checkbox(
                    is_check=self.data.get("neurological_disorder").get("creutzfeld"),
                    text=disease["creutzfeld"],
                ),
                self.reportlab_util.checkbox(
                    is_check=False,
                    text="Tidak Ada",
                ),
            ],
            [
                self.p(
                    f"Jelaskan: {self.data.get('neurological_disorder_notes') if self.data.get('neurological_disorder_notes') else '-'}"
                ),
                "",
            ],
        ]
        table = Table(
            table_data,
            colWidths=[80, 140, 110],
            style=[
                (EnumTableStyle.TOPPADDING, (0, 0), (-1, -1), 2),
                (EnumTableStyle.BOTTOMPADDING, (0, 0), (-1, -1), 2),
                (EnumTableStyle.VALIGN, (0, 0), (-1, -1), EnumTableStyle.MIDDLE),
                (EnumTableStyle.ALIGN, (0, 0), (-1, -1), EnumTableStyle.LEFT),
                (EnumTableStyle.SPAN, (0, 1), (1, 1)),
            ],
            hAlign=EnumTableStyle.LEFT,
        )

        return table


"""
response_type = query_params.get("response_type")
if response_type == "pdf":
    from pdf_template.form08 import Report
    from bson import ObjectId
    from models.eye_bank_donor import EyeBankDonor
    from models.hr_employee import HrEmployee

    donor = EyeBankDonor().find_one({"_id": ObjectId(result.get("donor_id"))})
    examiner = HrEmployee().find_one(
        {"_id": ObjectId(result.get("examined_by"))}
    )
    result["donor"] = donor
    result["examiner"] = examiner
    report = Report(result)
    return report.response
"""
