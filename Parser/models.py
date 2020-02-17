from django.db import models

class Group(models.Model):
    link = models.TextField()

    def __str__(self):
        return 'Group link: {0}'.format(self.link)

class Follower(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    fb_id = models.CharField(max_length=25)

    def __str__(self):
        return 'Follower ID: {0}, {1}'.format(self.fb_id, self.group)

