from pyrogram import Client, filters, emoji
from pyrogram.types import Message, CallbackQuery

import asyncio

from config import API_ID, API_HASH, BOT_TOKEN
import keyboards, buttons
from custom_filters import button_filter, inline_button_filter
import database 

class Client(Client):
    def __init__(self, *args, **kwargs):
        self.db = database.Database()
        super().__init__(*args, **kwargs)

    def stop(self, *args, **kwargs):
        return super().stop(*args, kwargs)


bot = Client(
    name="CryptoTycoonBot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,   
)


game_is_active = {}   # Состояние игры для каждого пользователя

# Список домов
houses = [
    ["🪫Дешевый дом", "img/cheep_house.jpg", ],
    ["⚖Средний дом", "img/medium_house.jpg", ],
    ["💰Дорогой дом", "img/expensive_house.jpg", ],
    ["💎Особняк", "img/mansion_house.jpg", ],
    ["🛸Замок на Марсе", "img/mars_castle.jpg", ]
]

for house, keyboard in zip(houses, keyboards.houses_keyboards):     
    house.append(keyboard)                                                                          


# Список машин
cars = [
    ["🚗Запорожец", "img/zaporozhets.jpg", ],
    ["🚙Nissan Pathfinder", "img/NissanPathfinder.jpg", ],
    ["🚘BMW M5", "img/bmw_m5.jpg", ],
    ["🚖Mercedes-Benz AMG GT", "img/mersedes_amg_gt_c.jpg", ],
    ["🏎Lamborghini Aventador", "img/lamborgini_aventador.jpg", ],
    ["🛸Марсоход", "img/Mars_car.jpg", ]
]
for car, keyboard in zip(cars, keyboards.cars_keyboards):
    car.append(keyboard)                                              

pets = [
    ["🐕Собака", "img/dog.jpg", ],
    ["🐈Кошка", "img/cat.jpg", ],
    ["Белый конь", "img/horse.jpg", ],
    ["Белый лев", "img/lion.jpg", ],
    ["Инопланетный питомец", "img/alien.jpg", ]
]
for pet, keyboard in zip(pets, keyboards.pets_keyboards):
    pet.append(keyboard)

entertainment=[
    ["Игровая консоль", "img/ps_5.jpg", ],
    ["Стол для бильярда", "img/billiard_table.jpg", ],
    ["Яхта", "img/yacht.jpg", ],
    ["Личный самолет", "img/plane.jpg", ],
    ["Стадион на марсе", "img/mars_stadium.jpg", ]
]
for entertain, keyboard in zip(entertainment, keyboards.entertainment_keyboards):
    entertain.append(keyboard)

# Start command handler
@bot.on_message(filters=filters.command("start"))
async def start(client, message: Message):
    client.db.create_table()
    await message.reply(f"Привет Это Крипто Тайкон Бот👋! Выбери или создай сохранение для начала игры.💾 Если нужна помощь - /help", reply_markup=keyboards.saves_keyboard)

@bot.on_message(filters=filters.command("help"))
async def help_command(client, message: Message):
    await message.reply(text="Добро пожаловать в Крипто Тайкон Бот! 🚀\n\n"
    " 💾 Сохранения\n\n"
    "Создать новое сохранение - начинает новую игру и создает полностью чистое сохранение. функция недоступна если у вас уже есть сохранение, чтоб создать новое неообходимо удалить старое\n"
    " Загрузить сохранение - загружает ваше последнее сохранение\n"
    " Удалить сохранение - удаляет ваше текущее сохранение\n\n"
    " 🚀 Игра\n\n"
    "Купить видеокарту - покупает видеокарту для майнинга криптовалюты. Одна видеокарта зарабатывает 1₵.\n"
    "Купить улучшение - покупает улучшение для повышения эффективности майнинга. Каждое улучшение увеличивает доход от всех видеокарт на 100% от первоначального зароботка.\n"
    "Магазин - открывает магазин где можно купить дома, машины, питомцев и развлечения за заработанную криптовалюту.\n"
    "Профиль - показывает ваш текущий прогресс в игре.\n\n"
    "Доступные команды:\n\n"
    "/start - начать игру или создать новое сохранение\n"
    "/help - показать это сообщение помощи\n"
    "/profile - показать ваш профиль\n"
    "/shop - открыть магазин\n")




