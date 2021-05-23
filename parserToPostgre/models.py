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
    post_id = models.ForeignKey(Group, to_field='number', on_delete=models.CASCADE, related_name='relate_post', null=True)
    post_base = models.IntegerField(null=True, blank=True)
    date = models.DateTimeField()
    text = models.TextField()
    likes = models.IntegerField()
    domain = models.TextField(default="hellyeahplay")


class User(models.Model):
    user_id = models.IntegerField(unique=True)
    first_name = models.TextField()
    last_name = models.TextField()
    is_closed = models.BooleanField()
    sex = models.CharField(max_length=5)
    nickname = models.TextField(null=True, blank=True)
    domain = models.TextField(null=True, blank=True)
    city = models.TextField(null=True, blank=True)
    county = models.TextField(null=True, blank=True)
    photo = models.TextField(null=True, blank=True)
    status = models.TextField(null=True, blank=True)
    checked = models.BooleanField()


class GroupListUser(models.Model):
    user = models.ForeignKey(User, to_field='user_id', on_delete=models.CASCADE, unique=True)
    group = models.TextField()


class BadWord(models.Model):
    slovo = models.TextField(unique=True)
    varianty = models.TextField()


class BadData(models.Model):
    number = models.IntegerField(unique=True)
    bad_word = models.TextField()
    text = models.TextField()
    user = models.IntegerField()