from django.db import models
from django.urls import reverse
from django.conf import settings

from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    pass

class Project(models.Model):
    # pid=models.CharField(unique=True,max_length=30)
    title=models.CharField(max_length=300)
    type=models.CharField(max_length=200,blank=True)
    # user=models.ManyToManyField(User,related_name='project')
    created_by=models.CharField(max_length=300,blank=True)

    class Meta:
        default_permissions = ('add',)
        permissions = (
        ('can_view', 'Can view the projects'),)


    def __str__(self):
        return self.title

    def get_absolute_url_detail(self):
        return reverse("client_portal:detail", kwargs={"pk": self.pk})

    def get_absolute_url_update(self):
        return reverse("client_portal:update", kwargs={"pk": self.pk})

    def get_absolute_url_delete(self):
        return reverse("client_portal:delete", kwargs={"pk": self.pk})
    def get_absolute_url_create(self):
        return reverse("client_portal:index", kwargs={"pk": self.pk})

    def get_absolute_url_create(self):
        return reverse("client_portal:member-create", kwargs={"pk": self.pk})






class Member(models.Model):
    address=models.CharField(max_length=200)
    description=models.CharField(max_length=400)
    created_on=models.DateTimeField(auto_now_add=True)
    active=models.BooleanField(default=False)
    user=models.OneToOneField(settings.AUTH_USER_MODEL,related_name='members_user',on_delete=models.CASCADE,null=True,blank=True)
    project=models.ManyToManyField(Project)

    def get_absolute_url_detail(self):
        return reverse("client_portal:memdetail", kwargs={"pk": self.pk})

    def get_absolute_url_update(self):
        return reverse("client_portal:memupdate", kwargs={"pk": self.pk})

    def get_absolute_url_delete(self):
        return reverse("client_portal:memdelete", kwargs={"pk": self.pk})



class Comments(models.Model):
    member = models.ForeignKey(User,related_name='comments', on_delete=models.CASCADE, null=True, blank=True)
    title = models.TextField()
    group = models.ForeignKey('CommentsGroups', on_delete=models.CASCADE, null=True, blank=True)
    created_on = models.DateTimeField(auto_now=True)
    updated_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Reply(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comments = models.ForeignKey(Comments, on_delete=models.CASCADE)
    reply_text = models.TextField()
    is_anonymous = models.BooleanField(default=False)

    # def __str__(self):
    #     return self.


class CommentsGroups(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


