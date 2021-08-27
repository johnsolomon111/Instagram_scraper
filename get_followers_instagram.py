# Imports
from selenium import webdriver
import time
import csv
import os


# Define Chrome driver
chrome_path = 'chromedriver.exe'
options = webdriver.ChromeOptions()
driver = webdriver.Chrome(chrome_path, chrome_options=options)
driver.maximize_window()
driver.implicitly_wait(15)


def start(url, username):
	# Go to url
	driver.get(url)
	time.sleep(1)
	
	# Log in
	usernameElement = driver.find_element_by_css_selector('input[name="username"]')
	passwrodElement = driver.find_element_by_css_selector('input[name="password"]')
	usernameElement.send_keys(username)
	passwrodElement.send_keys(os.environ.get('INSTAGRAM_PASSWORD'))
	time.sleep(1)
	driver.find_element_by_xpath('//*[@id="loginForm"]/div/div[3]/button').click()


	# Click "Not Now" Button
	not_now = driver.find_element_by_xpath('//*[@id="react-root"]/section/main/div/div/div/div/button')
	not_now.click()

	# Click "Not Now" Button
	driver.find_element_by_xpath("/html/body/div[5]/div/div/div/div[3]/button[2]").click()

	# Click "Profile Link"
	driver.find_element_by_xpath(f"//a[contains(text(),'{username}')]").click()

	# Click followers button
	driver.find_element_by_xpath('//*[@id="react-root"]/section/main/div/header/section/ul/li[2]/a').click()
	time.sleep(2)

	# Scroll until the bottom of the list
	for i in range(20):
		class_name = "isgrP"
		length = str((i+1)*10000)
		script = f'document.getElementsByClassName("{class_name}")[0].scrollTo(0,{length})'
		driver.execute_script(script)
		time.sleep(1)

	# Select the Unordered List "ul" then list all the "li"
	ul = driver.find_element_by_xpath('/html/body/div[6]/div/div/div[2]/ul')
	lists = ul.find_elements_by_css_selector('li')

	# Create a csv file to store the data
	with open('followers.csv', mode='w') as write_file:
		csv_writer = csv.writer(write_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL, lineterminator='\n')
		csv_writer.writerow(['username', 'url', 'fullname'])
		
		# Loop all "li" then write it as a row in a csv file
		for li in lists:
			try:
				# get the "a" tag on the list then get the attribute href, thats the account url
				acc_url = li.find_element_by_css_selector('a').get_attribute('href')

				# Username is the string from the profile url at the end
				username = acc_url.replace('https://www.instagram.com/', "").replace('/', "")
				full_name = li.text.split("\n")[1]

				# Write it on the csv
				csv_writer.writerow([username,acc_url,full_name])
				print(username, acc_url, full_name)
			except Exception as e:
				print(e)

	# Close webdriver
	driver.quit()

username_input = input("Enter your username: ")
start('https://www.instagram.com/', username_input)