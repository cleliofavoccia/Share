"""Tests of product django views"""

from django.test import TestCase
from django.urls import reverse

from group.models import Group
from group_member.models import GroupMember
from user.models import User

from ..models import Product


class ProductDetailViewTest(TestCase):
    """Tests on ProductDetailView generic detail view"""

    @classmethod
    def setUp(cls):
        """Set up a context to test ProductDetailView
         generic detail view"""
        cls.user = User.objects.create_user(
            username='Frodon',
            email='frodon@gmail.com',
            password='sam'
        )

        cls.group = Group.objects.create(name="La communauté de l'anneau")

        cls.group_member = GroupMember.objects.create(
            user=cls.user,
            group=cls.group
        )

        cls.product = Product.objects.create(
            name='Epée',
            user_provider=cls.group_member,
            tenant=cls.group_member,
            group=cls.group,
        )

    def test_login_user_dont_see_same_things_if_not_group_member(self):
        """Test user see some different informations about community
        from a product page if not group_member"""

        user = User.objects.get(username='Frodon')
        self.client.force_login(user)
        group = Group.objects.get(name="La communauté de l'anneau")
        product = Product.objects.get(name='Epée')

        group_member_list = list()
        group_member = GroupMember.objects.filter(
            user=user,
            group=group
        )

        # Add communities in which user has suscribed in a list
        # that added to context to verify if user is in a displayed
        # community
        for community_inscription in group_member:
            group_member_list.append(community_inscription.group.name)

        response = self.client.get(
            reverse("product:product", args=[product.pk])
        )
        self.assertEqual(
            group_member_list,
            response.context['group_member_list']
        )

    def test_view_url_accessible_by_name(self):
        """Test view can accessible by ProductDetailView
        generic detail view's name"""

        product = Product.objects.get(name='Epée')

        response = self.client.get(
            reverse('product:product', args=[product.pk])
        )
        # Check that we got a response "success"
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        """Test ProductDetailView use the correct template"""
        product = Product.objects.get(name='Epée')

        response = self.client.get(
            reverse('product:product', args=[product.pk])
        )

        self.assertTemplateUsed(response, 'product/product_detail.html')


class MySuppliedProductsListViewTest(TestCase):
    """Tests on MySuppliedProductsListView generic list view"""

    @classmethod
    def setUp(cls):
        """Set up a context to test MySuppliedProductsListView
         generic detail view"""
        cls.user = User.objects.create_user(
            username='Frodon',
            email='frodon@gmail.com',
            password='sam'
        )

        cls.user2 = User.objects.create_user(
            username='Sam',
            email='sam@gmail.com',
            password='frodon'
        )

        cls.group = Group.objects.create(name="La communauté de l'anneau")

        cls.group_member = GroupMember.objects.create(
            user=cls.user,
            group=cls.group
        )

        cls.product = Product.objects.create(
            name='Epée',
            user_provider=cls.group_member,
            tenant=cls.group_member,
            group=cls.group,
        )

    def test_redirect_if_not_logged_in(self):
        """Test user can't access to MySuppliedProductsListView
        generic list view and it is redirect to login form"""

        response = self.client.get(
            reverse('product:supplied_products')
        )

        self.assertRedirects(
            response,
            f'{reverse("account_login")}'
            f'?next={reverse("product:supplied_products")}'
        )

    def test_login_user_dont_see_products_if_dont_provide_product(self):
        """Test user don't see any products if he don't provide anything"""

        user = User.objects.get(username='Sam')
        self.client.force_login(user)

        response = self.client.get(
            reverse('product:supplied_products')
        )

        self.assertFalse(response.context['supplied_products'])

    def test_login_user_see_products_if_provide_product(self):
        """Test user see his products if he provide it"""

        user = User.objects.get(username='Frodon')
        group = Group.objects.get(name="La communauté de l'anneau")
        group_member = GroupMember.objects.get(
            user=user,
            group=group
        )
        self.client.force_login(user)

        product_provide = Product.objects.get(user_provider=group_member)

        response = self.client.get(
            reverse('product:supplied_products')
        )

        self.assertTrue(response.context['supplied_products'])
        self.assertEqual(
            response.context['supplied_products'][0],
            product_provide
        )

    def test_view_url_accessible_by_name(self):
        """Test view can accessible by MySuppliedProductsListView
        generic list view's name"""

        user = User.objects.get(username='Frodon')

        self.client.force_login(user)

        response = self.client.get(
            reverse('product:supplied_products')
        )

        # Check that we got a response "success"
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        """Test MySuppliedProductsListView use the correct template"""

        user = User.objects.get(username='Frodon')

        self.client.force_login(user)

        response = self.client.get(
            reverse('product:supplied_products')
        )

        self.assertTemplateUsed(response, 'product/supplied_products.html')


