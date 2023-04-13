from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from django.http import HttpResponse,HttpResponseRedirect,JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import User, Orders,Cities,Performers,Grade,Type,Chat,Chats
from .forms import OrdersForm
from .serializer import OrdersSerialize,GradeSerialize,ChatSerialize,PerformersSerialize
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib.auth.decorators import login_required
import json
import random
import requests


def Currency(rates):
        url =f"https://api.apilayer.com/exchangerates_data/latest?base=USD&symbols={rates}"
        payload = {}
        headers= {
        # Add apikey
        "apikey": ""
        }
        response = requests.request("GET", url, headers = headers, data = payload)
        status_code =response.status_code
        value =response.json()
        changer = round(value['rates'][f'{rates}'],2)
        changer = 1 if changer < 1 else changer
        return changer

def index(request):
    if request.method =="POST":
        Orders.objects.update(find = True)
        return redirect("/")
    origin=request.GET.get("origin")
    destination = request.GET.get("destination")
    tonnage = request.GET.get("tonnage")
    find_type = request.GET.get("type")
    if origin and destination and tonnage and find_type:
        try:
            orders =Orders.objects.filter(tonnage = tonnage, sender = Cities.objects.get(city = origin), receiver = Cities.objects.get(city = destination), type= Type.objects.get(type=find_type) ).order_by("-timestamp")
        except:
            return redirect("/")
    elif origin:
        try:
            orders =Orders.objects.filter(sender = Cities.objects.get(city = origin)).order_by("-timestamp")
        except:
            return redirect("/")
    elif destination:
        try:
            orders =Orders.objects.filter(receiver = Cities.objects.get(city = destination) ).order_by("-timestamp")
        except:
            return redirect("/")
    elif tonnage:
        try:
            orders =Orders.objects.filter(tonnage = tonnage).order_by("-timestamp")
        except:
            return redirect("/")
    elif find_type:
        try:
            orders =Orders.objects.filter(type= Type.objects.get(type=find_type) ).order_by("-timestamp")
        except:
            return redirect("/")
    else:
        orders =Orders.objects.order_by("-timestamp")
    changer = 1
    sign= '$'
    if request.GET.get("currency"):
        rates = request.GET.get("currency")
        changer = Currency(rates)
        if rates =="EUR":
            sign ='€'
        elif rates =="UAH":
            sign ="грн"
    type = Type.objects.all()
    orders_pagination = Paginator(orders, 2)
    orders_link = request.GET.get('page')
    orders_pagination = orders_pagination.get_page(orders_link)
    return render(request,"trucktrack/index.html",{
        "orders": orders_pagination,
        "type": type,
        'rates':changer,
        'sign':sign
    })

def register(request):
    if request.method == "POST":
        username =request.POST["username"]
        if User.objects.filter(username = username).first():
            return render(request,'trucktrack/register.html',{"username_error":"That user is already exist"})
        email = request.POST["email"]
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password !=confirmation:
            return render(request,'trucktrack/register.html',{"equal_error":"Passwords doesn't match"})
        try:
            user = User.objects.create_user(username, email, password)
        except:
            return redirect("register")
        user.save()
        return redirect("login")
    else:
        return render(request,"trucktrack/register.html")
    
def logining(request):
    if request.method =="POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(username = username, password = password)
        if user == None:
            return render(request, "trucktrack/login.html",{
                "user_error":"User doesn't exist"
            })
        login(request,user)
        return redirect("/")
    else:
        return render(request,"trucktrack/login.html")
@login_required   
def logouting(request):
    logout(request)
    return redirect("login")

@login_required
def neworder(request):
    if request.method == "POST":
        form = OrdersForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            text = form.cleaned_data["text"]
            bid = form.cleaned_data["bid"]
            sender = request.POST["send"]
            receiver = request.POST["receive"]
            tonnage = request.POST["tonnage"]
            type = request.POST["type"]
        if not Cities.objects.filter(city = receiver).first():
            receiver_city = Cities(city = receiver)
            receiver_city.save()
        if not Cities.objects.filter(city = sender).first():
            sender_city = Cities(city = sender)
            sender_city.save()
        if not Type.objects.filter(type=type).first():
            print("ok")
            new_type = Type(type=type)
            new_type.save()
        order = Orders(title = title, text = text, sender = Cities.objects.get(city = sender), receiver = Cities.objects.get(city = receiver), bid = bid, owner = request.user, tonnage= tonnage, type = Type.objects.get(type=type))
        order.save()
        return redirect("/")
    else:
        form = OrdersForm()
        return render(request,"trucktrack/create_order.html",{
            "form":form
        })
@login_required   
@csrf_exempt
def orders_map(request):
    if request.method =="POST":
        data = json.loads(request.body)
        if data["origin"] and data["destination"] and data["tonnage"]:
            Orders.objects.exclude(sender = Cities.objects.get(city = data["origin"]),receiver = Cities.objects.get(city = data["destination"]),tonnage = data["tonnage"]).update(find = False)
        elif data["origin"]:
            Orders.objects.exclude(sender = Cities.objects.get(city = data["origin"])).update(find = False)
        elif data["destination"]:
            Orders.objects.exclude(receiver = Cities.objects.get(city = data["destination"])).update(find = False)
        elif data["tonnage"]:
            Orders.objects.exclude(tonnage = data["tonnage"]).update(find = False)
        else:
            Orders.objects.exclude(type = Type.objects.get(type=data["type"])).update(find = False)
        return JsonResponse({"update":"succesfully"})
    orders = Orders.objects.filter(visability=True, find = True)
    serialize = OrdersSerialize(orders,many = True)
    return JsonResponse(serialize.data, safe= False)


