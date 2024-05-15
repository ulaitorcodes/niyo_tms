import contextlib

from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class UsersConfig(AppConfig):
    name = "niyo_tms.users"
    verbose_name = _("Users")

    def ready(self):
        with contextlib.suppress(ImportError):
            import niyo_tms.users.signals  # noqa: F401
