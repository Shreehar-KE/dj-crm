from django.contrib import admin
from .models import Contact, Lead, Prospect, Customer

admin.site.register(Contact)
admin.site.register(Lead)
admin.site.register(Prospect)
admin.site.register(Customer)
