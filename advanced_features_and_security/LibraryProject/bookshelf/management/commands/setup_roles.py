from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from bookshelf.models import Book

class Command(BaseCommand):
    help = "Create Viewers, Editors, Admins groups and assign custom Book permissions."

    def handle(self, *args, **kwargs):
        ct = ContentType.objects.get_for_model(Book)
        perm_map = {
            "can_view": "Can view book",
            "can_create": "Can create book",
            "can_edit": "Can edit book",
            "can_delete": "Can delete book",
        }
        perms = {}
        for codename, name in perm_map.items():
            perm, _ = Permission.objects.get_or_create(
                codename=codename,
                content_type=ct,
                defaults={"name": name},
            )
            perms[codename] = perm

        viewers, _ = Group.objects.get_or_create(name="Viewers")
        editors, _ = Group.objects.get_or_create(name="Editors")
        admins, _ = Group.objects.get_or_create(name="Admins")

        viewers.permissions.set([perms["can_view"]])
        editors.permissions.set([perms["can_view"], perms["can_create"], perms["can_edit"]])
        admins.permissions.set([perms["can_view"], perms["can_create"], perms["can_edit"], perms["can_delete"]])

        self.stdout.write(self.style.SUCCESS("Groups created and permissions assigned."))