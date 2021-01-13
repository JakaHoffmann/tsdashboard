let domain_global;
let legenda_global;
let api_name = 0;
let assigned = 0;
let lastId = 0;
let first_time = 0;

function offensesFunction(data) {
    legenda_global = data["legenda"];
    domain_global = data["domene"];
    podatki = data["podatki"];

    makeTabela(podatki);
    cas = document.getElementById("currentTime");
    t = new Date();
    cas.innerHTML = t.toLocaleTimeString(navigator.language, {hour: '2-digit', minute:'2-digit'});
}

function tmp_kartica(api_name, data, assigned) {
    let kartica = document.getElementById(api_name);
    let kartica_offense_id = document.getElementById(api_name + "_offense_id").childNodes;
    let kartica_start_time = document.getElementById(api_name + "_start_time").childNodes;
    
    kartica_offense_id[1].innerHTML = data[0];
    kartica_start_time[1].innerHTML = data[1];
    if (assigned == null) {
        kartica.classList.remove("bg-success");
        kartica.classList.add("bg-danger");
    } else {
        kartica.classList.add("bg-success");
        kartica.classList.remove("bg-danger");
    }
}

function resetTabela() {
    let tabela = document.getElementById("qradar-Table");
    tabela.innerHTML = "";
}

function makeGlavoTabele(tabela) {
    let glavaTabele = ["Tags", "ID", "Opis", "začetek", "M", "S", "R", "C", "kategorija", "status", "prevzel"];
    var header = tabela.createTHead();
    header.classList.add("thead-dark");
    var novaVrstica = header.insertRow();

    for(let i in glavaTabele) {
        let th = document.createElement("TH");
        th.innerHTML = "<div id='idStolpca" + i + "' onclick='sortCol(this.parentElement.parentElement.parentElement, " + i + ")'>" + glavaTabele[i] + "</div>";
        novaVrstica.appendChild(th);
    }
}

function makeOstaleVrstice(tabela, podatki) {
    for (let i in podatki) {
        for (let j in podatki[i]) {
            // USTVARI NOVO VRSTICO
            var novaVrstica = tabela.insertRow();

            // USTVARJANJE NOVIH CELIC - vsako celico posebaj
            var celica0 = novaVrstica.insertCell(0);
            var celica1 = novaVrstica.insertCell(1);
            var celica2 = novaVrstica.insertCell(2);
            var celica3 = novaVrstica.insertCell(3);
            var celica4 = novaVrstica.insertCell(4);
            var celica5 = novaVrstica.insertCell(5);
            var celica6 = novaVrstica.insertCell(6);
            var celica7 = novaVrstica.insertCell(7);
            var celica8 = novaVrstica.insertCell(8);
            var celica9 = novaVrstica.insertCell(9);
            var celica10 = novaVrstica.insertCell(10);

            // STOLPEC 0 - TAGS - tags, domain_id, ...
            let domain_name = searchDomains(i, podatki[i][j].domain_id);
            makeTags(celica0, domain_name, i, podatki[i][j].domain_id);
            
            // STOLPEC 1 - ID - id
            var tmp = Object.values(legenda_global).indexOf(i) + 1;
            celica1.innerHTML = '<a href="/offenses/' + tmp + '/' + podatki[i][j].id + '">' + podatki[i][j].id + '</a>';
            
            // STOLPEC 2 - OPIS - description
            celica2.innerHTML = podatki[i][j].description;

            // STOLPEC 3 - ZAČETEK - start_time
            var date = new Date(podatki[i][j].start_time);
            var str = date.toISOString();
            str = str.replace("T", " ");
            str = str.replace("Z", "") + " UTC";
            celica3.innerHTML = str;

            // STOLPEC 4 - M - magnitude
            celica4.innerHTML = podatki[i][j].magnitude;

            // STOLPEC 5 - S - severity
            celica5.innerHTML = podatki[i][j].severity;

            // STOLPEC 6 - R - relevance
            celica6.innerHTML = podatki[i][j].relevance;

            // STOLPEC 7 - C - credibility
            celica7.innerHTML = podatki[i][j].credibility;

            // STOLPEC 8 - KATEGORIJE - categories
            makeCategories(celica8, podatki[i][j].categories)
            
            // STOLPEC 9 - STATUS - status
            switch (podatki[i][j].status) {
                case "OPEN":
                    celica9.innerHTML = "<div class='w3-container'><span class='badge badge-success'>Open</span></div>";
                    break;
                case "HIDDEN":
                    celica9.innerHTML = "<div class='w3-container'><span class='badge badge-warning'>Hidden</span></div>";
                    break;
                case "CLOSED":
                    celica9.innerHTML = "<div class='w3-container'><span class='badge badge-danger'>Closed</span></div>";
                    break;
            }

            // STOLPEC 10 - PREVZEL - assigned_to
            celica10.innerHTML = '<a href="/stats/user/' + podatki[i][j].assigned_to + '">' + podatki[i][j].assigned_to + '</a>';

            // Kartice
            // TODO: naslednjo IF je treaba pogledat kako dela, če je več API-jev
            if (podatki[i][j].id > lastId) { 
                lastId = podatki[i][j].id;
            }
            if (typeof legenda_global[j] !== 'undefined') {
                if (api_name == 0) {
                    api_name = legenda_global[tmp].replace(/ /g,"_");
                }
            }
            if (first_time == 0) {
                first_time = str;
            }
            if (assigned == 0) {
                assigned = podatki[i][j].assigned_to;
            }
        }
        let data = [lastId, first_time];
        tmp_kartica(api_name, data, assigned);
        api_name = 0;
        assigned = 0;
        lastId = 0;
        first_time = 0;
    }
    
}

