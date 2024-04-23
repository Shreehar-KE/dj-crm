from django.db import models
from apps.contacts.models import Contact


class Log(models.Model):
    class Activites(models.TextChoices):
        CREATE_CONTACT = 'CREATE_CONTACT', 'create_contact'
        UPDATE_CONTACT = 'UPDATE_CONTACT', 'update_contact'
        SOFT_DELETE_CONTACT = 'SOFT_DELETE_CONTACT', 'soft_delete_contact'
        DELETE_CONTACT = 'DELETE_CONTACT', 'delete_contact'
        PROMOTE_CONTACT = 'PROMOTE_CONTACT', 'promote_contact'
        CLOSE_PROSPECT = 'CLOSE_PROSPECT', 'close_prospect'
        ARCHIVE_CUSTOMER = 'ARCHIVE_CUSTOMER', 'archive_customer'
        ALLOCATE_AGENT = 'ALLOCATE_AGENT', 'allocate_agent'
        CHANGE_AGENT = 'CHANGE_AGENT', 'change_agent'
        BULK_UPLOAD_CONTACT = 'BULK_UPLOAD_CONTACT', 'bulk_upload_contact'

    activity = models.CharField(max_length=19, choices=Activites.choices)
    contact = models.ForeignKey(Contact, on_delete=models.CASCADE, null=True)
    # agent
    # manager
    # company admin = boolean
    date_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.activity + ' - ' + str(self.date_time)
