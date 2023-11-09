from django.db import models


class Articlemetadata(models.Model):
    article = models.ForeignKey('Articles', models.DO_NOTHING, blank=True, null=True)
    categories = models.TextField(blank=True, null=True)
    image_url = models.TextField(blank=True, null=True)
    engagement_data = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ArticleMetadata'


class Articles(models.Model):
    id = models.CharField(primary_key=True, max_length=255)
    title = models.TextField()
    content = models.TextField(blank=True, null=True)
    published_date = models.DateTimeField(blank=True, null=True)
    author = models.CharField(max_length=255, blank=True, null=True)
    url = models.TextField()
    source = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Articles'


class Summaries(models.Model):
    id = models.IntegerField(primary_key=True)
    article = models.ForeignKey(Articles, models.DO_NOTHING, blank=True, null=True)
    summary = models.TextField(blank=True, null=True)
    is_bad = models.IntegerField(blank=True, null=True)
    generated_date = models.DateField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Summaries'
