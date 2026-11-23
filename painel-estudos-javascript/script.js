// Painel de Estudos - JavaScript puro, sem bibliotecas externas.
// Os dados ficam apenas neste navegador usando localStorage.

const CHAVE_DADOS = "foco_sessoes_v1";
const META_MINUTOS = 600; // 10 horas, apenas para exemplo
const AREAS = ["Python", "JavaScript", "HTML e CSS", "Outros"];

const form = document.querySelector("#form-sessao");
const busca = document.querySelector("#busca");
const filtroArea = document.querySelector("#filtro-area");
const listaSessoes = document.querySelector("#lista-sessoes");
const mensagemForm = document.querySelector("#mensagem-form");

let sessoes = carregarDados();

// Evita problemas de fuso horário ao colocar a data atual no campo.
function dataHoje() {
  const hoje = new Date();
  const ano = hoje.getFullYear();
  const mes = String(hoje.getMonth() + 1).padStart(2, "0");
  const dia = String(hoje.getDate()).padStart(2, "0");
  return `${ano}-${mes}-${dia}`;
}

document.querySelector("#data").value = dataHoje();

function carregarDados() {
  try {
    const texto = localStorage.getItem(CHAVE_DADOS);
    if (!texto) return [];
    const resultado = JSON.parse(texto);
    return Array.isArray(resultado) ? resultado : [];
  } catch (erro) {
    return []; // Se o armazenamento estiver bloqueado, o painel ainda funciona.
  }
}

function salvarDados() {
  try {
    localStorage.setItem(CHAVE_DADOS, JSON.stringify(sessoes));
  } catch (erro) {
    // Algumas configurações privadas do navegador bloqueiam o armazenamento.
    // Nesse caso, os registros funcionam até a página ser recarregada.
  }
}

function textoTempo(total) {
  const horas = Math.floor(total / 60);
  const minutos = total % 60;
  return horas > 0 ? `${horas}h ${String(minutos).padStart(2, "0")}min` : `${minutos}min`;
}

function formatarData(data) {
  const [ano, mes, dia] = data.split("-");
  return `${dia}/${mes}/${ano}`;
}

function atualizarIndicadores() {
  const minutos = sessoes.reduce((soma, sessao) => soma + sessao.minutos, 0);
  const media = sessoes.length ? Math.round(minutos / sessoes.length) : 0;
  document.querySelector("#total-tempo").textContent = textoTempo(minutos);
  document.querySelector("#total-sessoes").textContent = String(sessoes.length);
  document.querySelector("#media-sessao").textContent = textoTempo(media);

  const percentual = Math.round((minutos / META_MINUTOS) * 100);
  document.querySelector("#meta-texto").textContent = `${percentual}%`;
  document.querySelector("#meta-barra").style.width = `${Math.min(percentual, 100)}%`;
}

function atualizarGrafico() {
  const grafico = document.querySelector("#grafico");
  grafico.replaceChildren();
  const totais = AREAS.map((area) => ({
    area,
    minutos: sessoes.filter((sessao) => sessao.area === area)
      .reduce((soma, sessao) => soma + sessao.minutos, 0)
  })).filter((item) => item.minutos > 0);

  if (totais.length === 0) {
    const texto = document.createElement("p");
    texto.className = "chart-empty";
    texto.textContent = "Registre uma sessão para visualizar seu tempo por área.";
    grafico.appendChild(texto);
    return;
  }

  const maior = Math.max(...totais.map((item) => item.minutos));
  totais.forEach((item) => {
    const linha = document.createElement("div");
    linha.className = "chart-row";
    const legenda = document.createElement("div");
    legenda.className = "chart-label";
    const nome = document.createElement("span");
    nome.textContent = item.area;
    const duracao = document.createElement("strong");
    duracao.textContent = textoTempo(item.minutos);
    legenda.append(nome, duracao);
    const trilha = document.createElement("div");
    trilha.className = "chart-track";
    const barra = document.createElement("div");
    barra.className = "chart-fill";
    barra.style.width = `${(item.minutos / maior) * 100}%`;
    trilha.appendChild(barra);
    linha.append(legenda, trilha);
    grafico.appendChild(linha);
  });
}

