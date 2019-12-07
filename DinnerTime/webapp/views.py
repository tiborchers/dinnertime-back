# Create your views here.
from rest_framework import status
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.generics import (
    ListAPIView,
    RetrieveDestroyAPIView,
    UpdateAPIView,
    CreateAPIView,
    RetrieveUpdateDestroyAPIView,
)
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import (
    IsAuthenticated,
    IsAuthenticatedOrReadOnly,
    AllowAny,
)
from .models import *
from .serializers import *
import random


class BaseManageView(APIView):
    """
    The base class for ManageViews
        A ManageView is a view which is used to dispatch the requests to the appropriate views
        This is done so that we can use one URL with different methods (GET, PUT, etc)
    """

    def dispatch(self, request, *args, **kwargs):
        if not hasattr(self, "VIEWS_BY_METHOD"):
            raise Exception(
                "VIEWS_BY_METHOD static dictionary variable must be defined on a ManageView class!"
            )
        if request.method in self.VIEWS_BY_METHOD:
            return self.VIEWS_BY_METHOD[request.method]()(request, *args, **kwargs)

        return Response(status=405)


# Recipe


class RecipeDetailAPIView(RetrieveDestroyAPIView):
    permission_classes = (AllowAny,)
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    lookup_field = "id"


class RecipeUpdateAPIView(UpdateAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Recipe.objects.all()
    serializer_class = RecipeUpdateSerializer
    lookup_field = "id"


class RecipeCreateAPIView(CreateAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Recipe.objects.all()
    serializer_class = RecipeCreateSerializer
    lookup_field = "id"


class RecipeListAPIView(APIView):
    permission_classes = (AllowAny,)

    def get(self, request):
        data = Recipe.objects.all()
        categories = request.GET.get("categories")
        if categories is not None:
            catlist = categories.split(",")
            for i in catlist:
                category = get_object_or_404(Category, pk=i)
                data = data & category.recipe_set.all()
        ingredients = request.GET.get("ingredients")
        if ingredients is not None:
            inglist = ingredients.split(",")
            data = list(data)
            for i in inglist:
                ingredient = get_object_or_404(Ingredient, pk=i)
                hola = get_all_recipes_by_ingredient([], ingredient)
                data = list(set(data) & set(hola))
        data = RecipeListSerializer(data, many=True).data
        return Response(data, status=status.HTTP_200_OK)


class RecipeManageView(BaseManageView):
    VIEWS_BY_METHOD = {
        "DELETE": RecipeDetailAPIView.as_view,
        "GET": RecipeDetailAPIView.as_view,
        "PUT": RecipeUpdateAPIView.as_view,
        "PATCH": RecipeUpdateAPIView.as_view,
    }


class RecipeListManageView(BaseManageView):
    VIEWS_BY_METHOD = {
        "GET": RecipeListAPIView.as_view,
        "POST": RecipeCreateAPIView.as_view,
    }


# Ingredient
class IngredientListAPIView(ListAPIView):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer


class IngredientCreateAPIView(CreateAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Ingredient.objects.all()
    serializer_class = IngredientCreateSerializer
    lookup_field = "id"


class IngredientListManageView(BaseManageView):
    VIEWS_BY_METHOD = {
        "GET": IngredientListAPIView.as_view,
        "POST": IngredientCreateAPIView.as_view,
    }


class IngredientDetailAPIView(RetrieveDestroyAPIView):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    lookup_field = "id"


class IngredientUpdateAPIView(UpdateAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Ingredient.objects.all()
    serializer_class = IngredientUpdateSerializer
    lookup_field = "id"


def get_all_recipes_by_ingredient(recipe_list, ingredient):
    recipe_list = recipe_list + list(ingredient.recipe_set.all())
    other_ingredients = list(
        IngredientRequiredAlternative.objects.filter(ingredient=ingredient.id)
    )
    for i in other_ingredients:
        recipe_list.append(i.originalIngredient.recipe)
    if ingredient.generalIngredient:
        return get_all_recipes_by_ingredient(recipe_list, ingredient.generalIngredient)
    return recipe_list


class IngredientRecipeList(APIView):
    def get(self, request, id):
        ingredient = get_object_or_404(Ingredient, pk=self.kwargs["id"])
        hola = get_all_recipes_by_ingredient([], ingredient)
        data = RecipeSerializer(hola, many=True).data
        return Response(data, status=status.HTTP_200_OK)


class IngredientManageView(BaseManageView):
    VIEWS_BY_METHOD = {
        "DELETE": IngredientDetailAPIView.as_view,
        "GET": IngredientDetailAPIView.as_view,
        "PUT": IngredientUpdateAPIView.as_view,
        "PATCH": IngredientUpdateAPIView.as_view,
    }


# Categories


class CategoryListAPIView(ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class CategoryCreateAPIView(CreateAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Category.objects.all()
    serializer_class = CategoryCreateSerializer
    lookup_field = "id"


class CategoryListManageView(BaseManageView):
    VIEWS_BY_METHOD = {
        "GET": CategoryListAPIView.as_view,
        "POST": CategoryCreateAPIView.as_view,
    }


class CategoryDetailAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = "id"


class CategoryRecipeAPIView(APIView):
    def get(self, request, id):
        category = get_object_or_404(Category, pk=self.kwargs["id"])
        data = RecipeSerializer(category.recipe_set.all(), many=True).data
        return Response(data, status=status.HTTP_200_OK)


# User
class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


class UserListAPIView(ListAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = User.objects.all()
    serializer_class = UserSerializer


# Filter given queries


class RecipeRandomAPIView(APIView):
    def get(self, request):
        data = Recipe.objects.all()
        categories = request.GET.get("categories")
        if categories is not None:
            catlist = categories.split(",")
            for i in catlist:
                category = get_object_or_404(Category, pk=i)
                data = data & category.recipe_set.all()
        ingredients = request.GET.get("ingredients")
        if ingredients is not None:
            inglist = ingredients.split(",")
            data = list(data)
            for i in inglist:
                ingredient = get_object_or_404(Ingredient, pk=i)
                hola = get_all_recipes_by_ingredient([], ingredient)
                data = list(set(data) & set(hola))
        data = random.choice(data)
        print(data)
        data = RecipeSerializer(data, context={"request": request}).data

        return Response(data, status=status.HTTP_200_OK)
