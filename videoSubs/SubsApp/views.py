from django.shortcuts import render, redirect
from django.contrib.auth.models import User

from .models import *
from django.contrib.auth import logout
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.shortcuts import render, get_object_or_404, get_list_or_404, reverse
from django.http import (HttpResponse, HttpResponseNotFound, Http404,
                         HttpResponseRedirect, HttpResponsePermanentRedirect)
# Create your views here.


def home(request):

    # messages.info(request, 'Three credits remain in your account.')
    # messages.info(request, 'Three creditasdfs remain in your account.')

    # get list of first 10 free videos
    freeVideos = Video.objects.filter(subType__name="Free")[0:10]
    # get List of subscriptions
    accessList = []

    Sub_Type = SubType.objects.all()
    SubDetailsList = []
    for i in Sub_Type:
        SubDetailsList.append(
            [i,
             str(len(Video.objects.filter(subType=i)))+" "+i.name+" Videos"])
        temp = TypeAccess.objects.filter(
            subType=i)
        temp2 = [i.canAccess.name for i in temp]
        accessList.append(','.join(temp2))
    SubDetailsList.append(['', '24 hours access'])
    # print(SubDetailsList, accessList)
    context = {
        'freeVideos': freeVideos,
        'SubDetailsList': SubDetailsList,
        'Sub_Type': zip(Sub_Type, accessList),
    }
    return render(request, 'index.html', context)


def VideosPage(request):
    context = {
        'videos': Video.objects.all()
    }
    return render(request, 'videos.html', context)


def logout_request(request):
    logout(request)
    messages.info(request, "Logged out successfully!")
    return redirect('/')


def RegisterView(request):
    if request.method == 'POST':
        user = User.objects.create_user(username=request.POST.get('email'),
                                        password=request.POST.get('password'),
                                        first_name=request.POST.get('fname'),
                                        last_name=request.POST.get('lname'),
                                        )
        user.save()
        return HttpResponsePermanentRedirect(reverse('LoginView'))

    else:
        return render(request, 'register.html')


def LoginView(request):
    if request.method == 'POST':
        user = authenticate(username=request.POST.get(
            'username'), password=request.POST.get('password'))
        if user is not None:
            # print('here')
            login(request, user)
            return HttpResponsePermanentRedirect(reverse('home'))
        else:
            return render(request, 'login.html')

    else:

        return render(request, 'login.html')