function makeTabela(podatki) {
    let tabela = document.getElementById("qradar-Table");
    
    // GLAVA TABELE
    makeGlavoTabele(tabela);
    
    // OSTALE VRSTICE
    makeOstaleVrstice(tabela, podatki);
    
    // KLIK NA "ZAČETEK" STOLPEC
    document.getElementById("idStolpca3").click();
}

function searchDomains(base, domain_id) {
    let tmp;
    for (let i in domain_global) {
        if (domain_global[i].ApiVnasalec == base && domain_global[i].domain_id == domain_id) {
            if (domain_global[i].domain_name) {
                tmp = domain_global[i].domain_name;
            } else {
                if (domain_global[i].ApiVnasalec == "Telekom Slovenije d.d.") {
                    tmp = "TS";
                } else if (domain_global[i].ApiVnasalec == "ts oblak") {
                    tmp = "Oblak";
                }
            }
        }
    }
    return tmp;
}

function makeTags(celica, domain_name, baza, domain_id) {
    if (domain_name == "TS" || domain_name == "Oblak") {
        celica.innerHTML = "<div class='w3-container'><span class='w3-tag w3-round w3-small w3-blue'><a href='/stats/" + domain_name + "' method='post'>" + domain_name + "</a></span></div>";
    } else {
        if (baza == "Telekom Slovenije d.d.") {
            celica.innerHTML = "<div class='w3-container'><span class='w3-tag w3-round w3-small w3-blue'><a href='/stats/TS' method='post'>TS</a><span class='w3-tag w3-round w3-small w3-teal'><a href='/stats/" + domain_name + "' method='post'>" + domain_name + "</a></span></div>";
        } else if (baza == "ts oblak") {
            celica.innerHTML = "<div class='w3-container'><span class='w3-tag w3-round w3-small w3-blue'><a href='/stats/Oblak' method='post'>Oblak</a><span class='w3-tag w3-round w3-small w3-teal'><a href='/stats/" + domain_name + "' method='post'>" + domain_name + "</a></span></div>";
        }
    }
}

function makeCategories(celica, kategorije) {
    if (kategorije.length > 0) {
        let tmpcat = "";
        for (let i in kategorije) {
            let tmplink = kategorije[i].replace(/ /g, "_");
            if (i != kategorije.length-1) {
                tmpcat += ('<a href="/stats/cat/' + tmplink + '" method="post">' + kategorije[i] + '</a>, ');
            } else {
                tmpcat += ('<a href="/stats/cat/' + tmplink + '" method="post">' + kategorije[i] + '</a>');
            }
        }
        celica.innerHTML = tmpcat;
    } else {
        celica.innerHTML = "Ni kategorij"
    }
}

function sortCol(id, colNumb) {
    var novID = "idStolpca" + colNumb;
    var divStoplca = document.getElementById(novID);
    if (!divStoplca.classList.contains("vecji") && !divStoplca.classList.contains("manjsi")) {
        divStoplca.classList.add("vecji");
        sortTable(id, colNumb, 1);
    } else if (divStoplca.classList.contains("vecji")) {
        divStoplca.classList.remove("vecji");
        divStoplca.classList.add("manjsi");
        sortTable(id, colNumb, 0);
    } else if (divStoplca.classList.contains("manjsi")) {
        divStoplca.classList.add("vecji");
        sortTable(id, colNumb, 1);
    }   
}

