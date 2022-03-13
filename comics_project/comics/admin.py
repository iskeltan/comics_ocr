from django.contrib import admin

from comics.models import Comic, Tag, ComicSource

admin.site.register(Comic)
admin.site.register(Tag)
admin.site.register(ComicSource)