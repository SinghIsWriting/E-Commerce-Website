from django.shortcuts import render
from .forms import CustomerRegistrationForm, CustomerProfileForm
from django.views import View
from django.contrib import messages
from shop.models import Customer
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.models import User
from django.conf import settings
from django.core.mail import send_mail, EmailMultiAlternatives

def index(request):
	return render(request, 'index.html')

class CustomerRegistrationView(View):
	def get(self, request):
		form = CustomerRegistrationForm()
		return render(request, 'customerregistration.html', {'form':form})
	def post(self, request):
		form = CustomerRegistrationForm(request.POST)
		if form.is_valid():
			messages.success(request, "You've signed up successfully!")
			usn = form.cleaned_data['username']
			em = form.cleaned_data['email']
			p1 = form.cleaned_data['password1']
			p2 = form.cleaned_data['password2']
			cus = User(username=usn, email=em, password=p1)
			cus.save()
			# print("usn:",usn, "email:", em)
			subject = f'FavoriteItems-Registration Successful !'
			# message = f'Welcome {usn}, You have been registered successfully on FavoriteItems. Thanks for joing us, please go through the shop of favoriteitems and start purchasing your favorite itmes in few clicks. It\'s easy'
			message = f'''<div class='card' style="border-radius:20px; text-align:center; background-color:black; color:white;"><h1 style="text-align: center; padding:10px">Welcome to Favorite Itmes</h1> <h2 style="text-align: center; padding:10px;">Congratulations! Your registration has been completed successfully. Now you are all set with us. Go through the shop of Favorite itmes and purchase all kind of favorite itmes in few clicks.</h2> <p>&nbsp;</p></div> <div class='card' style='border-radius:10px; box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.2), 0 6px 20px 0 rgba(0, 0, 0, 0.19)'><h3>Your accounts details are following:</h3> <pre>username: <strong>{usn}<br /></strong>email: <strong><a href="mailto:{em}">{em}</a><br /></strong>password:<strong> xxxxxxxx</strong></pre></div> <div class='card' style="border-radius:200px; text-align:center; background-color:black;"><a style='text-decoration:none;' href='http://127.0.0.1:8000/accounts/login/'><h1 style='color:white; padding:5px;'>Login to your new account</h1></a></div></div>'''
			email_from = settings.EMAIL_HOST_USER
			recipient_list = [em]
			# send_mail( subject, message, email_from, recipient_list, fail_silently=False, )
			message = EmailMultiAlternatives(subject, message, email_from, recipient_list)
			message.content_subtype = "html"
			message.send()
			print("Registration completion mail has been sent.")
			# form.save()
		return render(request, 'customerregistration.html', {'form':form})

def passreset(request):
	usr = User.objects.filter(username=request.user)
	#print(usr)
	umail = usr.email
	subject = 'Successful !!!'
	# message = f'Hi {usr}, You have been registered successfully. Thanks for joing us your profile in favoriteitems.'
	message = f'''<div class='card' style="border-radius:20px; text-align:center; background-color:black; color:white;"><h1 style="text-align: center; padding:10px">Welcome to Favorite Itmes</h1> <h2 style="text-align: center; padding:10px;">Hi {usr}, You have been registered successfully. Thanks for joing us your profile in favoriteitems.</h2> <p>&nbsp;</p></div> <div class='card' style='border-radius:10px; box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.2), 0 6px 20px 0 rgba(0, 0, 0, 0.19)'><h3>Your accounts details are following:</h3> <pre>username: <strong>{usr}<br /></strong>email: <strong><a href="mailto:{umail}">{umail}</a><br /></strong>password:<strong> xxxxxxxx</strong></pre></div> <div class='card' style="border-radius:200px; text-align:center; background-color:black;"><a style='text-decoration:none;' href='http://127.0.0.1:8000/accounts/login/'><h1 style='color:white; padding:5px;'>Login to your account</h1></a></div>'''
	email_from = settings.EMAIL_HOST_USER
	recipient_list = [umail]
	send_mail( subject, message, email_from, recipient_list, fail_silently=False, )
	print("Password change mail hase been sent.")
	return render(request, 'password_reset_done.html')

@method_decorator(login_required, name='dispatch')
class ProfileView(View):
	def get(self, request):
		usr = User.objects.filter(username=request.user)[0]
		umail = usr.email
		form = CustomerProfileForm()
		return render(request, 'profile.html', {'form':form, 'active':'btn-dark', 'email':umail})
	def post(self, request):
		usr = User.objects.filter(username=request.user)[0]
		umail = usr.email
		form = CustomerProfileForm(request.POST)
		if form.is_valid():
			usr = request.user
			name = form.cleaned_data['name']
			email = umail
			locality = form.cleaned_data['locality']
			city = form.cleaned_data['city']
			state = form.cleaned_data['state']
			zipcode = form.cleaned_data['zipcode']
			reg = Customer(user=usr,name=name, email=email, locality=locality, city=city, state=state, zipcode=zipcode)
			reg.save()
			messages.success(request, "Profile is updated successfully!")

			subject = f'Welcome! {name}'
			message = f'Hi {usr}, thank you for updating your profile in favoriteitems. Now you can buy here anything in just few clicks.'
			email_from = settings.EMAIL_HOST_USER
			recipient_list = [email]
			send_mail( subject, message, email_from, recipient_list, fail_silently=False, )
			print("Email has been sent to you !!!")
		return render(request, 'profile.html', {'form':form, 'active':'btn-dark'})

@login_required
def address(request):
	addr = Customer.objects.filter(user=request.user)
	return render(request, 'address.html', {'add':addr, 'active':'btn-dark'})

@login_required
def remAddress(request):
	global add_no
	if request.method == "GET":
		add_no = request.GET['add_no']
	cust = Customer.objects.filter(user=request.user)
	#print("Add no:",type(add_no),"Customers:",cust)
	a = 1
	for c in cust:
		if int(add_no) > len(cust) or int(add_no) < 1:
			return render(request, 'address.html', {'noAdd':add_no})
		elif str(a) == add_no:
			c.delete()
			print(f"Addreaa {add_no} is deleted successfully!!")
			return render(request, 'address.html', {'success':True})
		else:
			return render(request, 'address.html', {'error':True})
		a += 1
	return render(request, 'address.html')
