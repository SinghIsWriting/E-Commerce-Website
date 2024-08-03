from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator

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
