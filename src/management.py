if __package__ is None or __package__ == '':
    import ui
    from utils import to_lowercase
    import shop_management
    import monster_management
else:
    from . import ui
    from .utils import to_lowercase
    from . import shop_management
    from . import monster_management


def run(GAME_STATE: dict[str, dict[str, str]]):
    while True:
        menu = _management_main_menu()

        if menu == 'exit':
            return
        elif menu == 'shop':
            shop_management.shop_admin(GAME_STATE)
        elif menu == 'monster':
            monster_management.monster_admin(GAME_STATE)
    return


def _management_main_menu() -> str:
    while True:
        contents = [
        {"type": "ASCII", "text": "MANAGE", "width": 98, "align": "^"},
        {"type": "TEXT", "text": "Silahkan pilih menu yang ingin kamu buka", "width": 0, "align": "^", "max_length": 80, "inner_align": "^"},
        {"type": "NEWLINE"},
        {"type": "BUTTON", "text": "Shop", "inner_width": 30, "inner_align": "^", "width": 98, "align": "^", "isNumbered": True},
        {"type": "BUTTON", "text": "Monster", "inner_width": 30, "inner_align": "^", "width": 98, "align": "^", "isNumbered": True},
        {"type": "BUTTON", "text": "Keluar", "inner_width": 30, "inner_align": "^", "width": 98, "align": "^", "isNumbered": True},
                ]
        choice = ui.render_menu([], contents, "Masukkan pilihanmu")
        choice = to_lowercase(choice)
        if choice == "1": choice = "shop"
        if choice == "2": choice = "monster"
        if choice == "3" or choice == 'keluar': choice = "exit"

        if choice in  ['shop', 'monster', 'exit']:
            return choice
