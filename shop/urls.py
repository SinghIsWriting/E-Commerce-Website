
from django.urls import path
from . import views

urlpatterns = [
	path('', views.index, name='ShopHome'),
	path('about/', views.about, name='About'),
	path('contact/', views.contact, name='ContactUs'),
	#path('cart/<slug:pname>', views.singleCart, name='SingleCart'),
	path('singleCart/', views.singleCart, name='SingleCart'),
	path('tracker/', views.tracker, name='Tracker'),
	path('singletracker/', views.singletracker, name='SingleTracker'),
	path('checkout/', views.checkout, name='CheckOut'),
	path('productview/<int:myid>', views.prodView, name='ProductView'),
	path('search/', views.search, name='Search'),
	path('orders/', views.orders, name='Orders'),
	path('cartorders/', views.cartorders, name='CartOrders'),
	#path("handlerequest/", views.handlerequest, name="HandleRequest"),
]


'''
int – Matches zero or any positive integer.
str – Matches any non-empty string, excluding the path separator(‘/’).
slug – Matches any slug string, i.e. a string consisting of alphabets, digits, hyphen and under score.
path – Matches any non-empty string including the path separator(‘/’)
uuid – Matches a UUID(universal unique identifier).
'''
