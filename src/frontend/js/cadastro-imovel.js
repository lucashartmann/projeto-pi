function salvar() {
    var form = document.getElementsByName("form");
    var data = {};

    for (formulario of form) {
        var formData = new FormData(form);
        formData.forEach(function (value, key) {
            data[key] = value;
        });
    };

    if (data) {
        try {
            fetch("http://localhost:3000/estoque/cadastrar/", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify(data)
            })
                .then(response => response.json())
                .then(data => {
                    console.log("Imóvel cadastrado com sucesso:", data);
                })
                .catch(error => {
                    console.error("Erro ao cadastrar imóvel:", error);
                });
        } catch (error) {
            console.error("Erro ao enviar dados do imóvel:", error);
        }

    }

    console.log("Dados do imóvel a serem enviados:", data);
}

function excluir() {
    try {
        fetch("http://localhost:3000/estoque/excluir/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ ref: 1 })
        })
            .then(response => response.json())
            .then(data => {
                console.log("Imóvel excluído com sucesso:", data);
            })
            .catch(error => {
                console.error("Erro ao excluir imóvel:", error);
            });
    } catch (error) {
        console.error("Erro ao enviar dados para exclusão do imóvel:", error);
    }
}

var tabDisplays = {};

function hideAllTabContents() {
    var tabcontent = document.getElementsByClassName("tabcontent");
    for (var i = 0; i < tabcontent.length; i++) {
        tabcontent[i].style.display = "none";
    }
}

function clearActiveTabLinks() {
    var tablinks = document.getElementsByClassName("tablinks");
    for (var i = 0; i < tablinks.length; i++) {
        tablinks[i].classList.remove("active");
    }
}

function findTabButtonByTarget(tabId) {
    var selector = ".tablinks[onclick*=\"'" + tabId + "'\"], .tablinks[onclick*=\"\\\"" + tabId + "\\\"\"]";
    return document.querySelector(selector);
}

function activateTab(tabId, tabButton) {
    var tabPanel = document.getElementById(tabId);
    if (!tabPanel) {
        return;
    }

    hideAllTabContents();
    clearActiveTabLinks();

    tabPanel.style.display = tabDisplays[tabId] || "block";

    if (tabButton) {
        tabButton.classList.add("active");
    } else {
        findTabButtonByTarget(tabId)?.classList.add("active");
    }

    sessionStorage.setItem("activeTab", tabId);
}

function openTab(evento, tabId) {
    activateTab(tabId, evento?.currentTarget || evento?.target || null);
}

