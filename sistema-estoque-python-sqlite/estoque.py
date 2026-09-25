from database import conectar

ESTOQUE_BAIXO = 3


def cadastrar_produto(nome, preco, quantidade, categoria):
    nome = nome.strip()
    categoria = categoria.strip()

    if not nome or not categoria:
        raise ValueError("Nome e categoria são obrigatórios.")
    if preco < 0:
        raise ValueError("O preço não pode ser negativo.")
    if quantidade < 0:
        raise ValueError("A quantidade não pode ser negativa.")

    with conectar() as conexao:
        cursor = conexao.execute(
            "INSERT INTO produtos (nome, preco, quantidade, categoria) VALUES (?, ?, ?, ?)",
            (nome, preco, quantidade, categoria),
        )
        return cursor.lastrowid


def listar_produtos():
    with conectar() as conexao:
        return conexao.execute(
            "SELECT id, nome, preco, quantidade, categoria FROM produtos ORDER BY id"
        ).fetchall()


def buscar_por_id(produto_id):
    with conectar() as conexao:
        return conexao.execute(
            "SELECT id, nome, preco, quantidade, categoria FROM produtos WHERE id = ?",
            (produto_id,),
        ).fetchone()


def buscar_por_nome(nome):
    with conectar() as conexao:
        return conexao.execute(
            """
            SELECT id, nome, preco, quantidade, categoria
            FROM produtos
            WHERE nome LIKE ?
            ORDER BY nome
            """,
            (f"%{nome.strip()}%",),
        ).fetchall()


def atualizar_produto(produto_id, nome, preco, quantidade, categoria):
    if buscar_por_id(produto_id) is None:
        return False

    nome = nome.strip()
    categoria = categoria.strip()

    if not nome or not categoria:
        raise ValueError("Nome e categoria são obrigatórios.")
    if preco < 0 or quantidade < 0:
        raise ValueError("Preço e quantidade não podem ser negativos.")

    with conectar() as conexao:
        conexao.execute(
            """
            UPDATE produtos
            SET nome = ?, preco = ?, quantidade = ?, categoria = ?
            WHERE id = ?
            """,
            (nome, preco, quantidade, categoria, produto_id),
        )
    return True


def excluir_produto(produto_id):
    with conectar() as conexao:
        cursor = conexao.execute("DELETE FROM produtos WHERE id = ?", (produto_id,))
        return cursor.rowcount > 0


def registrar_entrada(produto_id, quantidade):
    if quantidade <= 0:
        raise ValueError("A quantidade de entrada deve ser maior que zero.")

    produto = buscar_por_id(produto_id)
    if produto is None:
        return False

    with conectar() as conexao:
        conexao.execute(
            "UPDATE produtos SET quantidade = quantidade + ? WHERE id = ?",
            (quantidade, produto_id),
        )
    return True


def registrar_saida(produto_id, quantidade):
    if quantidade <= 0:
        raise ValueError("A quantidade de saída deve ser maior que zero.")

    produto = buscar_por_id(produto_id)
    if produto is None:
        return "nao_encontrado"
    if quantidade > produto["quantidade"]:
        return "estoque_insuficiente"

    with conectar() as conexao:
        conexao.execute(
            "UPDATE produtos SET quantidade = quantidade - ? WHERE id = ?",
            (quantidade, produto_id),
        )
    return "ok"


def produtos_com_estoque_baixo(limite=ESTOQUE_BAIXO):
    with conectar() as conexao:
        return conexao.execute(
            """
            SELECT id, nome, preco, quantidade, categoria
            FROM produtos
            WHERE quantidade <= ?
            ORDER BY quantidade, nome
            """,
            (limite,),
        ).fetchall()
