import time
from selenium import webdriver
from xvfbwrapper import Xvfb

SCROLL_PAUSE_TIME = 3

display = Xvfb()
display.start()
driver = webdriver.Chrome()
my_url = 'https://www.ces.tech/Show-Floor/Exhibitor-Directory.aspx?pageSize=300'
driver.get(my_url)

while True:
    # Get page height
    last_height = driver.execute_script("return document.body.scrollHeight")

    # Scroll down to bottom
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    # Wait to load page
    time.sleep(SCROLL_PAUSE_TIME)

    # Calculate new scroll height and compare with last scroll height
    new_height = driver.execute_script("return document.body.scrollHeight")

    if new_height == last_height:
        break

x=1
main_page = driver.find_elements_by_class_name("listingCard")
for item in main_page:
    print(item.find_element_by_tag_name('a').get_attribute('text'))
    item.find_element_by_tag_name('a').click()
    x=x+1
print(x)

data = {}
driver.get('https://ces20.mapyourshow.com/8_0/exhibitor/exhibitor-details.cfm?ExhID=T0014256')

address_and_telephone = driver.find_elements_by_class_name('pa0')
social = driver.find_elements_by_class_name('darken')
website_about = driver.find_elements_by_class_name('lh-copy')
employees_details = driver.find_element_by_class_name('mys-bullets').find_elements_by_tag_name('li')

data['CompanyName'] = driver.find_element_by_id('js-Vue-MyShow').find_element_by_tag_name('h1').text
data['Booth'] = driver.find_element_by_id('newfloorplanlink').text
data['Company Address'] = address_and_telephone[0].text.replace('\n', ' ')
data['Phone'] = address_and_telephone[1].text.split(' ')[1]
data['Web Site'] = website_about[0].text
data['FaceBook'] = social[0].get_attribute('href').split('?')[0]
data['Twitter'] = social[1].get_attribute('href').split('?')[0]
data['linkedin'] = social[2].get_attribute('href').split('?')[0]
data['About'] = website_about[1].text

for i, value in enumerate(employees_details):
    employee_details = value.text.split('\n')
    for j, detail in enumerate(employee_details):
        if j == 0:
            name_title = detail.split('(')
            data['Name'+str(i)] = name_title[0]
            data['Title'+str(i)] = name_title[1][:-1]

        elif j == 1:
            data['Email'+str(i)] = detail

        elif j == 2:
            data['Phone'+str(i)] = detail.split(' ')[0]


print(driver.page_source)
driver.close()
display.stop()
