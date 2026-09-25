# Sistema Web de Gerenciamento de Chamados

Aplicação web para cadastro e acompanhamento de chamados de suporte. O projeto integra interface web, Back-end em Flask e persistência de dados com SQLite.

## Tecnologias
- Python 3
- Flask
- SQLite / SQL
- HTML5
- CSS3

## Funcionalidades
- Abrir chamados
- Listar chamados
- Visualizar detalhes
- Editar e excluir chamados
- Alterar status
- Definir prioridade
- Pesquisar por título, descrição ou categoria
- Filtrar por status e prioridade
- Validação de formulário e página 404

## Como executar

Crie um ambiente virtual:
```bash
python -m venv .venv
```

No Windows:
```bash
.venv\Scripts\activate
```

Instale as dependências:
```bash
pip install -r requirements.txt
```

Execute:
```bash
python app.py
```

Abra no navegador:
```text
http://127.0.0.1:5000
```

O banco `data/chamados.db` e a tabela necessária são criados automaticamente quando a aplicação é carregada.

A aplicação gera automaticamente uma chave segura para as sessões. Opcionalmente, a variável de ambiente `SECRET_KEY` pode ser definida antes da execução.

## Estrutura

```text
sistema-chamados-flask-sqlite/
├── app.py
├── database.py
├── requirements.txt
├── README.md
├── .gitignore
├── static/
│   └── style.css
└── templates/
    ├── base.html
    ├── index.html
    ├── form.html
    ├── detalhes.html
    └── 404.html
```

## Conceitos demonstrados
CRUD, Flask, rotas, formulários, templates, requisições GET/POST, SQL, SQLite, validação, filtros e integração entre Front-end, Back-end e banco de dados.

## Contexto
Projeto de portfólio desenvolvido durante a graduação em Engenharia de Software para praticar uma aplicação completa, com foco principal em Back-end e banco de dados.
