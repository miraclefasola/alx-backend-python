#!/usr/bin/env python3
"""Test module for GithubOrgClient"""

import unittest
from unittest.mock import patch
from parameterized import parameterized
from unittest.mock import PropertyMock
from client import GithubOrgClient


class TestGithubOrgClient(unittest.TestCase):
    """Unit tests for GithubOrgClient"""

    @parameterized.expand(
        [
            ("google",),
            ("abc",),
        ]
    )
    @patch("client.get_json")
    def test_org(self, org_name, mock_get_json):
        """Test that GithubOrgClient.org returns the correct payload"""

        # Fake payload for the org
        expected_payload = {"org": org_name}
        mock_get_json.return_value = expected_payload

        client = GithubOrgClient(org_name)
        result = client.org

        # Assertions
        link = f"https://api.github.com/orgs/{org_name}"
        mock_get_json.assert_called_once_with(link)
        self.assertEqual(result, expected_payload)

    @patch.object(GithubOrgClient, "org", new_callable=property)
    def test_public_repos_url(self, mock_org):
        """Test _public_repos_url property returns the correct value"""

        # Mocked payload returned by GithubOrgClient.org
        pload = {"repos_url": "https://api.github.com/orgs/google/repos"}
        mock_payload = pload
        mock_org.return_value = mock_payload

        client = GithubOrgClient("google")

        # _public_repos_url should return repos_url from the mocked org data
        result = client._public_repos_url

        self.assertEqual(result, mock_payload["repos_url"])
        mock_org.assert_called_once()

    @patch("client.get_json")
    def test_public_repos(self, mock_json):
        """
        this method unit-test GithubOrgClient.public_repos
        """
        payload = [{"name": "Google"}, {"name": "Twitter"}]
        mock_json.return_value = payload

        with patch(
            "client.GithubOrgClient._public_repos_url", new_callable=PropertyMock
        ) as mock_public:

            mock_public.return_value = "hello world"
            test_class = GithubOrgClient("test")
            result = test_class.public_repos()

            expected = [item["name"] for item in payload]
            self.assertEqual(result, expected)

            mock_public.assert_called_once()
            mock_json.assert_called_once()

    @parameterized.expand(
        [
            ({"license": {"key": "my_license"}}, "my_license", True),
            ({"license": {"key": "other_license"}}, "my_license", False),
        ]
    )

if __name__ == "__main__":
    unittest.main()
