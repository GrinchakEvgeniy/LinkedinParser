from django.shortcuts import render
from django.contrib import messages
import csv
from django.http import HttpResponse
from . import Connect, DB
db = DB.DB()
connect_ = Connect.Connect()
# Create your views here.
post = {}   # main data set
stop_command = False
Export_Contacts_data_field = ['Contact Name', 'Contact Job Title', 'Company name', 'Company Address', 'Email Address', 'Phone Number', 'Website'] # array from create csv file Contacts
Export_Leads_data_field = ['Contact Name', 'Contact Job Title', 'Company Name', 'Company description', 'Company Address', 'Website'] # array from create csv file Leads
class MainView:
	# index main template method
	def index(request):
		if request.method == 'POST' and (request.POST.get('connect_linkedin') or request.POST.get('searchField')):
			MainView.connect(request)
			post['login'] = request.POST.get('userNameLinkedin') # for save data in field login
			post['password'] = request.POST.get('userPasswordLinkedin') # for save data in field pass
		if request.method == 'POST' and request.POST.get('clear'): # on click button clear
			db.clear() # call method clear in database
		if request.method == 'POST' and request.POST.get('delete_row'):
			db.delete(request.POST.get('delete_row'))
		if request.method == 'POST' and request.POST.get('stop'):
			global stop_command
			stop_command = True
		post['data'] = db.select() # add data screpping in super array post
		return render(request, 'main/index.html', post) # render page

	def connect(request):
		if request.method == 'POST' and request.POST.get('userNameLinkedin') and request.POST.get('userPasswordLinkedin') and request.POST.get('companyURL'):
			#get value in field login, password, companu url
			userNameLinkedin = request.POST.get('userNameLinkedin')
			userPasswordLinkedin = request.POST.get('userPasswordLinkedin')
			companyURL = request.POST.get('companyURL')
			# call main method for screpping
			connect_.main(userNameLinkedin, userPasswordLinkedin, companyURL)
		if request.method == 'POST' and request.POST.get('userNameLinkedin') and request.POST.get('userPasswordLinkedin') and request.POST.get('searchField'):
			userNameLinkedin = request.POST.get('userNameLinkedin')
			userPasswordLinkedin = request.POST.get('userPasswordLinkedin')
			search_value = request.POST.get('searchField')
			company_list_for_pars = connect_.search(userNameLinkedin, userPasswordLinkedin, search_value)
			print(company_list_for_pars)
			try:
				for company_url in company_list_for_pars:
					if stop_command:
						break
					connect_.main(userNameLinkedin, userPasswordLinkedin, company_url)
			except:
				messages.warning(request, f'Having trouble scraping!')
		else:
			messages.warning(request, f'Fill in the fields: required - "login" and "password", optionally "insert url" or "Search"') # error if empty fields

	def download_Leads(request):
		# create and download csv file Leads.csv
		response = HttpResponse(content_type='text/csv')
		response['Content-Disposition'] = 'attachment; filename="Leads.csv"'
		writer = csv.writer(response, delimiter=',')
		data_value = []
		# fields = ['Company_name', 'Company_discription',  'Split_address', 'URL', 'Contact1', 'Title1', 'Phone1', 'Email1', 'Contact2', 'Title2', 'Phone2', 'Email2', 'Contact3', 'Title3', 'Phone3', 'Email3', 'Contact4', 'Title4', 'Phone4', 'Email4']
		writer.writerow(Export_Leads_data_field) # first row (header)
		for i in post['data']:
			# create rows data
			data_value.append([[i[4],i[5],i[0],i[1],i[2],i[3]]])
		for i in data_value:
			# write rows data
			for j in i:
				if j[0] == 'None':
					break
				writer.writerow(j)
		return response

	def download_Contacts(request):
		# create and download csv file Contacts.csv
		response = HttpResponse(content_type='text/csv')
		response['Content-Disposition'] = 'attachment; filename="Contacts.csv"'
		writer = csv.writer(response, delimiter=',')
		data_value = []
		# fields = ['Company_name', 'Company_discription',  'Split_address', 'URL', 'Contact1', 'Title1', 'Phone1', 'Email1', 'Contact2', 'Title2', 'Phone2', 'Email2', 'Contact3', 'Title3', 'Phone3', 'Email3', 'Contact4', 'Title4', 'Phone4', 'Email4']
		writer.writerow(Export_Contacts_data_field) # write first row (header)
		for i in post['data']:
			# create data for write
			Address_pars = i[2].split()
			data_value.append([[i[4],i[5],i[0],i[2], i[7],i[6],i[3]],
				[i[8],i[9],i[0],i[2], i[11],i[10],i[3]],
				[i[12],i[13],i[0],i[2], i[15],i[14],i[3]],
				[i[16],i[17],i[0],i[2], i[19],i[18],i[3]]])
		for i in data_value:
			# write rows data
			for j in i:
				if j[0] == 'None':
					break
				writer.writerow(j)
		return response


	def break_loop(self):
		stop = stop_command
		return stop_command