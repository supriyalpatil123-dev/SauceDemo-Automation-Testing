
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait


class LoginPage:
    def __init__(self, driver):
        self.driver = driver

        self.usernameInput = (By.ID, "user-name")
        self.passwordInput = (By.ID, "password")
        self.loginButton = (By.ID, "login-button")

        # Hide demo credentials on login page
        self.hide_suggestions()

    def hide_suggestions(self):
        WebDriverWait(self.driver, 10).until(
            lambda d: d.find_elements(By.ID, "login-button")
        )

        self.driver.execute_script("""
            document.querySelectorAll(
                '.login_credentials_wrap, .login_credentials, .login_password'
            ).forEach(element => {
                element.style.display = 'none';
            });
        """)

    def enter_username(self, username):
        self.driver.find_element(
            *self.usernameInput
        ).send_keys(username)

    def enter_password(self, password):
        self.driver.find_element(
            *self.passwordInput
        ).send_keys(password)

    def click_login(self):
        self.driver.find_element(
            *self.loginButton
        ).click()
