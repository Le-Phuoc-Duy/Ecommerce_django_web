from django.http.response import JsonResponse
from django.shortcuts import render

from basket.basket import Basket

from .models import Order, OrderItem


def add(request):
    basket = Basket(request)
    if request.POST.get('action') == 'post': 
        user_id = request.user.id
        total_paid = basket.get_total_price() 
        order = Order.objects.create(user_id=user_id, full_name='name', address1='add1',
                                        address2='add2', total_paid=total_paid)
        order_id = order.pk

        for item in basket:
            OrderItem.objects.create(order_id=order_id, product=item['product'], price=item['price'],
                                        quantity=item['qty'])

        response = JsonResponse({'success': 'Return something'})
        return response 

def user_orders(request):
    user_id = request.user.id
    orders = Order.objects.filter(user_id=user_id).filter(billing_status=True)
    return orders
