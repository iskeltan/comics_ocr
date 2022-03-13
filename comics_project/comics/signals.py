from django.db.models.signals import post_save
from django.dispatch import receiver
from comics.models import Comic
from comics.tasks import comic_update_or_create


@receiver(post_save, sender=Comic)
def save_or_update_index(sender, **kwargs):
    instance = kwargs["instance"]
    created = kwargs["created"]
    comic_update_or_create.delay(instance.id, created)
