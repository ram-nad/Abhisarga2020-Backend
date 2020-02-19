from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=64)
    priority = models.IntegerField()

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name + "(" + str(self.priority) + ")"


class Sponsor(models.Model):
    name = models.CharField(max_length=100)
    logo = models.ImageField(upload_to='sponsors')
    website = models.URLField()
    category = models.ForeignKey(Category, related_name='sponsors', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.name + "(" + self.category.name + ")"
