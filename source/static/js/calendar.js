function calender() {
    let that = this;
    let month = ["Январь", "Февраль", "Март", "Апрель", "Май", "Июнь", "Июль", "Август", "Сентябрь", "Окротябрь", "Ноябрь", "Декабрь"];
    let event = {
        1: 'Event 1',
        2: 'Event 2',
        30: 'Event 30'
    };
    let calenderData = {};
    let weekdays = ["Пн", "Вт", "Ср", "Чт", "Пт", "Сб", "Вс"];
    that.monthCombo = document.getElementById('month')
    that.yearCombo = document.getElementById('year');
    let currentYear = new Date().getFullYear();
    let currentMonth = new Date().getMonth();
    let startDay, endDay, tableRow, tableData;
    let calenderArray = [];
    for (let i = 0; i < 12; i++) {
        let option = document.createElement('option');
        option.value = i;
        option.innerHTML = month[i];
        option.className = 'dropdown-item';
        monthCombo.appendChild(option);
    }
    for (let j = new Date(0).getFullYear(); j <= currentYear + 10; j++) {
        let option = document.createElement('option');
        option.value = j;
        option.innerHTML = j;
        option.className = 'dropdown-item';
        yearCombo.appendChild(option);
        if (currentYear === j) {
            option.selected = 'selected';
        }
    }
    let table = document.createElement('table');
    table.id = "cTable";
    table.className = 'table';
    document.getElementById('table-div').appendChild(table);
    monthCombo.addEventListener('change', function () {
        calculateDays();
        onLoad();
    });
    yearCombo.addEventListener('change', function () {
        calculateDays();
        onLoad()
    });
    let today = new Date();
    document.getElementById('month').options.selectedIndex = today.getMonth();
    calculateDays();

    function calculateDays() {
        let that = this;
        let storedData = JSON.parse(localStorage.getItem('year-' + that.yearCombo.selectedOptions[0].value + '' + 'month-' + that.monthCombo.options.selectedIndex));
        if (storedData) {
            calenderData = storedData;
        } else
            calenderData = {};
        document.getElementById('cTable').innerHTML = '';
        let th = document.createElement('tr');
        th.id = 'tr';
        th.className = 'thead-dark';
        document.getElementById('cTable').appendChild(th);
        for (let k = 0; k < weekdays.length; k++) {
            let td = document.createElement('td');
            td.innerHTML = weekdays[k];
            td.classList = ["weekdays-row"]
            document.getElementById('tr').appendChild(td);
        }
        calenderArray = [];
        let monthDays = new Date(parseInt(yearCombo.value), parseInt(monthCombo.value) + 1, 0).getDate();
        startDay = new Date(parseInt(yearCombo.value), parseInt(monthCombo.value), 1).getDay() - 1;
        console.log(startDay)
        endDay = new Date(parseInt(yearCombo.value), parseInt(monthCombo.value) + 1, 0).getDay();
        if (startDay !== 0) {
            for (let l = 0; l < startDay; l++) {
                calenderArray.push('b');
            }
        }
        for (let m = 1; m <= monthDays; m++) {
            calenderArray.push(m);
        }
        if (endDay !== 6) {
            for (let n = 0; n < 6 - endDay; n++) {
                calenderArray.push('b');
            }
        }
        for (let n = 0; n < calenderArray.length; n++) {
            if (n % 7 === 0) {
                tableRow = document.createElement('tr');
                tableRow.id = 'tr-' + (n / 7);
                tableRow.className = 'table-row';
                document.getElementById('cTable').appendChild(tableRow);
            }
            tableData = document.createElement('td');
            tableData.id = 'td-' + calenderArray[n];
            tableData.classList = ["table-days-row"]
            let outsideDiv = document.createElement('div')
            let insideDiv = document.createElement('div')
            let dayData = document.createElement('p')
            dayData.classList = ["day-information"]
            outsideDiv.classList = ["outside-div"]
            insideDiv.classList = ['inside-div']
            console.log(calenderArray)

            if (calenderArray[n] == 'b') {
                tableData.innerHTML = '';
            } else {
                dayData.innerText = calenderArray[n]
                insideDiv.id = "post-day-" + calenderArray[n]
                outsideDiv.appendChild(dayData)
                outsideDiv.appendChild(insideDiv)
                tableData.appendChild(outsideDiv);
                if (calenderArray[n] === today.getDate() && parseInt(yearCombo.value) === today.getFullYear() && parseInt(monthCombo.value) === today.getMonth()) {
                    tableData.classList.add('post-today');
                }
                if (calenderData[calenderArray[n]]) {
                    calenderData = storedData;
                    for (let p = 0; p < calenderData[calenderArray[n]].length; p++) {
                        let addEventDiv = document.createElement('div');
                        addEventDiv.id = 'event-on ' + calenderArray[n];
                        addEventDiv.classList.add('bg-card', 'card');
                        addEventDiv.innerHTML += calenderData[calenderArray[n]][p];
                        tableData.appendChild(addEventDiv);
                    }
                }
            }
            tableRow.appendChild(tableData);
        }

    }

    // TO set listener for each event card
    let allEvents = document.querySelectorAll('.bg-card');
    allEvents.forEach(function (eventCard, index) {
        eventCard.addEventListener('click', function () {
        })
    })

    function getTranslateStatus(status) {
        if (status === "new") {
            return "Новый"
        } else if (status === "finished") {
            return "Завершен"
        } else if (status === "canceled") {
            return "Отменен"
        }
    }

    async function onLoad() {
        let url = "api/order/list/?year=" + parseInt(yearCombo.value) + "&month=" + (parseInt(monthCombo.value) + 1)
        let response = await fetch(url, {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json',
                }
            }

        )
        let answer = await response.json()
        console.log(answer)
        console.log(monthCombo)
        for (i = 0; i < answer.length; i++) {
            let day = new Date(answer[i]["work_start"])

            let element = document.getElementById("post-day-" + day.getDate())
            let link = document.createElement("a")
            link.href = "order/" + answer[i]["id"] + "/"
            link.innerHTML = "<span>" + day.getHours() + ":" + day.getMinutes() + "</span>" + " " + getTranslateStatus(answer[i]["status"]) + " - " + answer[i]["address"]
            if (answer[i]["status"] === "new") {
                link.style = "background-color: #3DB357;"
            } else if (answer[i]["status"] === "finished"){
                link.style = "background-color: #855D99;"
            } else {
                link.style = "background-color: gray;"
            }
            element.appendChild(link)
        }
    }

    onLoad()
}