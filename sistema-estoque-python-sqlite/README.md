# Sistema de Gerenciamento de Estoque

Aplicação de terminal desenvolvida em Python com persistência em SQLite para gerenciamento de produtos e movimentações de estoque.

## Tecnologias
- Python 3
- SQLite
- SQL

## Funcionalidades
- Cadastro, consulta, edição e exclusão de produtos
- Busca por ID ou nome
- Entrada e saída de estoque
- Bloqueio de saída acima da quantidade disponível
- Identificação de produtos com estoque baixo
- Persistência local em SQLite
- Validação de entradas e tratamento básico de erros

## Como executar

```bash
python main.py
```

O banco `data/estoque.db` é criado automaticamente na primeira execução.

## Estrutura

```text
sistema-estoque-python-sqlite/
├── main.py
├── estoque.py
├── database.py
├── README.md
├── requirements.txt
└── .gitignore
```

## Conceitos demonstrados
CRUD, funções, regras de negócio, validação, tratamento de erros, SQL e persistência com SQLite.

## Contexto
Projeto de portfólio desenvolvido durante a graduação em Engenharia de Software para consolidar fundamentos de Python e introduzir banco de dados relacional.
