#here .cart is the cart.py file and Cart is the class in the cart.py file
from .cart import Cart 

#create context processor so our cart can work on all pages of  site
def cart(request):
    #return default data from our Cart
    return{'cart':Cart(request)}