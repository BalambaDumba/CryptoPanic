from aiogram import Bot, Dispatcher, types, executor
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import os

API_TOKEN = os.getenv("API_TOKEN")
ADMIN_ID = "130759988" #change to id from (check in @UserInfeBot)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
user_choice = {}
UAH_PRICE_MAP = {
    '1month': '2500 грн',
    '3months': '6650 грн',
    '6months': '13200 грн',
    'first_time': '2250 грн'  # discounted first month
}
PAYPAL_PRICE_MAP = {
    '1month': '60 USD',
    '3months': '160 USD',
    '6months': '320 USD',
    'first_time': '55 USD'  # discounted first month
}
CRYPTO_PRICE_MAP = {
    '1month': '60 USDT',
    '3months': '160 USDT',
    '6months': '320 USDT',
    'first_time': '55 USDT'  # discounted first month
} 

# Главное меню
main_menu = InlineKeyboardMarkup(row_width=2)
main_menu.add(
    InlineKeyboardButton("🔮 Обрати підписку", callback_data="subscribe"),
    InlineKeyboardButton("❓ Підтримка", callback_data="support")
)

# Тарифы меню
tariffs_menu = InlineKeyboardMarkup(row_width=1)
tariffs_menu.add(
    InlineKeyboardButton("🔹 1 місяць", callback_data="1month"),
    InlineKeyboardButton("🔹 3 місяці", callback_data="3months"),
    InlineKeyboardButton("🔹 6 місяців", callback_data="6months"),
    InlineKeyboardButton("🔹 Приєднатися вперше", callback_data="first_time"),
    InlineKeyboardButton("🔙 Головне меню", callback_data="main_menu")
)
# Кнопка назад
get_back = InlineKeyboardMarkup(row_width=1)
get_back.add(
    InlineKeyboardButton("🔙 Головне меню", callback_data="main_menu")
)

#Варианты оплаты
def get_payment_menu():
    menu = InlineKeyboardMarkup(row_width=1)
    menu.add(
        InlineKeyboardButton("💳 Карта ₴", callback_data="pay_uah"),
        InlineKeyboardButton("🌍 PayPal $ ", callback_data="pay_paypal"),
        InlineKeyboardButton("₿ Tether ₮", callback_data="pay_crypto"),
        InlineKeyboardButton("🌀 Інший спосіб", callback_data="other_payment"),
        InlineKeyboardButton("🔙 Назад до тарифів", callback_data="back_to_tariffs")
    )
    return menu

# Подтверждение оплаты
confirmation_menu = InlineKeyboardMarkup(row_width=1)
confirmation_menu.add(
    InlineKeyboardButton("✉️ Надіслати підтвердження", callback_data='confirm'),
    InlineKeyboardButton("🔙 Головне меню", callback_data="main_menu")
)

# Старт
@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    welcome_text = (
        "Привіт! 👋🏻\n\n"
        "Рада, що ти тут 🤍\n\n"
        "Я - бот-помічник BeIn, нашого онлайн йога-клубу 🌿\n"
        "Тут ти можеш оформити участь в клубі й задати будь-яке питання.\n\n"
        "👇🏻 Обери, з чого почати:"
    )
    await message.answer(welcome_text, reply_markup=main_menu)

# Support
@dp.callback_query_handler(lambda c: c.data == 'support')
async def support(callback: types.CallbackQuery):
    await callback.answer()
    await callback.message.edit_text(
        "Якщо маєш запитання чи щось не зрозуміло - просто напиши мені, я постараюсь допомогти якнайшвидше 🤍\n\n"
        "Можеш також звернутись напряму до Ані: @anna_baron 💬",
        reply_markup=get_back
    )

#Subscribe
@dp.callback_query_handler(lambda c: c.data == 'subscribe')
async def subscribe(callback: types.CallbackQuery):
    await callback.answer()
    await callback.message.edit_text(
        "BeIn - це онлайн-простір, де ми практикуємо йогу, вчимось слухати тіло й відпочивати розумом.\n\n"
        "🌸 живі та записані практики з йоги\n"
        "🌸 лекції від експертів\n"
        "🌸 підтримка спільноти\n\n"
        "👇🏻 Давай оберемо зручний тариф:",
        reply_markup=tariffs_menu
    )

