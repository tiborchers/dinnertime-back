from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from django import forms
from django.forms import PasswordInput, ModelForm
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

# Register your models here.

from .models import (
    Step,
    Recipe,
    Ingredient,
    IngredientRequired,
    IngredientRequiredAlternative,
    User,
    Category,
)


class MyUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = User
        widgets = {"password": PasswordInput()}


class MyUserAdmin(UserAdmin):
    form = MyUserChangeForm
    fieldsets = UserAdmin.fieldsets + ((None, {"fields": ("photo",)}),)


admin.site.register(Step)
admin.site.register(Recipe)
admin.site.register(Ingredient)
admin.site.register(IngredientRequired)
admin.site.register(IngredientRequiredAlternative)
admin.site.register(User, MyUserAdmin)
admin.site.register(Category)
