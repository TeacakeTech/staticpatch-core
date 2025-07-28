import random
import string

from django import forms

from .models import (
    BasicAuthUserModel,
    SiteAlternativeDomainModel,
    SiteModel,
    SitePreviewTypeModel,
    SiteSecurityKeyModel,
)


class NewSiteForm(forms.ModelForm):
    class Meta:
        model = SiteModel
        fields = [
            "slug",
            "main_domain",
            "main_domain_ssl",
            "basic_auth_user_required",
            "allow_override",
            "access_file_name",
            "public_info",
            "public_info_url",
            "active",
            "notes",
        ]
        widgets = {
            "notes": forms.Textarea(attrs={"rows": 4}),
        }


class NewSiteSecurityKeyForm(forms.ModelForm):
    class Meta:
        model = SiteSecurityKeyModel
        fields = ["active", "notes"]
        widgets = {
            "notes": forms.Textarea(attrs={"rows": 4}),
        }

    def save(self, commit=True):
        instance = super().save(commit=False)
        # Generate a random key between 100-200 characters
        length = random.randint(100, 200)
        chars = string.ascii_letters + string.digits
        instance.key = "".join(random.choice(chars) for _ in range(length))
        if commit:
            instance.save()
        return instance


class NewSitePreviewTypeForm(forms.ModelForm):
    class Meta:
        model = SitePreviewTypeModel
        fields = [
            "slug",
            "domain",
            "domain_ssl",
            "basic_auth_user_required",
            "active",
            "notes",
        ]


class NewBasicAuthUserForm(forms.ModelForm):
    class Meta:
        model = BasicAuthUserModel
        fields = ["username", "password_crypted", "active", "notes"]
        widgets = {
            "password_crypted": forms.PasswordInput(),
            "notes": forms.Textarea(attrs={"rows": 4}),
        }


class NewSiteAlternativeDomainForm(forms.ModelForm):
    class Meta:
        model = SiteAlternativeDomainModel
        fields = ["domain", "domain_ssl", "active", "notes"]
        widgets = {
            "notes": forms.Textarea(attrs={"rows": 4}),
        }


class EditSiteAlternativeDomainForm(forms.ModelForm):
    class Meta:
        model = SiteAlternativeDomainModel
        fields = ["domain", "domain_ssl", "active", "notes"]
        widgets = {
            "notes": forms.Textarea(attrs={"rows": 4}),
        }


class EditSiteForm(forms.ModelForm):
    class Meta:
        model = SiteModel
        fields = [
            "main_domain",
            "main_domain_ssl",
            "basic_auth_user_required",
            "allow_override",
            "access_file_name",
            "public_info",
            "public_info_url",
            "active",
            "notes",
        ]
        widgets = {
            "notes": forms.Textarea(attrs={"rows": 4}),
        }


class EditSitePreviewTypeForm(forms.ModelForm):
    class Meta:
        model = SitePreviewTypeModel
        fields = ["domain", "domain_ssl", "basic_auth_user_required", "active", "notes"]
        widgets = {
            "notes": forms.Textarea(attrs={"rows": 4}),
        }
