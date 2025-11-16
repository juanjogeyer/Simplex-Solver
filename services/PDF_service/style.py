from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER

# Paleta de colores
COLOR_PRIMARIO_HEX = "#003366"
COLOR_SECUNDARIO_HEX = "#6699CC"
ZEBRA = [colors.whitesmoke, colors.lightgrey]

# Estilo
class SimplexStyles:
    def __init__(self):
        base = getSampleStyleSheet()

        self.titulo_empresa = ParagraphStyle(
            "titulo_empresa",
            parent=base["Heading1"],
            alignment=TA_CENTER,
            textColor=colors.HexColor(COLOR_PRIMARIO_HEX),
            fontSize=20,
            spaceAfter=6,
        )

        self.subtitulo = ParagraphStyle(
            "subtitulo",
            parent=base["Heading2"],
            alignment=TA_CENTER,
            textColor=colors.grey,
            fontSize=12,
            spaceAfter=12,
        )

        self.h2 = ParagraphStyle(
            "h2",
            parent=base["Heading2"],
            textColor=colors.HexColor(COLOR_PRIMARIO_HEX),
            backColor=colors.lightgrey,
            spaceBefore=10,
            spaceAfter=10,
        )

        self.texto = base["BodyText"]
