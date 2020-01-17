import time
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from xvfbwrapper import Xvfb

SCROLL_PAUSE_TIME = 5

display = Xvfb()
display.start()
driver = webdriver.Chrome()
driver2 = webdriver.Chrome()
my_url = 'https://www.ces.tech/Show-Floor/Exhibitor-Directory.aspx?pageSize=300'
"https://www.ces.tech/Show-Floor/Exhibitor-Directory.aspx?searchTerm=&sortBy=alpha&filter=A&pageNo=1&pageSize=30"
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

x = 1
data = {}
main_page = driver.find_elements_by_class_name("listingCard")
for item in main_page:
    company_link = item.find_element_by_tag_name('a').get_attribute('href')
    driver2.get(company_link)

    address_and_telephone = driver2.find_elements_by_class_name('pa0')
    social = driver2.find_elements_by_class_name('darken')
    website_about = driver2.find_elements_by_class_name('lh-copy')
    try:
        employees_details = driver2.find_element_by_class_name('mys-bullets').find_elements_by_tag_name('li')
    except NoSuchElementException as e:
        print(e)
        employees_details = []

    data['CompanyName'] = driver2.find_element_by_id('js-Vue-MyShow').find_element_by_tag_name('h1').text
    data['Booth'] = driver2.find_element_by_id('newfloorplanlink').text
    data['Company Address'] = address_and_telephone[0].text.replace('\n', ' ')
    data['Phone'] = address_and_telephone[1].text.split(' ')[1]
    data['Web Site'] = website_about[0].text
    if len(social) > 0:
        data['FaceBook'] = social[0].get_attribute('href').split('?')[0]
    if len(social) > 1:
        data['Twitter'] = social[1].get_attribute('href').split('?')[0]
    if len(social) > 2:
        data['linkedin'] = social[2].get_attribute('href').split('?')[0]
    data['About'] = website_about[1].text

    for i, value in enumerate(employees_details):
        employee_details = value.text.split('\n')
        for j, detail in enumerate(employee_details):
            if j == 0:
                name_title = detail.split('(')
                data['Name' + str(i)] = name_title[0]
                data['Title' + str(i)] = name_title[1][:-1]

            elif j == 1:
                data['Email' + str(i)] = detail

            elif j == 2:
                data['Phone' + str(i)] = detail.split(' ')[0]

    print(x)
    print(data)
    x += 1
    data = {}

driver.close()
display.stop()
driver2.close()
