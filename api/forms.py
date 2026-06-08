# forms.py

from django import forms
from api.models import UserRole, RolePermission

class UserRoleAdminForm(forms.ModelForm):
    class Meta:
        model = UserRole
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if self.instance and self.instance.pk:
            role = self.instance.role

            self.fields["permissions"].queryset = (
                RolePermission.objects.filter(role=role).first().permissions.all()
            )