@login_required
@csrf_exempt
def order(request, id):
    if request.method == "PUT":
        data = json.loads(request.body)
        performers = Performers.objects.filter(order= Orders.objects.get(id = id), performer=User.objects.get(id=data["performer"])).first()
        if performers:
            return JsonResponse({"reply": "reply already exist"})
        performer = Performers(order= Orders.objects.get(id = id), performer=User.objects.get(id=data["performer"]))
        performer.save()
        return JsonResponse({"success": "reply add successfully"})
    elif request.method =="POST":
        body =json.loads(request.body.decode("utf-8"))
        if len(body) == 2:
            Orders.objects.filter(id=id).update(visability = body["visability"],perform = User.objects.get(id =body["perform"]))
        else:
            Orders.objects.filter(id=id).update(visability = body["visability"])
        return JsonResponse({"update": "successfully"})
    elif request.method =="DELETE":
        Orders.objects.filter(id=id).delete()
        return JsonResponse({"delete":"successfully"})
    else:
        try:
            order = Orders.objects.get(id = id)
            performers = Performers.objects.filter(order = Orders.objects.get(id = id))
            repliers = Performers.objects.filter(order = Orders.objects.get(id = id), performer= User.objects.get(id = request.user.id))
            changer = 1
            sign= '$'
            if request.GET.get("currency"):
                rates = request.GET.get("currency")
                changer = Currency(rates)
                if rates =="EUR":
                    sign ='€'
                elif rates =="UAH":
                    sign ="грн"
        except:
            return redirect("/")
        return render(request, "trucktrack/order.html",{
            "order":order,
            "performers":performers,
            "repliers":repliers,
            'rates':changer,
            'sign':sign
        })
@login_required
def orderstart(request,id):
        performers = Performers.objects.filter(order = Orders.objects.get(id=id))
        performers_serialize =PerformersSerialize(performers, many=True)
        return JsonResponse(performers_serialize.data, safe=False)


@login_required
@csrf_exempt
def profile_page(request,id):
    if request.method == "POST":
        body = request.body.decode("utf-8")
        data = json.loads(body)
        User.objects.filter(id= id).update(phone=data["phone"], city=data["city"], truck_tonnage = data["truck"])
        return JsonResponse({"settings":"update successfully"})
    elif request.method =="PUT":
        data = json.loads(request.body)
        number = random.randint(0,100)
        chat = Chats(chat_id = User.objects.get(id = id), main_user = User.objects.get(id = request.user.id),second_user = User.objects.get(id = id),number = number)
        chat.save()
        chat_number = Chats.objects.get(Q(second_user = User.objects.get(id = request.user.id), chat_id = User.objects.get(id=id)) |Q(main_user = User.objects.get(id = request.user.id), chat_id = User.objects.get(id=id)))
        writer = Chat(writer = User.objects.get(id = request.user.id),message= data["message"], chat_number = chat_number)
        writer.save()
        listener = Chat(writer = User.objects.get(id = id), chat_number = chat_number)
        listener.save()
        return JsonResponse({"add message": "successfully"})
    else:
        try:
            user = User.objects.get(id =id) 
        except:
            return redirect("/")
        return render(request,"trucktrack/profile.html",{
            "profile":user,
        })

@login_required
def my_orders(request):
    orders = Orders.objects.filter(perform = User.objects.get(id = request.user.id))
    changer = 1
    sign= '$'
    if request.GET.get("currency"):
        rates = request.GET.get("currency")
        changer = Currency(rates)
        if rates =="EUR":
            sign ='€'
        elif rates =="UAH":
            sign ="грн"
    return render(request,"trucktrack/my_orders.html",{
        "orders":orders,
        'rates':changer,
        'sign':sign
    })

@login_required
def profile_orders(request):
    orders = Orders.objects.filter(owner = User.objects.get(id= request.user.id))
    orders_serialize=OrdersSerialize(orders, many=True)
    return JsonResponse(orders_serialize.data , safe=False)

@login_required
@csrf_exempt
def rating(request,id):
    if request.method == "POST":
        data = json.loads(request.body)
        grade = Grade(user =User.objects.get(id=id), grade = data["grade"], comment=data["comment"], comentator= User.objects.get(id = request.user.id))
        grade.save()
        return JsonResponse({"comment":"Adding comment successfully"})
    else:
        grade = Grade.objects.filter(user = id)
        grade_serialize = GradeSerialize(grade, many = True)
        return JsonResponse(grade_serialize.data, safe=False)
    
@login_required
def chat(request):  
    chats = Chats.objects.filter(Q(second_user = User.objects.get(id = request.user.id)) | Q(main_user = User.objects.get(id = request.user.id)))
    return render(request,"trucktrack/chat.html",{
        "chats": chats,
    })


@login_required
@csrf_exempt
def chats(request, id):
    if request.method =="POST":
        data = json.loads(request.body)
        chats = Chats.objects.get(number = id)
        new_message = Chat(writer=User.objects.get(id =request.user.id), message=data["message"], chat_number= chats)
        new_message.save()
        return JsonResponse({"add message": "successfully"})
    else:
        chats = Chats.objects.filter(Q(main_user = User.objects.get(id = request.user.id),number = id) | Q(second_user = User.objects.get(id = request.user.id),number = id))
        list=[]
        for c in chats:
            chat = Chat.objects.filter(Q(chat_number = Chats.objects.get(number = id), writer = c.main_user) | Q(chat_number = Chats.objects.get(number = id), writer = c.second_user)).order_by("timestamp")
            for ch in chat:
                list.append(ch)
        chat_serialize = ChatSerialize(list,many=True)
        return JsonResponse(chat_serialize.data, safe=False)
    