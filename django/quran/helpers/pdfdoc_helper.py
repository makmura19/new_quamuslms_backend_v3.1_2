from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    PageBreak,
    ListFlowable,
    ListItem,
    Image,
    Table,
    TableStyle,
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.pagesizes import A4
from reportlab.lib.enums import TA_JUSTIFY, TA_LEFT, TA_CENTER, TA_RIGHT
from reportlab.lib.units import cm
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from datetime import datetime
from io import BytesIO
from django.http import HttpResponse
import os
from reportlab.lib.colors import HexColor
import re


class PdfDocHelper:
    def __init__(
        self,
        content,
        filename="document",
        title=None,
        paper_size="A4",
        orientation="portrait",
        margin=None,  # dict: {"top": cm, "left": cm, "right": cm, "bottom": cm}
    ):
        from reportlab.lib.pagesizes import A4, LETTER, A5, landscape, portrait

        self.content = content
        self.filename = f"{filename}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        self.title = title
        self.buffer = BytesIO()
        self.styles = self._init_styles()
        self.story = []
        self.absolute_paragraphs = []

        paper_sizes = {
            "A4": A4,
            "letter": LETTER,
            "A5": A5,
        }
        self.pagesize = paper_sizes.get(paper_size.lower(), A4)

        if orientation == "landscape":
            from reportlab.lib.pagesizes import landscape

            self.pagesize = landscape(self.pagesize)
        else:
            from reportlab.lib.pagesizes import portrait

            self.pagesize = portrait(self.pagesize)

        default_margin = {"top": 4, "bottom": 2.5, "left": 2.5, "right": 2.5}
        if margin:
            default_margin.update(margin)
        self.margin = default_margin

        self._generate()

    def _init_styles(self):
        styles = getSampleStyleSheet()
        styles.add(
            ParagraphStyle(
                name="Justify", alignment=TA_JUSTIFY, fontSize=11, leading=15
            )
        )
        styles.add(
            ParagraphStyle(name="ListItem", fontSize=11, leftIndent=15, leading=15)
        )

        if "CustomHeading1" not in styles:
            styles.add(
                ParagraphStyle(
                    name="CustomHeading1",
                    parent=styles["Heading1"],
                    fontSize=16,
                    spaceAfter=12,
                )
            )
        if "CustomHeading2" not in styles:
            styles.add(
                ParagraphStyle(
                    name="CustomHeading2",
                    parent=styles["Heading2"],
                    fontSize=14,
                    spaceAfter=10,
                )
            )

        return styles

    def parse_margins(self, style_parts):
        mb = ml = 0
        for part in style_parts:
            if part.startswith("mb-"):
                try:
                    mb = int(part.replace("mb-", "")) * cm
                except:
                    pass
            elif part.startswith("ml-"):
                try:
                    ml = int(part.replace("ml-", "")) * cm
                except:
                    pass
        return mb, ml

    def _generate(self):
        doc = SimpleDocTemplate(
            self.buffer,
            pagesize=A4,
            rightMargin=2.5 * cm,
            leftMargin=2.5 * cm,
            topMargin=4 * cm,
            bottomMargin=2.5 * cm,
        )

        for item in self.content:
            t = item.get("type")
            if t == "heading":
                level = item.get("level", 1)
                style = self.styles.get(f"Heading{level}", self.styles["Heading1"])
                self.story.append(Paragraph(item["text"], style))
            elif t == "paragraph":
                text = (
                    item["text"]
                    .replace("\t", "&nbsp;&nbsp;&nbsp;&nbsp;")
                    .replace("\n", "<br/>")
                )

                style_str = item.get("style", "")
                style_parts = style_str.split()

                is_absolute = "absolute" in style_parts
                style_name = f"Para_{style_str.replace(' ', '_') or 'Justify'}"

                if style_name not in self.styles:
                    style = ParagraphStyle(
                        name=style_name, parent=self.styles["Justify"]
                    )
                    for part in style_parts:
                        if part == "text-center":
                            style.alignment = TA_CENTER
                        elif part == "text-right":
                            style.alignment = TA_RIGHT
                        elif part == "text-left":
                            style.alignment = TA_LEFT
                        elif part == "font-bold":
                            style.fontName = "Helvetica-Bold"
                        elif part.startswith("size-"):
                            try:
                                style.fontSize = int(part.replace("size-", ""))
                            except:
                                pass
                        elif part.startswith("lh-"):
                            try:
                                style.leading = int(part.replace("lh-", ""))
                            except:
                                pass
                        elif part.startswith("color-"):
                            color_val = part.replace("color-", "")
                            hex_match = re.match(r"^\[([0-9a-fA-F]{6})\]$", color_val)
                            if hex_match:
                                hex_code = hex_match.group(1)
                                try:
                                    style.textColor = HexColor(f"#{hex_code}")
                                except:
                                    pass
                            else:
                                try:
                                    style.textColor = getattr(colors, color_val)
                                except AttributeError:
                                    pass
                    self.styles.add(style)

                if is_absolute:
                    self.absolute_paragraphs.append(
                        {
                            "text": text,
                            "style": self.styles[style_name],
                            "style_parts": style_parts,
                        }
                    )
                else:
                    mb, ml = self.parse_margins(style_parts)
                    para = Paragraph(text, self.styles[style_name])

                    if ml > 0:
                        self.story.append(Spacer(ml, 0))
                    self.story.append(para)
                    self.story.append(Spacer(1, mb if mb > 0 else 12))
            elif t == "ul":
                items = item.get("items", [])
                bullet_list = ListFlowable(
                    [ListItem(Paragraph(i, self.styles["ListItem"])) for i in items],
                    bulletType="bullet",
                    start="disc",
                    leftIndent=12,
                )
                self.story.append(bullet_list)
                self.story.append(Spacer(1, 12))
            elif t == "ol":
                items = item.get("items", [])
                numbered_list = ListFlowable(
                    [ListItem(Paragraph(i, self.styles["ListItem"])) for i in items],
                    bulletType="1",  # ordered
                    leftIndent=12,
                )
                self.story.append(numbered_list)
                self.story.append(Spacer(1, 12))
            elif t == "image":
                path = item.get("path")
                if path:
                    from PIL import Image as PILImage
                    import requests

                    try:
                        if path.startswith("http"):
                            response = requests.get(path)
                            response.raise_for_status()
                            img_data = BytesIO(response.content)
                            with PILImage.open(img_data) as img_src:
                                orig_w, orig_h = img_src.size
                        else:
                            with PILImage.open(path) as img_src:
                                orig_w, orig_h = img_src.size

                        raw_width = item.get("width", 5)
                        width = (
                            raw_width * cm
                            if isinstance(raw_width, (int, float))
                            else raw_width
                        )

                        aspect = orig_h / orig_w
                        height = width * aspect

                        if "max_height" in item:
                            max_h = item["max_height"] * cm
                            if height > max_h:
                                height = max_h
                                width = height / aspect

                        img = Image(path, width=width, height=height)

                        align = item.get("align", "left")
                        if align == "center":
                            img.hAlign = "CENTER"
                        elif align == "right":
                            img.hAlign = "RIGHT"
                        else:
                            img.hAlign = "LEFT"

                        self.story.append(img)
                        self.story.append(Spacer(1, 12))

                    except Exception as e:
                        self.story.append(
                            Paragraph(
                                f"[Gagal memuat gambar: {e}]", self.styles["Normal"]
                            )
                        )
            elif t == "table":
                table_data = item.get("data", [])
                setting = item.get("setting", [])
                col_widths = []
                table_style = [
                    ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
                    ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
                    ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ]

                formatted_data = []

                for row_idx, row in enumerate(table_data):
                    new_row = []
                    for col_idx, value in enumerate(row):
                        parts = (
                            setting[col_idx].split() if col_idx < len(setting) else []
                        )

                        if row_idx == 0:
                            new_row.append(value)
                            continue

                        if "date" in parts and isinstance(value, str):
                            try:
                                from datetime import datetime

                                dt = datetime.strptime(value, "%Y-%m-%d")
                                value = dt.strftime("%d-%m-%Y")
                            except:
                                pass

                        if "number" in parts:
                            try:
                                value = f"{int(value):,}".replace(",", ".")
                            except:
                                pass

                        new_row.append(value)
                    formatted_data.append(new_row)

                for col_idx, col_setting in enumerate(setting):
                    parts = col_setting.split()
                    width = 3 * cm
                    align = "LEFT"

                    for part in parts:
                        if part.startswith("w-"):
                            try:
                                width = int(part.replace("w-", "")) * 0.25 * cm
                            except:
                                pass
                        elif part == "text-center":
                            align = "CENTER"
                        elif part == "text-right":
                            align = "RIGHT"
                        elif part == "text-left":
                            align = "LEFT"

                    col_widths.append(width)
                    table_style.append(("ALIGN", (col_idx, 1), (col_idx, -1), align))
                    table_style.append(("ALIGN", (col_idx, 0), (col_idx, 0), "CENTER"))

                tbl = Table(formatted_data, colWidths=col_widths, hAlign="LEFT")
                tbl.setStyle(TableStyle(table_style))
                self.story.append(tbl)
                self.story.append(Spacer(1, 12))
            elif t == "line_chart":
                import matplotlib.pyplot as plt
                import pandas as pd

                chart_data = item.get("data", [])
                data_key = item.get("dataKey", "date")

                style_str = item.get("style", "")
                style_parts = style_str.split()
                width = 10 * cm
                align = "LEFT"

                for part in style_parts:
                    if part.startswith("w-") and "/" not in part:
                        try:
                            width = int(part.replace("w-", "")) * 0.25 * cm
                        except:
                            pass
                    elif part == "align-center":
                        align = "CENTER"
                    elif part == "align-right":
                        align = "RIGHT"

                df = pd.DataFrame(chart_data)
                x = df[data_key]
                plt.figure(figsize=(width / 2.54, 3))

                for col in df.columns:
                    if col != data_key:
                        plt.plot(x, df[col], marker="o", label=col)

                plt.legend()
                plt.grid(True, linestyle="--", alpha=0.5)
                plt.tight_layout()

                img_buf = BytesIO()
                plt.savefig(img_buf, format="png", bbox_inches="tight", dpi=150)
                img_buf.seek(0)

                img = Image(img_buf, width=width, height=width * 0.5)
                img.hAlign = align
                self.story.append(img)
                self.story.append(Spacer(1, 12))
            elif t == "pagebreak":
                self.story.append(PageBreak())

        doc.build(
            self.story,
            onFirstPage=self._header_footer,
            onLaterPages=self._header_footer,
        )

    def _header_footer(self, canvas, doc):
        canvas.saveState()
        for abs_para in self.absolute_paragraphs:
            style_parts = abs_para["style_parts"]
            x = y = w = None
            for part in style_parts:
                if part == "w-full":
                    w = self.pagesize[0] - self.margin["left"] - self.margin["right"]
                elif part == "w-1/2":
                    w = (
                        self.pagesize[0] - self.margin["left"] - self.margin["right"]
                    ) / 2
                elif part == "w-1/3":
                    w = (
                        self.pagesize[0] - self.margin["left"] - self.margin["right"]
                    ) / 3
                elif part == "w-1/4":
                    w = (
                        self.pagesize[0] - self.margin["left"] - self.margin["right"]
                    ) / 4
                elif part.startswith("w-"):
                    try:
                        w = int(part.replace("w-", "")) * 0.25 * cm  # default scaling
                    except:
                        pass
                elif part.startswith("x-") and part not in [
                    "x-left",
                    "x-center",
                    "x-right",
                ]:
                    x = int(part.replace("x-", "")) * cm
                elif part.startswith("y-"):
                    y = int(part.replace("y-", "")) * cm
                elif part == "x-left":
                    x = self.margin["left"]
                elif part == "x-center":
                    if w is not None:
                        x = (self.pagesize[0] - w) / 2
                elif part == "x-right":
                    if w is not None:
                        x = self.pagesize[0] - self.margin["right"] - w
            if x is not None and y is not None and w is not None:
                para = Paragraph(abs_para["text"], abs_para["style"])
                para.wrapOn(canvas, w, 100 * cm)
                para.drawOn(canvas, x, self.pagesize[1] - y)
        canvas.setFont("Helvetica", 8)
        canvas.drawString(
            2.5 * cm,
            A4[1] - 1.5 * cm,
            f"Dicetak: {datetime.now().strftime('%d-%m-%Y %H:%M')}",
        )
        canvas.drawRightString(A4[0] - 2.5 * cm, 1.5 * cm, f"Halaman {doc.page}")
        if self.title:
            canvas.setFont("Helvetica-Bold", 12)
            canvas.drawCentredString(A4[0] / 2, A4[1] - 2.5 * cm, self.title)
        canvas.restoreState()

    @property
    def response(self) -> HttpResponse:
        self.buffer.seek(0)
        response = HttpResponse(self.buffer, content_type="application/pdf")
        response["Content-Disposition"] = f'inline; filename="{self.filename}"'
        return response


