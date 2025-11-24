
from django.apps import AppConfig

# This class configures the 'accounts' app for Django.
# It sets the default primary key type and the app name, so Django knows how to handle models in this app.
class AccountsConfig(AppConfig):
    # Use BigAutoField for primary keys by default (good for large databases).
    default_auto_field = 'django.db.models.BigAutoField'
    # The name of this app as used in settings and migrations.
    name = 'accounts'
