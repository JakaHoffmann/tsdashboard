function userStat(user_podatki) {
    var c = document.getElementById("chart1");
    c.setAttribute("width", 900);
    c.setAttribute("height", 600);
    var ctx = c.getContext("2d");

    ctx.moveTo(0,0);
    ctx.lineTo(900,600);
    ctx.stroke();

    document.getElementById("demo").innerHTML = user_podatki;
}

function userGraf(userdata) {
    var ctx = document.getElementById("chart1");

    imena_strank = Object.keys(userdata);
    st_strank = Object.keys(imena_strank).length;
    document.getElementById("demo0").innerHTML = Object.keys(imena_strank).length;

    var myChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: imena_strank,
            datasets: [{
                label: '# of Votes',
                data: [12, 19, 3, 5, 2, 3],
                backgroundColor: [
                    'rgba(255, 99, 132, 0.2)',
                    'rgba(54, 162, 235, 0.2)',
                    'rgba(255, 206, 86, 0.2)',
                    'rgba(75, 192, 192, 0.2)',
                    'rgba(153, 102, 255, 0.2)',
                    'rgba(255, 159, 64, 0.2)'
                ],
                borderColor: [
                    'rgba(255, 99, 132, 1)',
                    'rgba(54, 162, 235, 1)',
                    'rgba(255, 206, 86, 1)',
                    'rgba(75, 192, 192, 1)',
                    'rgba(153, 102, 255, 1)',
                    'rgba(255, 159, 64, 1)'
                ],
                borderWidth: 1
            }]
        },
        options: {
            scales: {
                yAxes: [{
                    ticks: {
                        beginAtZero: true
                    }
                }]
            }
        }
    });
}

function catStat(cat_podatki) {};

function getUserData() {
    fetch(`${window.origin}/stats/_userdata`, {
        method: "POST",
        credentials: "include",
        body: JSON.stringify({"user": "ALL"}),
        cache: "no-cache",
        headers: new Headers({"content-type": "application/json"})
    })
    .then(function(response) {
        if(response.status !== 200) {
            console.log(`${response.status}`);
            return ;
        }
        response.json().then(function(data) {
            userGraf(data);
        })
    })
}

function getCatData() {
    fetch(`${window.origin}/stats/_catdata`, {
        method: "POST",
        credentials: "include",
        body: JSON.stringify({"cat": "ALL"}),
        cache: "no-cache",
        headers: new Headers({"content-type": "application/json"})
    })
    .then(function(response) {
        if(response.status !== 200) {
            return ;
        }
        response.json().then(function(data) {
            console.log(data);
        })
    })
}


function testFunction() {
    var sw = screen.availWidth;
    var sh = screen.availHeight;

    var c = document.getElementById("myChart");
    c.setAttribute("width", 900);
    c.setAttribute("height", 600);
    var ctx = c.getContext("2d");
    ctx.moveTo(0,0);
    ctx.lineTo(900,600);
    ctx.stroke();

    var c2 = document.getElementById("myChart2");
    c2.setAttribute("width", 900);
    c2.setAttribute("height", 600);
    var ctx2 = c2.getContext("2d");
    ctx2.moveTo(0,0);
    ctx2.lineTo(900,600);
    ctx2.stroke();
}

var c2 = document.getElementById("myChart2");
c2.setAttribute("width", 900);
c2.setAttribute("height", 600);
var ctx2 = c2.getContext("2d");
ctx2.moveTo(0,0);
ctx2.lineTo(900,600);
ctx2.stroke();
