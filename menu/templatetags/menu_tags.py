from django import template
from menu.models import Menu, MenuItem


register = template.Library()


def get_full_tree_menu(current: MenuItem, children: list) -> dict:
    """
    Рекурсивная функция, которая позволяет отсортировать все MenuItem
    :param current: Текущий MenuItem
    :param children: Список всех MenuItem
    :return: data: dict {
        'current_object': current,
        'children_objects': [...]
    }
    """
    # print(type(current), type(children))
    data = {
        'current_object': current,
        'children_objects': []
    }
    if children is None or not children:
        del data['children_objects']
        return data
    for i in range(len(children) - 1, -1, -1):
        if children[i].parent_menu_item == current:
            new_current = children[i]
            children.remove(children[i])
            data['children_objects'].append(get_full_tree_menu(new_current, children))
    if not data['children_objects']:
        del data['children_objects']
    return data


@register.inclusion_tag('menu/tree_menu.html', takes_context=True)
def draw_menu(context, menu_name: str):
    # menu = MenuItem.objects.filter(parent_menu__name=menu_name) \
    #     .select_related('parent_menu_item', 'parent_menu_item__title') \
    #     .values('id', 'title', 'parent_menu_item', 'parent_menu_item__title')
    print(context)
    menu = MenuItem.objects.filter(parent_menu__name=menu_name)\
        .select_related('parent_menu_item')
    children = []
    parents = []

    for item in menu:
        if item.parent_menu_item is not None:
            children.append(item)
        else:
            parents.append(item)
    # children = sorted(children, key=lambda d: d['parent_menu_item'])
    # parents = sorted(parents, key=lambda d: d['id'])
    result = {
        'current_object': None,
        'children_objects': []
    }
    for parent in parents:
        result['children_objects'].append(get_full_tree_menu(parent, children[:]))
    return {"menu": {"parent": parents, "child": children, "menu": menu, 'result': result}}



# def show_sub_items(menu, menu_item, data=None, sub_level=0):
#     data2 = []
#     if menu_item is None:
#         return data
#     sub_level += 1
#     for sub_item in menu.filter(parent_menu_item=menu_item):
#         print(f"{'-'*sub_level}{sub_item.title}")
#         data2.append(sub_item)
#         show_sub_items(menu, sub_item, data2, sub_level)
#     return data
#
#
# @register.inclusion_tag('menu/tree_menu.html')
# def draw_menu(menu_name: str):
#     menu = MenuItem.objects.filter(parent_menu__name=menu_name).select_related('parent_menu_item').values()
#     menu_items = {}
#     for item in menu:
#         print(item.title)
#         show_sub_items(menu, item)
#     return {"menu": menu}
