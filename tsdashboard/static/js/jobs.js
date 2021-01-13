
var starTrigger;

function triggerFunc() {
    var triggerSelect = document.getElementById("trigerSelect");
    var triggerValue = triggerSelect.options[triggerSelect.selectedIndex].value;
    if (triggerValue == "cron") {
        // naredimo neki, če je CRON
        console.log("CRON");
        glavaDodaj = [
            "year",
            "month",
            "day",
            "week",
            "day_of_week",
            "hour",
            "minute",
            "second",
            "start_date",
            "end_date",
            "timezone",
            "jitter"
        ]

        // year (int|str) – 4-digit year
        // month (int|str) – month (1-12)
        // day (int|str) – day of the (1-31)
        // week (int|str) – ISO week (1-53)
        // day_of_week (int|str) – number or name of weekday (0-6 or mon,tue,wed,thu,fri,sat,sun)
        // hour (int|str) – hour (0-23)
        // minute (int|str) – minute (0-59)
        // second (int|str) – second (0-59)
        // start_date (datetime|str) – earliest possible date/time to trigger on (inclusive)
        // end_date (datetime|str) – latest possible date/time to trigger on (inclusive)
        // timezone (datetime.tzinfo|str) – time zone to use for the date/time calculations (defaults to scheduler timezone)
        // jitter (int|None) – advance or delay the job execution by jitter seconds at most.

    } else {
        // naredimo neki, če je INTERVAL
        console.log("INTERVAL")
        glavaDodajInterval = [
            "weeks",
            "days",
            "hours",
            "minutes",
            "seconds",
            "start_date",
            "end_date",
            "timezone",
            "jitter"
        ]
        
        // weeks (int) – number of weeks to wait
        // days (int) – number of days to wait
        // hours (int) – number of hours to wait
        // minutes (int) – number of minutes to wait
        // seconds (int) – number of seconds to wait
        // start_date (datetime|str) – starting point for the interval calculation
        // end_date (datetime|str) – latest possible date/time to trigger on
        // timezone (datetime.tzinfo|str) – time zone to use for the date/time calculations
        // jitter (int|None) – advance or delay the job execution by jitter seconds at most.

    }
}

function reloadButton() {
    location.reload();
}

function checkTimer() {
    editTimerID();
    checkTrigger();
    pickFunc();
}

function editTimerID() {
    var timerID = document.getElementById("timerID");
    return timerID.replace(/\s/g, "_");
}

function checkTrigger() {
    var trigger = document.getElementById("triggerInput").value;

    // class apscheduler.triggers.cron.CronTrigger(year=None, month=None, day=None, week=None, day_of_week=None, hour=None, minute=None, second=None, start_date=None, end_date=None, timezone=None, jitter=None)
    // CronTrigger(
    //     year (int|str) – 4-digit year
    //     month (int|str) – month (1-12)
    //     day (int|str) – day of the (1-31)
    //     week (int|str) – ISO week (1-53)
    //     day_of_week (int|str) – number or name of weekday (0-6 or mon,tue,wed,thu,fri,sat,sun)
    //     hour (int|str) – hour (0-23)
    //     minute (int|str) – minute (0-59)
    //     second (int|str) – second (0-59)
    //     start_date (datetime|str) – earliest possible date/time to trigger on (inclusive)
    //     end_date (datetime|str) – latest possible date/time to trigger on (inclusive)
    //     timezone (datetime.tzinfo|str) – time zone to use for the date/time calculations (defaults to scheduler timezone)
    //     jitter (int|None) – advance or delay the job execution by jitter seconds at most.
    // )
    // Expression  Field   Description
    // *           any     Fire on every value
    // */a         any     Fire every a values, starting from the minimum
    // a-b         any     Fire on any value within the a-b range (a must be smaller than b)
    // a-b/c       any     Fire every c values within the a-b range
    // xth y       day     Fire on the x -th occurrence of weekday y within the month
    // last x      day     Fire on the last occurrence of weekday x within the month
    // last        day     Fire on the last day within the month
    // x,y,z       any     Fire on any matching expression; can combine any number of any of the above expressions


    // class apscheduler.triggers.interval.IntervalTrigger(weeks=0, days=0, hours=0, minutes=0, seconds=0, start_date=None, end_date=None, timezone=None, jitter=None)
    // IntervalTrigger(
    //     weeks (int) – number of weeks to wait
    //     days (int) – number of days to wait
    //     hours (int) – number of hours to wait
    //     minutes (int) – number of minutes to wait
    //     seconds (int) – number of seconds to wait
    //     start_date (datetime|str) – starting point for the interval calculation
    //     end_date (datetime|str) – latest possible date/time to trigger on
    //     timezone (datetime.tzinfo|str) – time zone to use for the date/time calculations
    //     jitter (int|None) – advance or delay the job execution by jitter seconds at most.
    // )

}

