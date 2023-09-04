from django.db import models
from django.contrib.auth import get_user_model
User = get_user_model()


class Module(models.Model):
    code = models.CharField(max_length=20)
    user = models.ForeignKey(
        User, blank=False, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.code


class Page(models.Model):
    user = models.ForeignKey(
        User, blank=False, null=True, on_delete=models.CASCADE)
    page_number = models.PositiveIntegerField()
    module = models.ForeignKey(Module,
                               on_delete=models.CASCADE,
                               related_name='pages')
    content = models.TextField()

    def __str__(self):
        return f"Module: {self.module.code}, Page: {self.page_number}"