@bot.on_message(filters=filters.command("profile") | inline_button_filter(buttons.profile_button))
async def profile(client, message: Message):
    user_id = message.from_user.id
    if client.db.cursor.execute("SELECT user_id FROM users WHERE user_id = ?", (user_id,)).fetchone() is not None:
        crypt = client.db.cursor.execute("SELECT crypt FROM users WHERE user_id = ?", (user_id,)).fetchone()[0]
        videocards = client.db.cursor.execute("SELECT videocards FROM users WHERE user_id = ?", (user_id,)).fetchone()[0]
        upgrades = client.db.cursor.execute("SELECT upgrades FROM users WHERE user_id = ?", (user_id,)).fetchone()[0]
        house = client.db.cursor.execute("SELECT house FROM users WHERE user_id = ?", (user_id,)).fetchone()[0]
        car = client.db.cursor.execute("SELECT car FROM users WHERE user_id = ?", (user_id,)).fetchone()[0]
        pet = client.db.cursor.execute("SELECT pet FROM users WHERE user_id = ?", (user_id,)).fetchone()[0]
        entertainment = client.db.cursor.execute("SELECT entertainment FROM users WHERE user_id = ?", (user_id,)).fetchone()[0]
        
        profile_text = (
            f"👤Профиль пользователя:\n\n\n"
            f"💰Баланс: {crypt}₵\n\n"
            f"🎮Видеокарты: {videocards}\n\n"
            f"🚀Улучшения: {upgrades}\n\n"
            f"🏠Дом: {house if house else 'Нет'}\n\n"
            f"🚗Машина: {car if car else 'Нет'}\n\n"
            f"🐕Питомец: {pet if pet else 'Нет'}\n\n"
            f"🎉Развлечения: {entertainment if entertainment else 'Нет'}\n\n"
        )
        await message.reply(profile_text)
    else:
        await message.reply("У вас еще нету сохранений💾. Создайте новое чтобы посмотреть профиль☺️")    

@bot.on_callback_query(filters=inline_button_filter(buttons.profile_button))
async def profile_callback(client, query: CallbackQuery):
    user_id = query.from_user.id
    if client.db.cursor.execute("SELECT user_id FROM users WHERE user_id = ?", (user_id,)).fetchone() is not None:
        crypt = client.db.cursor.execute("SELECT crypt FROM users WHERE user_id = ?", (user_id,)).fetchone()[0]
        videocards = client.db.cursor.execute("SELECT videocards FROM users WHERE user_id = ?", (user_id,)).fetchone()[0]
        upgrades = client.db.cursor.execute("SELECT upgrades FROM users WHERE user_id = ?", (user_id,)).fetchone()[0]
        house = client.db.cursor.execute("SELECT house FROM users WHERE user_id = ?", (user_id,)).fetchone()[0]
        car = client.db.cursor.execute("SELECT car FROM users WHERE user_id = ?", (user_id,)).fetchone()[0]
        pet = client.db.cursor.execute("SELECT pet FROM users WHERE user_id = ?", (user_id,)).fetchone()[0]
        entertainment = client.db.cursor.execute("SELECT entertainment FROM users WHERE user_id = ?", (user_id,)).fetchone()[0]
        
        profile_text = (
            f"👤Профиль пользователя:\n\n\n"
            f"💰Баланс: {crypt}₵\n\n"
            f"🎮Видеокарты: {videocards}\n\n"
            f"🚀Улучшения: {upgrades}\n\n"
            f"🏠Дом: {house if house else 'Нет'}\n\n"
            f"🚗Машина: {car if car else 'Нет'}\n\n"
            f"🐕Питомец: {pet if pet else 'Нет'}\n\n"
            f"🎉Развлечения: {entertainment if entertainment else 'Нет'}\n\n"
        )
        await query.message.reply(text=profile_text)
    else:
        await query.answer("У вас еще нету сохранений💾. Создайте новое чтобы посмотреть профиль☺️", show_alert=True)

# Delete save handler
@bot.on_callback_query(filters=inline_button_filter(buttons.delete_save_button))
async def delete_save(client, query: CallbackQuery):
    user_id = query.from_user.id
    if client.db.cursor.execute("SELECT user_id FROM users WHERE user_id = ?", (user_id,)).fetchone() is not None:
        client.db.delete_user(user_id)
        await query.answer("Ваше сохранение удалено🗑", show_alert=False)
        return
    else:
        await query.answer("У вас еще нету сохранений💾", show_alert=True)    


# Load save handler    
@bot.on_callback_query(filters=inline_button_filter(buttons.load_save_button))
async def load_save(client, query: CallbackQuery):
    user_id = query.from_user.id
    if client.db.cursor.execute("SELECT user_id FROM users WHERE user_id = ?", (user_id,)).fetchone() is not None:
        await query.edit_message_text("Сохранение загружено💾", reply_markup=keyboards.tycoon_keyboard)
    else:
        await query.answer("У вас еще нету сохранений💾", show_alert=True)


# New save handler
@bot.on_callback_query(filters=inline_button_filter(buttons.new_save_button))
async def new_save(client, query: CallbackQuery):
    user_id = query.from_user.id
    if client.db.cursor.execute("SELECT user_id FROM users WHERE user_id = ?", (user_id,)).fetchone() is not None:
        await query.answer("У вас уже есть сохранение💾. Удалите его чтобы создать новое☺️", show_alert=True)
    else:
        client.db.add_user(user_id)
        await query.edit_message_text("Новое сохранение создано💾", reply_markup=keyboards.tycoon_keyboard)


