import json

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render

from account.models import Address
from basket.basket import Basket
from orders.models import Order, OrderItem
from .models import DeliveryOptions
# from paypalcheckoutsdk.orders import OrdersGetRequest
# from .paypal import PayPalClient

@login_required
def delivery_choices(request):
    deliveryOptions = DeliveryOptions.objects.filter(is_active=True)
    return render(request, "checkout/delivery_choices.html", {"deliveryoptions": deliveryOptions})


@login_required
def basket_update_delivery(request):
    basket = Basket(request)
    if request.POST.get("action") == "post":
        delivery_id = int(request.POST.get("delivery_id"))
        # Lấy phương thức vận chuyển theo id
        delivery = DeliveryOptions.objects.get(id=delivery_id)
        updated_total_price = basket.basket_update_delivery(delivery.delivery_price)

        session = request.session
        # nếu không tồn tại delivery thì khởi tạo, còn tồn tại thì update trong session
        if "delivery" not in request.session:
            session["delivery"] = {
                "delivery_id": delivery.id,
            }
        else:
            session["delivery"]["delivery_id"] = delivery.id
            session.modified = True

        response = JsonResponse({"total": updated_total_price, "delivery_price": delivery.delivery_price})
        return response

@login_required
def delivery_address(request):
    session = request.session
    if "delivery" not in request.session:
        messages.success(request, "Vui lòng chọn phương thức vận chuyển")
        # chưa chọn thì quay lại trang gửi request thông báo cho người dùng
        return HttpResponseRedirect(request.META["HTTP_REFERER"])

    addresses = Address.objects.filter(customer=request.user).order_by("-default")

    # nếu không tồn tại địa chỉ thì tạo mới, ngược lại thì update trong session
    if "address" not in request.session:
        session["address"] = {"address_id": str(addresses[0].id)}
    else:
        session["address"]["address_id"] = str(addresses[0].id)
        session.modified = True

    return render(request, "checkout/delivery_address.html", {"addresses": addresses})

@login_required
def payment_complete(request):

    if request.method == 'POST':
        user_id = request.user.id

        basket = Basket(request) 
        
        # order_key = "OrderKeyDemo123" 
        full_name = request.POST.get('full_name')
        # email = "email@domain.com"
        address1 = request.POST.get('address_line')
        address2 = request.POST.get('address_line2')
        postal_code = request.POST.get('postcode')
        town_city = request.POST.get('town_city')
        phone = request.POST.get('phone')
        total_paid = request.POST.get('total').replace('$', '').replace(',', '') 
    
        print("full_name: ", full_name) 
        print("address1: ", address1)
        print("address2: ", address2)
        print("postal_code: ", postal_code)
        print("phone: ", phone)
        print("total_paid: ", total_paid)

        order = Order.objects.create(
            user_id=user_id,
            full_name=full_name,
            # email=email,
            address1=address1,
            address2=address2,
            postal_code=postal_code,
            city = town_city,
            # country_code=country_code,
            phone=phone,
            total_paid=total_paid,
            # order_key=order_key,
            # payment_option=payment_option,
            billing_status=True,
        )
        order_id = order.pk
        for item in basket:
            OrderItem.objects.create(order_id=order_id, product=item["product"], price=item["price"], quantity=item["qty"])
        
        # Xóa giỏ hàng sau khi thanh toán
        basket.clear()

        # return JsonResponse({"message": "Payment completed!", "orderID": order_id})
        return render(request, "checkout/payment_successful.html", {})
    return JsonResponse({"error": "Invalid request"}, status=400)


@login_required
def payment_successful(request):
    basket = Basket(request)
    basket.clear()
    return render(request, "checkout/payment_successful.html", {})
