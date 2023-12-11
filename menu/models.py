from django.db import models


class Menu(models.Model):
    name = models.CharField(max_length=255)
    url = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name}"


class MenuItem(models.Model):
    title = models.CharField(max_length=255)
    url = models.CharField(max_length=255)
    parent_menu = models.ForeignKey(Menu, on_delete=models.CASCADE, blank=True, null=True, related_name='menu')
    parent_menu_item = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True,
                                         related_name='menu_item')
    level = models.IntegerField(default=0, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if self.parent_menu_item:
            self.level = self.parent_menu_item.level + 1
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.title}"
