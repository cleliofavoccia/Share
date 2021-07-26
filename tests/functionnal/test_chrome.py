"""Functionnal test on Chrome session"""

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.contrib.auth import get_user_model
from django.conf import settings

from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from webdriver_manager.chrome import ChromeDriverManager

from group.models import Group

# Call chrome options class
chrome_options = webdriver.ChromeOptions()
# Headless mode
# chrome_options.add_argument('--headless')
# Navigate in a certain window
chrome_options.add_argument('window-size=1920x1080')


class ChromeFunctionalTestCases(StaticLiveServerTestCase):
    """Functional tests using the Chrome web browser in headless mode."""

    @classmethod
    def setUpClass(cls):
        """Create a Chrome session
        and define his behavior"""
        super().setUpClass()
        cls.driver = webdriver.Chrome(
            ChromeDriverManager().install(),
            options=chrome_options,
        )
        # Wait wait for a certain amount of time
        # before it throws a "No Such Element Exception"
        cls.driver.implicitly_wait(30)
        # Reduces the chances of Selenium scripts
        # missing out on web elements they must interact
        # with during automated tests
        cls.driver.maximize_window()

    @classmethod
    def tearDownClass(cls):
        """Close a Chrome session"""
        super().tearDownClass()
        cls.driver.quit()

    def setUp(self):
        """Create an user"""
        User = get_user_model()
        User.objects.create_user(
            username='Frodon',
            email='frodon@gmail.com',
            password='sam'
        )

        Group.objects.create(
            name="La communauté de l'anneau"
        )

    def test_user_can_connect_and_disconnect(self):
        """Test if user with a Chrome session can connect and
        disconnect to the website"""
        self.driver.get(self.live_server_url)
        # Connect
        self.driver.find_element_by_css_selector('#button-login').click()
        self.driver.find_element_by_name('login').send_keys(
            "frodon@gmail.com"
        )
        self.driver.find_element_by_css_selector('#id_password').send_keys(
            "sam"
        )
        self.driver.find_element_by_css_selector('#button-submit').click()
        # Disconnect
        self.driver.find_element_by_css_selector('#button-logout').click()
        self.driver.find_element_by_css_selector('#button-submit-out').click()
        # Test disconnection
        self.driver.find_element_by_css_selector('#button-login').click()

    def test_user_can_sign_up(self):
        """Test if user with a Chrome session can sign up
         to the website"""
        self.driver.get(self.live_server_url)
        # Sign in
        self.driver.find_element_by_css_selector('#button-login').click()
        self.driver.find_element_by_css_selector('#button-sign_in').click()
        self.driver.find_element_by_name('email').send_keys(
            "sam@gmail.com"
        )
        self.driver.find_element_by_name('password1').send_keys(
            "frodon"
        )
        self.driver.find_element_by_name('password2').send_keys(
            "frodon"
        )
        submit = self.driver.find_element_by_css_selector('#button-submit')

        self.driver.execute_script("arguments[0].click();", submit)
        # Connect
        self.driver.find_element_by_css_selector('#button-login').click()
        self.driver.find_element_by_name('login').send_keys(
            "sam@gmail.com"
        )
        self.driver.find_element_by_css_selector('#id_password').send_keys(
            "frodon"
        )
        self.driver.find_element_by_css_selector('#button-submit').click()
        # Test connection
        self.driver.find_element_by_css_selector('#button-account').click()

    def test_user_can_access_to_his_page_account(self):
        """Test if user with a Chrome session can access
        to his page account"""
        self.driver.get(self.live_server_url)
        # Connect
        self.driver.find_element_by_css_selector('#button-login').click()
        self.driver.find_element_by_name('login').send_keys(
            "frodon@gmail.com"
        )
        self.driver.find_element_by_css_selector('#id_password').send_keys(
            "sam"
        )
        self.driver.find_element_by_css_selector('#button-submit').click()
        self.driver.find_element_by_css_selector('#button-account').click()

    def test_user_can_consult_community_detail(self):
        """Test if user with a Chrome session can consult
        a community page"""

        self.driver.get(self.live_server_url)
        self.driver.find_element_by_css_selector('#community-page').click()

    def test_user_can_join_a_community(self):
        """Test if user with a Chrome session can join
        a community"""

        self.driver.get(self.live_server_url)

        self.driver.find_element_by_css_selector('#join-community').click()

    def test_user_can_leave_a_community(self):
        """Test if user with a Chrome session can join
        a community"""

        self.driver.get(self.live_server_url)

        self.driver.find_element_by_css_selector('#join-community').click()

        self.driver.find_element_by_css_selector('#leave-community').click()
