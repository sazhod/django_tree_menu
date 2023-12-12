from django import template
from menu.models import Menu, MenuItem
from itertools import groupby


register = template.Library()


@register.simple_tag()
def get_tags_for_current_item(current_item: MenuItem, menu_items: list):
    for index, value in enumerate(menu_items):
        if value == current_item:
            break
    count = abs(current_item.level - menu_items[index-1].level)
    tags = ''
    if current_item.level > menu_items[index-1].level:
        tags = '<ul>'
    elif current_item.level < menu_items[index-1].level:
        tags = '</ul>'

    return {'tags': tags * count}


def get_children_menu_items(parent_menu_item: MenuItem, menu: list):
    return [item for item in menu if item.parent_menu_item == parent_menu_item]


def func1(current_item: MenuItem, items_in_current_tree: list):
    return current_item.parent_menu_item in items_in_current_tree


def func2(current_key: MenuItem, dict_items: dict, list_items: list):
    """
    Функция должна рекурсивно формировать текущий путь от выбранного до начала для исключения лишних объектов
    """
    if current_key is None:
        list_items += dict_items[current_key]
        return list_items
    for key in list(dict_items.keys()):
        if key in dict_items[key]:
            current_key = key
        if key == current_key:
            dict_items.pop(key)
            list_items += func2(current_key, dict_items, list_items)

    return list_items




@register.inclusion_tag('menu/tree_menu.html', takes_context=True)
def draw_menu(context, menu_name: str):
    current_item_url = context['menu_item']
    menu = MenuItem.objects.filter(parent_menu__name=menu_name)\
        .select_related('parent_menu_item')
    children = []
    parents = []

    for item in menu[:]:
        if item.parent_menu_item is not None:
            children.append(item)
        else:
            parents.append(item)

    tmp_menu = parents[:]
    for index, item in enumerate(tmp_menu):
        for i, new_item in enumerate(get_children_menu_items(item, children[:])):
            tmp_menu.insert(index+i+1, new_item)

    current_item = None
    for i in range(len(tmp_menu)-1, -1, -1):
        if tmp_menu[i-1].url == current_item_url:
            if tmp_menu[i-1].level + 1 == tmp_menu[i].level:
                current_item = tmp_menu[i-1]

    dct = {}
    for key, group_items in groupby(tmp_menu, key=lambda x: x.parent_menu_item):
        if key in dct:
            dct[key] += list(group_items)
        else:
            dct[key] = list(group_items)
    print(dct)

    lst1 = []
    current_key = current_item

    # for key in list(dct.keys()):
    #     print(key, dct[key])
    #     if key in dct[key]:
    #         current_key = key
    #     if key == current_key:
    #         lst1 += dct.pop(key)
    print(func2(current_key, dct, []))
    print(lst1)
    is_current_item = False
    lst = []
    for i in range(len(tmp_menu) - 1, -1, -1):
        if tmp_menu[i] == current_item:
            is_current_item = True
        if is_current_item and tmp_menu[i].level <= current_item.level:
            lst.append(tmp_menu[i])
        elif is_current_item and tmp_menu[i].level > current_item.level:
            is_current_item = False

        last_level = tmp_menu[i].level
    # print(lst)
    for i in range(len(tmp_menu) - 1, -1, -1):
        if tmp_menu[i].level > 0 and not func1(tmp_menu[i], lst):
            tmp_menu.pop(i)

    return {"menu":  tmp_menu}
