"""DinnerTime URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls import url
from rest_framework_simplejwt import views as jwt_views

from .views import (
    RecipeListManageView,
    RecipeManageView,
    IngredientListManageView,
    IngredientManageView,
    CategoryListManageView,
    CategoryDetailAPIView,
    IngredientRecipeList,
    CategoryRecipeAPIView,
    RecipeRandomAPIView,
    MyTokenObtainPairView,
    UserListAPIView,
)

urlpatterns = [
    url(r"^recipes/$", RecipeListManageView.as_view(), name="Recipes"),
    url(
        r"^recipes/(?P<id>\d+)/$",
        RecipeManageView.as_view(),
        name="Recipe_detail_update_delete",
    ),
    url(r"^categories/$", CategoryListManageView.as_view(), name="Catgories"),
    url(
        r"^categories/(?P<id>\d+)/$",
        CategoryDetailAPIView.as_view(),
        name="Category_detail_update_delete",
    ),
    url(
        r"^categories/(?P<id>\d+)/recipes/$",
        CategoryRecipeAPIView.as_view(),
        name="Category_detail_update_delete",
    ),
    url(r"^ingredients/$", IngredientListManageView.as_view(), name="Ingredients"),
    url(
        r"^ingredients/(?P<id>\d+)/$",
        IngredientManageView.as_view(),
        name="Ingredient_detail_update_delete",
    ),
    url(
        r"^ingredients/(?P<id>\d+)/recipes/$",
        IngredientRecipeList.as_view(),
        name="Ingredient_detail_update_delete",
    ),
    url(
        r"^random/$",
        RecipeRandomAPIView.as_view(),
        name="Ingredient_detail_update_delete",
    ),
    url(r"^users/$", UserListAPIView.as_view(), name="users_list"),
    path("token/", MyTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", jwt_views.TokenRefreshView.as_view(), name="token_refresh"),
]
