from django.contrib import messages
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.views.decorators.cache import never_cache

# Create your views here.

@never_cache
def signin(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        username = request.POST['username']
        pass1 = request.POST['pass1']

        user = authenticate(username = username, password = pass1)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Invalid Credentials')

    return render(request, 'authentication/login.html')

@never_cache
def signup(request):
        if request.user.is_authenticated:
            return redirect('home')
        if request.method == 'POST':
            username = request.POST['username']
            email = request.POST['email']
            fname = request.POST['fname']
            lname = request.POST['lname']
            pass1 = request.POST['pass1']
            pass2 = request.POST['pass2']

            if User.objects.filter(username = username).exists():
                messages.error(request, 'Username already exists')
                return redirect('signup')
            
            if not username.isalnum():
                messages.error(request, 'Username must be Alphanumeric')
                return redirect('signup')
            
            if len(username)>10:
                messages.error(request, 'Username must be under 10 characters')
                return redirect('signup')

            if User.objects.filter(email = email).exists():
                messages.error(request, 'Email already exists')
                return redirect('signup')
            
            if pass1 != pass2:
                messages.error(request, 'Passwords do not match')
                return redirect('signup')

            myuser = User.objects.create_user(username,email, pass1)
            myuser.first_name = fname
            myuser.last_name = lname

            myuser.save()

            messages.success(request, 'Account created successfully')
            return redirect('signin')
        else:
            return render(request, 'authentication/signup.html')

def signout(request):
    logout(request)
    messages.success(request, 'Logged out Successfully')
    return redirect('signin')

@never_cache
def home(request):
    if request.user.is_authenticated:
        fname=request.user.first_name
        return render(request, 'authentication/home.html',{'fname':fname})
    else:
        return redirect('signin')