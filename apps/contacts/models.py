from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django_countries.fields import CountryField
from django.core.validators import MaxValueValidator
from utils.validators import validate_file_size
from django.urls import reverse


class ContactManager(models.Manager):
    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        return queryset

    def get_without_deleted(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs).exclude(is_deleted=True)
        return queryset

    def get_deleted(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs).filter(is_deleted=True)
        return queryset


class Contact(models.Model):

    objects = ContactManager()

    class Types(models.TextChoices):
        LEAD = 'LEAD', 'lead'
        PROSPECT = 'PROSPECT', 'prospect'
        CUSTOMER = 'CUSTOMER', 'customer'

    class ProspectStatus(models.TextChoices):
        OPEN = 'OPEN', 'open'
        CLOSED = 'CLOSED', 'closed'
        SUCCESS = 'SUCCESS', 'success'

    class CustomerStatus(models.TextChoices):
        ACTIVE = 'ACTIVE', 'active'
        ARCHIVED = 'ARCHIVED', 'archived'

    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    age = models.PositiveIntegerField()
    email = models.EmailField(unique=True)
    phone_number = PhoneNumberField(unique=True)
    type = models.CharField(
        max_length=8, choices=Types.choices)
    is_lead = models.BooleanField(default=False)
    is_prospect = models.BooleanField(default=False)
    is_customer = models.BooleanField(default=False)
    score = models.PositiveSmallIntegerField(
        default=0, validators=[MaxValueValidator(100)])
    # agent - agent user model, null,
    prospect_status = models.CharField(max_length=7,
                                       choices=ProspectStatus.choices, null=True)
    customer_status = models.CharField(max_length=8,
                                       choices=CustomerStatus.choices, null=True)
    address = models.TextField(max_length=255)
    country = CountryField()
    profile_picture = models.ImageField(
        upload_to="contacts/",
        validators=[validate_file_size],
        blank=True,
        null=True
    )
    is_deleted = models.BooleanField(default=False)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.first_name + ' ' + self.last_name

    def soft_delete(self):
        self.is_deleted = True
        self.save()


class LeadManager(models.Manager):
    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        queryset = queryset.filter(
            type=Contact.Types.LEAD)
        return queryset

    def get_without_deleted(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        queryset = queryset.filter(
            type=Contact.Types.LEAD).exclude(is_deleted=True)
        return queryset

    def get_deleted(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        queryset = queryset.filter(
            type=Contact.Types.LEAD)
        queryset = queryset.filter(is_deleted=True)
        return queryset


class Lead(Contact):
    class Meta:
        proxy = True
    objects = LeadManager()

    def promote(self, score):
        self.score = score
        self.is_lead = False
        self.is_prospect = True
        self.type = Contact.Types.PROSPECT
        self.prospect_status = Contact.ProspectStatus.OPEN
        self.save()

    def get_absolute_url(self):
        return reverse("contacts:lead-detail", kwargs={"pk": self.pk})


class ProspectManager(models.Manager):
    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        queryset = queryset.filter(
            type=Contact.Types.PROSPECT)
        return queryset

    def get_without_deleted(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        queryset = queryset.filter(
            type=Contact.Types.PROSPECT).exclude(is_deleted=True)
        return queryset

    def get_deleted(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        queryset = queryset.filter(
            type=Contact.Types.PROSPECT)
        queryset = queryset.filter(is_deleted=True)
        return queryset


class Prospect(Contact):
    class Meta:
        proxy = True
    objects = ProspectManager()

    def promote(self):
        self.is_prospect = False
        self.is_customer = True
        self.type = Contact.Types.CUSTOMER
        self.prospect_status = Contact.ProspectStatus.SUCCESS
        self.customer_status = Contact.CustomerStatus.ACTIVE
        self.save()

    def get_absolute_url(self):
        return reverse("contacts:prospect-detail", kwargs={"pk": self.pk})


class CustomerManager(models.Manager):
    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        queryset = queryset.filter(
            type=Contact.Types.CUSTOMER)
        return queryset

    def get_without_deleted(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        queryset = queryset.filter(
            type=Contact.Types.CUSTOMER).exclude(is_deleted=True)
        return queryset

    def get_deleted(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        queryset = queryset.filter(
            type=Contact.Types.CUSTOMER)
        queryset = queryset.filter(is_deleted=True)
        return queryset


class Customer(Contact):
    class Meta:
        proxy = True
    objects = CustomerManager()

    def get_absolute_url(self):
        return reverse("contacts:customer-detail", kwargs={"pk": self.pk})