# Tycoon start
@bot.on_callback_query(filters=inline_button_filter(buttons.start_tycoon_button) | inline_button_filter(buttons.back_button))
async def tycoon(client, query: CallbackQuery):
    user_id = query.from_user.id
    game_is_active[user_id] = True
    if game_is_active[user_id]:
        while game_is_active[user_id]:
            crypt = client.db.cursor.execute("SELECT crypt FROM users WHERE user_id = ?", (query.from_user.id,)).fetchone()[0]
            videocards = client.db.cursor.execute("SELECT videocards FROM users WHERE user_id = ?", (user_id,)).fetchone()[0]
            upgrades = client.db.cursor.execute("SELECT upgrades FROM users WHERE user_id = ?", (user_id,)).fetchone()[0]
            income = videocards * (1 + upgrades)
            await query.edit_message_text(f"Ваш Крипто Тайкон Бот готов к работе! 🚀\n\n💰Баланс: {crypt}₵", reply_markup=keyboards.main_menu_keyboard)
            client.db.crypt_earned(user_id=user_id, value=income)
            await asyncio.sleep(1)
    else:
        await query.answer("Сначала начните игру! 🚀", show_alert=True)


# Video card purchase handler
@bot.on_callback_query(filters=inline_button_filter(buttons.buy_video_card_button))
async def buy_video_card(client, query: CallbackQuery):
    user_id = query.from_user.id
    if game_is_active[user_id]:
        crypt = client.db.cursor.execute("SELECT crypt FROM users WHERE user_id = ?", (user_id,)).fetchone()[0]
        videocards = client.db.cursor.execute("SELECT videocards FROM users WHERE user_id = ?", (user_id,)).fetchone()[0]
        cost = 25 * (1 + videocards)
        if crypt < cost:
            await query.answer(f"💸Недостаточно средств! Видеокарта стоит {cost}₵💸", show_alert=True)
            return 
        client.db.buy_video_card(videocard_cost=cost, user_id=user_id)
        await query.answer(f"Видеокарта куплена за {cost}₵! 🛒", show_alert=False)    
    else:
        await query.answer("Сначала начните игру! 🚀", show_alert=True)


# Upgrade handler
@bot.on_callback_query(filters=inline_button_filter(buttons.buy_upgrade_button))
async def upgrade(client, query: CallbackQuery):
    user_id = query. from_user.id
    if game_is_active[user_id]:
        crypt = client.db.cursor.execute("SELECT crypt FROM users WHERE user_id = ?", (user_id,)).fetchone()[0] 
        upgrades = client.db.cursor.execute("SELECT upgrades FROM users WHERE user_id = ?", (user_id,)).fetchone()[0]
        cost = 500 * (1 + upgrades)
        if crypt < cost:
            await query.answer(f"💸Недостаточно средств! Улучшение стоит {cost}₵💸", show_alert=True)
            return
        client.db.buy_upgrade(upgrade_cost=cost, user_id=user_id)
        await query.answer(f"Улучшение куплено за {cost}₵! 🚀", show_alert=False)
    else:
        await query.answer("Сначала начните игру! 🚀", show_alert=True)


# Shop handlers
@bot.on_callback_query(filters=inline_button_filter(buttons.shop_button))
async def shop(client, query: CallbackQuery):
    user_id = query.from_user.id
    game_is_active[user_id] = False
    await query.edit_message_text("Добро пожаловать в магазин! 🛍 Выберите категорию:", reply_markup=keyboards.shop_keyboard)
    
@bot.on_message(filters=filters.command("shop"))
async def shop_message(client, message: Message):
    user_id = message.from_user.id
    game_is_active[user_id] = False
    await message.reply("Добро пожаловать в магазин! 🛍 Выберите категорию:", reply_markup=keyboards.shop_keyboard)


# End game handler
@bot.on_callback_query(filters=inline_button_filter(buttons.end_game_button))
async def stop_game(client, query: CallbackQuery):
    user_id = query.from_user.id
    game_is_active[user_id] = False
    crypt = client.db.cursor.execute("SELECT crypt FROM users WHERE user_id = ?", (user_id,)).fetchone()[0]
    upgrades = client.db.cursor.execute("SELECT upgrades FROM users WHERE user_id = ?", (user_id,)).fetchone()[0]
    videocards = client.db.cursor.execute("SELECT videocards FROM users WHERE user_id = ?", (user_id,)).fetchone()[0]
    client.db.save_progress(user_id, crypt=crypt, upgrades=upgrades, videocards=videocards)
    await query.edit_message_text("Игра остановлена😊.\nВаши данные сохранены💾. Вы можете возобновить её в любое время.\n Напишите /start чтобы продолжить✨")


# Houses handlers 
@bot.on_callback_query(filters=inline_button_filter(buttons.houses_button))
async def houses_func(client, query: CallbackQuery):
    await query.edit_message_text("Категория: 🏠Дома\nВыберите дом для покупки:")
    for house in houses:
        name, img, keyboard = house
        await query.message.reply_photo(photo=img, caption=name, reply_markup=keyboard)
    await query.message.reply_text("🎮Чтобы возобновить игру, введите /start. Чтобы вернуться в магазин напишите /shop.")


