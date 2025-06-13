import razorpay
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from .models import Payment
from jobs.models import Bid
from rest_framework import status
from django.shortcuts import get_object_or_404

client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_order(request):
    try:
        data = json.loads(request.body)
        bid_id = data.get('bid_id')
        
        # Get the bid and verify it exists
        bid = get_object_or_404(Bid, id=bid_id)
        
        # Check if payment already exists for this bid
        if Payment.objects.filter(bid=bid, status__in=['paid', 'authorized']).exists():
            return JsonResponse({
                'error': 'Payment already exists for this bid'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Create payment record
        payment = Payment.objects.create(
            user=request.user,
            bid=bid,
            amount=float(bid.fee/100*30),
            currency='INR',
            status='created'
        )
        
        # Create Razorpay order
        razorpay_order = client.order.create({
            'amount': int(float(bid.fee/100*30) * 100),  # Convert to paise
            'currency': 'INR',
            'payment_capture': 1,
            'notes': {
                'payment_id': str(payment.id),
                'bid_id': str(bid.id)
            }
        })
        
        # Update payment with order details
        payment.order_id = razorpay_order['id']
        payment.save()
        
        return JsonResponse({
            'order_id': razorpay_order['id'],
            'amount': razorpay_order['amount'],
            'currency': razorpay_order['currency'],
            'payment_id': payment.id
        })
        
    except Exception as e:
        return JsonResponse({
            'error': str(e)
        }, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def verify_payment(request):
    try:
        data = json.loads(request.body)
        payment_id = data.get('payment_id')
        razorpay_payment_id = data.get('razorpay_payment_id')
        razorpay_order_id = data.get('razorpay_order_id')
        razorpay_signature = data.get('razorpay_signature')
        
        # Get payment record
        payment = get_object_or_404(Payment, id=payment_id, user=request.user)
        
        # Verify signature
        params_dict = {
            'razorpay_payment_id': razorpay_payment_id,
            'razorpay_order_id': razorpay_order_id,
            'razorpay_signature': razorpay_signature
        }
        
        try:
            client.utility.verify_payment_signature(params_dict)
            
            # Update payment record
            payment.payment_id = razorpay_payment_id
            payment.signature = razorpay_signature
            payment.status = 'paid'
            payment.save()
            
            return JsonResponse({
                'status': 'success',
                'message': 'Payment verified successfully'
            })
            
        except razorpay.errors.SignatureVerificationError:
            payment.status = 'failed'
            payment.save()
            return JsonResponse({
                'error': 'Payment verification failed'
            }, status=status.HTTP_400_BAD_REQUEST)
            
    except Exception as e:
        return JsonResponse({
            'error': str(e)
        }, status=status.HTTP_400_BAD_REQUEST)

@csrf_exempt
def webhook(request):
    if request.method == 'POST':
        try:
            # Get webhook data
            webhook_data = json.loads(request.body)
            webhook_signature = request.headers.get('X-Razorpay-Signature')
            
            # Verify webhook signature
            client.utility.verify_webhook_signature(
                request.body.decode('utf-8'),
                webhook_signature,
                settings.RAZORPAY_WEBHOOK_SECRET
            )
            
            # Handle different webhook events
            event_type = webhook_data.get('event')
            
            if event_type == 'payment.authorized':
                payment_id = webhook_data['payload']['payment']['entity']['notes']['payment_id']
                payment = Payment.objects.get(id=payment_id)
                payment.status = 'authorized'
                payment.save()
                
            elif event_type == 'payment.failed':
                payment_id = webhook_data['payload']['payment']['entity']['notes']['payment_id']
                payment = Payment.objects.get(id=payment_id)
                payment.status = 'failed'
                payment.save()
                
            elif event_type == 'payment.captured':
                payment_id = webhook_data['payload']['payment']['entity']['notes']['payment_id']
                payment = Payment.objects.get(id=payment_id)
                payment.status = 'paid'
                payment.save()
                
            elif event_type == 'refund.processed':
                payment_id = webhook_data['payload']['payment']['entity']['notes']['payment_id']
                payment = Payment.objects.get(id=payment_id)
                payment.status = 'refunded'
                payment.save()
            
            return JsonResponse({'status': 'success'})
            
        except Exception as e:
            return JsonResponse({
                'error': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)
    
    return JsonResponse({
        'error': 'Invalid request method'
    }, status=status.HTTP_405_METHOD_NOT_ALLOWED)
