import unittest
import os
import tempfile
from services.graph_service import generar_grafico_2d


class TestGraphService(unittest.TestCase):

    def test_generar_grafico_2d_crea_archivo(self):
        """
        Verifica que generar_grafico_2d crea un archivo PNG válido
        cuando se especifica save_path.
        """
        C = [1, 1]
        LI = [[1, 0], [0, 1], [1, 1]]
        LD = [5, 6, 10]

        tmp_dir = tempfile.gettempdir()
        path = os.path.join(tmp_dir, "test_simplex_graph.png")
        try:
            out = generar_grafico_2d(C, LI, LD, save_path=path)
            self.assertEqual(out, path)
            self.assertTrue(os.path.exists(path))
            self.assertGreater(os.path.getsize(path), 0)
        finally:
            if os.path.exists(path):
                os.remove(path)

    def test_generar_grafico_2d_retorna_bytes(self):
        """
        Verifica que generar_grafico_2d retorna bytes cuando
        no se especifica save_path.
        """
        C = [1, 1]
        LI = [[1, 0], [0, 1], [1, 1]]
        LD = [5, 6, 10]

        resultado = generar_grafico_2d(C, LI, LD, save_path=None)
        self.assertIsInstance(resultado, bytes)
        self.assertGreater(len(resultado), 0)

    def test_generar_grafico_2d_con_punto_optimo(self):
        """
        Verifica que generar_grafico_2d acepta un punto óptimo
        para marcar en el gráfico.
        """
        C = [1, 1]
        LI = [[1, 0], [0, 1], [1, 1]]
        LD = [5, 6, 10]
        mark_point = (2.0, 3.0)

        resultado = generar_grafico_2d(C, LI, LD, mark_point=mark_point)
        self.assertIsInstance(resultado, bytes)
        self.assertGreater(len(resultado), 0)

    def test_generar_grafico_2d_error_mas_de_2_variables(self):
        """
        Verifica que generar_grafico_2d lanza ValueError cuando
        se intenta graficar con más de 2 variables.
        """
        C = [1, 1, 1]  # 3 variables
        LI = [[1, 0, 0], [0, 1, 0], [0, 0, 1]]
        LD = [5, 6, 10]

        with self.assertRaises(ValueError) as context:
            generar_grafico_2d(C, LI, LD)
        
        self.assertIn("exactamente 2 variables", str(context.exception))


if __name__ == "__main__":
    unittest.main()
