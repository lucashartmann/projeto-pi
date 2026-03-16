async function listarImoveis() {
    try {
        const resposta = await fetch("http://127.0.0.1:8000/imoveis/");

        if (!resposta.ok) {
            throw new Error(`HTTP ${resposta.status}`);
        }

        return await resposta.json();
    } catch (erro) {
        console.error("Falha ao conectar com o backend:", erro);
        return null;
    }
}


async function carregarAnuncios() {
    const dados = await listarImoveis();
    const section = document.getElementById("anuncios");

    console.log(dados)

    if (!section || !dados) return;

    let html = "";
    for (const imovel of dados) {
        const b64 = imovel.anuncio?.imagens?.[0] || "";
        const preco = imovel.endereco.valor_venda
            ? `<p>Preço: <span>${imovel.endereco.valor_venda}</span></p>`
            : (imovel.endereco.valor_aluguel ? `<p>${imovel.endereco.valor_aluguel}</p>` : "");
        html += `
            <div class="anuncio_imovel" onclick="abrirAnuncio(${imovel.id})">
                <img src="data:image/jpeg;base64,${b64}" />
                <h2>${imovel.anuncio.p_titulo}</h2>
                <p>${imovel.endereco.rua}, ${imovel.endereco.numero}, ${imovel.endereco.bairro}</p>
                ${preco}
                <p>${imovel.anuncio.descricao}</p>
            </div>
        `;
    }
    section.innerHTML = html;

    imovelPrincipal(dados);
    bannerImoveis(dados);
}

function mudarOrdem() {
    const section = document.getElementById("container_resultado");
    filtro = document.getElementById("select_filtro").value;
    botao = document.getElementById("seta");
    botao.textContent = botao.textContent === "⬇️" ? "⬆️" : "⬇️";
    if (!section) return;
}

function filtrar() {
    filtro = document.getElementById("select_filtro").value;
    const section = document.getElementById("container_resultado");
    if (!section) return;
}

window.addEventListener("DOMContentLoaded", () => {
    carregarAnuncios();
});

async function abrirAnuncio(imovel_id) {
    sessionStorage.setItem("imovel_id", imovel_id);
    window.location.href = "html/dados-imovel.html";
}