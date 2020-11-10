from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import *
from django.contrib.auth import logout
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.shortcuts import render, get_object_or_404, get_list_or_404, reverse
from django.http import (HttpResponse, HttpResponseNotFound, Http404,
                         HttpResponseRedirect, HttpResponsePermanentRedirect)
from django.views.decorators.csrf import csrf_exempt
from .Paytm import Checksum
# Create your views here.
MERCHANT_KEY = 'kbzk1DSbJiV_O3p5'


def home(request):

    # messages.info(request, 'Three credits remain in your account.')
    # messages.info(request, 'Three creditasdfs remain in your account.')

    # get list of first 10 free videos
    freeVideos = Video.objects.filter(subType__name="Free")
    freeVideos = freeVideos[0:]
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

    context = {
        'freeVideos': freeVideos,
        'SubDetailsList': SubDetailsList,
        'Sub_Type': zip(Sub_Type, accessList),
        'userSubType': None,

    }
    return render(request, 'index.html', context)


@login_required(login_url='/login')
def VideosPage(request):

    context = {
        'videos': Video.objects.all(),
        'userSubType': Subscription.objects.get(user=request.user)
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

# paytm here


def checkout(request, id):
    if request.method == "POST":
        # return render(request, 'shop/checkout.html', {'thank':thank, 'id': id})
        # Request paytm to transfer the amount to your account after payment by user
        price = SubType.objects.get(id=id)

        param_dict = {

            'MID': 'WorldP64425807474247',
            'ORDER_ID': str(3),
            'TXN_AMOUNT': str(price.price),
            'CUST_ID': request.user.username,
            'INDUSTRY_TYPE_ID': 'Retail',
            'WEBSITE': 'WEBSTAGING',
            'CHANNEL_ID': 'WEB',
            'CALLBACK_URL': 'http://127.0.0.1:8000/handlerequest/',

        }
        param_dict['CHECKSUMHASH'] = Checksum.generate_checksum(
            param_dict, MERCHANT_KEY)
        return render(request, 'paytm.html', {'param_dict': param_dict})


@csrf_exempt
def handlerequest(request):
    # paytm will send you post request here
    form = request.POST
    response_dict = {}
    for i in form.keys():
        response_dict[i] = form[i]
        if i == 'CHECKSUMHASH':
            checksum = form[i]

    verify = Checksum.verify_checksum(response_dict, MERCHANT_KEY, checksum)
    if verify:
        if response_dict['RESPCODE'] == '01':
            print('order successful')
        else:
            print('order was not successful because' +
                  response_dict['RESPMSG'])
    return render(request, 'paymentstatus.html', {'response': response_dict})
