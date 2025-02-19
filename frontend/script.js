document.addEventListener("DOMContentLoaded", () => {
    const scheduleContainer = document.getElementById("schedule");
    const weekSwitcher = document.getElementById("current-week");
    const daysButtons = document.querySelectorAll(".day");

    let currentWeek = "Числитель";
    let currentDay = "Пн";

    function fetchSchedule() {
        fetch(`https://your-api-url/get_schedule?day=${currentDay}&week=${currentWeek}`)
            .then(response => response.json())
            .then(data => {
                scheduleContainer.innerHTML = "";
                if (data.schedule.length === 0) {
                    scheduleContainer.innerHTML = "<p>🚫 Расписание отсутствует</p>";
                } else {
                    data.schedule.forEach(lesson => {
                        const lessonDiv = document.createElement("div");
                        lessonDiv.classList.add("lesson");
                        lessonDiv.innerHTML = `
                            <strong>${lesson.time}</strong><br>
                            📚 ${lesson.subject}<br>
                            👨‍🏫 ${lesson.teacher}<br>
                            🏫 ${lesson.room}
                        `;
                        scheduleContainer.appendChild(lessonDiv);
                    });
                }
            })
            .catch(error => {
                console.error("Ошибка загрузки расписания:", error);
                scheduleContainer.innerHTML = "<p>Ошибка загрузки данных</p>";
            });
    }

    daysButtons.forEach(button => {
        button.addEventListener("click", () => {
            currentDay = button.getAttribute("data-day");
            fetchSchedule();
        });
    });

    document.getElementById("prev-week").addEventListener("click", () => {
        currentWeek = "Числитель";
        weekSwitcher.textContent = "Числитель";
        fetchSchedule();
    });

    document.getElementById("next-week").addEventListener("click", () => {
        currentWeek = "Знаменатель";
        weekSwitcher.textContent = "Знаменатель";
        fetchSchedule();
    });

    fetchSchedule(); // Загрузка расписания при старте
});
