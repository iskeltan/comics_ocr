from django.core.management import BaseCommand

from core.es import bulk_create, exists, delete_indices, create_indice, create_doc_type

from comics.search_indexes import comics_mapping
from comics.models import Comic


class Command(BaseCommand):

    @staticmethod
    def parse_comic(obj):
        data = dict(id=obj.id, content=obj.content.split(), image=obj.image.url,
                    tags=list(obj.tags.values_list("content", flat=True)))
        return data

    def get_comics(self):
        comics = Comic.objects.prefetch_related().all()
        return list(map(self.parse_comic, comics))

    def handle(self, *args, **options):
        if exists():
            delete_indices()

        create_indice()

        cdt_comic = create_doc_type('comic', comics_mapping)
        if cdt_comic.get('acknowledged'):
            print("[+] doctype has been created: comic")

        comics = self.get_comics()
        if comics:
            bulk_create('comic', comics)
            print("[+] {} comics indexed".format(len(comics)))
