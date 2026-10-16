
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(
    title="API da Biblioteca Comunitária Saber",
    description="API para gerenciamento do acervo de livros",
    version="1.0.0"
)


# Modelo de dados do livro
class Livro(BaseModel):
    titulo: str
    autor: str
    ano: int


# Lista de livros armazenada em memória
livros = [
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
]

# Próximo ID disponível
proximo_id = 3


# Rota inicial
@app.get("/", tags=["Geral"], summary="Boas-vindas")
def home():
    return {"message": "Bem-vindo à Biblioteca Comunitária Saber"}


# Listar todos os livros
@app.get("/livros", tags=["Livros"], summary="Listar livros")
def listar_livros():
    return livros


# Buscar livro pelo ID
@app.get("/livros/{idlivro}", tags=["Livros"], summary="Buscar livro por ID")
def buscar_livro(idlivro: int):
    for livro in livros:
        if livro["idlivro"] == idlivro:
            return livro

    raise HTTPException(
        status_code=404,
        detail="Livro não encontrado"
    )


# Buscar livros pelo nome completo do autor
@app.get("/livros/autor/{nome}", tags=["Livros"], summary="Buscar livros por autor")
def buscar_por_autor(nome: str):
    encontrados = []

    for livro in livros:
        if livro["autor"].lower() == nome.lower():
            encontrados.append(livro)

    return encontrados


# Cadastrar um novo livro
@app.post("/livros", tags=["Livros"], summary="Cadastrar livro", status_code=201)
def cadastrar_livro(livro: Livro):
    global proximo_id

    novo_livro = {
        "idlivro": proximo_id,
        "titulo": livro.titulo,
        "autor": livro.autor,
        "ano": livro.ano
    }

    livros.append(novo_livro)
    proximo_id += 1

    return novo_livro


# Atualizar um livro existente
@app.put("/livros/{idlivro}", tags=["Livros"], summary="Atualizar livro")
def atualizar_livro(idlivro: int, dados: Livro):
    for livro in livros:
        if livro["idlivro"] == idlivro:
            livro["titulo"] = dados.titulo
            livro["autor"] = dados.autor
            livro["ano"] = dados.ano

            return livro

    raise HTTPException(
        status_code=404,
        detail="Livro não encontrado"
    )


# Excluir um livro
@app.delete("/livros/{idlivro}", tags=["Livros"], summary="Excluir livro")
def excluir_livro(idlivro: int):
    for livro in livros:
        if livro["idlivro"] == idlivro:
            livros.remove(livro)
            return {"message": "Livro excluído com sucesso"}

    raise HTTPException(
        status_code=404,
        detail="Livro não encontrado"
    )
