import requests

def test_api_returns_expected_fields():
   
   # Testa se a API retorna status 200 e os campos esperados no JSON.
  
    url = "https://api.openbrewerydb.org/v1/breweries"
    response = requests.get(url, timeout=10)

    # Verifica se a requisição foi bem-sucedida
    assert response.status_code == 200

    # Converte o JSON retornado em uma lista de dicionários
    data = response.json()

    # Garante que temos uma lista não vazia
    assert isinstance(data, list)
    assert len(data) > 0
    assert isinstance(data[0], dict)

    # Campos que esperamos encontrar em cada registro
    expected_keys = {
        "id", "name", "brewery_type", "address_1", "address_2", "address_3",
        "city", "state_province", "postal_code", "country", "longitude",
        "latitude", "phone", "website_url", "state", "street"
    }

    # Verifica se todos os campos esperados estão presentes no primeiro item
    assert expected_keys.issubset(data[0].keys()), \
        f"Campos ausentes: {expected_keys - data[0].keys()}"


def test_required_fields_are_not_empty():
   
    # Testa se campos obrigatórios não estão vazios ou nulos.
 
    url = "https://api.openbrewerydb.org/v1/breweries"
    response = requests.get(url, timeout=10)
    data = response.json()

    # Campos obrigatórios (considerei campos obrigatórios: id, name, brewery_type e state)
    required_fields = ["id", "name", "brewery_type", "state"]

    # Valida todos os registros retornados pela API
    for idx, brewery in enumerate(data):
        for field in required_fields:
            value = brewery.get(field)
            assert value is not None and value != "", \
                f"Campo '{field}' está vazio ou nulo no registro #{idx + 1}"
