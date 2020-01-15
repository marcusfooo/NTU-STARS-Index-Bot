from selenium import webdriver
from time import sleep
from pyvirtualdisplay import Display


# env
URL = "https://wish.wis.ntu.edu.sg/pls/webexe/ldap_login.login?w_url=https://wish.wis.ntu.edu.sg/pls/webexe/aus_stars_planner.main"
USERNAME = "ENTER YOUR USERNAME"
PASSWORD = "ENTER YOUR PASSWORD"
OLD_INDEX = "ENTER CURRENT INDEX NUMBER e.g 10123"
NEW_INDEX = "ENTER DESIRED INDEX NUMBER e.g 10123"

x = 0
SEARCH_INDEX = "'" + NEW_INDEX + "'"

def script():
    # Instantiate virtual display
    display = Display(visible=0, size=(800, 600))
    display.start()

    # Instantiate Firefox Browser
    driver = webdriver.Firefox()
    driver.implicitly_wait(30)
    driver.get(URL)

    # Access STARS as user
    username = driver.find_element_by_id("UID")
    username.clear()
    username.send_keys(USERNAME)
    username.submit()
    password = driver.find_element_by_id("PW")
    password.clear()
    password.send_keys(PASSWORD)
    password.submit()
    print("Login Successful as user %s!" % USERNAME)

    # Main script automation
    try:
        driver.find_elements_by_css_selector("input[type='radio'][value=%s]" % OLD_INDEX)[0].click()
        driver.find_element_by_xpath("//select[@name='opt']/option[text()='Change Index']").click()
        driver.find_element_by_xpath("//*[@id='ui_body_container_w']/table/tbody/tr[4]/td[2]/table/tbody/tr[2]/td/input[1]").click()

        index = driver.find_element_by_name('new_index_nmbr')
        for option in index.find_elements_by_tag_name('option'):
            if NEW_INDEX in option.text:
                option.click()
                break

        driver.find_element_by_xpath("//*[@id='ui_body_container']/form[1]/input[1]").click()
        driver.find_element_by_xpath("//*[@id='ui_body_container']/form[1]/input[1]").click()
        driver.quit()
        display.stop()

    except:
        driver.quit()
        display.stop()
        return


print("Attempting Index change from %s to %s..." % (OLD_INDEX, NEW_INDEX))


while True:
    try:
        script()
        x += 1
        print("Success! This is attempt number %s" % x)
    except:
        print("Trying again!")
        sleep(5)
        script()