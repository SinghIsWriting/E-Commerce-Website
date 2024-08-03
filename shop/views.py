from django.shortcuts import render
from django.http import HttpResponse
from .models import Product, Contact, Orders, OrderUpdate, SingleOrders, SingleOrderUpdate, Customer
from django.contrib import messages
from math import ceil
import json, platform
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
#from PayTm import Checksum	# pip install PayTm

MERCHANT_KEY = 'Your-Merchant-Key-Here'

def index(request):
	products = Product.objects.all()
	all = Orders.objects.all()
	n = len(products)
	allprods = []
	catprods = Product.objects.values('category', 'id')
	cats = {item['category'] for item in catprods}
	for cat in cats:
		prod = Product.objects.filter(category=cat)
		#print(Product.objects.get(id=1).image)
		n = len(prod)
		nSlides = n // 4 + ceil((n / 4) - (n // 4))
		allprods.append([prod, range(1, nSlides), nSlides])

	# for getting the device so that we can show the cards accordingly in responsive manner
	system = platform.system()
	machine = platform.machine()
	if system == 'Linux':
		if 'arm' in machine:
			device_width = 1
		elif 'aarch64' in machine:
			device_width = 1
		elif 'x86' in machine:
			device_width = 4
		else:
			return 2
	elif system == 'Windows':
		device_width = 4
	elif system == 'Darwin':
		if 'iPhone' in machine:
			device_width = 1
		elif 'iPad' in machine:
			device_width = 2
		elif 'x86_64' in machine:
			device_width = 4
		else:
			device_width = 4
	else:
		device_width = 4

	# print(f"DEVICE WIDTH: ==> {device_width}\n")
	params = {'allprods':allprods, 'device_width': device_width}
	return render(request, 'shop/index.html', params)

def about(request):
        return render(request,"shop/about.html")

@login_required
def singleCart(request):
        global prod_id
        if request.method == "GET":
                prod_id = request.GET['prod_id']
        prods = Product.objects.filter(id=prod_id)
        proname = prods[0].product_name
        proprice = prods[0].price
        #print("Mil gayi prod_id:",prod_id,"proname:",type(proname),"proprice:",type(proprice))
        thank=False
        odi = len(SingleOrders.objects.all())
        if request.method == "POST":
                try:
                    custid = request.POST.get('custid')
                    customer = Customer.objects.get(id=custid)
                    #print("custid:",custid,"Cusroooomer mil gaya:",customer,"locality:",customer.locality)
                    pname= proname
                    name = str(customer.name)+"s!#$%&'()*+,e-./:;<=>?@[\]x^_`{|}~y"+str(odi+18)+"s!#$%&'()*+,e-./:;<=>?@[\]x^_`{|}~y"+str(request.user.id)
                    pprice = proprice
                    quant = request.POST.get('quant','')
                    email = customer.email
                    phone = request.POST.get('phone','')
                    address = (customer.locality)+" "+(customer.city)+" "+(customer.state)+"-"+(str(customer.zipcode))
                    city = customer.city
                    state = customer.state
                    zip_code = customer.zipcode
                    if (quant !='' and (quant[0] !="." or "-" not in quant) and int(quant)>0 and name !='' and email !='' and phone !='' and address !='' and city !='' and state !='' and zip_code !=''):
                        order = SingleOrders(pname=pname, name=name, pprice=pprice, quant=quant, email=email, phone=phone, address=address, city=city, state=state, zip_code=zip_code)
                        order.save()
                        update= SingleOrderUpdate(order_id1= order.order_id1, update_desc="Your order has been placed")
                        update.save()
                        thank=True
                        id = order.order_id1
                        return render(request, 'shop/placed_order.html', {'id': id, 'active':'btn-dark'})
                    else:
                        return render(request, 'shop/siOrEr.html')
                        #return render(request, 'shop/prodView.html', {'thank':'thank'})
                except Exception as e:
                    #print("Errrrrrorrrr:",e)
                    return render(request, 'shop/siOrEr.html')

        return render(request,"shop/prodView.html")

def contact(request):
	thank=False
	if request.method == "POST":
		name = request.POST.get('name','')
		email = request.POST.get('email','')
		phone = request.POST.get('phone','')
		desc = request.POST.get('desc','')
		#print(name, email, phone, desc)
		if (name !='' and email !='' and phone !='' and desc !=''):
			contact = Contact(name=name, email=email, phone=phone, desc=desc)
			contact.save()
			thank=True
			return render(request,"shop/contact.html", {'thank':'alert alert-success'})
		else:
			return render(request,"shop/contact.html", {'thanks':'alert alert-danger'})
	return render(request, 'shop/contact.html')

