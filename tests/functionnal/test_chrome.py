"""Functionnal test on Chrome session"""

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.contrib.auth import get_user_model

from selenium import webdriver

from webdriver_manager.chrome import ChromeDriverManager

from product.models import Product
from group.models import Group

# Call chrome options class
chrome_options = webdriver.ChromeOptions()
# Headless mode
chrome_options.add_argument('--headless')
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

        group = Group.objects.create(
            name="La communauté de l'anneau"
        )

        Product.objects.create(
            name='Epée',
            group=group,
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

        self.driver.find_element_by_css_selector('#community-page').click()

        self.driver.find_element_by_css_selector('#join-community').click()

    def test_user_can_leave_a_community(self):
        """Test if user with a Chrome session can leave
        a community"""

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

        self.driver.find_element_by_css_selector('#community-page').click()

        self.driver.find_element_by_css_selector('#join-community').click()

        self.driver.find_element_by_css_selector('#leave-community').click()

    def test_user_can_vote_to_modify_community(self):
        """Test if user with a Chrome session can vote
        to modify a community"""

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

        self.driver.find_element_by_css_selector('#community-page').click()

        self.driver.find_element_by_css_selector('#join-community').click()

        self.driver.find_element_by_css_selector('#collective-decision').click()

        self.driver.find_element_by_css_selector('#vote-to-modify').click()

    def test_user_can_modify_community(self):
        """Test if user with a Chrome session can
        modify a community"""

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

        self.driver.find_element_by_css_selector('#community-page').click()

        self.driver.find_element_by_css_selector('#join-community').click()

        self.driver.find_element_by_css_selector('#collective-decision').click()

        self.driver.find_element_by_css_selector('#vote-to-modify').click()

        self.driver.find_element_by_css_selector('#modify-community').click()

    def test_user_can_vote_to_delete_community(self):
        """Test if user with a Chrome session can vote
        to delete a community"""

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

        self.driver.find_element_by_css_selector('#community-page').click()

        self.driver.find_element_by_css_selector('#join-community').click()

        self.driver.find_element_by_css_selector('#collective-decision').click()

        self.driver.find_element_by_css_selector('#vote-to-delete').click()

    def test_user_can_delete_community(self):
        """Test if user with a Chrome session can
        delete a community"""

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

        self.driver.find_element_by_css_selector('#community-page').click()

        self.driver.find_element_by_css_selector('#join-community').click()

        self.driver.find_element_by_css_selector('#collective-decision').click()

        self.driver.find_element_by_css_selector('#vote-to-delete').click()

    def test_user_can_view_a_product(self):
        """Test if user with a Chrome session can look
        a product"""

        self.driver.get(self.live_server_url)

        self.driver.find_element_by_css_selector('#community-page').click()

        self.driver.find_element_by_name('Epée').click()

    def test_user_can_estimate_a_product_cost(self):
        """Test if user with a Chrome session can estimate
        a product cost"""

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

        self.driver.find_element_by_css_selector('#community-page').click()

        self.driver.find_element_by_css_selector('#join-community').click()

        self.driver.find_element_by_name('Epée').click()

        self.driver.find_element_by_css_selector('#estimation').click()

    def test_user_can_create_community(self):
        """Test if user with a Chrome session can create
        a community"""

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

        self.driver.find_element_by_css_selector('#create-community').click()

    def test_user_can_add_product(self):
        """Test if user with a Chrome session can add
        a product"""

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

        self.driver.find_element_by_css_selector('#community-page').click()

        self.driver.find_element_by_css_selector('#join-community').click()

        self.driver.find_element_by_css_selector('#create-product').click()

        self.driver.find_element_by_name('name').send_keys(
            "Dague"
        )
        self.driver.find_element_by_name('description').send_keys(
            "Une dague de test"
        )

        self.driver.find_element_by_css_selector('#id_group_member').click()

        self.driver.find_element_by_name('cost').send_keys(
            "10"
        )
        self.driver.find_element_by_css_selector('#button-submit').click()

    def test_user_can_delete_product(self):
        """Test if user with a Chrome session can delete
        a product that he added"""

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

        self.driver.find_element_by_css_selector('#community-page').click()

        self.driver.find_element_by_css_selector('#join-community').click()

        self.driver.find_element_by_css_selector('#create-product').click()

        self.driver.find_element_by_name('name').send_keys(
            "Dague"
        )
        self.driver.find_element_by_name('description').send_keys(
            "Une dague de test"
        )

        self.driver.find_element_by_css_selector('#id_group_member').click()

        self.driver.find_element_by_name('cost').send_keys(
            "10"
        )
        self.driver.find_element_by_css_selector('#button-submit').click()

        self.driver.find_element_by_name('Dague').click()

        self.driver.find_element_by_css_selector('#delete-product').click()

    def test_user_can_modify_product(self):
        """Test if user with a Chrome session can modify
        a product"""

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

        self.driver.find_element_by_css_selector('#community-page').click()

        self.driver.find_element_by_css_selector('#join-community').click()

        self.driver.find_element_by_css_selector('#create-product').click()

        self.driver.find_element_by_name('name').send_keys(
            "Dague"
        )
        self.driver.find_element_by_name('description').send_keys(
            "Une dague de test"
        )

        self.driver.find_element_by_css_selector('#id_group_member').click()

        self.driver.find_element_by_name('cost').send_keys(
            "10"
        )
        self.driver.find_element_by_css_selector('#button-submit').click()

        self.driver.find_element_by_name('Dague').click()

        self.driver.find_element_by_css_selector('#modify-product').click()

    def test_user_can_rent_product(self):
        """Test if user with a Chrome session can rent
        a product"""

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

        self.driver.find_element_by_css_selector('#community-page').click()

        self.driver.find_element_by_css_selector('#join-community').click()

        self.driver.find_element_by_css_selector('#create-product').click()

        self.driver.find_element_by_name('name').send_keys(
            "Dague"
        )
        self.driver.find_element_by_name('description').send_keys(
            "Une dague de test"
        )

        self.driver.find_element_by_css_selector('#id_group_member').click()

        self.driver.find_element_by_name('cost').send_keys(
            "10"
        )
        self.driver.find_element_by_css_selector('#button-submit').click()

        self.driver.find_element_by_css_selector('.rent').click()
