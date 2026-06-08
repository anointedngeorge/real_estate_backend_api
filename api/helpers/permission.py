import yaml
from django.conf import settings





SYSTEM_ROLES = [
            ("admin", "Admin"),
            ("agent", "Agent"),
            ("buyer", "Buyer"),
            ("super_admin", "Super Admin"),
            ("manager", "Manager"),
            ("finance_admin", "Finance Admin"),
            ("sales_admin", "Sales Admin"),
            ("marketing_admin", "Marketing Admin"),
        ]




SYSTEM_PERMISSIONS = [
    ("view_properties", "Can view properties"),
    ("add_properties", "Can add properties"),
    ("edit_properties", "Can edit properties"),
    ("delete_properties", "Can delete properties"),
    ("view_users", "Can view users"),
    ("add_users", "Can add users"),
    ("edit_users", "Can edit users"),
    ("delete_users", "Can delete users"),
    ("view_roles", "Can view roles"),
    ("add_roles", "Can add roles"),
    ("edit_roles", "Can edit roles"),
    ("delete_roles", "Can delete roles"),
    ("view_reports", "Can view reports"),
    ("generate_reports", "Can generate reports"),
    ("manage_settings", "Can manage system settings"),
    ("view_financial_data", "Can view financial data"),
    ("edit_financial_data", "Can edit financial data"),
    ("view_sales_data", "Can view sales data"),
    ("edit_sales_data", "Can edit sales data"),
    ("view_marketing_data", "Can view marketing data"),
    ("edit_marketing_data", "Can edit marketing data"),
    ("manage_permissions", "Can manage user permissions"),
    ("manage_roles", "Can manage user roles"),
    ("view_audit_logs", "Can view audit logs"),
    ("manage_audit_logs", "Can manage audit logs"),
    ("view_system_health", "Can view system health"),
    ("manage_system_health", "Can manage system health"),
    ("view_user_activity", "Can view user activity"),
    ("manage_user_activity", "Can manage user activity"),
    ("view_notifications", "Can view notifications"),
    ("manage_notifications", "Can manage notifications"),
    ("view_support_tickets", "Can view support tickets"),
    ("manage_support_tickets", "Can manage support tickets"),
    ("view_api_usage", "Can view API usage"),
    ("manage_api_usage", "Can manage API usage"),
]



    
with open(settings.BASE_DIR / "api/data/roles.yml") as f:
     ROLE_CONFIG = yaml.safe_load(f)

def get_role_permissions(role: str):
    return ROLE_CONFIG["roles"].get(str(role).lower(), [])