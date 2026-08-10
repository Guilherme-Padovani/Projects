// Lista de Tarefas — JavaScript
// Manipulação de DOM, eventos e arrays

const form = document.getElementById("form-tarefa");
const input = document.getElementById("input-tarefa");
const lista = document.getElementById("lista-tarefas");
const contador = document.getElementById("contador");

let tarefas = [];

function atualizarContador() {
  const pendentes = tarefas.filter((t) => !t.concluida).length;
  contador.textContent = `${pendentes} tarefa${pendentes === 1 ? "" : "s"} pendente${pendentes === 1 ? "" : "s"}`;
}

function renderizarTarefas() {
  lista.innerHTML = "";

  tarefas.forEach((tarefa) => {
    const item = document.createElement("li");
    if (tarefa.concluida) item.classList.add("concluida");

    const texto = document.createElement("span");
    texto.textContent = tarefa.texto;
    texto.addEventListener("click", () => alternarConclusao(tarefa.id));

    const botaoRemover = document.createElement("button");
    botaoRemover.textContent = "Remover";
    botaoRemover.addEventListener("click", () => removerTarefa(tarefa.id));

    item.appendChild(texto);
    item.appendChild(botaoRemover);
    lista.appendChild(item);
  });

  atualizarContador();
}

function adicionarTarefa(texto) {
  tarefas.push({ id: Date.now(), texto, concluida: false });
  renderizarTarefas();
}

function alternarConclusao(id) {
  tarefas = tarefas.map((t) =>
    t.id === id ? { ...t, concluida: !t.concluida } : t
  );
  renderizarTarefas();
}

function removerTarefa(id) {
  tarefas = tarefas.filter((t) => t.id !== id);
  renderizarTarefas();
}

form.addEventListener("submit", (event) => {
  event.preventDefault();
  const texto = input.value.trim();
  if (!texto) return;

  adicionarTarefa(texto);
  input.value = "";
  input.focus();
});

renderizarTarefas();
