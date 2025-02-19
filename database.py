import sqlite3

def create_tables():
    conn = sqlite3.connect("schedule.db")
    cursor = conn.cursor()

    # Создаём таблицу расписания, если её нет
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS schedule (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        faculty TEXT,
        group_number TEXT,
        week_type TEXT,
        day TEXT,
        time TEXT,
        subject TEXT,
        teacher TEXT,
        room TEXT
    )
    """)

    conn.commit()
    conn.close()

if __name__ == "__main__":
    create_tables()
    print("База данных и таблица schedule успешно созданы!")

def check_schedule():
    conn = sqlite3.connect("schedule.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM schedule")
    rows = cursor.fetchall()

    if not rows:
        print("❌ Таблица schedule пуста!")
    else:
        print("✅ Данные в таблице schedule:")
        for row in rows:
            print(row)

    conn.close()

if __name__ == "__main__":
    create_tables()
    check_schedule()


import sqlite3

# Подключаемся к базе данных (если её нет, она создастся)
conn = sqlite3.connect("schedule.db")
cursor = conn.cursor()

# Создаём таблицу, если её нет
cursor.execute("""
CREATE TABLE IF NOT EXISTS schedule (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    faculty TEXT,
    group_number TEXT,
    week_type TEXT,
    day TEXT,
    time TEXT,
    subject TEXT,
    teacher TEXT,
    room TEXT
)
""")

conn.commit()
conn.close()

print("База данных и таблица schedule успешно созданы!")

import sqlite3

# Подключение к БД
conn = sqlite3.connect("schedule.db")
cursor = conn.cursor()

# Данные расписания
schedule_data = [
    ("ФВТ", "444", "Числитель", "Пн", "09:55-11:30", "Лаб. Программная инженерия", "Щенёва Ю.Б., Бубнов С.А.", "206-3 С"),
    ("ФВТ", "444", "Числитель", "Пн", "11:40-13:15", "Упр. Иностранный язык", "Трушкова И.Н., Термышева Е.Н.", "132 С"),
    ("ФВТ", "444", "Числитель", "Вт", "08:10-09:45", "Лек. Физическая культура и спорт", "Стадион РГРТУ", ""),
    ("ФВТ", "444", "Числитель", "Вт", "09:55-11:30", "Лек. Безопасность жизнедеятельности", "Чернышев С.В.", "337 С"),
    ("ФВТ", "444", "Числитель", "Ср", "08:10-09:45", "Лек. Высшая математика", "Соколов А.С.", "337 С"),
    ("ФВТ", "444", "Числитель", "Чт", "08:10-09:45", "Лек. Физические основы электротехники", "Михеев А.А.", "405 С"),
    ("ФВТ", "444", "Числитель", "Пт", "09:55-11:30", "Упр. Высшая математика", "Ципоркова К.А.", "403 С"),
]

# Вставка данных
cursor.executemany(
    "INSERT INTO schedule (faculty, group_number, week_type, day, time, subject, teacher, room) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
    schedule_data
)

conn.commit()
conn.close()

print("✅ Расписание успешно добавлено в базу данных!")

