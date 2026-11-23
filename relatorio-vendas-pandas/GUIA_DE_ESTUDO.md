# Como entender este projeto

**Objetivo:** entender o código e ser capaz de explicar cada parte, em vez de apenas executar.

1. Abra `dados/vendas_exemplo.csv`. A primeira linha contém os nomes das colunas.
2. Em `analise.py`, localize `carregar_vendas()`. `pd.read_csv()` transforma o arquivo em um **DataFrame** (tabela em memória).
3. A coluna `valor_total` é criada multiplicando `quantidade * preco_unitario`.
4. Em `gerar_relatorios()`, `groupby('categoria')` junta vendas da mesma categoria; `sum()` soma quantidades e faturamento.
5. `sort_values()` ordena as tabelas pelo valor do faturamento.
6. `to_csv()` salva as tabelas resultantes em arquivos, sem precisar de banco de dados.
7. Execute o projeto, depois acrescente uma venda ao CSV e observe o que mudou.

## Perguntas que você precisa saber responder

- O que é um DataFrame?
- Qual é a diferença entre `read_csv()` e `to_csv()`?
- De onde vem a coluna `valor_total`?
- Como você encontra o produto com maior faturamento?
- O que acontece quando um preço é zero ou uma data é inválida?

## Três modificações para fazer sozinho

- [ ] Acrescentar uma categoria e verificar os relatórios.
- [ ] Criar um resumo do faturamento por região, usando `groupby('regiao')`.
- [ ] Exibir também o produto com mais *unidades* vendidas (não necessariamente o de maior faturamento).
