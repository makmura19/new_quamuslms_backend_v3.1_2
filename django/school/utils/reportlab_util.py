from reportlab.platypus import Image, Spacer, Paragraph, ListFlowable, ListItem, Table
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen.canvas import Canvas
import requests
from io import BytesIO
from enum import Enum
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT
from reportlab.lib import colors
from reportlab.graphics.barcode import qr
from reportlab.graphics.shapes import Drawing
import re
from bs4 import BeautifulSoup


class ReportLabUtil:
    ALIGN_MAP = {
        "left": TA_LEFT,
        "center": TA_CENTER,
        "right": TA_RIGHT,
    }
    FONT_BASE_MAP = {
        "font-helvetica": "Helvetica",
        "font-arial": "Helvetica",  # Arial fallback
        "font-times": "Times-Roman",
        "font-courier": "Courier",
    }

    COLOR_MAP = {
        "black": colors.black,
        "red": colors.red,
        "blue": colors.blue,
        "green": colors.green,
        "gray": colors.gray,
        "white": colors.white,
        "yellow": colors.yellow,
        "orange": colors.orange,
    }

    def image(self, url, fixed_width=80):
        try:
            response = requests.get(url, timeout=5)
            response.raise_for_status()
            img_data = BytesIO(response.content)
            img_reader = ImageReader(img_data)

            orig_width, orig_height = img_reader.getSize()
            aspect_ratio = orig_height / orig_width
            height = fixed_width * aspect_ratio

            return Image(img_data, width=fixed_width, height=height)

        except requests.exceptions.RequestException as e:
            print(f"[ERROR] Failed to load image: {url} | Error: {e}")
            return Spacer(1, 40)

    def paragraph(
        self, text: str, style_str: str = "", bulletText: str = None
    ) -> Paragraph:
        classes = style_str.strip().split()

        style_kwargs = {
            "fontName": "Helvetica",
            "fontSize": 10,
            "leading": 12,
            "alignment": TA_LEFT,
            "textColor": colors.black,
            "spaceBefore": 0,
            "spaceAfter": 0,
            "leftIndent": 0,
            "rightIndent": 0,
        }

        is_bold = False
        is_italic = False

        for cls in classes:
            # Alignment
            if cls in self.ALIGN_MAP:
                style_kwargs["alignment"] = self.ALIGN_MAP[cls]

            # Font size like text-[14]
            elif match := re.match(r"text-\[(\d+)\]", cls):
                size = int(match.group(1))
                style_kwargs["fontSize"] = size
                style_kwargs["leading"] = size + 2

            # Font style
            elif cls == "bold":
                is_bold = True
            elif cls == "italic":
                is_italic = True

            # Font family
            elif cls.startswith("font-") and cls in self.FONT_BASE_MAP:
                style_kwargs["fontName"] = self.FONT_BASE_MAP[cls]

            # Margin
            elif cls.startswith("mt-"):
                style_kwargs["spaceBefore"] = int(cls.split("-")[1])
            elif cls.startswith("mb-"):
                style_kwargs["spaceAfter"] = int(cls.split("-")[1])
            elif cls.startswith("mx-"):
                val = int(cls.split("-")[1])
                style_kwargs["leftIndent"] = val
                style_kwargs["rightIndent"] = val
            elif cls.startswith("my-"):
                val = int(cls.split("-")[1])
                style_kwargs["spaceBefore"] = val
                style_kwargs["spaceAfter"] = val

            # Text color (based on exact class name)
            elif cls in self.COLOR_MAP:
                style_kwargs["textColor"] = self.COLOR_MAP[cls]

        # Final fontName with suffix
        base_font = style_kwargs["fontName"]
        if is_bold and is_italic:
            style_kwargs["fontName"] = f"{base_font}-BoldOblique"
        elif is_bold:
            style_kwargs["fontName"] = f"{base_font}-Bold"
        elif is_italic:
            style_kwargs["fontName"] = f"{base_font}-Oblique"

        # Unique style name (for debugging or reuse)
        style_name = f"auto_{hash(frozenset(style_kwargs.items()))}"

        # Create ParagraphStyle
        style = ParagraphStyle(name=style_name, **style_kwargs)

        # Return final Paragraph
        return Paragraph(text, style, bulletText=bulletText)

    def list_paragraph(
        self, texts=[], style="", bulletType="1", start=1
    ) -> ListFlowable:
        sample_paragraph = self.paragraph("preview", style)
        paragraph_style = sample_paragraph.style
        items = [ListItem(self.paragraph(text, style)) for text in texts]

        return ListFlowable(
            items,
            bulletType=bulletType,
            bulletFontSize=paragraph_style.fontSize,
            bulletFontName=paragraph_style.fontName,
            leftIndent=20,
            start=None if bulletType == "bullet" else start,
        )

    def parse_html_to_paragraphs(self, html: str) -> list:
        soup = BeautifulSoup(html, "html.parser")
        elements = []

        for node in soup.contents:
            # Handle <p>
            if node.name == "p":
                text = node.get_text(strip=True)
                if text:
                    elements.append(self.paragraph(text))

            # Handle <ol>
            elif node.name == "ol":
                items = []
                for li in node.find_all("li", recursive=False):
                    text = li.get_text(strip=True)
                    if text:
                        items.append(text)
                if items:
                    elements.append(self.list_paragraph(items, bulletType="1"))

        return elements

    def qr_code(self, url: str, size: int = 60) -> Drawing:
        qr_code = qr.QrCodeWidget(url)
        bounds = qr_code.getBounds()
        width = bounds[2] - bounds[0]
        height = bounds[3] - bounds[1]

        d = Drawing(size, size, transform=[size / width, 0, 0, size / height, 0, 0])
        d.add(qr_code)
        return d

    def checkbox(self, w=120, is_check=True, text="Checkbox"):
        check_url = "https://quamus-s3.s3.ap-southeast-3.amazonaws.com/logo/check20.png"
        uncheck_url = (
            "https://quamus-s3.s3.ap-southeast-3.amazonaws.com/logo/uncheck20.png"
        )
        url = check_url if is_check else uncheck_url
        table_data = [
            [
                self.image(url, 12),
                text,
            ],
        ]
        check_w = 16
        table = Table(
            table_data,
            colWidths=[check_w, w - check_w],
            style=[
                # (EnumTableStyle.GRID, (0, 0), (-1, -1), 0.5, colors.black),
                (EnumTableStyle.TOPPADDING, (0, 0), (-1, -1), 0),
                (EnumTableStyle.BOTTOMPADDING, (0, 0), (-1, -1), 0),
                (EnumTableStyle.LEFTPADDING, (0, 0), (-1, -1), 0),
                (EnumTableStyle.VALIGN, (0, 0), (-1, -1), EnumTableStyle.MIDDLE),
                (EnumTableStyle.ALIGN, (0, 0), (-1, -1), EnumTableStyle.LEFT),
            ],
            hAlign=EnumTableStyle.LEFT,
            rowHeights=12,
        )
        return table


