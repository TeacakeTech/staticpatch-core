from django.test import TestCase

from staticpatchcore.models import SubSiteModel


class TestModelSubSite(TestCase):

    def test_url_ok(self):
        assert SubSiteModel.normalise_url("/test") == "/test"

    def test_url_with_trailing_slash(self):
        assert SubSiteModel.normalise_url("/test/") == "/test"

    def test_url_without_leading_slash(self):
        assert SubSiteModel.normalise_url("test") == "/test"
