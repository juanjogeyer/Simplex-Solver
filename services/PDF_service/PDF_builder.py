from typing import List, Dict, Any, Optional
from reportlab.lib.pagesizes import letter
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Image,
)
from . import COLOR_SECUNDARIO_HEX, COLOR_PRIMARIO_HEX, SimplexStyles, TableBuilder
from schemas import SimplexSolution, Tableau, SimplexResponse

class SimplexPDFBuilder:
    """
    Genera un PDF completo a partir de un SimplexResponse.
    """

    def __init__(self, resultado: Dict[str, Any]):
        self._raw = resultado

        # Configuraciones generales
        self.empresa = "Mi Empresa S.A."
        self.subtitulo = "Reporte del Método Simplex"
        self.logo_path: Optional[str] = None

        self.page_size = letter
        self.margins = dict(right=30, left=30, top=30, bottom=30)

        self.styles = SimplexStyles()

    # Setters
    def set_empresa(self, empresa: str, subtitulo: Optional[str] = None, logo_path: Optional[str] = None):
        self.empresa = empresa
        if subtitulo is not None:
            self.subtitulo = subtitulo
        if logo_path is not None:
            self.logo_path = logo_path
        return self

    def set_page_margins(self, right=30, left=30, top=30, bottom=30):
        self.margins = dict(right=right, left=left, top=top, bottom=bottom)
        return self

    # Validaciones de entradas
    def _validate(self):
        if not isinstance(self._raw, dict):
            raise TypeError("El resultado debe ser un diccionario.")

        if "status" not in self._raw:
            raise ValueError("El resultado no contiene 'status'.")

    # Conversión de Dict utilizando schemas
    def _parse_resultado(self) -> SimplexResponse:
        self._validate()

        status = self._raw.get("status")

        # Solución
        solucion = None
        raw_sol = self._raw.get("solucion")

        if raw_sol:
            solucion = SimplexSolution(
                variables=raw_sol.get("variables", {}),
                valor_optimo=raw_sol.get("valor_optimo"),
            )

        # Tablas
        tablas = []
        for t in self._raw.get("tablas", []):
            tablas.append(
                Tableau(
                    titulo=t.get("titulo", ""),
                    headers=t.get("headers", []),
                    filas=t.get("filas", []),
                    fila_obj=t.get("fila_obj", []),
                )
            )

        return SimplexResponse(status=status, solucion=solucion, tablas=tablas)


    def build(self, nombre_pdf: str = "resultado_simplex.pdf"):
        resultado = self._parse_resultado()

        doc = SimpleDocTemplate(
            nombre_pdf,
            pagesize=self.page_size,
            **self.margins,
        )

        story: List[Any] = []

        # Header
        self._add_header(story)

        # Resultado principal
        self._add_result_section(story, resultado)

        # Tablas intermedias
        self._add_intermediate_tables(story, resultado.tablas)

        # Generar
        doc.build(story)

    # Secciones del informe final
    
    def _add_header(self, story: List[Any]):
        """Encabezado sin portada, todo en la primera página."""
        if self.logo_path:
            try:
                img = Image(self.logo_path, width=150, height=70)
                story.append(img)
                story.append(Spacer(1, 8))
            except Exception:
                print("No se pudo cargar el logo.")

        story.append(Paragraph(self.empresa, self.styles.titulo_empresa))
        story.append(Paragraph(self.subtitulo, self.styles.subtitulo))
        story.append(Spacer(1, 6))

    def _add_result_section(self, story: List[Any], resultado: SimplexResponse):
        """Muestra lo primero: estado, valor óptimo, variables."""
        story.append(Paragraph("Resultado Final", self.styles.h2))
        story.append(Spacer(1, 6))

        story.append(Paragraph(f"<b>Estado del problema:</b> {resultado.status}", self.styles.texto))
        story.append(Spacer(1, 6))

        if resultado.status.lower() == "optimo":
            sol = resultado.solucion

            if sol is not None:
                story.append(
                    Paragraph(f"<b>Valor Óptimo Z:</b> {sol.valor_optimo}", self.styles.texto)
                )
                story.append(Spacer(1, 8))

                # Variables
                story.append(Paragraph("<b>Variables de decisión</b>:", self.styles.texto))

                data_vars = [["Variable", "Valor"]]
                for var, val in sorted(sol.variables.items()):
                    data_vars.append([var, str(val)])

                tabla_vars = TableBuilder.build_table(data_vars, header_color=COLOR_PRIMARIO_HEX)
                story.append(tabla_vars)

                story.append(Spacer(1, 12))

        else:
            story.append(Paragraph("No se encontró una solución óptima.", self.styles.texto))
            story.append(Spacer(1, 8))

    def _add_intermediate_tables(self, story: List[Any], tablas: List[Tableau]):
        """Agrega las tablas de todas las iteraciones."""
        if not tablas:
            return

        story.append(Paragraph("Tablas Intermedias del Proceso Simplex", self.styles.h2))
        story.append(Spacer(1, 8))

        for t in tablas:
            story.append(Paragraph(t.titulo, self.styles.texto))
            story.append(Spacer(1, 5))

            # Construcción de datos
            data = [t.headers]

            for fila in t.filas:
                data.append([str(x) for x in fila])

            if t.fila_obj:
                data.append([str(x) for x in t.fila_obj])

            tabla = TableBuilder.build_table(data, header_color=COLOR_SECUNDARIO_HEX)
            story.append(tabla)
            story.append(Spacer(1, 12))
