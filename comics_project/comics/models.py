from django.db import models
from enum import Enum

from core.models import BaseModel


class TagType(Enum):
    keyword = "keyword"
    author = "author"


class Tag(BaseModel):
    content = models.CharField(max_length=50)
    tag_type = models.CharField(max_length=10,
                                choices=[(tag.value, tag.value) for tag in TagType],
                                default=TagType.keyword.value)

    def __str__(self):
        return "{} - {}".format(self.content, self.tag_type)


class Comic(BaseModel):
    name = models.CharField(max_length=255, null=True, blank=True)
    image = models.ImageField(upload_to="uploads/%Y/%m/%d/")
    tags = models.ManyToManyField(Tag)
    content = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.content[:30] if self.content else self.name


class ComicSource(BaseModel):
    name = models.CharField(max_length=100)
    user_id = models.CharField(max_length=11)
    tags = models.ManyToManyField(Tag, blank=True)

    def __str__(self):
        return "{} - {}".format(self.name, self.user_id)