import random
import string
from django.shortcuts import render
from datetime import date, timedelta
from django.http import HttpResponseRedirect
from library.models import User, Item, Service
from django.core.paginator import Paginator


def generate_unique_id(length=8):
    characters = string.ascii_uppercase + string.digits
    while True:
        user_id = "".join(random.choices(characters, k=length))
        if not User.objects.filter(user_ID=user_id).exists():
            return user_id


def register(request):
    if request.method == "POST":
        name = request.POST.get("name")
        address = request.POST.get("address")
        mobile = request.POST.get("mobile")
        dob = request.POST.get("dob")
        user_id = generate_unique_id()
        User.objects.create(
            user_ID=user_id,
            user_name=name,
            user_address=address,
            user_phone=mobile,
            user_dob=dob,
        )
        return HttpResponseRedirect("/")

    return render(request, "registration.html")


def userlist(request):
    user_list = User.objects.all()
    if request.method == "POST":
        search = request.POST.get("search_bar")
        user_list = User.objects.filter(
            user_ID__icontains=search
        ) | User.objects.filter(user_name__icontains=search)

    return render(request, "user_list.html", {"user_list": user_list})


def user_info(request, user_id):
    user_data = User.objects.get(user_ID=user_id)

    return render(request, "user_info.html", {"user": user_data})


def check_request():
    item = Item.objects.all()
    for i in item:
        if i.item_stock == 0:
            i.item_request = True
            i.save()
        elif i.item_stock != 0:
            i.item_request = False
            i.save()


def catalog(request, category):
    item_data = Item.objects.filter(item_type=category)
    check_request()
    if request.method == "POST":
        search = request.POST.get("search_bar")
        item_data = Item.objects.filter(
            item_name__icontains=search
        ) | Item.objects.filter(item_ID__icontains=search)

    return render(request, "catalog.html", {"item_data": item_data})


def age(dob):
    return (date.today() - dob).days // 365


def checkout(request, item_id):
    msg = ""
    if request.method == "POST":
        user_id = request.POST.get("user_id")
        try:
            item = Item.objects.get(item_ID=item_id)
        except Item.DoesNotExist:
            msg = "Invalid Item ID"
            return render(request, "checkout.html", {"message": msg})

        try:
            user = User.objects.get(user_ID=user_id)
        except User.DoesNotExist:
            msg = "Invalid User ID"
            return render(request, "checkout.html", {"message": msg})

        user_age = age(user.user_dob)
        if user_age <= 12:
            services_count = Service.objects.filter(user_ID=user_id).count()
            if services_count >= 5:
                msg = "Under age and already using five services"
                return render(request, "checkout.html", {"message": msg})

        if Service.objects.filter(user_ID=user_id, item_ID=item_id).exists():
            msg = "Item already checked out by this user"
            return render(request, "checkout.html", {"message": msg})

        iss_date = date.today()
        rt_date = iss_date + (
            timedelta(weeks=3)
            if item.item_type == "Book" and not item.best_seller
            else timedelta(weeks=2)
        )
        Service.objects.create(
            user_ID=user_id,
            item_ID=item_id,
            issued_date=iss_date,
            return_date=rt_date,
        )
        item.item_stock -= 1
        item.save()
        msg = "Checkout Successful"

    return render(request, "checkout.html", {"message": msg})


def fine(return_date, item):
    days = (date.today() - return_date).days
    fine = days * 0.10
    return min(fine, item.item_price)


def services(request, user_id):
    user_data = User.objects.get(user_ID=user_id)
    services_data = Service.objects.filter(user_ID=user_id)
    check_request()

    for service in services_data:
        item = Item.objects.get(item_ID=service.item_ID)
        if date.today() > service.return_date:
            service.fine = fine(service.return_date, item)
            service.save()

    if request.method == "POST":
        service_id = request.POST.get("service_id")
        action = request.POST.get("action")
        service = Service.objects.get(service_ID=service_id)
        item = Item.objects.get(item_ID=service.item_ID)

        if action == "renew":
            if not service.renewed and not item.item_request:
                service.return_date = date.today() + (
                    timedelta(weeks=3)
                    if item.item_type == "Book" and not item.best_seller
                    else timedelta(weeks=2)
                )
                service.fine = 0
                service.renewed = True
                service.issued_date = date.today()
                service.save()

        elif action == "return":
            item.item_stock += 1
            item.save()
            service.delete()

    return render(
        request,
        "services.html",
        {"user": user_data, "services_data": services_data},
    )


def item_info(request, item_id):
    item_data = Item.objects.get(item_ID=item_id)
    return render(request, "item_info.html", {"item": item_data})
