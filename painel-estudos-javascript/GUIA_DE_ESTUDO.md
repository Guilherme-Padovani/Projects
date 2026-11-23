# Entendendo o Painel de Estudos

1. Abra `index.html` e identifique os IDs dos elementos: `#form-sessao`, `#lista-sessoes` e `#grafico`.
2. Procure `document.querySelector` em `script.js`: ele encontra elementos da página para o JavaScript modificar.
3. `addEventListener('submit', ...)` reage ao envio do formulário.
4. `sessoes.push(...)` adiciona um objeto à lista em memória.
5. `reduce()` soma a duração das sessões; `filter()` seleciona sessões; `sort()` ordena o histórico.
6. `textContent` preenche os textos com segurança, sem interpretar HTML digitado pelo usuário.
7. `salvarDados()` usa `JSON.stringify()` e `localStorage.setItem()` para salvar os dados no navegador. `carregarDados()` faz o caminho inverso. Se isso é novidade, estude essas duas funções devagar.
8. `atualizarTela()` chama as funções que atualizam cartões, gráfico e histórico.

## Exercícios para você fazer

- [ ] Adicione uma opção 'Inglês' à lista de áreas e ao seletor.
- [ ] Troque a meta de 10 para 6 horas e observe o indicador.
- [ ] Altere a ordem para exibir as sessões mais antigas primeiro.
- [ ] Explique a diferença entre uma variável JavaScript e um elemento HTML.
- [ ] Explique por que usar `textContent` para exibir o assunto.

## Perguntas de entrevista

- Como os dados são mostrados na tela?
- Como os filtros funcionam?
- O que acontece se eu recarregar a página?
- Por que você valida o tempo informado no formulário?
