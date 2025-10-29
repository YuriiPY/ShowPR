from aiogram.fsm.state import State, StatesGroup


class Cook_Confirm(StatesGroup):
    Confirm = State()


class CookMenuSelection(StatesGroup):
    main_menu = State()
    Texts = State()
    Settings = State()


class Work(StatesGroup):
    main_work = State()
    work_hours = State()
    confirm_start_work = State()


class Cook_Menu(StatesGroup):
    menu = State()
    coked_menu = State()
    frozen_menu = State()
    delicious_menu = State()
    current_dish_menu = State()

    add_new_dish_menu = State()

    last_menu_window = State()


class Cook_Order(StatesGroup):
    main_window = State()
    current_order = State()
    current_dish_information = State()
    warning_window = State()


class Cook_Settings(StatesGroup):
    main_settings = State()
