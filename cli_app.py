from selenium import webdriver
from time import sleep



def start():
    URL = "https://wish.wis.ntu.edu.sg/pls/webexe/ldap_login.login?w_url=https://wish.wis.ntu.edu.sg/pls/webexe/aus_stars_planner.main"
    USERNAME = input("ENTER YOUR USERNAME: ")
    PASSWORD = input("ENTER YOUR PASSWORD: ")
    user = False
    pw = False

    while not user:
        try:
            OLD_INDEX = str(input("ENTER YOUR CURRENT INDEX NUMBER e.g 10123: "))
            user = True
        except TypeError:
            pass

    while not pw:
        try:
            NEW_INDEX = str(input("ENTER YOUR DESIRED INDEX NUMBER e.g 10123: "))
            pw = True
        except TypeError:
            pass

    print("Attempting Index change from %s to %s..." % (OLD_INDEX, NEW_INDEX))
    SEARCH_INDEX = NEW_INDEX
    OLD_INDEX = "'" + OLD_INDEX + "'"
    NEW_INDEX = "'" + NEW_INDEX + "'"

    return URL, USERNAME, PASSWORD, OLD_INDEX, NEW_INDEX, SEARCH_INDEX


def script(URL, USERNAME, PASSWORD, OLD_INDEX, NEW_INDEX, SEARCH_INDEX):
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
            if SEARCH_INDEX in option.text:
                option.click()
                break

        driver.find_element_by_xpath("//*[@id='ui_body_container']/form[1]/input[1]").click()
        driver.find_element_by_xpath("//*[@id='ui_body_container']/form[1]/input[1]").click()
        driver.quit()

    except:
        driver.quit()
        return


x = 0
URL, USERNAME, PASSWORD, OLD_INDEX, NEW_INDEX, SEARCH_INDEX = start()

while True:
    try:
        script(URL, USERNAME, PASSWORD, OLD_INDEX, NEW_INDEX, SEARCH_INDEX)
        x += 1
        print("Success! This is attempt number %s" % x)
    except:
        print("Trying again!")
        sleep(5)
        script()