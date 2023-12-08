from django.db import models


class Menu(models.Model):
    title = models.CharField(max_length=255)
    url = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title}"


class MenuItem(models.Model):
    title = models.CharField(max_length=255)
    url = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    parent_menu = models.ForeignKey(Menu, on_delete=models.CASCADE, blank=True, null=True, related_name='menu')
    parent_menu_item = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True,
                                         related_name='menu_item')

    def __str__(self):
        return f"{self.title}"
