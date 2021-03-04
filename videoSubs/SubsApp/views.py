from typing import Type
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
import datetime
import pytz
import collections
import json
import uuid
# Create your views here.
MERCHANT_KEY = 'kbzk1DSbJiV_O3p5'


def home(request):
    # if there is a pack and the limit is over remove it
    try:
        subCurrent = Subscription.objects.get(user=request.user)

        my_date = datetime.datetime.now(pytz.timezone('Asia/Calcutta'))
        timeLeft = my_date-subCurrent.date
        secondsLeft = timeLeft.seconds
        if(secondsLeft > 600):
            subCurrent.delete()
    except:
        messages.info(request, 'Buy a pack to watch videos')

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
        'testimonials': Testimonials.objects.all(),

    }
    return render(request, 'index.html', context)


@login_required(login_url='/login')
def VideosPage(request):
    try:
        userSubType = Subscription.objects.get(user=request.user)
        typesAll = TypeAccess.objects.filter(subType=userSubType.subType)
        typesAllowed = []
        for i in typesAll:
            typesAllowed.append(i.canAccess.name)
    except:
        typesAllowed = []

    typesAllowed = ','.join(typesAllowed)

    context = {
        'videos': Video.objects.all(),
        'typesAllowed': typesAllowed,
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
    if not request.user.is_authenticated:
        return HttpResponsePermanentRedirect(reverse('LoginView'))
    if request.method == "POST":
        # return render(request, 'shop/checkout.html', {'thank':thank, 'id': id})
        # Request paytm to transfer the amount to your account after payment by user
        subType = SubType.objects.get(id=id)
        if(subType.discountPrice > 0):
            price = subType.discountPrice
        else:
            price = subType.price
        trans = Transations(user=request.user, amount=price, subType=subType
                            )
        trans.save()
        trans.paytmOID = uuid.uuid4().hex[:20]+str(trans.id)
        trans.save()
        param_dict = {
            'MID': 'WorldP64425807474247',
            'ORDER_ID': trans.paytmOID,
            'TXN_AMOUNT': str(trans.amount),
            'CUST_ID': str(trans.user.id),
            'INDUSTRY_TYPE_ID': 'Retail',
            'WEBSITE': 'WEBSTAGING',
            'CHANNEL_ID': 'WEB',
            'CALLBACK_URL': 'https://gymdjango.herokuapp.com/handlerequest/',

        }
        param_dict['CHECKSUMHASH'] = Checksum.generate_checksum(
            param_dict, MERCHANT_KEY)
        return render(request, 'paytm.html', {'param_dict': param_dict})


@csrf_exempt
def handlerequest(request):
    # paytm will send you post request here
    form = request.POST
    print(form)
    msg = ""

    response_dict = {}
    for i in form.keys():
        response_dict[i] = form[i]
        if i == 'CHECKSUMHASH':
            checksum = form[i]

    verify = Checksum.verify_checksum(response_dict, MERCHANT_KEY, checksum)
    if verify:
        if response_dict['RESPCODE'] == '01':
            trans = Transations.objects.get(paytmOID=form['ORDERID'])
            trans.success = True
            trans.save()
            try:
                tuser = Subscription.objects.get(user=trans.user)
                tuser.subType = trans.subType
                tuser.save()
            except:
                tuser = Subscription(user=trans.user, subType=trans.subType)
                tuser.save()

            tuser.subType = trans.subType
            tuser.save()
            msg = 'payment successful'

        else:
            msg = 'order was not successful because ' + \
                response_dict['RESPMSG']

    messages.info(request, msg)
    return HttpResponsePermanentRedirect(reverse('home'))

    # return render(request, 'paymentstatus.html', {'response': response_dict})


def AdminHome(request):

    if request.user.is_staff:
        l = []
        for i in Transations.objects.all():
            l.append(str(i.date)[5:7])
            # print(i.date)
        c = collections.Counter(l)
        l = []
        l.append(["date", "Month"])
        for k in c:
            l.append([int(k), int(c[k])])

        # print(json.dumps(l))
        context = {
            "totalNoOfUsers": len(User.objects.all()),
            "totalNoOfVideos": len(Video.objects.all()),
            'recentTrans': Transations.objects.all().order_by("-date")[:5],
            'noOfSubs': len(Subscription.objects.all()),
            'noOfSubtypes': len(SubType.objects.all()),
            'activitesGraph': json.dumps(l)

        }
        return render(request, 'home.html', context)
    else:
        return HttpResponsePermanentRedirect(reverse('home'))


def AddVideo(request):
    if request.user.is_staff:
        if request.method == "POST":
            temp = Video(title=request.POST['title'],
                         ytId=request.POST['ytID'],
                         desc=request.POST['desc'],
                         subType=SubType.objects.get(
                             id=int(request.POST['year']))

                         )
            temp.save()
        context = {
            "allVideos": Video.objects.all(),
            'year': SubType.objects.all()

        }
        return render(request, 'AddVideos.html', context)
    else:
        return HttpResponsePermanentRedirect(reverse('home'))


def DeleteVideo(request, **kwargs):
    temp = Video.objects.get(id=kwargs['id'])
    temp.delete()
    messages.info(request, 'Deleted Successfully')
    return HttpResponsePermanentRedirect(reverse('AddVideo'))


def AddTestimonial(request):
    if request.user.is_staff:
        if request.method == "POST":
            temp = Testimonials(name=request.POST['name'],

                                desc=request.POST['desc'],

                                )
            temp.save()
        context = {
            "allVideos": Testimonials.objects.all(),


        }
        return render(request, 'AddTestimonial.html', context)
    else:
        return HttpResponsePermanentRedirect(reverse('home'))


def DeleteTestimonial(request, **kwargs):
    temp = Testimonials.objects.get(id=kwargs['id'])
    temp.delete()
    messages.info(request, 'Deleted Successfully')
    return HttpResponsePermanentRedirect(reverse('AddTestimonial'))


def AddTestimonial(request):
    if request.user.is_staff:
        if request.method == "POST":
            temp = Testimonials(name=request.POST['name'],

                                desc=request.POST['desc'],

                                )
            temp.save()
            context = {
                "allVideos": Testimonials.objects.all(),


            }
            return render(request, 'AddTestimonial.html', context)
        else:
            return HttpResponsePermanentRedirect(reverse('home'))
    else:
        return HttpResponsePermanentRedirect(reverse('home'))


def AddTestimonial(request):
    if request.user.is_staff:
        if request.method == "POST":
            temp = Testimonials(name=request.POST['name'],

                                desc=request.POST['desc'],

                                )
            temp.save()

        context = {
            "allVideos": Testimonials.objects.all(),


        }
        return render(request, 'AddTestimonial.html', context)
    else:

        return HttpResponsePermanentRedirect(reverse('home'))


def AddSubType(request):
    if request.user.is_staff:
        if request.method == "POST":
            temp = SubType(name=request.POST['name'],

                           price=float(request.POST['price']),
                           color=request.POST['color'],
                           discountPrice=float(
                request.POST['discountPrice']),

            )
            temp.save()

        context = {
            "allVideos": SubType.objects.all(),


        }
        return render(request, 'AddSubType.html', context)

    else:
        return HttpResponsePermanentRedirect(reverse('home'))


def DeleteSubType(request, **kwargs):
    temp = SubType.objects.get(id=kwargs['id'])
    temp.delete()
    messages.info(request, 'Deleted Successfully')
    return HttpResponsePermanentRedirect(reverse('AddSubType'))


def EditSubType(request, **kwargs):
    if request.method == "POST":
        temp = SubType.objects.get(id=int(kwargs['id']))
        temp.name = request.POST['name']
        temp.price = request.POST['price']
        temp.discountPrice = request.POST['dprice']
        temp.color = request.POST['color']
        temp.save()
        return HttpResponsePermanentRedirect(reverse('AddSubType'))

    context = {
        "sub": SubType.objects.get(id=int(kwargs['id'])),


    }
    return render(request, 'EditPricing.html', context)
    # return HttpResponsePermanentRedirect(reverse('AddSubType'))


def AddTypeAccess(request):
    if request.user.is_staff:
        if request.method == "POST":

            temp = TypeAccess(
                subType=SubType.objects.get(id=int(request.POST['type'])),
                canAccess=SubType.objects.get(id=int(request.POST['can'])),



            )
            temp.save()

        context = {
            "allVideos": TypeAccess.objects.all().order_by('subType'),
            'year': SubType.objects.all()


        }
        return render(request, 'AddTypeAccess.html', context)

    else:
        return HttpResponsePermanentRedirect(reverse('home'))


def DeleteTypeAccess(request, **kwargs):
    temp = TypeAccess.objects.get(id=kwargs['id'])
    temp.delete()
    messages.info(request, 'Deleted Successfully')
    return HttpResponsePermanentRedirect(reverse('AddTypeAccess'))
