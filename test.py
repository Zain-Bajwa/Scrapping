import time
from selenium import webdriver

SCROLL_PAUSE_TIME = 3

driver = webdriver.Chrome()

my_url = 'https://www.ces.tech/Show-Floor/Exhibitor-Directory.aspx?pageSize=300'
driver.get(my_url)

# Get scroll height
last_height = driver.execute_script("return document.body.scrollHeight")

while True:
    # Scroll down to bottom
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    # Wait to load page
    time.sleep(SCROLL_PAUSE_TIME)

    # Calculate new scroll height and compare with last scroll height
    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        break
    last_height = new_height

x = 1
for item in driver.find_elements_by_class_name("listingCard"):
    print(item)
    x = x + 1
print(x)
# aa = driver.find_element_by_class_name("listingCard")

# driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
# driver.execute_script("window.scrollTo(0, Y)")
# driver.get('file:///C:/Users/zaina/Downloads/zain/test1.html')
# print(driver.page_source)
# print(driver.get_log('browser'))
# driver.execute_script("document.getElementById('intro-text').innerHTML = 'This is my script.'")
# print(driver.page_source)
driver.close()
