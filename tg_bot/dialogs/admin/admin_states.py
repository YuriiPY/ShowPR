from aiogram.fsm.state import State, StatesGroup


class AdminMenuSelection(StatesGroup):
    main_menu = State()
    Cooks = State()
    Texts = State()
    Settings = State()


class Server(StatesGroup):
    Server = State()
    Selection_close_time = State()


class Admin_Confirm(StatesGroup):
    Confirm = State()


class Admin_Menu(StatesGroup):
    menu = State()
    coked_menu = State()
    frozen_menu = State()
    delicious_menu = State()
    current_dish_menu = State()

    add_new_dish_menu = State()

    last_menu_window = State()


class Cooks(StatesGroup):
    cooks_list = State()
    current_cook = State()
    last_cook_window = State()


class Admin_Settings(StatesGroup):
    main_settings = State()


class Admin_Order(StatesGroup):
    main_window = State()
    current_order = State()
    current_dish_information = State()
    warning_window = State()
