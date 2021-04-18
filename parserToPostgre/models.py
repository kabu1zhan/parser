from django.db import models


class Group(models.Model):
    title = models.TextField()
    count = models.IntegerField()
    number = models.IntegerField(unique=True)
    comment_number = models.IntegerField()
    views = models.IntegerField()
    reposts = models.IntegerField()
    likes = models.IntegerField()
    date = models.DateTimeField()
    owner = models.IntegerField()
    domain = models.TextField()
    from_id = models.IntegerField()


class Comments(models.Model):
    number = models.IntegerField(unique=True)
    from_id = models.IntegerField()
    post_id = models.ForeignKey(Group, to_field='number', on_delete=models.CASCADE, related_name='relate_post')
    date = models.DateTimeField()
    text = models.TextField()
    likes = models.IntegerField()
    domain = models.TextField(default="hellyeahplay")


class User(models.Model):
    user_id = models.IntegerField()
    first_name = models.TextField()
    last_name = models.TextField()
    is_closed = models.BooleanField()
    sex = models.CharField(max_length=5)
    nickname = models.TextField()
    domain = models.TextField()
    city = models.TextField()
    county = models.TextField()
    photo = models.TextField()
    status = models.TextField()


class BadWord(models.Model):
    slovo = models.TextField(unique=True)
    varianty = models.JSONField()


class BadData(models.Model):
    number = models.IntegerField(unique=True)
    bad_word = models.TextField()
    text = models.TextField()
    user = models.IntegerField()