async function abrirCadastro(imovel_id) {
    imovel = await getDadosImovel(imovel_id);
    console.log("Dados do imóvel para cadastro:", imovel);
    if (imovel) {
        form = document.getElementById("container_cadastro");

        if (imovel.condominio) {
             document.getElementById("ta_nome_condominio").disabled = true;
        }

        if (imovel.endereco) {
                document.getElementById("ta_rua").value = imovel.endereco.rua || "";
                document.getElementById("ta_bairro").value = imovel.endereco.bairro || "";
                document.getElementById("ta_cidade").value = imovel.endereco.cidade || "";
                document.getElementById("ta_estado").value = imovel.endereco.uf || "";
            }
        }

        
            document.getElementById("ta_numero").value = imovel.endereco.numero || "";
            document.getElementById("ta_complemento").value = imovel.complemento || "";
            document.getElementById("ta_bloco").value = imovel.bloco || "";
            document.getElementById("ta_andar").value = imovel.andar || "";
            document.getElementById("ta_salas").value = imovel.quantidade_salas || "";
            document.getElementById("ta_banheiros").value = imovel.quantidade_banheiros || "";
            <textarea name="ref" id="ta_ref" disabled=True>${imovel.id}</textarea>
            <select name="categoria" id="select_categoria" prompt="Selecionar"></select>
            <select name="situacao" id="select_situacao"></select>
            <select name="estado_imovel" id="select_estado" prompt="Selecionar"></select>
            <select name="ocupacao" id="select_ocupacao" prompt="Selecionar"></select>
            <select name="status" id="select_status" prompt="Selecionar"></select>
           
            <input type="date" placeholder="0000" id="ta_ano_construcao" minlength="4" maxlength="4" name="ano_construcao" value="${imovel.ano_construcao || ""}">
            <input type="number" placeholder="00000-000" id="ta_cep" required minlength="9" maxlength="9" name="cep" value="${imovel.endereco.cep || ""}">
            
            <input type="text" id="ta_numero" type="integer" name="numero" value="${imovel.endereco.numero || ""}">
            <textarea name="complemento" id="ta_complemento">${imovel.complemento || ""}</textarea>
            <textarea name="bloco" id="ta_bloco">${imovel.bloco || ""}</textarea>
            <input type="number" placeholder="00" id="ta_andar" minlength="1" maxlength="2" name="andar" value="${imovel.andar || ""}">
            <textarea id="ta_bairro" disabled=True name="bairro">${imovel.endereco.bairro || ""}</textarea>
            <input type="text" disabled=True, placeholder="XX" id="ta_estado" minlength="2" maxlength="2" name="uf" value="${imovel.endereco.uf || ""}">
            <input type="number" placeholder="00" id="ta_salas" minlength="1" maxlength="2" name="quantidade_salas" value="${imovel.quantidade_salas || ""}">
            <input type="number" placeholder="00" id="ta_banheiros" minlength="1" maxlength="2" name="quantidade_banheiros" value="${imovel.quantidade_banheiros || ""}">
            <input type="number" placeholder="00" id="ta_vagas" minlength="1" maxlength="2" name="quantidade_vagas" value="${imovel.quantidade_vagas || ""}">
            <input type="number" placeholder="00" id="ta_varandas" minlength="1" maxlength="2" name="quantidade_varandas" value="${imovel.quantidade_varandas || ""}">
            <input type="number" placeholder="00" id="ta_quartos" minlength="1" maxlength="2" name="quantidade_quartos" value="${imovel.quantidade_quartos || ""}">
            <input type="number" id="ta_area_total" type="number" name="area_total" value="${imovel.area_total || ""}">
            <input type="number" id="ta_area_privativa" type="number" name="area_privativa" value="${imovel.area_privativa || ""}">
            <input type="number" id="ta_venda" type="number" name="valor_venda}" value="${imovel.valor_venda || ""}">
            <input type="number" id="ta_aluguel" type="number}" name="valor_aluguel" value="${imovel.valor_aluguel || ""}">
            <input type="number" id="ta_condominio" name="valor_condominio" type="number" value="${imovel.valor_condominio || ""}">
            <input type="number" name="iptu" id="ta_iptu" type="number" value="${imovel.valor_iptu || ""}">
        `;

    } else {
        alert("Imóvel não encontrado!");
        window.location.href = "estoque.html";
    }
}

window.addEventListener("DOMContentLoaded", function () {
    var tabcontent = document.getElementsByClassName("tabcontent");

    for (var i = 0; i < tabcontent.length; i++) {
        var panel = tabcontent[i];
        var inlineDisplay = panel.style.display;
        if (inlineDisplay && inlineDisplay !== "none") {
            tabDisplays[panel.id] = inlineDisplay;
        } else {
            var computedDisplay = window.getComputedStyle(panel).display;
            tabDisplays[panel.id] = computedDisplay !== "none" ? computedDisplay : "block";
        }
    }

    var savedTabId = sessionStorage.getItem("activeTab");
    var defaultTabId = tabcontent.length > 0 ? tabcontent[0].id : null;
    var initialTabId = savedTabId && document.getElementById(savedTabId) ? savedTabId : defaultTabId;

    if (initialTabId) {
        activateTab(initialTabId, null);
    }

    var imovel_id = this.sessionStorage.getItem("imovel_id_estoque") || null;
    if (imovel_id) {
        sessionStorage.removeItem("imovel_id_estoque");
        abrirCadastro(imovel_id);
    }
});
