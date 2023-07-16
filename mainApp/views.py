from django.shortcuts import render, HttpResponseRedirect
from django.contrib.auth.models import User
from mainApp.models import Recipe
from django.contrib import messages
from django.contrib.auth import authenticate , login , logout
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required(login_url="/login/")
def homepage(Request):
    if Request.method == "POST":

        data= Request.POST
        recipe_image= Request.FILES.get('recipe_image')
        recipe_name= data.get('recipe_name')
        recipe_description= data.get('recipe_description')

        Recipe.objects.create(
            recipe_image= recipe_image,
            recipe_name= recipe_name,
            recipe_description= recipe_description,
            
        )

        return HttpResponseRedirect('/')
    
    queryset= Recipe.objects.all()

    if Request.GET.get('search'):
        queryset= queryset.filter(recipe_name__icontains= Request.GET.get('search'))
    context={'recipes': queryset}
    return render(Request,"index.html",context)


def delete_recipe(Request,id):
    queryset= Recipe.objects.get(id = id)
    queryset.delete()
    return HttpResponseRedirect('/view/')
 
def update_recipe(Request,id):
    queryset= Recipe.objects.get(id = id)

    if Request.method == "POST":
        data= Request.POST

        recipe_image= Request.FILES.get('recipe_image')
        recipe_name= data.get('recipe_name')
        recipe_description= data.get('recipe_description')

        queryset.recipe_name = recipe_name
        queryset.recipe_description = recipe_description

        if recipe_image:
            queryset.recipe_image = recipe_image

        queryset.save()
        return HttpResponseRedirect('/view/')


    context={'recipe': queryset}

    return render(Request,"update.html",context)

@login_required(login_url="/login/")
def addPage(Request):
    if Request.method == "POST":

        data= Request.POST
        recipe_image= Request.FILES.get('recipe_image')
        recipe_name= data.get('recipe_name')
        recipe_description= data.get('recipe_description')

        Recipe.objects.create(
            recipe_image= recipe_image,
            recipe_name= recipe_name,
            recipe_description= recipe_description,
            
        )

        return HttpResponseRedirect('/view/')
    
    
    return render(Request,"add.html") 

@login_required(login_url="/login/")
def viewPage(Request):
    queryset= Recipe.objects.all()

    if Request.GET.get('search'):
        queryset= queryset.filter(recipe_name__icontains= Request.GET.get('search'))
    context={'recipes': queryset}
    return render(Request,"view.html",context)


def registerPage(Request):

    if Request.method == "POST":
        first_name= Request.POST.get('first_name')
        last_name= Request.POST.get('last_name')
        username= Request.POST.get('username')
        password= Request.POST.get('password')

        user= User.objects.filter(username = username)

        if user.exists():
            messages.info(Request, "User name already taken try some other name")
            return HttpResponseRedirect('/register/')

        user= User.objects.create(
            first_name= first_name,
            last_name= last_name,
            username= username,
        )
        user.set_password(password)
        user.save()
        messages.info(Request, "User created Successfully")

        return HttpResponseRedirect('/register/')

    return render(Request,"register.html")

def loginPage(Request):
          
    if Request.method == 'POST':
        username= Request.POST.get('username')
        password= Request.POST.get('password')

        if not User.objects.filter(username = username).exists():
            
            messages.error(Request,"Invalid User Name ")
            return HttpResponseRedirect('/login/')
    
        user = authenticate(username = username , password = password )

        if user is None:
            messages.error(Request,"Invalid Password")
            return HttpResponseRedirect('/login/')
        
        else:
            login(Request,user)
            return HttpResponseRedirect('/')

    return render(Request,"login.html")

def logoutPage(Request):
    logout(Request)
    return HttpResponseRedirect('/login/')