#!/usr/bin/env python3
"""Test module for GithubOrgClient"""

import unittest
from unittest.mock import patch
from parameterized import parameterized

from client import GithubOrgClient


class TestGithubOrgClient(unittest.TestCase):
    """Unit tests for GithubOrgClient"""

    @parameterized.expand([
        ("google",),
        ("abc",),
    ])
    @patch('client.get_json')
    def test_org(self, org_name, mock_get_json):
        """Test that GithubOrgClient.org returns the correct payload"""

        # Fake payload for the org
        expected_payload = {"org": org_name}
        mock_get_json.return_value = expected_payload

        client = GithubOrgClient(org_name)
        result = client.org

        # Assertions
        mock_get_json.assert_called_once_with(
            f"https://api.github.com/orgs/{org_name}"
        )
        self.assertEqual(result, expected_payload)

    @patch.object(GithubOrgClient, 'org', new_callable=property)
    def test_public_repos_url(self, mock_org):
            """Test _public_repos_url property returns the correct value"""

            # Mocked payload returned by GithubOrgClient.org
            mock_payload = {
                "repos_url": "https://api.github.com/orgs/google/repos"
            }
            mock_org.return_value = mock_payload

            client = GithubOrgClient("google")

            # _public_repos_url should return repos_url from the mocked org data
            result = client._public_repos_url

            self.assertEqual(result, mock_payload["repos_url"])
            mock_org.assert_called_once()




    @patch('client.get_json')
    def test_public_repos(self, mock_get_json):
        """Test public_repos returns the correct list"""

        # Fake JSON returned by get_json()
        mock_payload = [
            {"name": "repo1"},
            {"name": "repo2"},
        ]
        mock_get_json.return_value = mock_payload

        # Fake URL returned by _public_repos_url property
        fake_url = "https://api.github.com/orgs/google/repos"

        with patch.object(GithubOrgClient,
                        '_public_repos_url',
                        new_callable=property,
                        return_value=fake_url):

            client = GithubOrgClient("google")
            result = client.public_repos()

            # Expected repo names extracted from mock_payload
            expected = ["repo1", "repo2"]
            self.assertEqual(result, expected)

            # Ensure get_json() was called once with our fake URL
            mock_get_json.assert_called_once_with(fake_url)


if __name__ == "__main__":
    unittest.main()
