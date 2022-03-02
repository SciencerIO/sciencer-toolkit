from unittest import TestCase
from sciencer.policies import HasPolicy, Policy
from typing import List


class Fake_Policy_Holder(HasPolicy):
    def __init__(self, policies: List[Policy]) -> None:
        super().__init__(policies)


class TestPolicy(TestCase):
    def test_get_policy(self):
        policy_holder = Fake_Policy_Holder([Policy.BY_AUTHOR])

        resulting_policies = policy_holder.available_policies

        self.assertEqual(len(resulting_policies), 1)
        self.assertIn(Policy.BY_AUTHOR, resulting_policies)
