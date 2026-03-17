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
});
