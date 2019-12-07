from rest_framework.serializers import (
    ModelSerializer,
    PrimaryKeyRelatedField,
    HyperlinkedIdentityField,
)
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import (
    Recipe,
    Category,
    Ingredient,
    Step,
    IngredientRequired,
    IngredientRequiredAlternative,
    User,
)

# Recipe


class RecipeUserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username"]
        extra_kwargs = {"username": {"validators": []}, "id": {"read_only": False}}


class RecipeCategorySerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = ["name", "logo"]


class RecipeStepSerializer(ModelSerializer):
    class Meta:
        model = Step
        fields = ["id", "text", "optional", "photo", "order"]
        extra_kwargs = {
            "id": {"read_only": False},
            "order": {"validators": []},
            "recipe_id": {"validators": []},
        }
        validators = []


class RecipeIngredientSerializer(ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ["id", "name", "photo"]
        extra_kwargs = {"id": {"read_only": False}, "name": {"validators": []}}
        validators = []


class RecipeIngredientRequiredAlternativeSerializer(ModelSerializer):
    ingredient = RecipeIngredientSerializer(label="name")

    class Meta:
        model = IngredientRequiredAlternative
        fields = [
            "id",
            "ingredient",
            "quantity",
            "measure",
            "optional",
            "customMeasure",
        ]
        extra_kwargs = {"id": {"read_only": False}}


class RecipeIngredientRequiredSerializer(ModelSerializer):
    ingredient = RecipeIngredientSerializer(label="name")
    alternatives = RecipeIngredientRequiredAlternativeSerializer(
        source="ingredientrequiredalternative_set", many=True
    )

    class Meta:
        model = IngredientRequired
        fields = [
            "id",
            "ingredient",
            "quantity",
            "measure",
            "optional",
            "customMeasure",
            "alternatives",
        ]
        extra_kwargs = {"id": {"read_only": False}}


class RecipeSerializer(ModelSerializer):
    author = RecipeUserSerializer()
    editors = RecipeUserSerializer(many=True)
    ingredients = RecipeIngredientRequiredSerializer(
        source="ingredientrequired_set", many=True
    )
    steps = RecipeStepSerializer(source="step_set", many=True)

    class Meta:
        model = Recipe
        fields = [
            "id",
            "name",
            "author",
            "photo",
            "video_url",
            "category",
            "ingredients",
            "steps",
            "editors",
        ]
        depth = 2
        extra_kwargs = {"id": {"read_only": False}}
        validators = []


class RecipeListSerializer(ModelSerializer):
    author = RecipeUserSerializer()
    ingredients = RecipeIngredientRequiredSerializer(
        source="ingredientrequired_set", many=True
    )

    class Meta:
        model = Recipe
        fields = [
            "id",
            "name",
            "author",
            "photo",
            "video_url",
            "category",
            "ingredients",
        ]
        depth = 2
        extra_kwargs = {"id": {"read_only": False}}
        validators = []


# Recipe Update


class RecipeUpdateIngredientRequiredAlternativeSerializer(ModelSerializer):
    ingredient = PrimaryKeyRelatedField(queryset=Ingredient.objects.all())

    class Meta:
        model = IngredientRequiredAlternative
        fields = [
            "id",
            "ingredient",
            "quantity",
            "measure",
            "optional",
            "customMeasure",
        ]
        extra_kwargs = {"id": {"read_only": False}}


class RecipeUpdateIngredientRequiredSerializer(ModelSerializer):
    ingredient = PrimaryKeyRelatedField(queryset=Ingredient.objects.all())
    alternatives = RecipeUpdateIngredientRequiredAlternativeSerializer(
        source="ingredientrequiredalternative_set", many=True
    )

    class Meta:
        model = IngredientRequired
        fields = [
            "id",
            "ingredient",
            "quantity",
            "measure",
            "optional",
            "customMeasure",
            "alternatives",
        ]
        extra_kwargs = {"id": {"read_only": False}}


class RecipeUpdateSerializer(ModelSerializer):
    author = PrimaryKeyRelatedField(queryset=User.objects.all())
    category = PrimaryKeyRelatedField(queryset=Category.objects.all(), many=True)
    ingredients = RecipeUpdateIngredientRequiredSerializer(
        source="ingredientrequired_set", many=True
    )
    steps = RecipeStepSerializer(source="step_set", many=True)
    editors = PrimaryKeyRelatedField(
        queryset=User.objects.all(), many=True, allow_null=True
    )

    class Meta:
        model = Recipe
        fields = [
            "id",
            "name",
            "author",
            "photo",
            "video_url",
            "category",
            "ingredients",
            "steps",
            "editors",
        ]
        depth = 2
        extra_kwargs = {"id": {"read_only": False}}
        validators = []

    def update(self, instance, validated_data):
        steps_data = validated_data.pop("step_set")
        ingredients_data = validated_data.pop("ingredientrequired_set")
        category_data = validated_data.get("category", instance.category)
        editors_data = validated_data.pop("editors")
        instance.name = validated_data.get("name", instance.name)
        instance.author = validated_data.get("author", instance.author)
        instance.photo = validated_data.get("photo", instance.photo)
        instance.category.clear()
        for category in category_data:
            instance.category.add(category)
        instance.editors.clear()
        for editor in editors_data:
            instance.editors.add(editor)
        instance.video_url = validated_data.get("video_url", instance.video_url)
        all_steps = instance.step_set.all()
        for step in steps_data:
            step_id = step.get("id", None)
            all_steps = all_steps.exclude(id=step_id)
        all_steps.all().delete()
        for step in steps_data:
            step_id = step.get("id", None)
            if step_id and step_id != 0:
                up_step = Step.objects.get(id=step_id)
                up_step.text = step.get("text", up_step.text)
                up_step.optional = step.get("optional", up_step.optional)
                up_step.photo = step.get("photo", up_step.photo)
                up_step.order = step.get("order", up_step.order)
                up_step.save()
            else:
                step.pop("id")
                new_step = Step.objects.create(recipe=instance, **step)
                all_steps = all_steps.exclude(id=new_step.id)

        all_ingredients = instance.ingredientrequired_set.all()
        for ingredient in ingredients_data:
            alternative_data = ingredient.pop("ingredientrequiredalternative_set")
            ingredient_id = ingredient.get("id", None)
            if ingredient_id and ingredient_id != 0:
                all_ingredients = all_ingredients.exclude(id=ingredient_id)
                up_ingredient = IngredientRequired.objects.get(id=ingredient_id)
                up_ingredient.ingredient = ingredient.get(
                    "ingredient", up_ingredient.ingredient.id
                )
                up_ingredient.quantity = ingredient.get(
                    "quantity", up_ingredient.quantity
                )
                up_ingredient.measure = ingredient.get("measure", up_ingredient.measure)
                up_ingredient.optional = ingredient.get(
                    "optional", up_ingredient.optional
                )
                up_ingredient.customMeasure = ingredient.get(
                    "customMeasure", up_ingredient.customMeasure
                )
                up_ingredient.save()
            else:
                ingredient.pop("id")
                up_ingredient = IngredientRequired.objects.create(
                    recipe=instance, **ingredient
                )
                all_ingredients = all_ingredients.exclude(id=up_ingredient.id)
            all_alternatives = up_ingredient.ingredientrequiredalternative_set.all()
            for alternative in alternative_data:
                alternative_id = alternative.get("id", None)
                if alternative_id and ingredient_id != 0:
                    all_alternatives = all_alternatives.exclude(id=alternative_id)
                    up_alternative = IngredientRequiredAlternative.objects.get(
                        id=alternative_id
                    )
                    up_alternative.ingredient = alternative.get(
                        "ingredient", up_alternative.ingredient
                    )
                    up_alternative.quantity = alternative.get(
                        "quantity", up_alternative.quantity
                    )
                    up_alternative.measure = alternative.get(
                        "measure", up_alternative.measure
                    )
                    up_alternative.optional = alternative.get(
                        "optional", up_alternative.optional
                    )
                    up_alternative.customMeasure = alternative.get(
                        "customMeasure", up_alternative.customMeasure
                    )
                    up_alternative.save()
                else:
                    alternative.pop("id")
                    new_alt = IngredientRequiredAlternative.objects.create(
                        originalIngredient=up_ingredient, **alternative
                    )
                    all_alternatives = all_alternatives.exclude(id=new_alt.id)
            all_alternatives.all().delete()
        all_ingredients.all().delete()
        instance.save()
        return instance


# Recipe Create


class RecipeCreateIngredientRequiredAlternativeSerializer(ModelSerializer):
    ingredient = PrimaryKeyRelatedField(queryset=Ingredient.objects.all())

    class Meta:
        model = IngredientRequiredAlternative
        fields = ["ingredient", "quantity", "measure", "optional", "customMeasure"]


class RecipeCreateIngredientRequiredSerializer(ModelSerializer):
    ingredient = PrimaryKeyRelatedField(queryset=Ingredient.objects.all())
    alternatives = RecipeCreateIngredientRequiredAlternativeSerializer(
        source="ingredientrequiredalternative_set", many=True
    )

    class Meta:
        model = IngredientRequired
        fields = [
            "ingredient",
            "quantity",
            "measure",
            "optional",
            "customMeasure",
            "alternatives",
        ]


class RecipeCreateStepSerializer(ModelSerializer):
    class Meta:
        model = Step
        fields = ["text", "optional", "photo", "order"]


class RecipeCreateSerializer(ModelSerializer):
    author = PrimaryKeyRelatedField(queryset=User.objects.all())
    category = PrimaryKeyRelatedField(
        queryset=Category.objects.all(), many=True, allow_null=True
    )
    ingredients = RecipeCreateIngredientRequiredSerializer(
        source="ingredientrequired_set", many=True
    )
    steps = RecipeCreateStepSerializer(source="step_set", many=True)
    editors = PrimaryKeyRelatedField(
        queryset=User.objects.all(), many=True, allow_null=True
    )

    class Meta:
        model = Recipe
        fields = [
            "id",
            "name",
            "author",
            "photo",
            "video_url",
            "category",
            "ingredients",
            "steps",
            "editors",
        ]

    def create(self, validated_data):
        steps_data = validated_data.pop("step_set")
        ingredients_data = validated_data.pop("ingredientrequired_set")
        category_data = validated_data.pop("category")
        editors_data = validated_data.pop("editors")
        recipe = Recipe.objects.create(**validated_data)
        for category in category_data:
            recipe.category.add(category)
        for editor in editors_data:
            recipe.editors.add(editor)
        recipe.save()

        for step in steps_data:
            Step.objects.create(recipe=recipe, **step)
        for ingredient in ingredients_data:
            alternative_data = ingredient.pop("ingredientrequiredalternative_set")
            ingredient = IngredientRequired.objects.create(recipe=recipe, **ingredient)
            for alternative in alternative_data:
                IngredientRequiredAlternative.objects.create(
                    originalIngredient=ingredient, **alternative
                )
        return recipe


# Ingredient


class IngredientSerializer(ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ["id", "name", "photo"]


class IngredientUpdateSerializer(ModelSerializer):
    generalIngredient = PrimaryKeyRelatedField(queryset=Ingredient.objects.all())

    class Meta:
        model = Ingredient
        fields = ["id", "name", "photo", "generalIngredient"]


class IngredientCreateSerializer(ModelSerializer):
    generalIngredient = PrimaryKeyRelatedField(
        queryset=Ingredient.objects.all(), allow_null=True
    )

    class Meta:
        model = Ingredient
        fields = ["id", "name", "photo", "generalIngredient"]


# Category


class CategorySerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name", "logo"]


class CategoryCreateSerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name", "logo"]


# USER
class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        refresh = self.get_token(self.user)
        data["refresh"] = str(refresh)
        data["access"] = str(refresh.access_token)
        user_dict = {}
        user_dict["id"] = self.user.id
        user_dict["username"] = self.user.username
        user_dict["photo"] = self.user.photo
        user_dict["first_name"] = self.user.first_name
        user_dict["last_name"] = self.user.last_name
        user_dict["email"] = self.user.email

        # Add extra responses here
        data["user"] = user_dict
        return data


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username"]
        extra_kwargs = {"username": {"validators": []}, "id": {"read_only": False}}