@login_required
def tracker(request):
	if request.method == "POST":
		orderId = request.POST.get('orderId','')
		email = request.POST.get('email','')
		try:
			order = Orders.objects.filter(order_id=orderId, email=email)
			if len(order)>0:
				update = OrderUpdate.objects.filter(order_id=orderId)
				updates = []
				for item in update:
					updates.append({'text':item.update_desc,'time':item.timestamp})
					response = json.dumps({"status":"success","updates":updates, "itemsJson":order[0].items_json}, default=str)
					# print(response)
				return HttpResponse(response)
			else:
				return HttpResponse('{"status":"no item found"}')
		except Exception as e:
			return HttpResponse('{"status":"error"}')
	return render(request,"shop/tracker.html")

@login_required
def singletracker(request):
        if request.method == "POST":
                orderId1 = request.POST.get('orderId1','')
                email = request.POST.get('email','')
                try:
                        order = SingleOrders.objects.filter(order_id1=orderId1, email=email)
                        #print(order[0].pname, order[0].pprice, order[0].quant)
                        if len(order)>0:
                                update = SingleOrderUpdate.objects.filter(order_id1=orderId1)
                                updates = []
                                for item in update:
                                        updates.append({'text':item.update_desc, 'time':item.timestamp})
                                        itemsJson =[{'pname':order[0].pname,'pprice':order[0].pprice,'quant':int(order[0].quant) }]
                                        response = json.dumps({"status":"success","updates":updates, "itemsJson":itemsJson}, default=str)
                                        #print(itemsJson)
                                return HttpResponse(response)
                        else:
                                return HttpResponse('{"status":"no item found"}')
                except Exception as e:
                        return HttpResponse('{"status":"error"}')
        return render(request,"shop/singletracker.html")

def orders(request):
	#print("User:",request.user.username, "Email:",request.user.id,"Single Order: #", len(SingleOrders.objects.all()))
	sOrd = SingleOrders.objects.all()
	global allorders
	orderss = []
	for u in sOrd:
		c = u.name.split("s!#$%&'()*+,e-./:;<=>?@[\]x^_`{|}~y")
		try:
			if c[2].strip() == str(request.user.id).strip():
				ords = SingleOrders.objects.filter(order_id1=int(c[1]))[0]
				ostat = SingleOrderUpdate.objects.filter(order_id1=int(c[1]))[0]
				ordict = {"ords":ords,"ostat":ostat}
				stat = (ostat.update_desc).split()
				#print('Update desc:',ostat.update_desc, stat)
				if ("placed" in stat or "accepted" in stat):ordict.update({"stCol":"#2389da"})
				elif "shipped" in stat or "packed" in stat:ordict.update({"stCol":"#FFD700"})
				elif "dispatched" in stat or "sent" in stat:ordict.update({"stCol":"#FF8C00"})
				elif "delivered" in stat or "arrived" in stat:ordict.update({"stCol":"#32CD32"})
				else:ordict.update({"stCol":"rgba(0, 0, 0, 0.19)"})
				orderss.append(ordict)
		except:
			pass
	allorders = list(reversed(orderss))
	return render(request,"shop/orders.html", {'orders':allorders, 'active':'btn-dark'})

def cartorders(request):
	cOrd = Orders.objects.all()
	cartorderss = []
	for v in cOrd:
		d = v.name.split("s!#$%&'()*+,e-./:;<=>?@[\]x^_`{|}~y")
		#print(d[0],d[1],d[2])
		try:
			if d[2].strip() == str(request.user.id).strip():
				cOrds = Orders.objects.filter(order_id=int(d[1]))[0]
				ostat = OrderUpdate.objects.filter(order_id=int(d[1]))[0]
				stat = (ostat.update_desc).split()
				if ("placed" in stat or "accepted" in stat): stCol="#2389da"
				elif "shipped" in stat or "packed" in stat: stCol="#FFD700"
				elif "dispatched" in stat or "sent" in stat: stCol="#FF8C00"
				elif "delivered" in stat or "arrived" in stat: stCol="#32CD32"
				else: stCol="rgba(0, 0, 0, 0.19)"
				o = {
					"itemsJson":json.loads(cOrds.items_json),
					"amount":cOrds.amount,
					"email":cOrds.email,
					"id":cOrds.order_id,
					"timestamp":cOrds.timestamp,
					"stCol":stCol,
				}
				cartorderss.append(o)
				#print("All orders json:",type(json.loads(cOrds.items_json)),"Amount:",cOrds.amount)
		except:
			pass
	cartorders = list(reversed(cartorderss))
	#print(type(cartorders))
	return render(request,"shop/cartorders.html", {'active':'btn-dark','orders':cartorders})