@bot.on_callback_query(filters=inline_button_filter(buttons.buy_cheep_house_button))
async def buy_cheep_house(client, query: CallbackQuery):
    user_id = query.from_user.id
    crypt = client.db.cursor.execute("SELECT crypt FROM users WHERE user_id = ?", (user_id,)).fetchone()[0]
    user_houses = client.db.cursor.execute("SELECT house FROM users WHERE user_id = ?", (user_id,)).fetchone()[0]
    if "Дешевый дом" in user_houses:
        await query.answer("🏠У вас уже есть этот дом!🏠", show_alert=True)   
    else:    
        if crypt < 1000:
            await query.answer(f"💸Недостаточно средств! Дешевый дом стоит 1000₵ а у вас только {crypt}💸", show_alert=True)
            return
        client.db.buy_house(user_id=user_id, house_name="Дешевый дом", house_cost=1000)
        crypt = client.db.cursor.execute("SELECT crypt FROM users WHERE user_id = ?", (user_id,)).fetchone()[0]
        await query.answer(f"🏠Дешевый дом куплен!🏠\n Теперь на балансе: {crypt}", show_alert=False)


@bot.on_callback_query(filters=inline_button_filter(buttons.buy_medium_house_button))
async def buy_medium_house(client, query: CallbackQuery):
    user_id = query.from_user.id
    crypt = client.db.cursor.execute("SELECT crypt FROM users WHERE user_id = ?", (user_id,)).fetchone()[0]
    user_houses = client.db.cursor.execute("SELECT house FROM users WHERE user_id = ?", (user_id,)).fetchone()[0]
    if "Средний дом" in user_houses:
        await query.answer("🏠У вас уже есть этот дом!🏠", show_alert=True)   
    else:    
        if crypt < 50000:
            await query.answer(f"💸Недостаточно средств! Средний дом стоит 50000₵ а у вас только {crypt}💸", show_alert=True)
            return
        client.db.buy_house(user_id=user_id, house_name="Средний дом", house_cost=50000)
        crypt = client.db.cursor.execute("SELECT crypt FROM users WHERE user_id = ?", (user_id,)).fetchone()[0]
        await query.answer(f"🏠Средний дом куплен!🏠\n Теперь на балансе: {crypt}", show_alert=False)


@bot.on_callback_query(filters=inline_button_filter(buttons.buy_expensive_house_button))
async def buy_expensive_house(client, query: CallbackQuery):
    user_id = query.from_user.id
    crypt = client.db.cursor.execute("SELECT crypt FROM users WHERE user_id = ?", (user_id,)).fetchone()[0]
    user_houses = client.db.cursor.execute("SELECT house FROM users WHERE user_id = ?", (user_id,)).fetchone()[0]
    if "Дорогой дом" in user_houses:
        await query.answer("🏠У вас уже есть этот дом!🏠", show_alert=True)   
    else:    
        if crypt < 400000:
            await query.answer(f"💸Недостаточно средств! Дорогой дом стоит 400000₵ а у вас только {crypt}💸", show_alert=True)
            return
        client.db.buy_house(user_id=user_id, house_name="Дорогой дом", house_cost=400000)
        crypt = client.db.cursor.execute("SELECT crypt FROM users WHERE user_id = ?", (user_id,)).fetchone()[0]
        await query.answer(f"🏠Дорогой дом куплен!🏠\n Теперь на балансе: {crypt}", show_alert=False)


@bot.on_callback_query(filters=inline_button_filter(buttons.buy_mansion_house_button))
async def buy_mansion_house(client, query: CallbackQuery):
    user_id = query.from_user.id
    crypt = client.db.cursor.execute("SELECT crypt FROM users WHERE user_id = ?", (user_id,)).fetchone()[0]
    user_houses = client.db.cursor.execute("SELECT house FROM users WHERE user_id = ?", (user_id,)).fetchone()[0]
    if "Особняк" in user_houses:
        await query.answer("🏠У вас уже есть этот дом!🏠", show_alert=True)   
    else:    
        if crypt < 10000000:
            await query.answer(f"💸Недостаточно средств! Особняк стоит 10000000₵ а у вас только {crypt}💸", show_alert=True)
            return
        client.db.buy_house(user_id=user_id, house_name="Особняк", house_cost=10000000)
        crypt = client.db.cursor.execute("SELECT crypt FROM users WHERE user_id = ?", (user_id,)).fetchone()[0]
        await query.answer(f"🏠Особняк куплен!🏠\n Теперь на балансе: {crypt}", show_alert=False)


@bot.on_callback_query(filters=inline_button_filter(buttons.buy_mars_house_button))
async def buy_mars_house(client, query: CallbackQuery):
    user_id = query.from_user.id
    crypt = client.db.cursor.execute("SELECT crypt FROM users WHERE user_id = ?", (user_id,)).fetchone()[0]
    user_houses = client.db.cursor.execute("SELECT house FROM users WHERE user_id = ?", (user_id,)).fetchone()[0]
    if "Замок на марсе" in user_houses:
        await query.answer("🏠У вас уже есть этот дом!🏠", show_alert=True)   
    else:    
        if crypt < 6666666666:
            await query.answer(f"💸Недостаточно средств! Замок на марсе стоит 6666666666₵ а у вас только {crypt}💸", show_alert=True)
            return
        client.db.buy_house(user_id=user_id, house_name="Замок на марсе", house_cost=6666666666)
        crypt = client.db.cursor.execute("SELECT crypt FROM users WHERE user_id = ?", (user_id,)).fetchone()[0]
        await query.answer(f"🏠Замок на марсе куплен!🏠\n Теперь на балансе: {crypt}", show_alert=False)
    
