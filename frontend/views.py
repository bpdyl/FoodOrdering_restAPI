from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import *
from accounts.models import UserProfile
from .serializers import *

import stripe

stripe.api_key = settings.STRIPE_SECRET_KEY


# Create your views here.
# class OrderView(APIView):
#     pass
# class AddressView(APIView):
#     pass
class CartView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        user = request.user
        cart = Cart.objects.filter(user = user, ordered = False).first()
        queryset = CartItem.objects.filter(cart = cart)
        serializer = CartItemSerializer(queryset, many = True)
        return Response(serializer.data) 
    def post(self, request):
        data = request.data
        user = request.user
        cart,_ = Cart.objects.get_or_create(user = user, ordered=False)

        food_item = restFoodModel.objects.get(id = data.get('food_item'))
        cart_restaurant = food_item.cart_restaurant
        # restaurants = restaurantModel.objects.get(id = data.get('cart_restaurant'))
        food_price = food_item.food_price
        quantity = data.get('quantity')
        cart_item = CartItem(cart = cart, user = user, food_item = food_item,cart_restaurant = cart_restaurant,food_price = food_price, quantity = quantity)
        cart_item.save()

        total_price = 0
        cart_item = CartItem.objects.filter(user = user, cart = cart.id)
        for item in cart_item:
            total_price += item.food_price
        cart.total_price = total_price
        cart.save()
 
        return Response({'success': 'Items Added to your cart'})

    def put(self, request):
        data = request.data
        cart_item = CartItem.objects.get(id=data.get('id'))
        quantity = data.get('quantity')
        cart_item.quantity += quantity
        cart_item.save()
        return Response({'success': 'Items Updated'})

    def delete(self, request):
        user = request.user
        data = request.data

        cart_item = CartItem.objects.get(id = data.get('id'))
        cart_item.delete()

        cart = Cart.objects.filter(user = user, ordered = False).first()
        queryset = CartItem.objects.filter(cart = cart)
        serializer = CartItemSerializer(queryset, many = True)
        return Response(serializer.data) 

class OrderView(generics.ListAPIView):
    permission_classes = [IsAuthenticated,]
    serializer_class = OrderSerializer
    def get_queryset(self):
        try:
            order = Order.objects.filter(user = request.user,ordered = True)
            return order
        except ObjectDoesNotExist:
            raise Http404("You do not have an active order") 
    # def get(self, request):
    #     queryset = Orders.objects.filter(user = request.user,ordered = True)
    #     serializer = OrderSerializer(queryset, many = True)
    #     return Response(serializer.data)


class AddressListView(generics.ListAPIView):
    permission_classes = (IsAuthenticated,) 
    serializer_class = AddressSerializer

    def get_queryset(self):
        return Address.objects.filter(user = self.request.user)


class Checkout(APIView):
    

class PaymentView(APIView):

    def post(self, request, *args, **kwargs):
        order = Order.objects.get(user=self.request.user, ordered=False)
        userprofile = UserProfile.objects.get(user=self.request.user)
        token = request.data.get('stripeToken')
        billing_address_id = request.data.get('selectedBillingAddress')
        shipping_address_id = request.data.get('selectedShippingAddress')

        billing_address = Address.objects.get(id=billing_address_id)
        shipping_address = Address.objects.get(id=shipping_address_id)

        if userprofile.stripe_customer_id != '' and userprofile.stripe_customer_id is not None:
            customer = stripe.Customer.retrieve(
                userprofile.stripe_customer_id)
            customer.sources.create(source=token)

        else:
            customer = stripe.Customer.create(
                email=self.request.user.email,
            )
            customer.sources.create(source=token)
            userprofile.stripe_customer_id = customer['id']
            userprofile.one_click_purchasing = True
            userprofile.save()

        amount = int(order.get_total() * 100)

        try:

                # charge the customer because we cannot charge the token more than once
            charge = stripe.Charge.create(
                amount=amount,  # cents
                currency="usd",
                customer=userprofile.stripe_customer_id
            )
            # charge once off on the token
            # charge = stripe.Charge.create(
            #     amount=amount,  # cents
            #     currency="usd",
            #     source=token
            # )

            # create the payment
            payment = Payment()
            payment.stripe_charge_id = charge['id']
            payment.user = self.request.user
            payment.amount = order.get_total()
            payment.save()

            # assign the payment to the order

            order_items = OrderItem.objects.filter(order = order)
            order_items.update(ordered=True)
            for item in order_items:
                item.save()

            order.ordered = True
            order.payment = payment
            order.billing_address = billing_address
            order.shipping_address = shipping_address
            # order.ref_code = create_ref_code()
            order.save()

            return Response(status=HTTP_200_OK)

        except stripe.error.CardError as e:
            body = e.json_body
            err = body.get('error', {})
            return Response({"message": f"{err.get('message')}"}, status=HTTP_400_BAD_REQUEST)

        except stripe.error.RateLimitError as e:
            # Too many requests made to the API too quickly
            messages.warning(self.request, "Rate limit error")
            return Response({"message": "Rate limit error"}, status=HTTP_400_BAD_REQUEST)

        except stripe.error.InvalidRequestError as e:
            print(e)
            # Invalid parameters were supplied to Stripe's API
            return Response({"message": "Invalid parameters"}, status=HTTP_400_BAD_REQUEST)

        except stripe.error.AuthenticationError as e:
            # Authentication with Stripe's API failed
            # (maybe you changed API keys recently)
            return Response({"message": "Not authenticated"}, status=HTTP_400_BAD_REQUEST)

        except stripe.error.APIConnectionError as e:
            # Network communication with Stripe failed
            return Response({"message": "Network error"}, status=HTTP_400_BAD_REQUEST)

        except stripe.error.StripeError as e:
            # Display a very generic error to the user, and maybe send
            # yourself an email
            return Response({"message": "Something went wrong. You were not charged. Please try again."}, status=HTTP_400_BAD_REQUEST)

        except Exception as e:
            # send an email to ourselves
            return Response({"message": "A serious error occurred. We have been notifed."}, status=HTTP_400_BAD_REQUEST)

        return Response({"message": "Invalid data received"}, status=HTTP_400_BAD_REQUEST)