class NumberedCanvas(Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_number(num_pages)
            Canvas.showPage(self)
        Canvas.save(self)

    def draw_page_number(self, page_count):
        page = self.getPageNumber()
        text = f"{page} / {page_count}"
        self.setFont("Helvetica", 9)
        page_width, page_height = self._pagesize
        self.drawRightString(page_width - 45, 20, text)


class EnumTableStyle(str, Enum):
    GRID = "GRID"
    BOX = "BOX"
    OUTLINE = "OUTLINE"
    INNERGRID = "INNERGRID"
    LINEBEFORE = "LINEBEFORE"
    LINEAFTER = "LINEAFTER"
    LINEABOVE = "LINEABOVE"
    LINEBELOW = "LINEBELOW"

    ALIGN = "ALIGN"
    VALIGN = "VALIGN"
    LEFTPADDING = "LEFTPADDING"
    RIGHTPADDING = "RIGHTPADDING"
    TOPPADDING = "TOPPADDING"
    BOTTOMPADDING = "BOTTOMPADDING"
    TEXTCOLOR = "TEXTCOLOR"
    FONT = "FONT"
    FONTSIZE = "FONTSIZE"
    LEADING = "LEADING"

    BACKGROUND = "BACKGROUND"
    ROWBACKGROUNDS = "ROWBACKGROUNDS"
    COLBACKGROUNDS = "COLBACKGROUNDS"

    SPAN = "SPAN"
    NOSPLIT = "NOSPLIT"

    WORDWRAP = "WORDWRAP"
    ROWHEIGHT = "ROWHEIGHT"
    COLWIDTH = "COLWIDTH"
    LINESTYLE = "LINESTYLE"
    ROTATE = "ROTATE"

    LEFT = "LEFT"
    RIGHT = "RIGHT"
    CENTER = "CENTER"

    TOP = "TOP"
    MIDDLE = "MIDDLE"
    BOTTOM = "BOTTOM"


class EnumFont(Enum):
    HELVETICA = "Helvetica"
    HELVETICA_BOLD = "Helvetica-Bold"
    HELVETICA_OBLIQUE = "Helvetica-Oblique"
    HELVETICA_BOLD_OBLIQUE = "Helvetica-BoldOblique"

    TIMES = "Times-Roman"
    TIMES_BOLD = "Times-Bold"
    TIMES_ITALIC = "Times-Italic"
    TIMES_BOLD_ITALIC = "Times-BoldItalic"

    COURIER = "Courier"
    COURIER_BOLD = "Courier-Bold"
    COURIER_OBLIQUE = "Courier-Oblique"
    COURIER_BOLD_OBLIQUE = "Courier-BoldOblique"

    SYMBOL = "Symbol"
    ZAPF_DINGBATS = "ZapfDingbats"

    @classmethod
    def list(cls):
        return [font.value for font in cls]


NORMAL_STYLE = ParagraphStyle("normal", fontName="Helvetica", fontSize=10, leading=12)


class HelveticaStyle:
    NORMAL = ParagraphStyle(
        "HelveticaStyle_NORMAL",
        parent=NORMAL_STYLE,
        fontName=EnumFont.HELVETICA.value,
    )
    ITALIC = ParagraphStyle(
        "HelveticaStyle_ITALIC",
        parent=NORMAL_STYLE,
        alignment=1,
        fontName=EnumFont.HELVETICA_OBLIQUE.value,
    )
    BOLD = ParagraphStyle(
        "HelveticaStyle_BOLD",
        parent=NORMAL_STYLE,
        fontName=EnumFont.HELVETICA_BOLD.value,
    )
