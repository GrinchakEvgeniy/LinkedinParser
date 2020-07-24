from django.db import models

# Create your models here.
class Main_db(models.Model):
	id = models.AutoField(primary_key=True)
	company_name = models.CharField(max_length = 100)
	company_description = models.TextField()
	adress = models.CharField(max_length = 100)
	url = models.URLField()
	email = models.EmailField(default = 'NULL', max_length = 100)
	phone = models.CharField(default = 'NULL', max_length = 100)
	contact_1 = models.CharField(default = 'NULL', max_length = 100)
	title_1 = models.CharField(default = 'NULL', max_length = 100)
	contact_2 = models.CharField(default = 'NULL', max_length = 100)
	title_2 = models.CharField(default = 'NULL', max_length = 100)
	contact_3 = models.CharField(default = 'NULL', max_length = 100)
	title_3 = models.CharField(default = 'NULL', max_length = 100)
	contact_4 = models.CharField(default = 'NULL', max_length = 100)
	title_4 = models.CharField(default = 'NULL', max_length = 100)
