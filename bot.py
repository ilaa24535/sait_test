import sqlite3
import asyncio
import ssl
import logging
from aiogram import Bot, Dispatcher, Router, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo
from aiogram.filters import Command
from aiogram.client.default import DefaultBotProperties
from config import TOKEN

logging.basicConfig(level=logging.DEBUG)

ssl._create_default_https_context = ssl._create_unverified_context

bot = Bot(
    token=TOKEN,
    default=DefaultBotProperties(parse_mode="HTML")
)

router = Router()
dp = Dispatcher()
dp.include_router(router)

user_selection = {}

logging.debug("Bot initialized")

week_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="🔄 Перезапустить", callback_data="restart_bot")],
    [InlineKeyboardButton(text="📅 Открыть расписание", web_app=WebAppInfo(url="https://ilaa24535.github.io/sait_test/",
                                                                          headers={"bypass-tunnel-reminder": "true",
                                                                                   "User-Agent": "Mozilla/5.0"}))]
])


def get_days_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="Пн", callback_data="day_Пн"),
            InlineKeyboardButton(text="Вт", callback_data="day_Вт"),
            InlineKeyboardButton(text="Ср", callback_data="day_Ср"),
        ],
        [
            InlineKeyboardButton(text="Чт", callback_data="day_Чт"),
            InlineKeyboardButton(text="Пт", callback_data="day_Пт"),
            InlineKeyboardButton(text="Сб", callback_data="day_Сб"),
        ],
        [
            InlineKeyboardButton(text="⬅ Назад", callback_data="back_week"),
            InlineKeyboardButton(text="🔄 Перезапустить", callback_data="restart_bot")
        ]
    ])


@router.message(Command("start"))
async def cmd_start(message: types.Message):
    logging.info(f"User {message.from_user.id} started the bot")
    await message.answer("📅 Выберите тип недели:", reply_markup=week_keyboard)


@router.callback_query(lambda c: c.data == "restart_bot")
async def callback_restart_bot(callback_query: types.CallbackQuery):
    logging.info(f"User {callback_query.from_user.id} restarted the bot")
    await callback_query.message.delete()
    await cmd_start(callback_query.message)
    await callback_query.answer()


@router.callback_query(lambda c: c.data.startswith("week_"))
async def callback_select_week(callback_query: types.CallbackQuery):
    week_type = callback_query.data.split("_")[1]
    user_selection[callback_query.from_user.id] = {"week_type": week_type}
    logging.info(f"User {callback_query.from_user.id} selected week type: {week_type}")
    await callback_query.message.edit_text(
        "📅 Выберите день недели:",
        reply_markup=get_days_keyboard()
    )
    await callback_query.answer()


@router.callback_query(lambda c: c.data.startswith("day_"))
async def callback_select_day(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    if user_id not in user_selection or "week_type" not in user_selection[user_id]:
        logging.warning(f"User {user_id} tried selecting a day without choosing a week type")
        await callback_query.message.edit_text("⚠ Сначала выберите неделю через /start")
        return

    selected_day = callback_query.data.split("_")[1]
    selected_week = user_selection[user_id]["week_type"]
    logging.info(f"User {user_id} selected day: {selected_day} ({selected_week})")
    schedule_text = get_schedule_for_day(selected_day, selected_week)
    back_keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="⬅ Назад", callback_data="back_days"),
            InlineKeyboardButton(text="🔄 Перезапустить", callback_data="restart_bot")
        ]
    ])
    await callback_query.message.edit_text(
        f"📅 <b>Расписание на {selected_day} ({selected_week}):</b>\n\n{schedule_text}",
        reply_markup=back_keyboard
    )
    await callback_query.answer()


@router.callback_query(lambda c: c.data == "back_days")
async def callback_back_to_days(callback_query: types.CallbackQuery):
    logging.info(f"User {callback_query.from_user.id} went back to day selection")
    await callback_query.message.edit_text(
        "📅 Выберите день недели:",
        reply_markup=get_days_keyboard()
    )
    await callback_query.answer()


def get_schedule_for_day(day, week_type):
    logging.debug(f"Fetching schedule for {day}, {week_type}")
    conn = sqlite3.connect("schedule.db")
    cursor = conn.cursor()
    cursor.execute(
        "SELECT time, subject, teacher, room FROM schedule WHERE day=? AND week_type=?",
        (day, week_type)
    )
    rows = cursor.fetchall()
    conn.close()
    if not rows:
        logging.warning(f"No schedule found for {day}, {week_type}")
        return "🚫 <b>Расписания на этот день нет.</b>"
    return "\n".join([
        f"<b>{time}</b>\n📚 {subject}\n👨‍🏫 {teacher}\n🏫 {room}"
        for (time, subject, teacher, room) in rows
    ])


async def main():
    logging.info("Bot started")
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