function sortTable(idTable, colNumb, smer) {
    var table, rows, switching, i, x, y, shouldSwitch;
    table = idTable;
    switching = true;

    /* Make a loop that will continue until no switching has been done: */
    while (switching) {
        // Start by saying: no switching is done:
        switching = false;
        rows = table.rows;
        //alert("rows: " + rows + " " + table.rows);
        /* Loop through all table rows (except the first, which contains table headers): */
        for (i = 1; i < (rows.length - 1); i++) {
        // Start by saying there should be no switching:
            shouldSwitch = false;
            /* Get the two elements you want to compare, one from current row and one from the next: */
            x = rows[i].getElementsByTagName("td")[colNumb];
            y = rows[i + 1].getElementsByTagName("td")[colNumb];
            // Check if the two rows should switch place:
            // alert("x.inerhtml: " + x.innerHTML.toLowerCase() + " y.inerhtml: " + y.innerHTML.toLowerCase());
            // alert("x number: " + Number(x.innerHTML) + " y number: " + Number(y.innerHTML));
            if (smer == 1) {
                if (isNaN(Number(x.innerHTML)) && isNaN(Number(y.innerHTML))) { // preveri če je vrednost v celicah številka - if: ni številka, else: je številka
                    if (x.innerHTML.toLowerCase() < y.innerHTML.toLowerCase()) {
                        // If so, mark as a switch and break the loop:
                        shouldSwitch = true;
                        break;
                    }
                } else {
                    if (Number(x.innerHTML) < Number(y.innerHTML)) {
                        // If so, mark as a switch and break the loop:
                        shouldSwitch = true;
                        break;
                    }    
                }
            } else {
                if (isNaN(Number(x.innerHTML)) && isNaN(Number(y.innerHTML))) { // preveri če je vrednost v celicah številka - if: ni številka, else: je številka
                    if (x.innerHTML.toLowerCase() > y.innerHTML.toLowerCase()) {
                        // If so, mark as a switch and break the loop:
                        shouldSwitch = true;
                        break;
                    }
                } else {
                    if (Number(x.innerHTML) > Number(y.innerHTML)) {
                        // If so, mark as a switch and break the loop:
                        shouldSwitch = true;
                        break;
                    }    
                }
            }
        }
        if (shouldSwitch) {
            /* If a switch has been marked, make the switch and mark that a switch has been done: */
            rows[i].parentNode.insertBefore(rows[i + 1], rows[i]);
            switching = true;
        }
    }
}

function init() {
    fetch(`${window.origin}/offenses/_init`, {
        method: "POST",
        credentials: "include",
        body: JSON.stringify({"siem": "ALL"}),
        cache: "no-cache",
        headers: new Headers({"content-type": "application/json"})
    })
    .then(function(response) {
        if(response.status !== 200) {
            return ;
        }
        response.json().then(function(data) {
            offensesFunction(data)
        })
    })
}

function checkNew() {
    fetch(`${window.origin}/offenses/_is_new`, {
        method: "POST",
        credentials: "include",
        body: JSON.stringify({"siem": "ALL"}),
        cache: "no-cache",
        headers: new Headers({"content-type": "application/json"})
    })
    .then(function(response) {
        if(response.status !== 200) {
            // console.log(`${response.status}`);
            return ;
        }
        response.json().then(function(data) {
            resetTabela();
            makeTabela(data);
            // console.log(data);
        })
    })
}

function refreshTime() {
    cas = document.getElementById("currentTime");
    t = new Date();
    cas.innerHTML = t.toLocaleTimeString(navigator.language, {hour: '2-digit', minute:'2-digit'});
}

function makeKartica(api_name, data) {}

document.onkeydown = function(event) {
    if (event.keyCode == 122) {
        var element = document.body;
        element.classList.toggle("dark-mode");

        var main_header = document.getElementById("main-header");
        main_header.classList.toggle("hajdinguj");

        var offense_nav = document.getElementById("offense-nav");
        offense_nav.classList.toggle("hajdinguj");

        var main_footer = document.getElementById("main-footer");
        main_footer.classList.toggle("hajdinguj");
    }
}
