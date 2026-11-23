"""Relatório simples de vendas usando Python e Pandas.

Como executar: python analise.py
Todos os dados usados estão no arquivo dados/vendas_exemplo.csv.
"""

from pathlib import Path
import pandas as pd

PASTA = Path(__file__).resolve().parent
ARQUIVO_VENDAS = PASTA / "dados" / "vendas_exemplo.csv"
PASTA_RESULTADOS = PASTA / "resultados"
COLUNAS = ["data", "produto", "categoria", "quantidade", "preco_unitario", "regiao"]


def carregar_vendas(caminho=ARQUIVO_VENDAS):
    """Lê e valida os dados, criando a coluna 'valor_total'."""
    vendas = pd.read_csv(caminho)
    faltando = [coluna for coluna in COLUNAS if coluna not in vendas.columns]
    if faltando:
        raise ValueError(f"Colunas ausentes no CSV: {', '.join(faltando)}")
    if vendas.empty:
        raise ValueError("O arquivo de vendas está vazio.")

    vendas["data"] = pd.to_datetime(vendas["data"], format="%Y-%m-%d", errors="coerce")
    vendas["quantidade"] = pd.to_numeric(vendas["quantidade"], errors="coerce")
    vendas["preco_unitario"] = pd.to_numeric(vendas["preco_unitario"], errors="coerce")

    if vendas["data"].isna().any():
        raise ValueError("Existe uma data inválida. Use o formato AAAA-MM-DD.")
    if vendas[["quantidade", "preco_unitario"]].isna().any().any():
        raise ValueError("Quantidade e preço precisam ser números válidos.")
    if (vendas["quantidade"] <= 0).any() or (vendas["preco_unitario"] <= 0).any():
        raise ValueError("Quantidade e preço precisam ser maiores que zero.")
    if (vendas["quantidade"] % 1 != 0).any():
        raise ValueError("Quantidade precisa ser um número inteiro.")
    if vendas[["produto", "categoria", "regiao"]].isna().any().any():
        raise ValueError("Produto, categoria e região são campos obrigatórios.")
    for coluna in ["produto", "categoria", "regiao"]:
        if (vendas[coluna].astype(str).str.strip() == "").any():
            raise ValueError(f"Existem valores vazios na coluna '{coluna}'.")

    vendas["valor_total"] = (vendas["quantidade"] * vendas["preco_unitario"]).round(2)
    return vendas


def gerar_relatorios(vendas):
    """Cria três tabelas de análise a partir de um DataFrame."""
    por_categoria = (
        vendas.groupby("categoria", as_index=False)
        .agg(quantidade_vendida=("quantidade", "sum"), faturamento=("valor_total", "sum"))
        .sort_values("faturamento", ascending=False)
    )
    por_produto = (
        vendas.groupby("produto", as_index=False)
        .agg(quantidade_vendida=("quantidade", "sum"), faturamento=("valor_total", "sum"))
        .sort_values("faturamento", ascending=False)
    )
    com_mes = vendas.copy()
    com_mes["mes"] = com_mes["data"].dt.strftime("%Y-%m")
    por_mes = (
        com_mes.groupby("mes", as_index=False)
        .agg(quantidade_vendida=("quantidade", "sum"), faturamento=("valor_total", "sum"))
        .sort_values("mes")
    )
    return {"categorias": por_categoria, "produtos": por_produto, "meses": por_mes}


def reais(valor):
    """Converte um valor numérico para um texto no padrão de moeda brasileira."""
    return f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


def exibir_resumo(vendas, relatorios):
    """Mostra os principais resultados no terminal."""
    faturamento = vendas["valor_total"].sum()
    print("\n" + "=" * 54)
    print("                RELATÓRIO DE VENDAS")
    print("=" * 54)
    print(f"Registros analisados: {len(vendas)}")
    print(f"Unidades vendidas:    {int(vendas['quantidade'].sum())}")
    print(f"Faturamento total:    {reais(faturamento)}")
    print(f"Valor médio por linha de venda: {reais(vendas['valor_total'].mean())}")

    melhor_produto = relatorios["produtos"].iloc[0]
    print(f"Produto com maior faturamento: {melhor_produto['produto']} ({reais(melhor_produto['faturamento'])})")
    print("\nFATURAMENTO POR CATEGORIA")
    for _, linha in relatorios["categorias"].iterrows():
        print(f"  {linha['categoria']:<19} {reais(linha['faturamento']):>13}")
    print("\nFATURAMENTO POR MÊS")
    for _, linha in relatorios["meses"].iterrows():
        print(f"  {linha['mes']:<19} {reais(linha['faturamento']):>13}")


def salvar_relatorios(relatorios, pasta=PASTA_RESULTADOS):
    pasta.mkdir(parents=True, exist_ok=True)
    for nome, tabela in relatorios.items():
        tabela.to_csv(pasta / f"relatorio_{nome}.csv", index=False, encoding="utf-8-sig")
    print(f"\n3 arquivos CSV gerados na pasta: {pasta.name}/")


def main():
    try:
        vendas = carregar_vendas()
        relatorios = gerar_relatorios(vendas)
        exibir_resumo(vendas, relatorios)
        salvar_relatorios(relatorios)
    except (FileNotFoundError, pd.errors.ParserError, ValueError) as erro:
        print(f"Erro ao analisar os dados: {erro}")
        raise SystemExit(1) from erro


if __name__ == "__main__":
    main()
