from locust import HttpUser, task, between


class UsuarioProdutos(HttpUser):
    """
    Simula um usuário navegando pelas APIs do Automation Exercise.

    Comportamento:
    - A cada ciclo, o usuário escolhe uma task aleatória com base no peso.
    - Entre cada ação, espera entre 1 e 3 segundos (simula comportamento humano).
    """

    host = "https://automationexercise.com"
    wait_time = between(1, 3)

    @task(3)
    def listar_produtos(self):
        """
        GET /api/productsList
        Retorna todos os produtos disponíveis no site.
        """
        with self.client.get(
            "/api/productsList",
            name="GET /api/productsList",   
            catch_response=True             
        ) as response:

            if response.status_code == 200:
                # Validação básica: confirma que a resposta tem conteúdo
                if "products" in response.text:
                    response.success()
                else:
                    response.failure("Resposta 200 mas sem campo 'products'")
            else:
                response.failure(f"Status inesperado: {response.status_code}")

    @task(1)
    def buscar_produto(self):
        """
        POST /api/searchProduct
        Envia uma busca pelo termo 'top' e valida o retorno.
        """
        payload = {"search_product": "top"}

        with self.client.post(
            "/api/searchProduct",
            data=payload,                           # envia como form-data
            name="POST /api/searchProduct",
            catch_response=True
        ) as response:

            if response.status_code == 200:
                if "products" in response.text:
                    response.success()
                else:
                    response.failure("Busca retornou 200 mas sem 'products'")
            else:
                response.failure(f"Status inesperado: {response.status_code}")