# cars handlers
@bot.on_callback_query(filters=inline_button_filter(buttons.cars_button))
async def cars_func(client: Client, query: CallbackQuery):
    await query.edit_message_text("Категория: 🚗Машины\nВыберите машину для покупки:")
    for car in cars:
        name, img, keyboard = car
        await query.message.reply_photo(photo=img, caption=name, reply_markup=keyboard)
    await query.message.reply_text("🎮Чтобы возобновить игру, введите /start. Чтобы вернутья в магазин напишите /shop.")

@bot.on_callback_query(filters=inline_button_filter(buttons.buy_Zaporozhets_car_button))
async def buy_Zaporozhets_car(client: Client, query: CallbackQuery):
    user_id = query.from_user.id
    crypt = client.db.cursor.execute("SELECT crypt FROM users WHERE user_id = ?", (user_id,)).fetchone()[0]
    user_cars = client.db.cursor.execute("SELECT car FROM users WHERE user_id = ?", (user_id,)).fetchone()[0]
    if "Запорожец" in user_cars:
        await query.answer("🚗У вас уже есть эта машина!🚗", show_alert=True)   
    else:    
        if crypt < 500:
            await query.answer(f"💸Недостаточно средств! Запорожец стоит 500₵ а у вас только {crypt}💸", show_alert=True)
            return
        client.db.buy_car(user_id=user_id, car_name="Запорожец", car_cost=500)
        crypt = client.db.cursor.execute("SELECT crypt FROM users WHERE user_id = ?", (user_id,)).fetchone()[0]
        await query.answer(f"🚗Запорожец куплен!🚗\n Теперь на балансе: {crypt}", show_alert=False)

@bot.on_callback_query(filters=inline_button_filter(buttons.buy_Nissan_car_button))
async def buy_Nissan_car(client: Client, query: CallbackQuery):
    user_id = query.from_user.id
    crypt = client.db.cursor.execute("SELECT crypt FROM users WHERE user_id = ?", (user_id,)).fetchone()[0]
    user_cars = client.db.cursor.execute("SELECT car FROM users WHERE user_id = ?", (user_id,)).fetchone()[0]
    if "Nissan Pathfinder" in user_cars:
        await query.answer("🚙У вас уже есть эта машина!🚙", show_alert=True)   
    else:    
        if crypt < 5400:
            await query.answer(f"💸Недостаточно средств! Nissan Pathfinder стоит 5400₵ а у вас только {crypt}💸", show_alert=True)
            return
        client.db.buy_car(user_id=user_id, car_name="Nissan Pathfinder", car_cost=5400)
        crypt = client.db.cursor.execute("SELECT crypt FROM users WHERE user_id = ?", (user_id,)).fetchone()[0]
        await query.answer(f"🚙Nissan Pathfinder куплен!🚙\n Теперь на балансе: {crypt}", show_alert=False)

@bot.on_callback_query(filters=inline_button_filter(buttons.buy_BMW_car_button))
async def buy_BMW_car(client: Client, query: CallbackQuery):
    user_id = query.from_user.id
    crypt = client.db.cursor.execute("SELECT crypt FROM users WHERE user_id = ?", (user_id,)).fetchone()[0]
    user_cars = client.db.cursor.execute("SELECT car FROM users WHERE user_id = ?", (user_id,)).fetchone()[0]
    if "BMW M5" in user_cars:
        await query.answer("🚘У вас уже есть эта машина!🚘", show_alert=True)   
    else:    
        if crypt < 70000:
            await query.answer(f"💸Недостаточно средств! BMW M5 стоит 70000₵ а у вас только {crypt}💸", show_alert=True)
            return
        client.db.buy_car(user_id=user_id, car_name="BMW M5", car_cost=70000)
        crypt = client.db.cursor.execute("SELECT crypt FROM users WHERE user_id = ?", (user_id,)).fetchone()[0]
        await query.answer(f"🚘BMW M5 куплен!🚘\n Теперь на балансе: {crypt}", show_alert=False)

@bot.on_callback_query(filters=inline_button_filter(buttons.buy_Mersedes_car_button))
async def buy_Mersedes_car(client: Client, query: CallbackQuery):
    user_id = query.from_user.id
    crypt = client.db.cursor.execute("SELECT crypt FROM users WHERE user_id = ?", (user_id,)).fetchone()[0]
    user_cars = client.db.cursor.execute("SELECT car FROM users WHERE user_id = ?", (user_id,)).fetchone()[0]
    if "Mercedes-Benz AMG GT" in user_cars:
        await query.answer("🚖У вас уже есть эта машина!🚖", show_alert=True)   
    else:    
        if crypt < 240000:
            await query.answer(f"💸Недостаточно средств! Mercedes-Benz AMG GT стоит 240000₵ а у вас только {crypt}💸", show_alert=True)
            return
        client.db.buy_car(user_id=user_id, car_name="Mercedes-Benz AMG GT", car_cost=240000)
        crypt = client.db.cursor.execute("SELECT crypt FROM users WHERE user_id = ?", (user_id,)).fetchone()[0]
        await query.answer(f"🚖Mercedes-Benz AMG GT куплен!🚖\n Теперь на балансе: {crypt}", show_alert=False)

