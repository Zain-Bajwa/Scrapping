import time
from selenium import webdriver

SCROLL_PAUSE_TIME = 3

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

driver2 = webdriver.Chrome()
x=1
main_page = driver.find_elements_by_class_name("listingCard")
for item in main_page:
    company_link = item.find_element_by_tag_name('a').get_attribute('href')
    driver2.get(company_link)
    print(x)
    x=x+1

driver.close()
driver2.close()

