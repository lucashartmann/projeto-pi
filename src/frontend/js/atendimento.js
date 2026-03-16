async function listarAtendimentos() {
    try {
        const resposta = await fetch("http://127.0.0.1:8000/atendimentos/");

        if (!resposta.ok) {
            throw new Error(`HTTP ${resposta.status}`);
        }

        return await resposta.json();
    } catch (erro) {
        console.error("Falha ao conectar com o backend:", erro);
        return null;
    }
}


async function carregarAtendimentos() {
    const dados = await listarAtendimentos();
    const section = document.getElementById("container_horizontal");

    if (!section || !dados) return;

    for (let i = 0; i < 5; i++) {
        const div_recem_cadastrados = document.getElementById("container_cadastrados");
        const div_card = document.createElement("div");
        div_card.id = "card_cadastrado";
        div_card.onclick = () => abrirAtendimento(dados[i].id);
        div_card.innerHTML = `
            <h2>Nome ${dados[i].cliente.nome}</h2>
            <p>Idade ${dados[i].cliente.idade}</p>
            <p>Telefone ${dados[i].cliente.telefone}</p>
            <p>Email ${dados[i].cliente.email}</p>
        `;
        div_recem_cadastrados.appendChild(div_card);
    }

    for (const atendimento of dados) {
        if (atendimento.status === "Em andamento") {
            const div_em_andamento = document.getElementById("container_em_andamento");
            if (!div_em_andamento) continue;
            const div_card = document.createElement("div");
            div_card.id = "card_cadastrado";
            div_card.onclick = () => abrirAtendimento(dados[i].id);
            div_card.innerHTML = `
                <h2>Nome ${dados[i].cliente.nome}</h2>
                <p>Idade ${dados[i].cliente.idade}</p>
                <p>Telefone ${dados[i].cliente.telefone}</p>
                <p>Email ${dados[i].cliente.email}</p>
            `;
            div_em_andamento.appendChild(div_card);
        } else if (atendimento.status === "Pendente") {
            const div_pendente = document.getElementById("container_esperando");
            if (!div_pendente) continue;
            const div_card = document.createElement("div");
            div_card.id = "card_cadastrado";
            div_card.onclick = () => abrirAtendimento(dados[i].id);
            div_card.innerHTML = `
                <h2>Nome ${dados[i].cliente.nome}</h2>
                <p>Idade ${dados[i].cliente.idade}</p>
                <p>Telefone ${dados[i].cliente.telefone}</p>
                <p>Email ${dados[i].cliente.email}</p>
            `;
            div_pendente.appendChild(div_card);
        }
    }

}


window.addEventListener("DOMContentLoaded", () => {
    carregarAtendimentos();
});

async function abrirAtendimento(atendimento_id) {
    sessionStorage.setItem("atendimento_id", atendimento_id);
    window.location.href = "html/dados-atendimento.html";
}