from django.shortcuts import render ,redirect, HttpResponse
from django.contrib.auth import authenticate , logout ,login
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from .models import UserProfile

def login_view (request):
    if request.method == 'POST':
        username= request.POST['email']
        password= request.POST['password']
        code= request.POST['code']
        user =authenticate(request, username=username,password=password)
        if user is not None :
            login(request , user)
            return redirect('home', code)
    else:
        return render(request , 'home/index.html')
    


def home(request , pk):
    user = UserProfile.objects.filter(user = request.user, pk=pk)
    # if request.user.is_superuser ==True:
    #     return render(request , 'admin/add-mony.html')
    # else:
    print(user)
    return render(request , 'home/home.html' ,{'new':user})
    

def logout_view(request):
    logout(request)
    return redirect('login')


def add_money(request):
    if request.method == 'POST':
        user_name = request.POST['id']
        balance = request.POST['balance']
        user = UserProfile.objects.filter(pk=user_name)
        print(user_name)
        user.update(
            balance=balance
        )
        return redirect('home' , user_name)
    else:
        
        return render(request , 'admin/add-mony.html')

def edit_user (request):
    if request.method == 'POST':
        user_name = request.POST['username']
        code = request.POST['code']
        bol = request.POST['bolean']
        user = UserProfile.objects.filter(pk=code , user__username=user_name)
        if bol == 'disactive':
            user.update(
                balance=0
            )
        return redirect('home' , code)
    else:
        
        return render(request , 'admin/add-user-info.html')