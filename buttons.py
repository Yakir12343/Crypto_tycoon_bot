from pyrogram.types import KeyboardButton, InlineKeyboardButton

from custom_filters import button_filter, inline_button_filter

# Кнопки сохранения
new_save_button = InlineKeyboardButton(text="➕ Создать новое сохранение", callback_data="new_save")
load_save_button = InlineKeyboardButton(text="💾 Загрузить сохранение", callback_data="load_save")
delete_save_button = InlineKeyboardButton(text="🗑 Удалить сохранение", callback_data="delete_save")

# Кнопки главного меню
buy_video_card_button = InlineKeyboardButton(text="🛒 Купить видеокарту", callback_data="buy_video_card")
buy_upgrade_button = InlineKeyboardButton(text="⬆ Купить улучшение", callback_data="buy_upgrade")
shop_button = InlineKeyboardButton(text="🛍 Магазин", callback_data="shop")
profile_button = InlineKeyboardButton(text="👤 Профиль", callback_data="profile")
end_game_button = InlineKeyboardButton(text="🏁 Завершить игру", callback_data="end_game")

# Кнопка end menu
new_game_button = InlineKeyboardButton(text="📍 Главное меню 📍", callback_data="end_game")

# продолжить игру
continue_game_button = InlineKeyboardButton(text="▶ Продолжить игру", callback_data="continue_game")

# Начать тайкон
start_tycoon_button = InlineKeyboardButton(text="📍 Начать Крипто Тайкон Бот 📍", callback_data="start_tycoon")

# Кнопки магазина
houses_button = InlineKeyboardButton(text="🏠Дома", callback_data="houses")
cars_button = InlineKeyboardButton(text="🚗Машины", callback_data="cars")
pets_button = InlineKeyboardButton(text="🐕Питомцы", callback_data="pets")
entertainment_button = InlineKeyboardButton(text="🎡Развлечения", callback_data="entertainment")
back_button = InlineKeyboardButton(text="🔙 Назад", callback_data="back_tycoon")

# Кнопки домов
buy_cheep_house_button = InlineKeyboardButton(text="🏠 Купить дешевый дом (1000 крипты)", callback_data="buy_cheep_house")
buy_medium_house_button = InlineKeyboardButton(text="🏡 Купить средний дом (50000 крипты)", callback_data="buy_medium_house")
buy_expensive_house_button = InlineKeyboardButton(text="🏰 Купить дорогой дом (400000 крипты)", callback_data="buy_expensive_house")
buy_mars_house_button = InlineKeyboardButton(text="🚀 Купить дом на Марсе (6666666666 крипты)", callback_data="buy_mars_house")
buy_mansion_house_button = InlineKeyboardButton(text="🏯 Купить особняк (10000000 крипты)", callback_data="buy_mansion_house")

house_buttons = [
    buy_cheep_house_button,
    buy_medium_house_button,
    buy_expensive_house_button,
    buy_mansion_house_button,
    buy_mars_house_button
]

# Кнопки машин
buy_Zaporozhets_car_button = InlineKeyboardButton(text="🚗 Купить Запорожец (500 крипты)", callback_data="buy_Zaporozhets_car")
buy_Nissan_car_button = InlineKeyboardButton(text="🚙 Купить Nissan Pathfinder (5400 крипты)", callback_data="buy_Nissan_car")
buy_BMW_car_button = InlineKeyboardButton(text="🚘 Купить BMW M5 (70000 крипты)", callback_data="buy_BMW_car")
buy_Mersedes_car_button = InlineKeyboardButton(text="🚖 Купить Mercedes-Benz AMG GT (240000 крипты)", callback_data="buy_Mersedes_car")
buy_Lamborghini_car_button = InlineKeyboardButton(text="🏎 Купить Lamborghini Aventador (790000 крипты)", callback_data="buy_Lamborghini_car")
buy_mars_car_button = InlineKeyboardButton(text="🚀 Купить Марсоход (12300000 крипты)", callback_data="buy_mars_car")
car_buttons = [
    buy_Zaporozhets_car_button,
    buy_Nissan_car_button,
    buy_BMW_car_button,
    buy_Mersedes_car_button,
    buy_Lamborghini_car_button,
    buy_mars_car_button
]

# Кнопки питомцев
buy_cat_pet_button = InlineKeyboardButton(text="🐈 Купить котенка (800 крипты)", callback_data="buy_cat_pet")
buy_dog_pet_button = InlineKeyboardButton(text="🐕 Купить щенка (5000 крипты)", callback_data="buy_dog_pet")
buy_white_hourse_pet_button = InlineKeyboardButton(text="🦄 Купить белую лошадь (150000 крипты)", callback_data="buy_white_horse_pet")
buy_lion_pet_button = InlineKeyboardButton(text="🦁 Купить белого львенка (1000000 крипты)", callback_data="buy_lion_pet")
buy_alien_pet_button = InlineKeyboardButton(text="👽 Купить инопланетного питомца (9999999 крипты)", callback_data="buy_alien_pet")
pet_buttons = [
    buy_dog_pet_button,
    buy_cat_pet_button,
    buy_white_hourse_pet_button,
    buy_lion_pet_button,
    buy_alien_pet_button
]

# Кнопки развлечений
buy_playstation_entertainment_button = InlineKeyboardButton(text="🎮 Купить PlayStation 5 (3000 крипты)", callback_data="buy_playstation_entertainment")
buy_billiard_entertainment_button = InlineKeyboardButton(text="🎱 Купить бильярдный стол (15000 крипты)", callback_data="buy_billiard_entertainment")
buy_yacht_entertainment_button = InlineKeyboardButton(text="🛥 Купить яхту (750000 крипты)", callback_data="buy_yacht_entertainment")
buy_plane_entertainment_button = InlineKeyboardButton(text="✈ Купить частный самолет (3200000 крипты)", callback_data="buy_plane_entertainment")
buy_mars_stadium_entertainment_button = InlineKeyboardButton(text="🚀 Купить стадион на Марсе (12345678 крипты)", callback_data="buy_mars_stadium_entertainment")
entertainment_buttons = [
    buy_playstation_entertainment_button,
    buy_billiard_entertainment_button,
    buy_yacht_entertainment_button,
    buy_plane_entertainment_button,
    buy_mars_stadium_entertainment_button
]   