from django.http import HttpResponseRedirect
from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control

# Create your views here.
@cache_control(no_cache=True,must_revalidate=True,no_store=True)
def index(request):
    if request.user.is_authenticated:
        return redirect('home')
    return render(request, 'user_auth/login_page.html')


@cache_control(no_cache=True,must_revalidate=True,no_store=True)
@login_required(login_url='signin')
def home(request):
    return render(request, 'user_auth/index_page.html')

# sign-up page 
@cache_control(no_cache=True,must_revalidate=True,no_store=True)
def signup(request):

# capturing the form input values from the HTTP POST request 
    if request.method== 'POST':
        username = request.POST.get("username")
        firstname = request.POST.get("firstname")
        lastname = request.POST.get("lastname")
        email = request.POST.get("email")
        pass1 = request.POST.get("pass1")
        pass2 = request.POST.get("pass2")

# Form validation for signup details
        if User.objects.filter(username=username):
            messages.error(request, "Username already exist!")
            return redirect('signup')
        
        if User.objects.filter(email=email):
            messages.error(request, "email already exist!")
            return redirect('signup')
        
        
        if not  username:
            messages.error(request, 'please enter the user name')
            return redirect('signup')

        if not  firstname:
            messages.error(request, 'please enter first name')
            return redirect('signup')
        
        if not  lastname:
            messages.error(request, 'please enter last name')
            return redirect('signup')
        
        if not  email:
            messages.error(request, 'please enter the email id')
            return redirect('signup')

        if not  pass1:
            messages.error(request, 'please enter the password')
            return redirect('signup')

        if not  pass2:
            messages.error(request, 'please enter the password')
            return redirect('signup')     
            
        if len(username)>10:
            messages.error(request, "Username contain lessthan 10 characters")
            return redirect('signup')

        if pass1!=pass2:
            messages.error(request, "password didn't match!")
            return redirect('signup')

        if not username.isalnum():
            messages.error(request, "Username must be alpha numeric!")
            return redirect('signup')
        
        if not firstname.isalpha():
            messages.error(request, "firstname must be alphabets!")
            return redirect('signup')
        
        if not lastname.isalpha():
            messages.error(request, "Lastname must be alphabets!")
            return redirect('signup')
        


# save the user details while signup
        myuser = User.objects.create_user(username, email, pass1)
        myuser.first_name = firstname
        myuser.last_name = lastname
        myuser.save()
        messages.success(request, "your account is created")
        return redirect('signin')
    if request.user.is_authenticated:
        return redirect('home')

    return render(request, 'user_auth/signup_page.html')


@cache_control(no_cache=True,must_revalidate=True,no_store=True)
def signin(request):
    if request.method == "POST":
        username = request.POST.get('username')
        pass1 = request.POST.get('pass1')
        user = authenticate(request, username=username, password = pass1)

        if user is not None:
            login(request, user)
            messages.error(request, "logged in")
            return redirect('home')
        else:
            messages.error(request, "invalid username of password")
            return redirect('index')
        
    if request.user.is_authenticated:
        return redirect('index')


    return render(request, 'user_auth/login_page.html')


@cache_control(no_cache=True,must_revalidate=True,no_store=True)
def signout(request):
    logout(request)
    messages.success(request, 'successfully logged out')
    return render(request, 'user_auth/login_page.html')