class MyRentedProductsListViewTest(TestCase):
    """Tests on MyRentedProductsListView generic list view"""

    @classmethod
    def setUp(cls):
        """Set up a context to test MyRentedProductsListView
         generic detail view"""
        cls.user = User.objects.create_user(
            username='Frodon',
            email='frodon@gmail.com',
            password='sam'
        )

        cls.user2 = User.objects.create_user(
            username='Sam',
            email='sam@gmail.com',
            password='frodon'
        )

        cls.group = Group.objects.create(name="La communauté de l'anneau")

        cls.group_member = GroupMember.objects.create(
            user=cls.user,
            group=cls.group
        )

        cls.product = Product.objects.create(
            name='Epée',
            user_provider=cls.group_member,
            tenant=cls.group_member,
            group=cls.group,
        )

    def test_redirect_if_not_logged_in(self):
        """Test user can't access to MyRentedProductsListView
        generic list view and it is redirect to login form"""

        response = self.client.get(
            reverse('product:rented_products')
        )

        self.assertRedirects(
            response,
            f'{reverse("account_login")}'
            f'?next={reverse("product:rented_products")}'
        )

    def test_login_user_dont_see_products_if_dont_rent_product(self):
        """Test user don't see any products if he don't rent anything"""

        user = User.objects.get(username='Sam')
        self.client.force_login(user)

        response = self.client.get(
            reverse('product:rented_products')
        )

        self.assertFalse(response.context['rented_products'])

    def test_login_user_see_products_if_rent_product(self):
        """Test user see his products if he rent it"""

        user = User.objects.get(username='Frodon')
        group = Group.objects.get(name="La communauté de l'anneau")
        group_member = GroupMember.objects.get(
            user=user,
            group=group
        )
        self.client.force_login(user)

        product_provide = Product.objects.get(user_provider=group_member)

        response = self.client.get(
            reverse('product:rented_products')
        )

        self.assertTrue(response.context['rented_products'])
        self.assertEqual(
            response.context['rented_products'][0],
            product_provide
        )

    def test_view_url_accessible_by_name(self):
        """Test view can accessible by MyRentedProductsListView
        generic list view's name"""

        user = User.objects.get(username='Frodon')

        self.client.force_login(user)

        response = self.client.get(
            reverse('product:rented_products')
        )

        # Check that we got a response "success"
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        """Test MyRentedProductsListView use the correct template"""

        user = User.objects.get(username='Frodon')

        self.client.force_login(user)

        response = self.client.get(
            reverse('product:rented_products')
        )

        self.assertTemplateUsed(response, 'product/rented_products.html')


