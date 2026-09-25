from flask import Flask, jsonify, request

from database import conectar, criar_tabela

app = Flask(__name__)
STATUS_VALIDOS = {"pendente", "em andamento", "concluida"}

criar_tabela()


def tarefa_para_dict(tarefa):
    return {
        "id": tarefa["id"],
        "titulo": tarefa["titulo"],
        "descricao": tarefa["descricao"],
        "status": tarefa["status"],
        "data_criacao": tarefa["data_criacao"],
    }


def validar_dados(dados, parcial=False):
    if not isinstance(dados, dict):
        return "O corpo da requisição deve ser um JSON válido."

    if not parcial and "titulo" not in dados:
        return "O campo 'titulo' é obrigatório."

    if "titulo" in dados:
        titulo = dados["titulo"]
        if not isinstance(titulo, str) or not titulo.strip():
            return "O campo 'titulo' deve ser um texto não vazio."

    if "descricao" in dados:
        descricao = dados["descricao"]
        if not isinstance(descricao, str):
            return "O campo 'descricao' deve ser um texto."

    if "status" in dados:
        status = dados["status"]
        if not isinstance(status, str):
            return "O campo 'status' deve ser um texto."
        status = status.strip().lower()
        if status not in STATUS_VALIDOS:
            return "Status inválido. Use: pendente, em andamento ou concluida."

    return None


@app.get("/")
def inicio():
    return jsonify(
        {
            "mensagem": "API de Gerenciamento de Tarefas",
            "endpoints": "/api/tarefas",
        }
    )


@app.post("/api/tarefas")
def criar_tarefa():
    dados = request.get_json(silent=True)
    erro = validar_dados(dados)
    if erro:
        return jsonify({"erro": erro}), 400

    titulo = dados["titulo"].strip()
    descricao = dados.get("descricao", "").strip()
    status = dados.get("status", "pendente").strip().lower()

    with conectar() as conexao:
        cursor = conexao.execute(
            "INSERT INTO tarefas (titulo, descricao, status) VALUES (?, ?, ?)",
            (titulo, descricao, status),
        )
        tarefa = conexao.execute(
            "SELECT * FROM tarefas WHERE id = ?", (cursor.lastrowid,)
        ).fetchone()

    return jsonify(tarefa_para_dict(tarefa)), 201


@app.get("/api/tarefas")
def listar_tarefas():
    status = request.args.get("status", "").strip().lower()

    if status and status not in STATUS_VALIDOS:
        return jsonify({"erro": "Status de filtro inválido."}), 400

    with conectar() as conexao:
        if status:
            tarefas = conexao.execute(
                "SELECT * FROM tarefas WHERE status = ? ORDER BY id DESC", (status,)
            ).fetchall()
        else:
            tarefas = conexao.execute(
                "SELECT * FROM tarefas ORDER BY id DESC"
            ).fetchall()

    return jsonify([tarefa_para_dict(tarefa) for tarefa in tarefas]), 200


@app.get("/api/tarefas/<int:tarefa_id>")
def buscar_tarefa(tarefa_id):
    with conectar() as conexao:
        tarefa = conexao.execute(
            "SELECT * FROM tarefas WHERE id = ?", (tarefa_id,)
        ).fetchone()

    if tarefa is None:
        return jsonify({"erro": "Tarefa não encontrada."}), 404

    return jsonify(tarefa_para_dict(tarefa)), 200


@app.put("/api/tarefas/<int:tarefa_id>")
def substituir_tarefa(tarefa_id):
    dados = request.get_json(silent=True)
    erro = validar_dados(dados)
    if erro:
        return jsonify({"erro": erro}), 400

    titulo = dados["titulo"].strip()
    descricao = dados.get("descricao", "").strip()
    status = dados.get("status", "pendente").strip().lower()

    with conectar() as conexao:
        existe = conexao.execute(
            "SELECT id FROM tarefas WHERE id = ?", (tarefa_id,)
        ).fetchone()
        if existe is None:
            return jsonify({"erro": "Tarefa não encontrada."}), 404

        conexao.execute(
            """
            UPDATE tarefas
            SET titulo = ?, descricao = ?, status = ?
            WHERE id = ?
            """,
            (titulo, descricao, status, tarefa_id),
        )
        tarefa = conexao.execute(
            "SELECT * FROM tarefas WHERE id = ?", (tarefa_id,)
        ).fetchone()

    return jsonify(tarefa_para_dict(tarefa)), 200


@app.patch("/api/tarefas/<int:tarefa_id>")
def atualizar_tarefa(tarefa_id):
    dados = request.get_json(silent=True)
    erro = validar_dados(dados, parcial=True)
    if erro:
        return jsonify({"erro": erro}), 400

    campos_permitidos = {"titulo", "descricao", "status"}
    campos = []
    valores = []

    for campo in campos_permitidos:
        if campo in dados:
            valor = dados[campo]
            if campo in {"titulo", "descricao"}:
                valor = valor.strip()
            if campo == "status":
                valor = valor.strip().lower()
            campos.append(f"{campo} = ?")
            valores.append(valor)

    if not campos:
        return jsonify({"erro": "Informe pelo menos um campo para atualizar."}), 400

    with conectar() as conexao:
        existe = conexao.execute(
            "SELECT id FROM tarefas WHERE id = ?", (tarefa_id,)
        ).fetchone()
        if existe is None:
            return jsonify({"erro": "Tarefa não encontrada."}), 404

        valores.append(tarefa_id)
        conexao.execute(
            f"UPDATE tarefas SET {', '.join(campos)} WHERE id = ?", valores
        )
        tarefa = conexao.execute(
            "SELECT * FROM tarefas WHERE id = ?", (tarefa_id,)
        ).fetchone()

    return jsonify(tarefa_para_dict(tarefa)), 200


@app.delete("/api/tarefas/<int:tarefa_id>")
def excluir_tarefa(tarefa_id):
    with conectar() as conexao:
        cursor = conexao.execute("DELETE FROM tarefas WHERE id = ?", (tarefa_id,))

    if cursor.rowcount == 0:
        return jsonify({"erro": "Tarefa não encontrada."}), 404

    return "", 204


@app.errorhandler(404)
def rota_nao_encontrada(_erro):
    return jsonify({"erro": "Rota não encontrada."}), 404


@app.errorhandler(500)
def erro_interno(_erro):
    return jsonify({"erro": "Erro interno do servidor."}), 500


if __name__ == "__main__":
    app.run(debug=True)
