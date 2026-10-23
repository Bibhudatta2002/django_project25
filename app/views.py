from django.shortcuts import render, redirect

# Create your views here.
from app.forms import *
from django.http import HttpResponse,HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import login,authenticate,logout
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.contrib import messages

def registration(request):

    if request.method == 'POST' and request.FILES:
        NMUMFDO = UserMF(request.POST)
        NMPMFDO = ProfileMF(request.POST,request.FILES)
        if NMUMFDO.is_valid() and NMPMFDO.is_valid():
            MUMFDO = NMUMFDO.save(commit=False)
            PW = NMUMFDO.cleaned_data['password']
            MUMFDO.set_password(PW)
            MUMFDO.save()
            MPMFDO = NMPMFDO.save(commit=False)
            MPMFDO.username = MUMFDO
            MPMFDO.save()
            send_mail('registration',
                        'Thank u for registering',
                        'mallickbibhudatta803@gmail.com',
                        [MUMFDO.email],
                        fail_silently=False)

            return HttpResponse("registration is successfull")
        else:
            return HttpResponse('invalid registration data')
           

    EUMFO = UserMF()
    EPMFO = ProfileMF()
    d = {'EUMFO':EUMFO,'EPMFO':EPMFO}

    return render(request,'registration.html',d)


def home(request):
      if request.session.get('username'):
            username=request.session.get('username')
            d={'username':username}
            return render(request,'home.html',d)
      return render(request,'home.html')


def user_login(request):
      if request.method=='POST':
            username=request.POST['username']
            password=request.POST['password']
            AUO=authenticate(username=username,password=password)
            if AUO:
                  if AUO.is_active:
                        login(request,AUO)
                        request.session['username']=username
                        return HttpResponseRedirect(reverse('home'))
                  else:
                        return HttpResponse('not a active user')
            else:
                  return HttpResponse('invalid credentials')
      return render(request,'user_login.html')

@login_required
def user_logout(request):
      logout(request)
      return HttpResponseRedirect(reverse('user_login'))

@login_required
def display_user_data(request):
    username=request.session['username']
    UO=User.objects.get(username=username)
    PO=Profile.objects.get(username=UO)
    d={'UO':UO,'PO':PO}
    return render(request,'display_user_data.html',d)

@login_required
def change_password(request):
    if request.method=='POST':
        username=request.session['username']
        password=request.POST['npw']
        UO=User.objects.get(username=username)
        UO.set_password(password)
        UO.save()
        return HttpResponse('password is changed')

    return render(request,'change_password.html')

def reset_password(request):
    if request.method == "POST":
        username = request.POST.get('username')
        new_password = request.POST.get('new_password')

        try:
            user = User.objects.get(username=username)
            user.set_password(new_password)
            user.save()

            messages.success(request, "Password reset successfully!")
            return redirect('user_login')

        except User.DoesNotExist:
            messages.error(request, "Username does not exist!")

    return render(request, 'reset_password.html')