"""
Usage

helper = PdfDocHelper(
content=[
    {"type": "heading", "text": "Bab 1 - Pendahuluan", "level": 2},
    {
        "type": "paragraph",
        "text": "Ini adalah pengantar.\nIni baris 2",
        "style": "text-center color-green font-bold size-10 lh-12 mb-2",
    },
    {
        "type": "paragraph",
        "text": "Absolute",
        "style": "absolute text-center color-red font-bold size-10 w-full x-left y-20",
    },
    {"type": "ul", "items": ["Satu", "Dua"]},
    {"type": "ol", "items": ["Langkah 1", "Langkah 2"]},
    {
        "type": "image",
        "path": "https://quamus-lms-s3.s3.ap-southeast-3.amazonaws.com/school_logo/675cf8dc08a1147eacab29a1.png?x=305",
        "width": 5,
        "align": "center",
        "max_height": 6,
    },
    {
        "type": "table",
        "data": [
            ["No", "Nama", "Tanggal Lahir", "Gaji"],
            ["1", "Joe", "1987-02-21", 250000],
        ],
        "setting": [
            "w-4 text-center",
            "w-10",
            "w-15 date",
            "w-15 text-right number",
        ],
    },
    {
        "type": "line_chart",
        "style": "w-70 align-left",
        "data": [
            {
                "date": "Mar 22",
                "Apples": 2890,
                "Oranges": 2338,
                "Tomatoes": 2452,
            },
            {
                "date": "Mar 23",
                "Apples": 2756,
                "Oranges": 2103,
                "Tomatoes": 2402,
            },
            {
                "date": "Mar 24",
                "Apples": 3322,
                "Oranges": 986,
                "Tomatoes": 1821,
            },
        ],
        "dataKey": "date",
        "curveType": "linear",
    },
],
title="Laporan Lengkap",
)

return helper.response
"""
