from django.contrib.auth import get_user_model
from django.shortcuts import render,redirect,get_object_or_404
import braintree
from django.conf import settings
from orders.models import Order
from tracking_analyzer.models import Tracker
from django_user_interaction_log.registrars import create_log_record

# Create your views here.

gateway = braintree.BraintreeGateway(settings.BRAINTREE_CONF)

def payment_process(request):
    order_id = request.session.get('order_id')
    order = get_object_or_404(Order, id=order_id)
    total_cost = order.get_total_cost()
    target_object = None
    if get_user_model().objects.filter().exists():
        target_object = get_user_model().objects.first()
    create_log_record(request=request, log_detail='The user has reached the part for entering credit card information',
                      log_target=target_object)
    if request.method == 'POST':
        nonce = request.POST.get('payment_method_nonce',None)
        result = gateway.transaction.sale({
            'amount' : f'{total_cost:.2f}',
            'payment_method_nonce' : nonce,
            'options':{
                'submit_for_settlement':True
            }
        })

        if result.is_success:
            order.paid = True
            order.braintree_id = result.transaction.id
            order.save()
            return redirect('payment:done')
        else:
            return redirect('payment:cancled')
        Tracker.objects.create_from_request(request, order)
    else:
        client_token = gateway.client_token.generate()
        Tracker.objects.create_from_request(request, order)
        return render(request,'payment/process.html',{
            'order':order,
            'client_token':client_token
        })

def payment_done(request):
    return render(request,'payment/done.html')

def payment_canceled(request):
    target_object = None
    if get_user_model().objects.filter().exists():
        target_object = get_user_model().objects.first()
    create_log_record(request=request, log_detail='The user has abandoned the purchase',
                      log_target=target_object)
    return render(request,'payment/canceled.html')