@bot.on_callback_query(filters=inline_button_filter(buttons.buy_Lamborghini_car_button))
async def buy_Lamborghini_car(client: Client, query: CallbackQuery):
    user_id = query.from_user.id
    crypt = client.db.cursor.execute("SELECT crypt FROM users WHERE user_id = ?", (user_id,)).fetchone()[0]
    user_cars = client.db.cursor.execute("SELECT car FROM users WHERE user_id = ?", (user_id,)).fetchone()[0]
    if "Lamborghini Aventador" in user_cars:
        await query.answer("🏎У вас уже есть эта машина!🏎", show_alert=True)   
    else:    
        if crypt < 790000:
            await query.answer(f"💸Недостаточно средств! Lamborghini Aventador стоит 790000₵ а у вас только {crypt}💸", show_alert=True)
            return
        client.db.buy_car(user_id=user_id, car_name="Lamborghini Aventador", car_cost=790000)
        crypt = client.db.cursor.execute("SELECT crypt FROM users WHERE user_id = ?", (user_id,)).fetchone()[0]
        await query.answer(f"🏎Lamborghini Aventador куплен!🏎\n Теперь на балансе: {crypt}", show_alert=False)

@bot.on_callback_query(filters=inline_button_filter(buttons.buy_mars_car_button))
async def buy_mars_car(client: Client, query: CallbackQuery):
    user_id = query.from_user.id
    crypt = client.db.cursor.execute("SELECT crypt FROM users WHERE user_id = ?", (user_id,)).fetchone()[0]
    user_cars = client.db.cursor.execute("SELECT car FROM users WHERE user_id = ?", (user_id,)).fetchone()[0]
    if "Марсоход" in user_cars:
        await query.answer("🚀У вас уже есть эта машина!🚀", show_alert=True)   
    else:    
        if crypt < 12300000:
            await query.answer(f"💸Недостаточно средств! Марсоход стоит 12300000₵ а у вас только {crypt}💸", show_alert=True)
            return
        client.db.buy_car(user_id=user_id, car_name="Марсоход", car_cost=12300000)
        crypt = client.db.cursor.execute("SELECT crypt FROM users WHERE user_id = ?", (user_id,)).fetchone()[0]
        await query.answer(f"🚀Марсоход куплен!🚀\n Теперь на балансе: {crypt}", show_alert=False)

# Pets handlers
@bot.on_callback_query(filters=inline_button_filter(buttons.pets_button))
async def pets_func(client: Client, query: CallbackQuery):
    await query.edit_message_text("Категория: 🐾Питомцы\nВыберите питомца для покупки:")
    for pet in pets:
        name, img, keyboard = pet
        await query.message.reply_photo(photo=img, caption=name, reply_markup=keyboard)
    await query.message.reply_text("🎮Чтобы возобновить игру, введите /start. Чтобы вернутья в магазин напишите /shop.")


@bot.on_callback_query(filters=inline_button_filter(buttons.buy_cat_pet_button))
async def buy_cat_pet(client: Client, query: CallbackQuery):
    user_id = query.from_user.id
    crypt = client.db.cursor.execute("SELECT crypt FROM users WHERE user_id = ?", (user_id,)).fetchone()[0]
    user_pets = client.db.cursor.execute("SELECT pet FROM users WHERE user_id = ?", (user_id,)).fetchone()[0]
    if "Котенок" in user_pets:
        await query.answer("🐈У вас уже есть этот питомец!🐈", show_alert=True)   
    else:    
        if crypt < 800:
            await query.answer(f"💸Недостаточно средств! Котенок стоит 800₵ а у вас только {crypt}💸", show_alert=True)
            return
        client.db.buy_pet(user_id=user_id, pet_name="Котенок", pet_cost=800)
        crypt = client.db.cursor.execute("SELECT crypt FROM users WHERE user_id = ?", (user_id,)).fetchone()[0]
        await query.answer(f"🐈Котенок куплен!🐈\n Теперь на балансе: {crypt}", show_alert=False)


@bot.on_callback_query(filters=inline_button_filter(buttons.buy_dog_pet_button))
async def buy_dog_pet(client: Client, query: CallbackQuery):
    user_id = query.from_user.id
    crypt = client.db.cursor.execute("SELECT crypt FROM users WHERE user_id = ?", (user_id,)).fetchone()[0]
    user_pets = client.db.cursor.execute("SELECT pet FROM users WHERE user_id = ?", (user_id,)).fetchone()[0]
    if "Щенок" in user_pets:
        await query.answer("🐕У вас уже есть этот питомец!🐕", show_alert=True)   
    else:    
        if crypt < 5000:
            await query.answer(f"💸Недостаточно средств! Щенок стоит 5000₵ а у вас только {crypt}💸", show_alert=True)
            return
        client.db.buy_pet(user_id=user_id, pet_name="Щенок", pet_cost=5000)
        crypt = client.db.cursor.execute("SELECT crypt FROM users WHERE user_id = ?", (user_id,)).fetchone()[0]
        await query.answer(f"🐕Щенок куплен!🐕\n Теперь на балансе: {crypt}", show_alert=False)


