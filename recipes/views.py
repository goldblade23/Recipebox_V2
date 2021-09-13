from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import HttpResponse, HttpResponseRedirect, render, reverse

from recipes.forms import AddAuthorForm, AddRecipeForm, LoginForm
from recipes.models import Author, Recipe

# from django.contrib.admin.views.decorators import staff_member_required


def index(request):
    template_name = "index.html"
    recipes = Recipe.objects.all()
    context = {"recipes": recipes}
    return render(request, template_name, context)


def recipe_detail(request, id):
    template_name = "recipe.html"
    recipe = Recipe.objects.get(id=id)
    context = {"recipe": recipe}
    return render(request, template_name, context)


def author_detail(request, id):
    template_name = "author.html"
    author = Author.objects.get(id=id)
    recipes = Recipe.objects.filter(author=author)
    context = {"author": author, "recipes": recipes}
    return render(request, template_name, context)


def add_author(request):
    if not request.user.is_staff:
        return HttpResponse("Access Denied - Need staff/admin permissions")
    if request.method == "POST":
        form = AddAuthorForm(request.POST)

        if form.is_valid():
            data = form.cleaned_data
            user = User.objects.create_user(
                username=data.get("username"), password=data.get("password")
            )
            author = Author.objects.create(
                name=data.get("name"), bio=data.get("bio"), user=user
            )
            return HttpResponseRedirect(reverse("homepage"))

    else:
        form = AddAuthorForm()

    return render(request, "generic_form.html", {"form": form})


@login_required
def add_recipe(request):
    if request.method == "POST":
        form = AddRecipeForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            author = Recipe.objects.create(
                title=data.get("title"),
                author=data.get("author"),
                description=data.get("description"),
                time_required=data.get("time_required"),
                instructions=data.get("instructions"),
            )
            return HttpResponseRedirect(reverse("homepage"))

    else:
        form = AddRecipeForm()

    return render(request, "generic_form.html", {"form": form})


def login_view(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = authenticate(
                request, username=data.get("username"), password=data.get("password")
            )
            if user:
                login(request, user)
                return HttpResponseRedirect(
                    request.GET.get("next", reverse("homepage"))
                )
    else:
        form = LoginForm()
    return render(request, "generic_form.html", {"form": form})


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("homepage"))
