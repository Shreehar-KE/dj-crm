from django.db import models
from apps.contacts.models import Contact


class Note(models.Model):
    title = models.CharField(max_length=200)
    note = models.TextField()
    contact = models.ForeignKey(Contact, on_delete=models.CASCADE)
    # user = models.ManyToManyField()
    date_time_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-date_time',)

    def __str__(self):
        return self.title

    def get_contact_id(self):
        return self.contact.id

    def is_contact_deleted(self):
        return self.contact.is_deleted

    # def get_user(self):
    #     return self.user
