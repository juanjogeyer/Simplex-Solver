import unittest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from routers.simplex_router import router


class TestGraphRoutes(unittest.TestCase):

    def setUp(self):
        """Configura la aplicación FastAPI y el cliente de prueba."""
        app = FastAPI()
        app.include_router(router)
        self.client = TestClient(app)

    def test_generate_graph_html_endpoint(self):
        """
        Verifica que el endpoint /generate-graph-html retorna
        una página HTML con una imagen base64 embebida.
        """
        payload = {
            "problem_type": "maximization",
            "C": [3, 5],
            "LI": [[1, 0], [0, 2], [3, 2]],
            "LD": [4, 12, 18],
            "O": ["<=", "<=", "<="]
        }
        
        response = self.client.post("/simplex/generate-graph-html", json=payload)
        
        self.assertEqual(response.status_code, 200)
        body = response.text
        self.assertIn("<img", body)
        self.assertIn("data:image/png;base64", body)

    def test_generate_graph_endpoint(self):
        """
        Verifica que el endpoint /generate-graph retorna
        un archivo PNG válido.
        """
        payload = {
            "problem_type": "maximization",
            "C": [3, 5],
            "LI": [[1, 0], [0, 2], [3, 2]],
            "LD": [4, 12, 18],
            "O": ["<=", "<=", "<="]
        }
        
        response = self.client.post("/simplex/generate-graph", json=payload)
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers["content-type"], "image/png")
        self.assertGreater(len(response.content), 0)

    def test_generate_graph_error_mas_de_2_variables(self):
        """
        Verifica que el endpoint retorna error 400 cuando
        se intenta graficar con más de 2 variables.
        """
        payload = {
            "problem_type": "maximization",
            "C": [3, 5, 2],  # 3 variables
            "LI": [[1, 0, 0], [0, 2, 0], [3, 2, 1]],
            "LD": [4, 12, 18],
            "O": ["<=", "<=", "<="]
        }
        
        response = self.client.post("/simplex/generate-graph-html", json=payload)
        
        self.assertEqual(response.status_code, 400)
        self.assertIn("2 variables", response.text)


if __name__ == "__main__":
    unittest.main()