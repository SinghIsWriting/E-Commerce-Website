from django.db import models
from django.utils.safestring import mark_safe
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
# from tinymce.models import HTMLField

STATE_CHOICES = (
        ('Andhra Pradesh','Andhra Pradesh'),
  ('Arunachal Pradesh','Arunachal Pradesh'),
                          ('Assam','Assam'),
                          ('Bihar','Bihar'),
            ('Chhattisgarh','Chhattisgarh'),
                    ('Delhi','Delhi'),
                              ('Goa','Goa'),
                      ('Gujarat','Gujarat'),
                      ('Haryana','Haryana'),
    ('Himachal Pradesh','Himachal Pradesh'),
  ('Jammu and Kashmir','Jammu and Kashmir'),
                  ('Jharkhand','Jharkhand'),
                  ('Karnataka','Karnataka'),
                        ('Kerala','Kerala'),
        ('Madhya Pradesh','Madhya Pradesh'),
              ('Maharashtra','Maharashtra'),
                      ('Manipur','Manipur'),
                  ('Meghalaya','Meghalaya'),
                      ('Mizoram','Mizoram'),
                    ('Nagaland','Nagaland'),
                        ('Odisha','Odisha'),
          ('Puducherry[b]','Puducherry[b]'),
                        ('Punjab','Punjab'),
                  ('Rajasthan','Rajasthan'),
                        ('Sikkim','Sikkim'),
                ('Tamil Nadu','Tamil Nadu'),
                  ('Telangana','Telangana'),
                      ('Tripura','Tripura'),
          ('Uttar Pradesh','Uttar Pradesh'),
              ('Uttarakhand','Uttarakhand'),
              ('West Bengal','West Bengal'),
)

# Create your models here.
class Product(models.Model):
	product_id = models.AutoField
	product_name = models.CharField(max_length=50)
	category = models.CharField(max_length=50, default='')
	subcategory = models.CharField(max_length=50, default="")
	price = models.IntegerField(default=0)
	# desc = HTMLField(default="")
	desc = models.CharField(default="", max_length=5000)
	image = models.ImageField(upload_to="shop/images/", default = '')
	pub_date = models.DateField()

	def __str__(self):
		return self.product_name

	def image_tag(self):
		if self.image:
			return mark_safe('<img src="%s" style="width: 45px; height:45px;" />' % self.image.url)
		else:
			return 'No Image Found'
	image_tag.short_description = 'Image'

class Contact(models.Model):
	msg_id = models.AutoField(primary_key=True)
	name = models.CharField(max_length=50)
	email = models.CharField(max_length=70, default='')
	phone = models.CharField(max_length=50, default='')
	desc = models.CharField(max_length=500, default='')

	def __str__(self):
		return self.name

class Orders(models.Model):
	order_id = models.AutoField(primary_key=True)
	items_json = models.CharField(max_length=5000)
	amount = models.FloatField(default=0)
	name = models.CharField(max_length=120)
	email = models.CharField(max_length=70)
	phone = models.CharField(max_length=50)
	address = models.CharField(max_length=200)
	city = models.CharField(max_length=70)
	state = models.CharField(max_length=70)
	zip_code = models.CharField(max_length=50)
	timestamp = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.name

class SingleOrders(models.Model):
        order_id1 = models.AutoField(primary_key=True)
        pname = models.CharField(max_length=500)
        pprice = models.FloatField(default=0)
        quant = models.FloatField(default=0)
        name = models.CharField(max_length=120)
        email = models.CharField(max_length=70)
        phone = models.CharField(max_length=50)
        address = models.CharField(max_length=200)
        city = models.CharField(max_length=70)
        state = models.CharField(max_length=70)
        zip_code = models.CharField(max_length=50)
        timestamp = models.DateTimeField(auto_now_add=True)

        def __str__(self):
                return self.name+"_"
        @property
        def total_cost(self):
            return self.pprice * self.quant

class OrderUpdate(models.Model):
	update_id = models.AutoField(primary_key=True)
	order_id = models.IntegerField(default="")
	update_desc = models.CharField(max_length=5000)
	timestamp = models.DateField(auto_now_add=True)

	def __str__(self):
		return self.update_desc[0:27] + "..."

class SingleOrderUpdate(models.Model):
        update_id = models.AutoField(primary_key=True)
        order_id1 = models.IntegerField(default="")
        update_desc = models.CharField(max_length=5000)
        timestamp = models.DateField(auto_now_add=True)

        def __str__(self):
                return self.update_desc[0:27] + "..."

STATE_CHOICES = (
        ('Andhra Pradesh','Andhra Pradesh'),
  ('Arunachal Pradesh','Arunachal Pradesh'),
                          ('Assam','Assam'),
                          ('Bihar','Bihar'),
            ('Chhattisgarh','Chhattisgarh'),
                    ('Delhi','Delhi'),
                              ('Goa','Goa'),
                      ('Gujarat','Gujarat'),
                      ('Haryana','Haryana'),
    ('Himachal Pradesh','Himachal Pradesh'),
  ('Jammu and Kashmir','Jammu and Kashmir'),
                  ('Jharkhand','Jharkhand'),
                  ('Karnataka','Karnataka'),
                        ('Kerala','Kerala'),
        ('Madhya Pradesh','Madhya Pradesh'),
              ('Maharashtra','Maharashtra'),
                      ('Manipur','Manipur'),
                  ('Meghalaya','Meghalaya'),
                      ('Mizoram','Mizoram'),
                    ('Nagaland','Nagaland'),
                        ('Odisha','Odisha'),
          ('Puducherry[b]','Puducherry[b]'),
                        ('Punjab','Punjab'),
                  ('Rajasthan','Rajasthan'),
                        ('Sikkim','Sikkim'),
                ('Tamil Nadu','Tamil Nadu'),
                  ('Telangana','Telangana'),
                      ('Tripura','Tripura'),
          ('Uttar Pradesh','Uttar Pradesh'),
              ('Uttarakhand','Uttarakhand'),
              ('West Bengal','West Bengal'),
)

class Customer(models.Model):
        user = models.ForeignKey(User, on_delete=models.CASCADE)
        name = models.CharField(max_length=200)
        email = models.CharField(max_length=70, default = "")
        locality = models.CharField(max_length=200)
        city = models.CharField(max_length=70)
        zipcode = models.IntegerField()
        state = models.CharField(choices=STATE_CHOICES,max_length=50)

        def __str__(self):
                return str(self.id)
