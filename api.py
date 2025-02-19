from fastapi import FastAPI
import sqlite3
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Разрешаем CORS (чтобы фронтенд мог делать запросы)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Главная страница API для проверки работоспособности
@app.get("/")
async def root():
    return {"message": "API работает!"}

# Эндпоинт для получения расписания
@app.get("/get_schedule")
async def get_schedule():
    try:
        conn = sqlite3.connect("schedule.db")
        cursor = conn.cursor()
        cursor.execute("SELECT time, subject, teacher, room FROM schedule")
        rows = cursor.fetchall()
        conn.close()

        if not rows:
            return {"schedule": [], "message": "Расписание не найдено"}

        schedule = [
            {"time": time, "subject": subject, "teacher": teacher, "room": room}
            for (time, subject, teacher, room) in rows
        ]
        return {"schedule": schedule}
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
