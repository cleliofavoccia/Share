# """Tests of utilites method"""
#
# from django.test import TestCase
#
# from group_member.models import GroupMember
# from group.models import Group
# from user.models import User
# from product.models import Product
# from collective_decision.models import Estimation
#
# from point_provider.utils import update_communities_informations
#
#
# class UtilsTest(TestCase):
#     """Test on utilities method"""
#
#     @classmethod
#     def setUp(cls):
#         """Set up a context to test utilities method"""
#         cls.user1 = User.objects.create_user(
#             username='Frodon',
#             email='frodon@gmail.com',
#             password='sam'
#         )
#         cls.user2 = User.objects.create_user(
#             username='Sam',
#             email='sam@gmail.com',
#             password='frodon'
#         )
#         cls.group1 = Group.objects.create(name="La communauté de l'anneau")
#         cls.group2 = Group.objects.create(name="Mordor")
#
#         cls.group1_member1 = GroupMember.objects.create(
#             user=cls.user1,
#             group=cls.group1
#         )
#         cls.group2_member = GroupMember.objects.create(
#             user=cls.user1,
#             group=cls.group2
#         )
#
#         cls.group1_member2 = GroupMember.objects.create(
#             user=cls.user2,
#             group=cls.group1
#         )
#
#         cls.product1 = Product.objects.create(
#             name='Epée',
#             user_provider=cls.group1_member1,
#             group=cls.group1
#         )
#
#         cls.group1_member1_estimate_product1 = (
#             Estimation.objects.create(
#                 cost=10,
#                 group_member=cls.group1_member1,
#                 product=cls.product1)
#         )
#         cls.group1_member2_estimate_product1 = (
#             Estimation.objects.create(
#                 cost=30,
#                 group_member=cls.group1_member2,
#                 product=cls.product1)
#         )
#
#     def test_update_communities_information_return_good_product_cost(self):
#         update_communities_informations()
#
#         product = self.product1
#         product_cost = (
#             (
#                     self.group1_member1_estimate_product1.cost +
#                     self.group1_member2_estimate_product1.cost
#             )
#             // 2)
#         self.assertEqual(product.points, product_cost)
