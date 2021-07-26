"""Tests of group_member django forms"""

from django.test import TestCase

from user.models import User
from group.models import Group

from ..models import Product
from ..forms import ProductSuppressionForm


class ProductSuppressionFormTest(TestCase):
    """Tests on ProductSuppressionForm"""
    @classmethod
    def setUp(cls):
        """Set up a context to test ProductSuppressionForm object"""
        cls.user = User.objects.create_user(
            username='Frodon',
            email='frodon@gmail.com',
            password='sam'
        )
        cls.group = Group.objects.create(name="La communauté de l'anneau")

        cls.product = Product.objects.create(
            name='Epée',
            group=cls.group,
        )

        cls.cleaned_data = {
            'product_to_delete': None,
            'group': None
        }

    def test_form_work_with_existant_datas(self):
        """Test ProductSuppressionForm work with existant Group,
        and Product instance"""

        group = Group.objects.get(name="La communauté de l'anneau")
        product = Product.objects.get(name='Epée')

        form = ProductSuppressionForm(data={
            'product_to_delete': product.id,
            'group': group.id,
        })
        self.assertTrue(form.is_valid())

    def test_form_doesnt_work_with_unexistant_datas(self):
        """Test GroupMemberInscriptionForm doesn't work with unexistant datas
        or existant and unexistant datas. Datas are User and
        Group instance"""

        product = Product.objects.get(name='Epée')
        try:
            group = Group.objects.get(name="Mordor")
        except Group.DoesNotExist:
            group = {'name': 'Mordor', 'id': '3'}

        form = ProductSuppressionForm(data={
            'product_to_delete': product.id,
            'group': int(group['id'])
        })
        self.assertFalse(form.is_valid())

        try:
            product = Product.objects.get(name='Dague')
        except Product.DoesNotExist:
            product = {'name': 'dague', 'id': '1'}
        try:
            group = Group.objects.get(name="Mordor")
        except Group.DoesNotExist:
            group = {'name': 'Mordor', 'id': '3'}

        form = ProductSuppressionForm(data={
            'product_to_delete': product['id'],
            'group': int(group['id'])
        })
        self.assertFalse(form.is_valid())

        try:
            product = Product.objects.get(name='Dague')
        except Product.DoesNotExist:
            product = {'name': 'Dague', 'id': '1'}
        group = Group.objects.get(name="La communauté de l'anneau")

        form = ProductSuppressionForm(data={
            'product_to_delete': product['id'],
            'group': group.id
        })
        self.assertFalse(form.is_valid())

    def test_form_delete_product_objects(self):
        """Test ProductSuppressionForm return
        and delete Product object"""
        user = User.objects.get(username='Frodon')

        self.client.force_login(user)

        product = Product.objects.get(name='Epée')
        group = Group.objects.get(name="La communauté de l'anneau")

        data = {
            'product_to_delete': product.id,
            'group': group.id
        }

        form = ProductSuppressionForm(data=data)
        form.is_valid()

        form.delete()

        try:
            product = Product.objects.get(name='Epée')
        except Product.DoesNotExist:
            product = 'DoesNotExist'

        self.assertEqual(product, 'DoesNotExist')

    def test_clean_product_to_delete(self):
        """Test ProductSuppressionForm verify if User
        input by user exist and is valid"""

        product = Product.objects.get(name='Epée')
        self.cleaned_data['product_to_delete'] = product.id
        self.assertEqual(
            product,
            ProductSuppressionForm.clean_product_to_delete(self)
        )

    def test_clean_group(self):
        """Test GroupMemberVoteForm verify if Group
        input by user exist and is valid"""

        group = Group.objects.get(name="La communauté de l'anneau")
        self.cleaned_data['group'] = group.id
        self.assertEqual(group, ProductSuppressionForm.clean_group(self))
