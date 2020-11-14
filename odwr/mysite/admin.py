from django.contrib import admin
from mysite import models
# Register your models here.

@admin.register(models.Institution)
class InstitutionAdmin(admin.ModelAdmin ):
    pass

@admin.register(models.Category)
class CategoryAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)
