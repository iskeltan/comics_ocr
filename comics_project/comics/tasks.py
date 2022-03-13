import pytesseract
import requests
from PIL import Image
from urllib.parse import urlparse

from django.core.files import File
from django.core.files.temp import NamedTemporaryFile

from comics.models import Comic, ComicSource
from comics.utils import normalize_content, fetch_instagram_photos
from comics_project.celery import app
from core.es import create


@app.task
def comic_update_or_create(instance_id, created):
    if created:
        comic = Comic.objects.get(id=instance_id)
        image = Image.open(comic.image)
        data = pytesseract.image_to_string(image, lang="tur")
        comic.content = normalize_content(data)
        comic.save()
    else:
        comic_update_or_create_index.delay(instance_id)


@app.task
def comic_update_or_create_index(comic_id):
    instance = Comic.objects.get(id=comic_id)
    doc = {
        "id": instance.id,
        "content": list(set(instance.content.split())),
        "tags": list(instance.tags.values_list("content", flat=True)),
        "image": instance.image.url
    }

    create(doc_type="comic", doc=doc, object_id=instance.id)


@app.task
def save_instagram_photos(source_id):
    source = ComicSource.objects.get(id=source_id)
    for url in fetch_instagram_photos(source.user_id):
        file_name = urlparse(url).path.rsplit("/")[-1]
        img_data = requests.get(url)
        img_temp = NamedTemporaryFile(delete=True)
        img_temp.write(img_data.content)
        img_temp.flush()

        comic = Comic()
        comic.name = "{} - {}".format(source.name, file_name[:30])
        comic.image.save(file_name, File(img_temp), save=True)
        for tag in source.tags.all():
            comic.tags.add(tag)
        comic.save()


@app.task
def get_comics_from_instagram():
    comic_sources = ComicSource.objects.all()
    for source in comic_sources:
        save_instagram_photos.delay(source.id)