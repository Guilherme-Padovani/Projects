# Foco — Painel de Estudos

**Projeto de portfólio | JavaScript, HTML5 e CSS3**

Painel interativo para registrar tempo de estudo, acompanhar indicadores e visualizar quanto tempo foi dedicado a diferentes tecnologias. Não usa React, Next.js, APIs nem bancos de dados.


![Prévia da interface](preview.png)

## Funcionalidades

- Criar sessões informando assunto, área, duração e data.
- Calcular tempo total, número de sessões e média de duração.
- Mostrar barras comparando o tempo por área.
- Filtrar as sessões por assunto ou tecnologia.
- Excluir sessões e limpar o histórico.
- Salvar os registros **neste navegador** usando `localStorage` (conceito simples explicado no guia).
- Carregar dados demonstrativos para explorar a interface.

## Como usar

Abra `index.html` em um navegador. Não exige instalação. Caso o navegador bloqueie armazenamento em arquivos locais, execute um servidor simples a partir desta pasta:

```bash
python -m http.server 8000
```

Acesse `http://localhost:8000`.

## Conceitos utilizados

- Estrutura de página com HTML e responsividade com CSS.
- Formulários, eventos (`addEventListener`) e manipulação do DOM.
- Arrays e funções (`map`, `filter`, `reduce`, `sort`).
- Validação dos campos do formulário.
- `localStorage` para manter dados após recarregar (não é banco de dados).

**Importante:** se ainda não estudou `localStorage`, leia `GUIA_DE_ESTUDO.md` e experimente remover a função de persistência para entender a diferença. Só cite essa tecnologia numa entrevista depois de compreendê-la.

## Ideias para evoluir depois

- Permitir editar uma sessão.
- Criar metas diferentes para cada matéria.
- Exibir somente registros desta semana.
