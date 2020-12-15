import click
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.wait import WebDriverWait

NETFLIX_URL = "https://www.netflix.com/"


def get_driver():
    """ Get an instance of headless driver """

    # Disable selenium logging and make browser headless
    chrome_options = webdriver.ChromeOptions()
    chrome_options.headless = True
    chrome_options.add_argument("--log-level=3")
    chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
    driver = webdriver.Chrome(options=chrome_options)
    driver = webdriver.Chrome()

    return driver


def login(email, password):
    """ Tries to log in and return the Logged In driver """

    click.echo("Trying to log in...")

    driver = get_driver()

    driver.get(NETFLIX_URL + 'login')
    login_input = driver.find_element_by_name("userLoginId")
    password_input = driver.find_element_by_name("password")
    remember_checkbox = driver.find_element_by_css_selector("label[data-uia=\"label+rememberMe\"]")
    login_button = driver.find_element_by_class_name("login-button")

    login_input.send_keys(email)
    password_input.send_keys(password)
    remember_checkbox.click()
    login_button.click()

    # Check whether we have logged in
    try:
        result = WebDriverWait(driver, 10).until(
            lambda x: x.find_element_by_class_name("profile-gate-label")
        )

        print("Successfully logged in.")

        return driver

    except TimeoutException as e:
        print("Invalid login/password. Please check your credentials and try again.")
        driver.quit()


def get_logged_in_driver_clone(driver):
    """ Returns a Logged In clone of driver using cookies """

    driver_clone = get_driver()
    driver_clone.get(NETFLIX_URL)
    cookies = driver.get_cookies()

    for cookie in cookies:
        driver_clone.add_cookie(cookie)

    driver_clone.refresh()

    return driver_clone


def get_profiles(logged_in_driver):
    profile_divs = logged_in_driver.find_elements_by_class_name("profile-link")
    profiles = {}
    for profile_div in profile_divs:
        name = profile_div.find_element_by_class_name("profile-name").get_attribute("innerHTML")
        uid = profile_div.find_element_by_class_name("profile-icon").get_attribute("data-profile-guid")
        profiles[name] = uid

    return profiles


@click.command()
@click.option('--email', help='Email to your Netflix account.', prompt='Your Email')
@click.option('--password', help='Password to your Netflix account.', prompt='Your Password', hide_input=True)
@click.option('-p',
              help='Profile that you want to process '
                   '(you can specify more accounts by '
                   'reusing this flag).',
              multiple=True)
@click.option('--action',
              help='What action do you want to perform: '
                   'import (upload data to Netflix) or '
                   'export download data from Netflix)',
              type=click.Choice(['import', 'export']))
def main(email, password, p, action):
    logged_in_driver = login(email, password)
    profiles = get_profiles(logged_in_driver)
    print(f"Found {len(profiles.keys)} profiles: {', '.join(profiles.keys)}.")


    if action == 'export':
        print(f"Exporting following profiles: {', '.join(p)}")
        clone = get_logged_in_driver_clone(logged_in_driver)


if __name__ == "__main__":
    main()
