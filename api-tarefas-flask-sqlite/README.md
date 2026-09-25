# API REST de Gerenciamento de Tarefas

API REST desenvolvida em Python com Flask e SQLite para praticar conceitos de Back-end, HTTP, CRUD e banco de dados.

## Tecnologias
- Python 3
- Flask
- SQLite
- SQL
- JSON / HTTP

## Funcionalidades
- Criar tarefas
- Listar todas as tarefas
- Consultar tarefa por ID
- Atualizar tarefa inteira ou parcialmente
- Alterar status
- Excluir tarefa
- Filtrar tarefas por status
- Validação de dados e respostas HTTP adequadas

## Status disponíveis
- `pendente`
- `em andamento`
- `concluida`

## Como executar

```bash
python -m venv .venv
```

Windows:
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

A API ficará disponível em `http://127.0.0.1:5000`.

## Endpoints principais

| Método | Rota | Função |
|---|---|---|
| POST | `/api/tarefas` | Criar tarefa |
| GET | `/api/tarefas` | Listar tarefas |
| GET | `/api/tarefas/<id>` | Buscar tarefa |
| PUT | `/api/tarefas/<id>` | Substituir dados da tarefa |
| PATCH | `/api/tarefas/<id>` | Atualizar parte da tarefa |
| DELETE | `/api/tarefas/<id>` | Excluir tarefa |

Filtro por status:
```text
GET /api/tarefas?status=pendente
```

### Exemplo de criação

```json
{
  "titulo": "Estudar Flask",
  "descricao": "Revisar rotas e métodos HTTP",
  "status": "pendente"
}
```

O banco `data/tarefas.db` e a tabela necessária são criados automaticamente quando a aplicação é carregada.

## Conceitos demonstrados
API REST, CRUD, rotas, JSON, métodos HTTP, códigos de status, validação, SQL e persistência em SQLite.

## Contexto
Projeto de portfólio criado durante a graduação em Engenharia de Software, com foco na evolução para desenvolvimento Back-end, APIs e banco de dados.
