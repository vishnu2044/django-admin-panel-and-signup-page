from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control



# Create your views here.

# Landing page for admin section
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def admin_index(request):
    if request.user.is_authenticated and  request.user.is_superuser:
        return redirect('admin_dashboard')
    
    return render(request, 'admin_panel/admin_login_page.html')


# Admin dashboard page
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='admin_index')
def admin_dashboard(request):
    if request.user.is_authenticated and request.user.is_superuser:
        member = User.objects.all()
        return render(request, 'admin_panel/admin_page.html', {'member': member})
    return render(request, 'admin_panel/admin_login_page.html')


# Admin login page
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def admin_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = username = authenticate(username = username, password = password)

        if user is not None and user.is_superuser:
            login(request, user)
            return redirect('admin_dashboard')
            
        else:
            messages.error(request, "invalid superuser credentials !")
            return redirect('admin_login')
    
    if request.user.is_authenticated and request.user.is_superuser:
        return redirect('admin_dashboard')
    

    return render(request, 'admin_panel/admin_login_page.html')


# Delete a user
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def delete(request, id):
    member = User.objects.get(id=id)
    member.delete()
    return redirect('admin_dashboard')


#search a user with username
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def search(request):
    if request.method == 'GET':
        query = request.GET.get('query')
        if query:
            detail = User.objects.filter(username=query)
            return render(request, 'admin_panel/search.html', {'details': detail})
        else:
            return render(request, 'admin_panel/search.html', {})
        

# redirect to the page for updating user details
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def update(request, id):
    member = User.objects.get(id=id)
    return render(request, 'admin_panel/update.html', {'member': member})


# process for updating a users information
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def update_record(request, id):

    if request.method == "POST":
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')

        if not firstname:
            messages.error(request, "first name column is required")
            return redirect('update')
        
        if not lastname:
            messages.error(request, "first name column is required")
            return redirect('update')
        
        myuser = User.objects.get(id = id)
        myuser.first_name = firstname
        myuser.last_name = lastname

        myuser.save()
        return redirect('admin_dashboard')


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def add(request):
    return render(request, 'admin_panel/add_user_page.html')


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def add_record(request):
    if request.method == "POST":
        username = request.POST.get('username')
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        email = request.POST.get('email')
        pass1 = request.POST.get('pass1')
        pass2 = request.POST.get('pass2')

        if not  username:
            messages.error(request, 'please enter the user name')
            return redirect('add')

        if not  firstname:
            messages.error(request, 'please enter first name')
            return redirect('add')
        
        if not  lastname:
            messages.error(request, 'please enter last name')
            return redirect('add')
        
        if not  email:
            messages.error(request, 'please enter the email id')
            return redirect('add')

        if not  pass1:
            messages.error(request, 'please enter the password')
            return redirect('add')

        if not  pass2:
            messages.error(request, 'please enter the password')
            return redirect('add')     

        if User.objects.filter(username=username).exists():
            messages.error(request, 'this username is already taken')
            return redirect('add')
        
        if User.objects.filter(email=email).exists():
            messages.error(request, 'this email id is already taken')
            return redirect('add')
        
        if len(username)>10:
            messages.error(request, "Username contain lessthan 10 characters")
            return redirect('add')

        if pass1!=pass2:
            messages.error(request, "password didn't match!")
            return redirect('add')

        if not username.isalnum():
            messages.error(request, "Username must be alpha numeric!")
            return redirect('add')
        
        if not firstname.isalpha():
            messages.error(request, "firstname must be alphabets!")
            return redirect('add')
        
        if not lastname.isalpha():
            messages.error(request, "Lastname must be alphabets!")
            return redirect('add')
        
        myuser = User.objects.create_user(username, email, pass1)
        myuser.first_name = firstname
        myuser.last_name = lastname
        myuser.save()

        messages.success(request, 'your account has been successfully created')
        return redirect('admin_dashboard')



# Admin sign out
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def admin_signout(request):
    logout(request)
    messages.success(request, "successfully logged out")
    return redirect('admin_dashboard')




