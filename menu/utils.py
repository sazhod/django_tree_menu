from .models import MenuItem


def get_children_menu_items(parent_menu_item: MenuItem, menu: list) -> list:
    """
    Функция, которая возвращает список вложенных MenuItem
    :param parent_menu_item: Родительский MenuItem для которого ищем вложенные
    :param menu: Список всех MenuItem
    :return:
    """
    return [item for item in menu if item.parent_menu_item == parent_menu_item]


def get_parent_menu_item(current_item: MenuItem, group_items: dict) -> MenuItem:
    """
    Функция, которая возвращает родительский MenuItem вложенного MenuItem
    :param current_item: Вложенный MenuItem
    :param group_items:  Словарь сгруппированных MenuItems { MenuItem: [MenuItem] }
    :return:
    """
    for key, value in group_items.items():
        if current_item in value:
            return key


def get_current_menu_item(current_item_url: str, menu_items: list) -> MenuItem | None:
    """
    Функция, которая определяет и возвращает следующий MenuItem после выбранного по переданному url.
    Следующий MenuItem становится текущим.
    Если найденный MenuItem не имеет вложенных объектов, то вернется None
    :param current_item_url: url выбранного MenuItem
    :param menu_items: Список отсортированных MenuItem
    :return:
    """
    for i in range(len(menu_items) - 1, -1, -1):
        if menu_items[i - 1].url == current_item_url:
            if menu_items[i - 1].level + 1 == menu_items[i].level:
                return menu_items[i - 1]
            else:
                return None


def get_sorted_menu_items(menu_items: list) -> list:
    """
    Функция принимает сырой список MenuItem и возвращает отсортированный список MenuItem
    :param menu_items: Сырой список MenuItem
    :return:
    """
    children = []
    parents = []

    for item in menu_items:
        if item.parent_menu_item is not None:
            children.append(item)
        else:
            parents.append(item)

    sorted_menu = parents[:]
    for index, item in enumerate(sorted_menu):
        for i, new_item in enumerate(get_children_menu_items(item, children)):
            sorted_menu.insert(index + i + 1, new_item)

    return sorted_menu
