from typing import List,  Any
from reportlab.lib import colors
from reportlab.platypus import (
    Table,
    TableStyle
)
from . import COLOR_SECUNDARIO_HEX, ZEBRA

class TableBuilder:
    @staticmethod
    def build_table(
        data: List[List[Any]],
        header_color: str = COLOR_SECUNDARIO_HEX,
        zebra: List = ZEBRA,
    ) -> Table:

        tabla = Table(data)

        tabla.setStyle(
            TableStyle(
                [
                    ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor(header_color)),
                    ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                    ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                    ("GRID", (0, 0), (-1, -1), 0.5, colors.black),
                    ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                    ("ROWBACKGROUNDS", (0, 1), (-1, -1), zebra),
                ]
            )
        )

        return tabla