# Relatório de Vendas com Python e Pandas

**Projeto de portfólio | Python • Pandas • CSV**

Programa que lê vendas de uma loja fictícia, valida os dados, calcula resultados e gera relatórios. Não usa banco de dados, API REST nem Flask.

## O que o programa faz

- Lê uma planilha simples no formato CSV.
- Calcula o faturamento de cada venda e o faturamento total.
- Encontra o produto com maior faturamento.
- Agrupa os resultados por **categoria, produto e mês**.
- Mostra indicadores no terminal e exporta **três relatórios CSV**.
- Exibe uma mensagem útil quando os dados estão inválidos.

## Como executar

1. Instale o Python 3.10 ou superior.
2. No terminal, dentro desta pasta, instale a biblioteca:

   ```bash
   pip install -r requirements.txt
   ```

3. Execute:

   ```bash
   python analise.py
   ```

A pasta `resultados/` será criada automaticamente. Os dados são **fictícios**, apenas para demonstração.

## Como testar com outros dados

Edite `dados/vendas_exemplo.csv` usando Excel ou um editor de texto. As colunas exigidas são:

| Coluna | Exemplo |
|---|---|
| data | 2026-03-18 |
| produto | Garrafa térmica |
| categoria | Utilidades |
| quantidade | 2 |
| preco_unitario | 58.90 |
| regiao | São Paulo |

**Atenção:** no arquivo CSV o separador decimal é ponto; no terminal a moeda aparece no padrão brasileiro.

## Executar testes

```bash
python -m unittest discover -s testes -v
```

## O que estudar antes de colocar no currículo

Abra `GUIA_DE_ESTUDO.md`. É importante entender o papel de `read_csv`, DataFrame, filtros, `groupby`, `sum`, `sort_values` e `to_csv`. A habilidade de explicar as decisões do projeto é mais importante que o número de arquivos.

## Ideias para evoluir depois

- Adicionar um filtro de região.
- Mostrar o faturamento de uma categoria escolhida.
- Gerar um gráfico com Matplotlib depois de aprender a biblioteca.
