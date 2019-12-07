from enum import Enum
from django.db import models
from django.core.validators import MinValueValidator
from django.contrib.auth.models import AbstractUser


class MeasureChoice(Enum):  # A subclass of Enum
    g = "Gramos"
    kg = "Kilogramos"
    taza = "Tazas"
    cuchara = "Cucharas"
    cucharita = "Cucharitas"
    lts = "Litros"
    partes = "Partes"
    cantidad = "Unidades"
    al_gusto = "Al gusto"
    other = "Otro"


class User(AbstractUser):
    class Meta:
        ordering = ["username"]

    email = models.EmailField(unique=True)
    username = models.CharField(max_length=100, unique=True)
    photo = models.CharField(max_length=200, blank=True, null=True)
    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email"]

    def __str__(self):
        return self.username


class Ingredient(models.Model):
    class Meta:
        ordering = ["name"]

    name = models.CharField(max_length=100, unique=True)
    photo = models.CharField(max_length=200, blank=True, null=True)
    generalIngredient = models.ForeignKey(
        "self", on_delete=models.SET_NULL, null=True, blank=True
    )

    def __str__(self):
        return self.name


class Category(models.Model):
    class Meta:
        verbose_name_plural = "categories"
        ordering = ["name"]

    name = models.CharField(max_length=100, unique=True)
    logo = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return self.name


class Recipe(models.Model):
    class Meta:
        ordering = ["name", "author"]

    name = models.CharField(max_length=100)
    description = models.TextField(max_length=100, null=True, blank=True)
    video_url = models.CharField(max_length=100, null=True, blank=True)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    photo = models.CharField(max_length=200, blank=True, null=True)
    ingredients = models.ManyToManyField(Ingredient, through="IngredientRequired")
    editors = models.ManyToManyField(User, related_name="editors")
    category = models.ManyToManyField(Category)

    def __str__(self):
        return self.name


class Step(models.Model):
    class Meta:
        ordering = ["recipe", "order"]
        unique_together = ("recipe", "order")

    text = models.CharField(max_length=200)
    optional = models.BooleanField(default=False)
    photo = models.CharField(max_length=200, blank=True, null=True)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    order = models.IntegerField()

    def __str__(self):
        return str(self.recipe) + ": " + str(self.order) + ".- " + self.text


class IngredientRequired(models.Model):
    class Meta:
        verbose_name_plural = "Ingredients required"
        ordering = ["ingredient", "recipe"]
        unique_together = ("ingredient", "recipe")

    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(
        Ingredient, on_delete=models.CASCADE, related_name="ingredients"
    )
    quantity = models.FloatField(validators=[MinValueValidator(0)])
    measure = models.CharField(
        max_length=50,
        choices=[
            (tag.value, tag.name) for tag in MeasureChoice
        ],  # Choices is a list of Tuple
    )
    optional = models.BooleanField(default=False)
    customMeasure = models.CharField(max_length=200, blank=True, null=True)
    alternatives = models.ManyToManyField(
        Ingredient,
        through="IngredientRequiredAlternative",
        related_name="alternative_ingredients",
    )

    def __str__(self):
        return str(self.ingredient) + " for " + str(self.recipe)


class Menu(models.Model):
    name = models.CharField(max_length=100)
    days = models.IntegerField()
    categories = models.ManyToManyField(Category, through="CategoryPerDay")
    recipes = models.ManyToManyField(Recipe, through="RecipeForDay")

    def __str__(self):
        return self.name


class Refrigerator(models.Model):
    name = models.CharField(max_length=100)
    content = models.ManyToManyField(Ingredient, through="RefrigeratorContent")
    members = models.ManyToManyField(User)
    recipes = models.ManyToManyField(Recipe)
    photo = models.CharField(max_length=200, blank=True, null=True)
    menu = models.OneToOneField(Menu, on_delete=models.CASCADE, primary_key=True)

    def __str__(self):
        return self.name


class RefrigeratorContent(models.Model):
    refrigerator = models.ForeignKey(Refrigerator, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    quantity = models.FloatField(validators=[MinValueValidator(0)])
    measure = models.CharField(
        max_length=50,
        choices=[
            (tag.value, tag.name) for tag in MeasureChoice
        ],  # Choices is a list of Tuple
    )
    customMeasure = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return str(self.ingredient) + " in " + str(self.refrigerator)


class RecipeForDay(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE)
    day = models.IntegerField()

    def __str__(self):
        return (
            str(self.recipe)
            + " for day "
            + str(self.day)
            + " for menu "
            + str(self.menu)
        )


class CategoryPerDay(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE)
    day = models.IntegerField()

    def __str__(self):
        return (
            str(self.category)
            + " for day "
            + str(self.day)
            + " for menu "
            + str(self.menu)
        )


class IngredientRequiredAlternative(models.Model):
    class Meta:
        ordering = ["originalIngredient", "ingredient"]
        unique_together = ("originalIngredient", "ingredient")

    originalIngredient = models.ForeignKey(IngredientRequired, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    quantity = models.FloatField(validators=[MinValueValidator(0)])
    measure = models.CharField(
        max_length=50,
        choices=[
            (tag.value, tag.name) for tag in MeasureChoice
        ],  # Choices is a list of Tuple
    )
    optional = models.BooleanField(default=False)
    customMeasure = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return str(self.ingredient) + " for " + str(self.originalIngredient.recipe)
