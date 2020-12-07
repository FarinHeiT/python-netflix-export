import click
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.wait import WebDriverWait

NETFLIX_URL = "https://www.netflix.com/"

# Disable selenium logging and make browser headless
chrome_options = webdriver.ChromeOptions()
chrome_options.headless = True
chrome_options.add_argument("--log-level=3")
chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
driver = webdriver.Chrome(options=chrome_options)


@click.command()
@click.option('--email', help='Email to your Netflix account.', prompt='Your Email')
@click.option('--password', help='Password to your Netflix account.', prompt='Your Password', hide_input=True)
def login(email, password):
    click.echo("Trying to log in...")
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

    except TimeoutException as e:
        print("Invalid login/passowrd. Please check your credentials and try again.")
        driver.quit()


if __name__ == "__main__":
    login()
