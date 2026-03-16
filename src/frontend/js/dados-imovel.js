function setupDados(dados) {
    var div = document.getElementById("dados_imovel");
    let imagensHtml = "";
    if (dados.anuncio.imagens && dados.anuncio.imagens.length > 0) {
        imagensHtml += `<img src="data:image/jpeg;base64,${dados.anuncio.imagens[0]}" alt="Imagem do imóvel" />`;
        imagensHtml += `<ul id="ul_imagens">`;
        for (const imagem of dados.anuncio.imagens) {
            imagensHtml += `<li><img src="data:image/jpeg;base64,${imagem}" alt="Imagem do imóvel" /></li>`;
        }
        imagensHtml += `</ul>`;
    }

    let html = `
        <div id="div_pai">
            <div id="div_titulo">
                <h3>${dados.anuncio.titulo}</h3>
                <p>${dados.endereco.rua}, ${dados.endereco.numero}, ${dados.endereco.bairro}</p>
                ${imagensHtml}
            </div>
            <h3>Descrição</h3>
            <p>${dados.anuncio.descricao}</p>
        </div>
        <div id="entrar_contato">
            <div>
                <button>Agendar Visita</button>
                <button id="whatsapp">Whatsapp</button>
            </div>
            <div>
                <label id="condominio">Condominio: <p style='color:green;'>${dados.valor_condominio}</p></label>
                <div>
                    <label id="iptu">IPTU: <p style='color:green;'>${dados.valor_iptu}</p></label>
                    <button id="bt_contato">Entrar em contato</button>
                    <label>Um especialista irá entrar em contato por email ou whatsapp</label>
                </div>
            </div>
    `;
    div.innerHTML = html;
    
    //TODO: adicionar filtros, localizacao, valores, etc
}

async function getDadosImovel(id) {
    console.log("Buscando dados do imóvel com id:", id);
    try {
        const resposta = await fetch(`http://127.0.0.1:8000/imoveis/${id}/`,
            {
                method: "GET",
                headers: {
                    "Content-Type": "application/json"
                }
            }
        );

        if (!resposta.ok) {
            throw new Error(`HTTP ${resposta.status}`);
        }

        return await resposta.json();
    } catch (erro) {
        console.error("Falha ao conectar com o backend:", erro);
        return null;
    }

}

window.addEventListener("DOMContentLoaded", async () => {
    id = sessionStorage.getItem("imovel_id");
    if (!id) {
        alert("Imóvel não encontrado!");
        window.location.href = "../html/index.html";
        return;
    }
    dados = await getDadosImovel(id);
    if (dados) {
        setupDados(dados);
    }
});