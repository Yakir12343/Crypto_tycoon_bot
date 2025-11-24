from pyrogram.types import ReplyKeyboardMarkup, InlineKeyboardMarkup

import buttons

saves_keyboard = InlineKeyboardMarkup(
    [
        [buttons.new_save_button],
        [buttons.load_save_button],
        [buttons.delete_save_button],
    ]
)

main_menu_keyboard = InlineKeyboardMarkup(
    [
        [buttons.buy_video_card_button],
        [buttons.buy_upgrade_button],
        [buttons.shop_button],
        [buttons.profile_button],
        [buttons.end_game_button],
    ]
)            

end_menu_keyboard = InlineKeyboardMarkup(
    [
        [buttons.new_game_button]
    ]
)



tycoon_keyboard = InlineKeyboardMarkup(
    [
        [buttons.start_tycoon_button]
    ]
)

shop_keyboard = InlineKeyboardMarkup(
    [
        [buttons.houses_button],
        [buttons.cars_button],
        [buttons.pets_button],
        [buttons.entertainment_button],
        [buttons.back_button]
    ]
)

continue_keyboard = InlineKeyboardMarkup(
    [
        [buttons.continue_game_button]
    ]
)


houses_keyboards = []
for button in buttons.house_buttons:
    houses_keyboards.append(InlineKeyboardMarkup(
    [
        [button],
    ]))

cars_keyboards = []
for button in buttons.car_buttons:
    cars_keyboards.append(InlineKeyboardMarkup(
    [
        [button],
    ]))
        
pets_keyboards = []
for button in buttons.pet_buttons:
    pets_keyboards.append(InlineKeyboardMarkup(
    [
        [button],
    ]))

entertainment_keyboards = []
for button in buttons.entertainment_buttons:
    entertainment_keyboards.append(InlineKeyboardMarkup(
    [
        [button],
    ]))