# Month button respond
@dp.callback_query_handler(lambda c: c.data in ['1month', '3months', '6months', 'first_time'])
async def choose_tariff(callback: types.CallbackQuery):
    await callback.answer()
    user_choice[callback.from_user.id] = callback.data
    if callback.data == '1month':
        text = "Клас! Дякую тобі за вибір 💜 \n\nОбери зручний для себе спосіб оплати:"
    elif callback.data == '3months':
        text = "Супер вибір! Це гарна можливість відчути результат 🙌🏻\n\nОбери зручний для себе спосіб оплати:"
    elif callback.data == '6months':
        text = "Вау, ти неймовірна! Така рішучість завжди надихає ✨\n\nОбери зручний для себе спосіб оплати:"
    else:
        text = "Для нових учасниць діє спеціальна пропозиція - знижка 10% на перший місяць 🌙"
    await callback.message.edit_text(text, reply_markup=get_payment_menu())

#Other payment
@dp.callback_query_handler(lambda c: c.data == 'other_payment')
async def other_payment(callback: types.CallbackQuery):
    await callback.answer()
    menu = InlineKeyboardMarkup(row_width=1)
    menu.add(
        InlineKeyboardButton("🌸 Написати Ані", url="https://t.me/anna_baron"),
        InlineKeyboardButton("🔙 Назад до тарифів", callback_data="back_to_tariffs")
    )
    await callback.message.edit_text("Не знайшла зручного способу оплати? Не хвилюйся 🌱\n \nНатисни кнопку нижче, щоб написати Ані - вона допоможе знайти варіант 💌", reply_markup=menu)

#UAH
@dp.callback_query_handler(lambda c: c.data == 'pay_uah')
async def pay_uah(callback: types.CallbackQuery):
    await callback.answer()
    tariff = user_choice.get(callback.from_user.id)
    price = UAH_PRICE_MAP.get(tariff)
    await callback.message.edit_text(
        "Супер, ми майже на фініші 🎯\n\n"
        "💳 Картка для оплати: 4441 1110 4149 2384\n"
        "👤 Отримувач: Барон Ганна Іванівна\n"
        f"💰 Сума: {price}\n\n"
        "Після оплати натисни кнопку:",
        reply_markup=confirmation_menu
    )
    
#PAYPAL
@dp.callback_query_handler(lambda c: c.data == 'pay_paypal')
async def pay_paypal(callback: types.CallbackQuery):
    await callback.answer()
    tariff = user_choice.get(callback.from_user.id)
    price = PAYPAL_PRICE_MAP.get(tariff)
    await callback.message.edit_text(
        "Чудово! \nОсь реквізити для оплати:\n\n"
        "📩 PayPal: brn.anna26@gmail.com\n"
        f"💰 Сума: {price}\n\n"
        "Після оплати натисни кнопку:",
        reply_markup=confirmation_menu
    )

#CRYPTO
@dp.callback_query_handler(lambda c: c.data == 'pay_crypto')
async def pay_crypto(callback: types.CallbackQuery):
    await callback.answer()
    tariff = user_choice.get(callback.from_user.id)
    price = CRYPTO_PRICE_MAP.get(tariff)
    await callback.message.edit_text(
        "Дякую за вибір!\n\n"
        f"Ось криптогаманець для оплати:\nВалюта USDT, мережа TRC20: \n \n `TAkhXBSU9h5x7dauzcPTxktip4obiuu5fN` \n\n"
        f"💰 Сума: {price}\n\n"
        "Після оплати натисни кнопку:",
        reply_markup=confirmation_menu, 
        parse_mode="Markdown"
    )

@dp.callback_query_handler(lambda c: c.data == 'confirm')
async def confirm(callback: types.CallbackQuery):
    await callback.answer()
    await bot.send_message(chat_id=ADMIN_ID, text=f"Користувач @{callback.from_user.username} натиснув кнопку про здійснену оплату")

    final_step_menu = InlineKeyboardMarkup(row_width=1)
    final_step_menu.add(
        InlineKeyboardButton("🔙 Головне меню", callback_data="main_menu")
    )
    
    await callback.message.edit_text("Супер! Ти молодець, залишився останній крок 🤍\n \n Надішли, будь ласка, скрін або квитанцію Ані у приватні повідомлення, щоб підтвердити оплату @anna_baron💌", 
                                     reply_markup=final_step_menu
                                    )

@dp.callback_query_handler(lambda c: c.data == 'back_to_tariffs')
async def back_to_tariffs(callback: types.CallbackQuery):
    await subscribe(callback)

@dp.callback_query_handler(lambda c: c.data == 'main_menu')
async def back_to_main(callback: types.CallbackQuery):
    # emulate /start
    class Msg: pass
    await callback.answer()
    await callback.message.delete()
    msg = Msg()
    msg.answer = callback.message.answer
    await send_welcome(msg)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