@bot.on_callback_query(filters=inline_button_filter(buttons.buy_white_hourse_pet_button))
async def buy_white_horse_pet(client: Client, query: CallbackQuery):
    user_id = query.from_user.id
    crypt = client.db.cursor.execute("SELECT crypt FROM users WHERE user_id = ?", (user_id,)).fetchone()[0]
    user_pets = client.db.cursor.execute("SELECT pet FROM users WHERE user_id = ?", (user_id,)).fetchone()[0]
    if "Белая лошадь" in user_pets:
        await query.answer("🦄У вас уже есть этот питомец!🦄", show_alert=True)   
    else:    
        if crypt < 150000:
            await query.answer(f"💸Недостаточно средств! Белая лошадь стоит 150000₵ а у вас только {crypt}💸", show_alert=True)
            return
        client.db.buy_pet(user_id=user_id, pet_name="Белая лошадь", pet_cost=150000)
        crypt = client.db.cursor.execute("SELECT crypt FROM users WHERE user_id = ?", (user_id,)).fetchone()[0]
        await query.answer(f"🦄Белая лошадь куплена!🦄\n Теперь на балансе: {crypt}", show_alert=False)


@bot.on_callback_query(filters=inline_button_filter(buttons.buy_lion_pet_button))
async def buy_lion_pet(client: Client, query: CallbackQuery):
    user_id = query.from_user.id
    crypt = client.db.cursor.execute("SELECT crypt FROM users WHERE user_id = ?", (user_id,)).fetchone()[0]
    user_pets = client.db.cursor.execute("SELECT pet FROM users WHERE user_id = ?", (user_id,)).fetchone()[0]
    if "Лев" in user_pets:
        await query.answer("🦁У вас уже есть этот питомец!🦁", show_alert=True)   
    else:    
        if crypt < 1000000:
            await query.answer(f"💸Недостаточно средств! Лев стоит 1000000₵ а у вас только {crypt}💸", show_alert=True)
            return
        client.db.buy_pet(user_id=user_id, pet_name="Лев", pet_cost=1000000)
        crypt = client.db.cursor.execute("SELECT crypt FROM users WHERE user_id = ?", (user_id,)).fetchone()[0]
        await query.answer(f"🦁Лев куплен!🦁\n Теперь на балансе: {crypt}", show_alert=False)


@bot.on_callback_query(filters=inline_button_filter(buttons.buy_alien_pet_button))
async def buy_alien_pet(client: Client, query: CallbackQuery):
    user_id = query.from_user.id
    crypt = client.db.cursor.execute("SELECT crypt FROM users WHERE user_id = ?", (user_id,)).fetchone()[0]
    user_pets = client.db.cursor.execute("SELECT pet FROM users WHERE user_id = ?", (user_id,)).fetchone()[0]
    if "Инопланетянин" in user_pets:
        await query.answer("👽У вас уже есть этот питомец!👽", show_alert=True)   
    else:    
        if crypt < 9999999:
            await query.answer(f"💸Недостаточно средств! Инопланетянин стоит 9999999₵ а у вас только {crypt}💸", show_alert=True)
            return
        client.db.buy_pet(user_id=user_id, pet_name="Инопланетянин", pet_cost=9999999)
        crypt = client.db.cursor.execute("SELECT crypt FROM users WHERE user_id = ?", (user_id,)).fetchone()[0]
        await query.answer(f"👽Инопланетянин куплен!👽\n Теперь на балансе: {crypt}", show_alert=False)


# entertainment handlers
@bot.on_callback_query(filters=inline_button_filter(buttons.entertainment_button))
async def entertainment_func(client: Client, query: CallbackQuery):
    await query.edit_message_text("Категория: 🎉Развлечения\nВыберите развлечение для покупки:")
    for entertain in entertainment:
        name, img, keyboard = entertain
        await query.message.reply_photo(photo=img, caption=name, reply_markup=keyboard)
    await query.message.reply_text("🎮Чтобы возобновить игру, введите /start. Чтобы вернутья в магазин напишите /shop.")


@bot.on_callback_query(filters=inline_button_filter(buttons.buy_playstation_entertainment_button))
async def buy_ps5_entertainment(client: Client, query: CallbackQuery):
    user_id = query.from_user.id
    crypt = client.db.cursor.execute("SELECT crypt FROM users WHERE user_id = ?", (user_id,)).fetchone()[0]
    user_entertainment = client.db.cursor.execute("SELECT entertainment FROM users WHERE user_id = ?", (user_id,)).fetchone()[0]
    if "Игровая консоль" in user_entertainment:
        await query.answer("🎮У вас уже есть это развлечение!🎮", show_alert=True)   
    else:    
        if crypt < 3000:
            await query.answer(f"💸Недостаточно средств! Игровая консоль стоит 3000₵ а у вас только {crypt}💸", show_alert=True)
            return
        client.db.buy_entertainment(user_id=user_id, entertainment_name="Игровая консоль", entertainment_cost=3000)
        crypt = client.db.cursor.execute("SELECT crypt FROM users WHERE user_id = ?", (user_id,)).fetchone()[0]
        await query.answer(f"🎮Игровая консоль куплена!🎮\n Теперь на балансе: {crypt}", show_alert=False)