@login_required
def checkout(request):
	odsi = len(Orders.objects.all())
	#print("Length of Orders",odsi)
	thank=False
	add = Customer.objects.filter(user=request.user)
	if request.method == "POST":
		try:
			custid = request.POST.get('custid')
			customer = Customer.objects.get(id=custid)
			#print("custid:",custid,"customer:",customer)
			items_json= request.POST.get('itemsJson', '')
			name = str(customer.name)+"s!#$%&'()*+,e-./:;<=>?@[\]x^_`{|}~y"+str(odsi+3)+"s!#$%&'()*+,e-./:;<=>?@[\]x^_`{|}~y"+str(request.user.id)
			amount = request.POST.get('amount','')
			email = customer.email
			phone = request.POST.get('phone','')
			address = (customer.locality)+" "+(customer.city)+" "+(customer.state)+"-"+(str(customer.zipcode))
			city = customer.city
			state = customer.state
			zip_code = customer.zipcode
			if (items_json !='' and amount !='' and state !='' and name !='' and email !='' and phone !='' and address !='' and city !='' and zip_code !=''):
				order = Orders(items_json=items_json, name=name, amount=amount, email=email, phone=phone, address=address, city=city, state=state, zip_code=zip_code)
				order.save()
				update= OrderUpdate(order_id= order.order_id, update_desc="Your order has been placed")
				update.save()
				thank=True
				id = order.order_id
				return render(request, 'shop/placed_order.html', {'thanks':thank, 'id': id})
			else:
				return render(request, 'shop/siOrEr.html', {'thank':"alert alert-danger"})
		except:
			return render(request, 'shop/siOrEr.html')
	return render(request, 'shop/checkout.html', {"add":add})
		#request paytm to transfer the amount to your account after payment by user
'''

		param_dict={
			'MID': 'WorldP64425807474247',
			'ORDER_ID': 'order.order_id',
			'TXN_AMOUNT': '1',
			'CUST_ID': 'email',
			'INDUSTRY_TYPE_ID': 'Retail',
			'WEBSITE': 'WEBSTAGING',
			'CHANNEL_ID': 'WEB',
			'CALLBACK_URL':'http://127.0.0.1:8000/shop/handlepayment/',
		}
		param_dict['CHECKSUMHASH'] = Checksum.generate_checksum(param_dict, MERCHANT_KEY)
		return  render(request, 'shop/paytm.html', {'param_dict': param_dict})
	return render(request, 'shop/checkout.html')

'''

'''
@login_required
@csrf_exempt
def handlerequest(request):
    # paytm will send you post request here
    form = request.POST
    response_dict = {}
    for i in form.keys():
        response_dict[i] = form[i]
        if i == 'CHECKSUMHASH':
            checksum = form[i]

    verify = Checksum.verify_checksum(response_dict, MERCHANT_KEY, checksum)
    if verify:
        if response_dict['RESPCODE'] == '01':
            print('order successful')
        else:
            print('order was not successful because' + response_dict['RESPMSG'])
    return render(request, 'shop/paymentstatus.html', {'response': response_dict})
'''

def prodView(request, myid):
	product = Product.objects.filter(id=myid)
	pNmPr = product[0].product_name + "_" + str(product[0].price)
	#print("product id:",product[0].id)
	add = Customer.objects.filter(user=request.user)
	return render(request,"shop/prodView.html",{'product':product[0],'pNmPr':pNmPr, 'add':add})

def searchMatch(query1, item):
    '''return true only if query matches the item'''
    queries = query1.lower().split()
    a = 0
    for query in queries:
        if query in item.desc.lower() or query in item.product_name.lower() or query in item.category.lower() or query in str(item.price):
            a += 1
        else:
            pass
    if a>=1:
        return True
    else:
        return False

def search(request):
    query = request.GET.get('search','')
    allProds = []

    ctg = Product.objects.filter(category__icontains=query.strip())
    pnm = Product.objects.filter(product_name__icontains=query.strip())
    dsc = Product.objects.filter(desc__icontains=query.strip())
#    prod = [item for item in prodtemp if searchMatch(query, item)]
    prod = [item for item in ctg] + [item for item in pnm] + [item for item in dsc]

    n = len(prod)
    nSlides = n // 4 + ceil((n / 4) - (n // 4))
    if len(prod) != 0:
        allProds.append([prod, range(1, nSlides), nSlides])
    params = {'allProds': allProds, "msg": ""}
    if len(allProds) == 0 or len(query)<4:
        params = {'msg': "Please make sure to enter relevant search query"}
    return render(request, 'shop/search.html', params)

'''
    catprods = Product.objects.values('category', 'id')
    cats = {item['category'] for item in catprods}
    #for cat in cats:
'''