function pickFunc() {}

function openJobs(evt, operacija) {
    // Declare all variables
    var i, tabcontent, tablinks;
  
    // Get all elements with class="tabcontent" and hide them
    tabcontent = document.getElementsByClassName("tabcontent");
    for (i = 0; i < tabcontent.length; i++) {
      tabcontent[i].style.display = "none";
    }
  
    // Get all elements with class="tablinks" and remove the class "active"
    tablinks = document.getElementsByClassName("tablinks");
    for (i = 0; i < tablinks.length; i++) {
      tablinks[i].className = tablinks[i].className.replace(" active", "");
    }
  
    // Show the current tab, and add an "active" class to the link that opened the tab
    document.getElementById(operacija).style.display = "block";
    evt.currentTarget.className += " active";

    // document.getElementById('btnSeznam').click();
  } 


function addRowHandlers() {
    var table = document.getElementById("timersTableID");
    var rows = table.getElementsByTagName("tr");
    // console.log(table)
    for (i = 1; i < rows.length; i++) {
        var currentRow = table.rows[i];
        var createClickHandler = function(row) {
            return function() {
                // "klikent" morm na edit button
                document.getElementById("btnEdit").click();
                // nafilat je treba tabelo v edit način
                var editTable = document.getElementById("timersEditTableID");
                var editColls = editTable.getElementsByTagName("td");

                var cellNum = editColls.length;
                var editTr = editTable.insertRow();
                for (var tmp = 0; tmp < cellNum; tmp++) {
                    var editTd = editTr.insertCell();
                    if (tmp == 1) {
                        // sprememba imena
                        var editInputName = document.createElement("input");
                        editInputName.type = "text";
                        editInputName.id = "triggerName";
                        editInputName.name = "triggerName";
                        editInputName.value = row.getElementsByTagName('td')[tmp].innerHTML;
                        editTd.appendChild(editInputName);
                    } else if (tmp == 2) {
                        // sprememba triggerja
                        var editInputTrig = document.createElement("input");
                        editInputTrig.type = "text";
                        editInputTrig.id = "triggerTrig";
                        editInputTrig.name = "triggerTrig";
                        editInputTrig.value = row.getElementsByTagName('td')[tmp].innerHTML;
                        starTrigger = row.getElementsByTagName('td')[tmp].innerHTML;
                        editTd.appendChild(editInputTrig);
                    } else if (tmp == 5) {
                        var btn = document.createElement("button");
                        // document.getElementById("editForm").action = "{{ url_for('timers.edit_timer', id=" + row.getElementsByTagName('td')[0].innerHTML + ") }}";
                        document.getElementById("editForm").action = "/timers/" + row.getElementsByTagName('td')[0].innerHTML + "/edit";
                        // document.getElementById("myForm").submit();
                        // btn.href = "/timers/" + row.getElementsByTagName("td")[0].innerHTML + "/edit";
                        btn.className = "material-icons";
                        btn.innerText = "save";
                        btn.type = "submit";
                        editTd.appendChild(btn);
                    } else {
                        var cell = row.getElementsByTagName("td")[tmp];
                        var cellData = cell.innerHTML;
                        editTd.appendChild(document.createTextNode(cellData));
                    }
                }
            };
        };
        currentRow.onclick = createClickHandler(currentRow);
    }
}

//   window.onload = addRowHandlers();
window.addEventListener("load", function(){
    // ....
    document.getElementById("defaultOpen").click();
    addRowHandlers();
    // alert("addRowHandlers");
});