function atualizarHistorico() {
  const termo = busca.value.trim().toLocaleLowerCase("pt-BR");
  const areaSelecionada = filtroArea.value;
  const visiveis = sessoes
    .filter((sessao) => areaSelecionada === "Todas" || sessao.area === areaSelecionada)
    .filter((sessao) => sessao.assunto.toLocaleLowerCase("pt-BR").includes(termo))
    .sort((a, b) => b.data.localeCompare(a.data));

  listaSessoes.replaceChildren();
  visiveis.forEach((sessao) => {
    const linha = document.createElement("li");
    linha.className = "session";
    const marcador = document.createElement("span");
    marcador.className = "session-mark";
    marcador.setAttribute("aria-hidden", "true");
    marcador.textContent = "◷";

    const conteudo = document.createElement("div");
    conteudo.className = "session-content";
    const titulo = document.createElement("span");
    titulo.className = "session-title";
    titulo.textContent = sessao.assunto; // textContent protege contra HTML inserido pelo usuário.
    const meta = document.createElement("div");
    meta.className = "session-meta";
    meta.textContent = `${sessao.area}  ·  ${formatarData(sessao.data)}`;
    conteudo.append(titulo, meta);

    const tempo = document.createElement("span");
    tempo.className = "session-duration";
    tempo.textContent = textoTempo(sessao.minutos);
    const remover = document.createElement("button");
    remover.className = "delete-btn";
    remover.type = "button";
    remover.textContent = "×";
    remover.setAttribute("aria-label", `Excluir sessão: ${sessao.assunto}`);
    remover.addEventListener("click", () => {
      sessoes = sessoes.filter((item) => item.id !== sessao.id);
      salvarDados();
      atualizarTela();
    });

    linha.append(marcador, conteudo, tempo, remover);
    listaSessoes.appendChild(linha);
  });
  document.querySelector("#vazio").hidden = visiveis.length !== 0;
  document.querySelector("#contador-lista").textContent = `${visiveis.length} sessão(ões) exibida(s)`;
}

function atualizarTela() {
  atualizarIndicadores();
  atualizarGrafico();
  atualizarHistorico();
}

form.addEventListener("submit", (evento) => {
  evento.preventDefault();
  const assunto = document.querySelector("#assunto").value.trim();
  const area = document.querySelector("#materia").value;
  const minutos = Number(document.querySelector("#minutos").value);
  const data = document.querySelector("#data").value;

  if (!assunto || !AREAS.includes(area) || !Number.isInteger(minutos) || minutos < 1 || minutos > 600 || !/^\d{4}-\d{2}-\d{2}$/.test(data)) {
    mensagemForm.textContent = "Preencha assunto, área, data e uma duração entre 1 e 600 minutos.";
    return;
  }
  mensagemForm.textContent = "";
  sessoes.push({ id: `${Date.now()}-${Math.random()}`, assunto, area, minutos, data });
  salvarDados();
  form.reset();
  document.querySelector("#data").value = dataHoje();
  atualizarTela();
  document.querySelector("#assunto").focus();
});

busca.addEventListener("input", atualizarHistorico);
filtroArea.addEventListener("change", atualizarHistorico);

document.querySelector("#limpar-tudo").addEventListener("click", () => {
  if (!sessoes.length) return;
  if (window.confirm("Deseja remover todas as sessões salvas?")) {
    sessoes = [];
    salvarDados();
    atualizarTela();
  }
});

document.querySelector("#carregar-exemplos").addEventListener("click", () => {
  const hoje = dataHoje();
  const exemplos = [
    { assunto: "Funções e listas", area: "Python", minutos: 75 },
    { assunto: "DataFrames com Pandas", area: "Python", minutos: 45 },
    { assunto: "Eventos e DOM", area: "JavaScript", minutos: 60 },
    { assunto: "Layout responsivo", area: "HTML e CSS", minutos: 50 }
  ];
  const novos = exemplos.map((exemplo, indice) => ({ ...exemplo, data: hoje, id: `exemplo-${Date.now()}-${indice}` }));
  sessoes.push(...novos);
  salvarDados();
  atualizarTela();
});

atualizarTela();
