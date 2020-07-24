from . import DB
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
from bs4 import BeautifulSoup
import re
db = DB.DB()
arr_company = []
class Connect:
	# main class for scrapping
	def main(self, login, password, url):
		# company = Company(url)
		try:
			chrome_options = Options()
			chrome_options.add_argument("--user-data-dir=chrome-data")
			driver = webdriver.Chrome('D:\\LinkedinParser\\chromedriver.exe', options=chrome_options) # path the place app driver
			driver.get("https://www.linkedin.com/login") # redirect the log in page linkedin
			if driver.current_url != "https://www.linkedin.com/feed/":
				element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "username"))) # wait fields login

				email_elem = driver.find_element_by_id("username") # find field login
				email_elem.send_keys(login) # send login

				password_elem = driver.find_element_by_id("password") # find field password
				password_elem.send_keys(password) # send password
				driver.find_element_by_tag_name("button").click() # find button and click for log in
			driver.get(url) # redirect the input url
			# time.sleep(3) # wait 3 seconds
		except:
			return
		post_data = []
		try:
			Company_name = driver.find_element_by_class_name("title.inline-block").text.strip() # find company name
		except:
			Company_name = "Not found"

		try:
			Address = driver.find_element_by_xpath("//a[@data-control-name='topcard_headquarters']").get_attribute("href") #find address and set split
			Split_address = Connect.split_adress(Address)
		except:
			Split_address = "Not found"

		try:
			URL = driver.find_element_by_xpath("//a[@data-control-name='topcard_website']").get_attribute("href") # find url company
		except:
			URL = "Not found"

		try:
			but = driver.find_element_by_class_name("button--unstyled.link-without-visited-state.inline-block.font-size-inherit.topcard-see-more-link").click() #find button for see more information about company and click her
			time.sleep(2)
			Company_discription = driver.find_element_by_xpath("//div[@class='topcard-extended-description-modal-content-padding']/p").text.strip() # take discription
			Company_discription_dismiss = driver.find_element_by_xpath("//button[@aria-label='Dismiss']").click() # click button for close window
		except:
			Company_discription = "Not found"

		try:
			Contact = driver.find_elements_by_xpath("//a[@data-control-name='recommendedLeads_viewLead']") # find contacts href
		except:
			Contact = []
		Contact_href_link = []
		if Contact:
			for i in Contact:
				#create link for redirect contacts
				Contact_href_link.append(i.get_attribute("href"))
		second_value_data = []
		iterr_for_create_second_dict = 0
		if Contact_href_link:
			for i in Contact_href_link:
				if iterr_for_create_second_dict == 4:
					break
				try:
					#try take more information contacts
					driver.get(i)
					er = BeautifulSoup(driver.page_source, 'html.parser') #parse all page
					time.sleep(5)
					contact_ = er.find_all("span", class_ = "profile-topcard-person-entity__name Sans-24px-black-90%-bold")[0].text.strip() if er.find_all("span", class_ = "profile-topcard-person-entity__name Sans-24px-black-90%-bold") else "Not found"
					title_ = er.find_all("dd", class_ = "mt2")[0].text.strip() if er.find_all("dd", class_ = "mt2") else "Not found"
					phone_ = er.find_all("a", href=re.compile('tel'))[0].text.strip() if er.find_all("a", href=re.compile('tel')) else "Not found"
					email_ = er.find_all("a", href=re.compile('mailto'))[0].text.strip() if er.find_all("a", href=re.compile('mailto')) else "Not found"
					second_value_data.append([contact_,title_,phone_,email_])
				except:
					pass
				iterr_for_create_second_dict += 1
		else:
			second_value_data = [["Not found" for x in range(0,16)]]
		driver.close() #close driver
		first_value_data = [Company_name, Company_discription, Split_address, URL]
		#---------------------------------------------------------------------
		for h in second_value_data:
			for i in h:
				first_value_data.append(i)
		db.main(first_value_data) # send data screpping in database
		#---------------------------------------------------------------------


	def split_adress(address):
		# take from href only address
		f = ' '.join(' '.join(address.split("place/")[1].split("%")).split("+"))
		return f #return string


	def search(self, login, password, value_search):

		try:
			chrome_options = Options()
			chrome_options.add_argument("--user-data-dir=chrome-data")
			driver = webdriver.Chrome('D:\\LinkedinParser\\chromedriver.exe', options=chrome_options) # path the place app driver
			driver.maximize_window()
			driver.get("https://www.linkedin.com/login") # redirect the log in page linkedin
			if driver.current_url != "https://www.linkedin.com/feed/":
				element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "username"))) # wait fields login

				email_elem = driver.find_element_by_id("username") # find field login
				email_elem.send_keys(login) # send login

				password_elem = driver.find_element_by_id("password") # find field password
				password_elem.send_keys(password) # send password
				driver.find_element_by_tag_name("button").click() # find button and click for log in # wait 3 seconds
		except:
			return

		try:
			driver.get(value_search)
		except:
			pass

		def parse():
			time.sleep(4)
			html = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "html")))
			html.send_keys(u'\ue010')
			time.sleep(4)
			er = BeautifulSoup(driver.page_source, 'html.parser')
			url = er.find_all("a", href=re.compile('/sales/company/'))
			arr_company.append(url)
		pagin = 2
		while True:
			parse()
			try:
				# next = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "search-results__pagination-next-button")))
				next = driver.find_element_by_xpath(f"//button[@data-page-number=\"{pagin}\"]")
				# webdriver.ActionChains(driver).move_to_element(next).click(next).perform()
				next.click()
			except:
				next = 'done'
			if next == 'done':
				break
			pagin += 1
		time.sleep(3)
		driver.close()
		out_array_company_link = []
		for i in arr_company:
			for j in i:
				if j['class'][0] == 'ember-view':
					out_array_company_link.append('https://www.linkedin.com' + j['href'])
		return out_array_company_link