class ProductInscriptionViewTest(TestCase):
    """Tests on ProductInscriptionView generic view"""
    @classmethod
    def setUp(cls):
        """Set up a context to test ProductInscriptionView generic view"""

        cls.user = User.objects.create_user(
            username='Frodon',
            email='frodon@gmail.com',
            password='sam'
        )
        cls.group = Group.objects.create(name="La communauté de l'anneau")
        cls.group_member = GroupMember.objects.create(
            user=cls.user,
            group=cls.group
        )

    def test_redirect_if_not_logged_in(self):
        """Test user can't access to ProductInscriptionView generic view
         and it is redirect to login form"""

        group = Group.objects.get(name="La communauté de l'anneau")

        response = self.client.get(
            reverse('product:add_product', args=[group.pk])
        )
        self.assertRedirects(
            response,
            f'{reverse("account_login")}'
            f'?next={reverse("product:add_product", args=[group.pk])}'
        )

    def test_view_url_accessible_by_name(self):
        """Test view can accessible by
        ProductInscriptionView generic view's name"""

        user = User.objects.get(username='Frodon')
        self.client.force_login(user)
        group = Group.objects.get(name="La communauté de l'anneau")

        get_response = self.client.get(
            reverse('product:add_product', args=[group.pk]),
        )

        post_response = self.client.post(
            reverse('product:add_product', args=[group.pk]),
            data={
                'csrfmiddlewaretoken':
                    ['2NFhGPdsobAfUWtJZFxBnkUL7uSdSe5hj'
                     '17l20tZbFZaLtxaTbx9NbKaZDfwTMfU'],
                'name': ['claymore'],
                'image': [''],
                'description': ['claymore pas terrible'],
                'cost': ['25']
            }
        )

        # Check that we got a response "success"
        self.assertEqual(get_response.status_code, 200)
        self.assertEqual(post_response.status_code, 302)

    def test_view_verify_datas_with_form(self):
        """Test GroupInscriptionView generic view
        verify datas correctly"""

        self.client.force_login(self.user)
        group = Group.objects.get(name="La communauté de l'anneau")

        true_request = {
                'csrfmiddlewaretoken':
                ['2NFhGPdsobAfUWtJZFxBnkUL7uSdSe5hj'
                    '17l20tZbFZaLtxaTbx9NbKaZDfwTMfU'],
                'name': ['claymore'],
                'image': [''],
                'description': ['claymore pas terrible'],
                'cost': ['25']
            }
        true_response = self.client.post(
            reverse('product:add_product', args=[group.pk]),
            data=true_request
        )

        self.assertRedirects(
            true_response,
            reverse('group:community', args=[group.pk])
        )

        false_request = {
            'group_member': ['1'],
            'group': ['Y']
                        }
        false_response = self.client.post(
            reverse('product:add_product', args=[group.pk]),
            data=false_request
        )

        self.assertEqual(
            false_response.status_code,
            200
        )


class ProductSuppressionViewTest(TestCase):
    """Tests on ProductInscriptionView generic view"""
    @classmethod
    def setUp(cls):
        """Set up a context to test ProductInscriptionView generic view"""

        cls.user = User.objects.create_user(
            username='Frodon',
            email='frodon@gmail.com',
            password='sam'
        )
        cls.group = Group.objects.create(name="La communauté de l'anneau")
        cls.group_member = GroupMember.objects.create(
            user=cls.user,
            group=cls.group
        )

        cls.product = Product.objects.create(
            name='Epée',
            user_provider=cls.group_member,
            tenant=cls.group_member,
            group=cls.group,
        )

    def test_redirect_if_not_logged_in(self):
        """Test user can't access to ProductInscriptionView generic view
         and it is redirect to login form"""

        response = self.client.get(
            reverse('product:delete_product')
        )
        self.assertRedirects(
            response,
            f'{reverse("account_login")}'
            f'?next={reverse("product:delete_product")}'
        )

    def test_view_url_accessible_by_name(self):
        """Test view can accessible by
        ProductInscriptionView generic view's name"""

        user = User.objects.get(username='Frodon')
        group = Group.objects.get(name="La communauté de l'anneau")
        product = Product.objects.get(name='Epée')

        self.client.force_login(user)

        response = self.client.post(
            reverse('product:delete_product'),
            data={
                'csrfmiddlewaretoken':
                    ['CRzyY84t1qcw7QkDzKQ9NKkjopJecxvC3ncK44'
                     'gH1Ku7BzCUE0aJ1twhklZ57lQo'],
                'product_to_delete': [f'{product.pk}'],
                'group': [f'{group.pk}']
            }
        )

        # Check that we got a response "success"
        self.assertEqual(response.status_code, 302)

    def test_view_verify_datas_with_form(self):
        """Test ProductInscriptionView generic view
        verify datas correctly"""

        user = User.objects.get(username='Frodon')
        group = Group.objects.get(name="La communauté de l'anneau")
        product = Product.objects.get(name='Epée')

        self.client.force_login(user)

        true_request = {
                'csrfmiddlewaretoken':
                    ['CRzyY84t1qcw7QkDzKQ9NKkjopJecxvC3ncK44'
                     'gH1Ku7BzCUE0aJ1twhklZ57lQo'],
                'product_to_delete': [f'{product.pk}'],
                'group': [f'{group.pk}']
            }
        true_response = self.client.post(
            reverse('product:delete_product'),
            data=true_request
        )

        self.assertRedirects(
            true_response,
            reverse('group:community', args=[group.pk])
        )

        false_request = {
            'group_member': ['1'],
            'group': ['Y']
                        }
        false_response = self.client.post(
            reverse('product:delete_product'),
            data=false_request
        )

        self.assertRedirects(
            false_response,
            reverse('website:fail')
        )
