import pytest
from fastapi.testclient import TestClient
from main import app, livros

client = TestClient(app)


@pytest.fixture(autouse=True)
def restaurar_livros():
    livros.clear()
    livros.extend([
        {
            "idlivro": 1,
            "titulo": "Dom Casmurro",
            "autor": "Machado de Assis",
            "ano": 1899
        },
        {
            "idlivro": 2,
            "titulo": "O Cortiço",
            "autor": "Aluísio Azevedo",
            "ano": 1890
        }
    ])


def test_home():
    resposta = client.get("/")

    assert resposta.status_code == 200
    assert resposta.json() == {
        "message": "Bem-vindo à Biblioteca Comunitária Saber"
    }


def test_listar_livros():
    resposta = client.get("/livros")

    assert resposta.status_code == 200
    assert len(resposta.json()) == 2


def test_cadastrar_livro():
    novo_livro = {
        "titulo": "Capitães da Areia",
        "autor": "Jorge Amado",
        "ano": 1937
    }

    resposta = client.post("/livros", json=novo_livro)

    assert resposta.status_code == 201
    assert resposta.json()["titulo"] == "Capitães da Areia"
    assert resposta.json()["idlivro"] == 3


def test_buscar_livro():
    resposta = client.get("/livros/1")

    assert resposta.status_code == 200
    assert resposta.json()["titulo"] == "Dom Casmurro"


def test_atualizar_livro():
    dados_atualizados = {
        "titulo": "Dom Casmurro - Nova edição",
        "autor": "Machado de Assis",
        "ano": 1900
    }

    resposta = client.put("/livros/1", json=dados_atualizados)

    assert resposta.status_code == 200
    assert resposta.json()["titulo"] == "Dom Casmurro - Nova edição"
    assert resposta.json()["ano"] == 1900


def test_excluir_livro():
    resposta = client.delete("/livros/1")

    assert resposta.status_code == 200
    assert resposta.json()["message"] == "Livro excluído com sucesso"

    busca = client.get("/livros/1")
    assert busca.status_code == 404