@bot.on_callback_query(filters=inline_button_filter(buttons.buy_billiard_entertainment_button ))
async def buy_billiard_table_entertainment(client: Client, query: CallbackQuery):
    user_id = query.from_user.id
    crypt = client.db.cursor.execute("SELECT crypt FROM users WHERE user_id = ?", (user_id,)).fetchone()[0]
    user_entertainment = client.db.cursor.execute("SELECT entertainment FROM users WHERE user_id = ?", (user_id,)).fetchone()[0]
    if "Стол для бильярда" in user_entertainment:
        await query.answer("🎱У вас уже есть это развлечение!🎱", show_alert=True)   
    else:    
        if crypt < 15000:
            await query.answer(f"💸Недостаточно средств! Стол для бильярда стоит 15000₵ а у вас только {crypt}💸", show_alert=True)
            return
        client.db.buy_entertainment(user_id=user_id, entertainment_name="Стол для бильярда", entertainment_cost=15000)
        crypt = client.db.cursor.execute("SELECT crypt FROM users WHERE user_id = ?", (user_id,)).fetchone()[0]
        await query.answer(f"🎱Стол для бильярда куплен!🎱\n Теперь на балансе: {crypt}", show_alert=False)


@bot.on_callback_query(filters=inline_button_filter(buttons.buy_yacht_entertainment_button))
async def buy_yacht_entertainment(client: Client, query: CallbackQuery):
    user_id = query.from_user.id
    crypt = client.db.cursor.execute("SELECT crypt FROM users WHERE user_id = ?", (user_id,)).fetchone()[0]
    user_entertainment = client.db.cursor.execute("SELECT entertainment FROM users WHERE user_id = ?", (user_id,)).fetchone()[0]
    if "Яхта" in user_entertainment:
        await query.answer("🛥У вас уже есть это развлечение!🛥", show_alert=True)   
    else:    
        if crypt < 750000:
            await query.answer(f"💸Недостаточно средств! Яхта стоит 750000₵ а у вас только {crypt}💸", show_alert=True)
            return
        client.db.buy_entertainment(user_id=user_id, entertainment_name="Яхта", entertainment_cost=750000)
        crypt = client.db.cursor.execute("SELECT crypt FROM users WHERE user_id = ?", (user_id,)).fetchone()[0]
        await query.answer(f"🛥Яхта куплена!🛥\n Теперь на балансе: {crypt}", show_alert=False)


@bot.on_callback_query(filters=inline_button_filter(buttons.buy_plane_entertainment_button))
async def buy_plane_entertainment(client: Client, query: CallbackQuery):
    user_id = query.from_user.id
    crypt = client.db.cursor.execute("SELECT crypt FROM users WHERE user_id = ?", (user_id,)).fetchone()[0]
    user_entertainment = client.db.cursor.execute("SELECT entertainment FROM users WHERE user_id = ?", (user_id,)).fetchone()[0]
    if "Личный самолет" in user_entertainment:
        await query.answer("✈У вас уже есть это развлечение!✈", show_alert=True)   
    else:    
        if crypt < 3200000:
            await query.answer(f"💸Недостаточно средств! Личный самолет стоит 3200000₵ а у вас только {crypt}💸", show_alert=True)
            return
        client.db.buy_entertainment(user_id=user_id, entertainment_name="Личный самолет", entertainment_cost=3200000)
        crypt = client.db.cursor.execute("SELECT crypt FROM users WHERE user_id = ?", (user_id,)).fetchone()[0]
        await query.answer(f"✈Личный самолет куплен!✈\n Теперь на балансе: {crypt}", show_alert=False)


@bot.on_callback_query(filters=inline_button_filter(buttons.buy_mars_stadium_entertainment_button))
async def buy_mars_stadium_entertainment(client: Client, query: CallbackQuery):
    user_id = query.from_user.id
    crypt = client.db.cursor.execute("SELECT crypt FROM users WHERE user_id = ?", (user_id,)).fetchone()[0]
    user_entertainment = client.db.cursor.execute("SELECT entertainment FROM users WHERE user_id = ?", (user_id,)).fetchone()[0]
    if "Стадион на марсе" in user_entertainment:
        await query.answer("🏟У вас уже есть это развлечение!🏟", show_alert=True)   
    else:    
        if crypt < 12345678:
            await query.answer(f"💸Недостаточно средств! Стадион на марсе стоит 12345678₵ а у вас только {crypt}💸", show_alert=True)
            return
        client.db.buy_entertainment(user_id=user_id, entertainment_name="Стадион на марсе", entertainment_cost=12345678)
        crypt = client.db.cursor.execute("SELECT crypt FROM users WHERE user_id = ?", (user_id,)).fetchone()[0]
        await query.answer(f"🏟Стадион на марсе куплен!🏟\n Теперь на балансе: {crypt}", show_alert=False)

@bot.on_message(filters=filters.text)
async def echo_message(client: Client, message: Message):
    await message.reply("Команда не опознана❗️ Пожалуйста, используйте доступные команды из меню. Для просмотра доступных команд введите /help.")


if __name__ == "__main__":
    bot.run()