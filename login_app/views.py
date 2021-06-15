from django.shortcuts import render, redirect
from django.contrib import messages
from .models import User
import bcrypt

def home(request):
    return render(request,'index.html')

def register(request):
    errors = User.objects.basic_validator(request.POST)
    if len(errors) > 0:
        for key, msg in errors.items():
            messages.error(request, msg)
        return redirect('/')
    else:
        password = request.POST['password']
        hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
        new_user = User.objects.create(
        first_name = request.POST['fname'],
        last_name = request.POST['lname'],
        email = request.POST['email'],
        password = hashed,
    )
    request.session['logged_user'] = new_user.id
    print("success hashed pw is", new_user.password )
    return redirect('/home')

def dashboard(request):
    if 'logged_user' not in request.session:
        return redirect('/') #kick out if logout
    my_user = User.objects.get(id=request.session['logged_user'])
    print("logged user is",request.session['logged_user'])
    context = {
        'logged_user':my_user
    }
    return render(request, 'dashboard.html', context)

def logout(request):
    # request.session.flush()#learn the difference
    request.session.clear()
    return redirect ('/')

def login(request):
    errors = User.objects.login_validator(request.POST)
    if len(errors) > 0:
        for key, msg in errors.items():
            messages.error(request, msg)
        return redirect('/')
    else:

        email_users = User.objects.filter(email=request.POST['email'])#not .get, which errors out on multi-matches
        if len(email_users) < 1:
            messages.error(request,'no existing user with that email')
            return redirect('/')
        user_to_verify = email_users[0]
        password = request.POST['password']
        if bcrypt.checkpw(password.encode(), user_to_verify.password.encode()):#truthy falsey check
            request.session['logged_user'] = user_to_verify.id
            return redirect('/home')
        messages.error (request, "Passwords don't match!")
        return redirect('/')
        

