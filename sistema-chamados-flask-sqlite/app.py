import os
import secrets

from flask import Flask, abort, flash, redirect, render_template, request, url_for

from database import conectar, criar_tabela

app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY") or secrets.token_hex(32)

PRIORIDADES = ["Baixa", "Média", "Alta"]
STATUS = ["Aberto", "Em andamento", "Resolvido"]

criar_tabela()


def validar_chamado(formulario):
    titulo = formulario.get("titulo", "").strip()
    descricao = formulario.get("descricao", "").strip()
    categoria = formulario.get("categoria", "").strip()
    prioridade = formulario.get("prioridade", "").strip()
    status = formulario.get("status", "Aberto").strip()

    if not titulo or not descricao or not categoria:
        return None, "Preencha título, descrição e categoria."
    if prioridade not in PRIORIDADES:
        return None, "Prioridade inválida."
    if status not in STATUS:
        return None, "Status inválido."

    return {
        "titulo": titulo,
        "descricao": descricao,
        "categoria": categoria,
        "prioridade": prioridade,
        "status": status,
    }, None


def buscar_chamado_ou_404(chamado_id):
    with conectar() as conexao:
        chamado = conexao.execute(
            "SELECT * FROM chamados WHERE id = ?", (chamado_id,)
        ).fetchone()
    if chamado is None:
        abort(404)
    return chamado


@app.get("/")
def index():
    pesquisa = request.args.get("q", "").strip()
    status = request.args.get("status", "").strip()
    prioridade = request.args.get("prioridade", "").strip()

    consulta = "SELECT * FROM chamados WHERE 1=1"
    parametros = []

    if pesquisa:
        consulta += " AND (titulo LIKE ? OR descricao LIKE ? OR categoria LIKE ?)"
        termo = f"%{pesquisa}%"
        parametros.extend([termo, termo, termo])

    if status in STATUS:
        consulta += " AND status = ?"
        parametros.append(status)

    if prioridade in PRIORIDADES:
        consulta += " AND prioridade = ?"
        parametros.append(prioridade)

    consulta += " ORDER BY id DESC"

    with conectar() as conexao:
        chamados = conexao.execute(consulta, parametros).fetchall()

    return render_template(
        "index.html",
        chamados=chamados,
        pesquisa=pesquisa,
        status_selecionado=status,
        prioridade_selecionada=prioridade,
        status_opcoes=STATUS,
        prioridades=PRIORIDADES,
    )


@app.route("/chamados/novo", methods=["GET", "POST"])
def novo_chamado():
    if request.method == "POST":
        dados, erro = validar_chamado(request.form)
        if erro:
            flash(erro, "erro")
            return render_template(
                "form.html",
                titulo_pagina="Novo chamado",
                chamado=request.form,
                prioridades=PRIORIDADES,
                status_opcoes=STATUS,
                novo=True,
            )

        with conectar() as conexao:
            cursor = conexao.execute(
                """
                INSERT INTO chamados (titulo, descricao, categoria, prioridade, status)
                VALUES (?, ?, ?, ?, ?)
                """,
                (
                    dados["titulo"],
                    dados["descricao"],
                    dados["categoria"],
                    dados["prioridade"],
                    dados["status"],
                ),
            )
            chamado_id = cursor.lastrowid

        flash("Chamado criado com sucesso.", "sucesso")
        return redirect(url_for("detalhes_chamado", chamado_id=chamado_id))

    return render_template(
        "form.html",
        titulo_pagina="Novo chamado",
        chamado=None,
        prioridades=PRIORIDADES,
        status_opcoes=STATUS,
        novo=True,
    )


@app.get("/chamados/<int:chamado_id>")
def detalhes_chamado(chamado_id):
    chamado = buscar_chamado_ou_404(chamado_id)
    return render_template("detalhes.html", chamado=chamado, status_opcoes=STATUS)


@app.route("/chamados/<int:chamado_id>/editar", methods=["GET", "POST"])
def editar_chamado(chamado_id):
    chamado = buscar_chamado_ou_404(chamado_id)

    if request.method == "POST":
        dados, erro = validar_chamado(request.form)
        if erro:
            flash(erro, "erro")
            return render_template(
                "form.html",
                titulo_pagina="Editar chamado",
                chamado=request.form,
                prioridades=PRIORIDADES,
                status_opcoes=STATUS,
                novo=False,
            )

        with conectar() as conexao:
            conexao.execute(
                """
                UPDATE chamados
                SET titulo = ?, descricao = ?, categoria = ?, prioridade = ?, status = ?
                WHERE id = ?
                """,
                (
                    dados["titulo"],
                    dados["descricao"],
                    dados["categoria"],
                    dados["prioridade"],
                    dados["status"],
                    chamado_id,
                ),
            )

        flash("Chamado atualizado com sucesso.", "sucesso")
        return redirect(url_for("detalhes_chamado", chamado_id=chamado_id))

    return render_template(
        "form.html",
        titulo_pagina="Editar chamado",
        chamado=chamado,
        prioridades=PRIORIDADES,
        status_opcoes=STATUS,
        novo=False,
    )


@app.post("/chamados/<int:chamado_id>/status")
def alterar_status(chamado_id):
    buscar_chamado_ou_404(chamado_id)
    novo_status = request.form.get("status", "").strip()

    if novo_status not in STATUS:
        flash("Status inválido.", "erro")
        return redirect(url_for("detalhes_chamado", chamado_id=chamado_id))

    with conectar() as conexao:
        conexao.execute(
            "UPDATE chamados SET status = ? WHERE id = ?", (novo_status, chamado_id)
        )

    flash("Status atualizado.", "sucesso")
    return redirect(url_for("detalhes_chamado", chamado_id=chamado_id))


@app.post("/chamados/<int:chamado_id>/excluir")
def excluir_chamado(chamado_id):
    buscar_chamado_ou_404(chamado_id)
    with conectar() as conexao:
        conexao.execute("DELETE FROM chamados WHERE id = ?", (chamado_id,))

    flash("Chamado excluído.", "sucesso")
    return redirect(url_for("index"))


@app.errorhandler(404)
def pagina_nao_encontrada(_erro):
    return render_template("404.html"), 404


if __name__ == "__main__":
    app.run(debug=True)
