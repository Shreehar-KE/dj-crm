from django.db.models.base import Model as Model
from django.db.models.query import QuerySet
from django.forms import BaseModelForm
from django.http.response import HttpResponse as HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView, ListView, DetailView, UpdateView
from .models import Contact, Lead, Prospect, Customer
from . import forms
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404, HttpRequest
from django.contrib import messages
from apps.logs.models import Log


class TestView(TemplateView):
    template_name = 'test.html'


class ToastView(TemplateView):
    template_name = 'toast.html'


class LeadCreateView(CreateView):
    model = Lead
    form_class = forms.LeadCreateForm
    template_name = 'contacts/lead_create.html'

    def form_valid(self, form):
        obj = form.save(commit=False)

        obj.is_lead = True
        obj.type = Contact.Type.LEAD

        obj.save()
        log_activity(activity=Log.Activites.CREATE_CONTACT, contact=obj)
        return super().form_valid(form)


class ProspectCreateView(CreateView):
    model = Prospect
    form_class = forms.ProspectCreateForm
    template_name = 'contacts/prospect_create.html'

    def form_valid(self, form):
        obj = form.save(commit=False)

        obj.is_prospect = True
        obj.type = Contact.Type.PROSPECT

        obj.save()
        log_activity(activity=Log.Activites.CREATE_CONTACT, contact=obj)

        return super().form_valid(form)


class CustomerCreateView(CreateView):
    model = Customer
    form_class = forms.CustomerCreateForm
    template_name = 'contacts/customer_create.html'

    def form_valid(self, form):
        obj = form.save(commit=False)

        obj.is_customer = True
        obj.type = Contact.Type.CUSTOMER

        obj.save()
        log_activity(activity=Log.Activites.CREATE_CONTACT, contact=obj)

        return super().form_valid(form)


class LeadListView(ListView):
    model = Lead
    template_name = 'contacts/lead_list.html'

    def get_queryset(self) -> QuerySet[any]:
        return super().get_queryset().exclude(is_deleted=True)


class ProspectListView(ListView):
    model = Prospect
    template_name = 'contacts/prospect_list.html'

    def get_queryset(self) -> QuerySet[any]:
        return super().get_queryset().exclude(is_deleted=True)


class CustomerListView(ListView):
    model = Customer
    template_name = 'contacts/customer_list.html'

    def get_queryset(self) -> QuerySet[any]:
        return super().get_queryset().exclude(is_deleted=True)


class ContactDetailView(DetailView):
    model = Contact
    template_name = 'contacts/contact_detail.html'
    context_object_name = 'contact'
    queryset = Contact.objects.get_queryset().filter(is_deleted=False)


# class LeadDetailView(DetailView):
#     model = Lead
#     template_name = 'contacts/contact_detail.html'
#     context_object_name = 'contact'
#     queryset = Lead.objects.get_queryset().exclude(is_deleted=True)

#     def get_queryset(self) -> QuerySet[any]:
#         return super().get_queryset().exclude(is_deleted=True)

#     def get_object(self, queryset=None):
#         obj = super().get_object(queryset=queryset)
#         raise Http404
#         if obj.is_lead:  # Replace 'boolean_field' with your actual field name
#             raise Http404("Object not found")  # More specific message optional
#         return obj


# class ProspectDetailView(DetailView):
#     model = Prospect
#     template_name = 'contacts/contact_detail.html'
#     context_object_name = 'contact'


# class CustomerDetailView(DetailView):
#     model = Customer
#     template_name = 'contacts/contact_detail.html'
#     context_object_name = 'contact'


class LeadUpdateView(UpdateView):
    model = Lead
    form_class = forms.LeadCreateForm
    template_name = 'contacts/lead_update.html'

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        log_activity(activity=Log.Activites.CREATE_CONTACT,
                     contact=self.get_object())
        messages.success(self.request, 'Updated Successfully!')
        return super().form_valid(form)


class ProspectUpdateView(UpdateView):
    model = Prospect
    form_class = forms.ProspectCreateForm
    template_name = 'contacts/prospect_update.html'

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        log_activity(activity=Log.Activites.CREATE_CONTACT,
                     contact=self.get_object())
        messages.success(self.request, 'Updated Successfully!',
                         extra_tags="htmx-toast")
        return super().form_valid(form)


class CustomerUpdateView(UpdateView):
    model = Customer
    form_class = forms.CustomerCreateForm
    template_name = 'contacts/customer_update.html'

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        log_activity(activity=Log.Activites.CREATE_CONTACT,
                     contact=self.get_object())
        messages.success(self.request, 'Updated Successfully!')
        return super().form_valid(form)


def lead_soft_delete_view(request, pk):
    lead = check_lead(pk)
    if request.method == 'POST':
        lead.soft_delete()
        log_activity(activity=Log.Activites.SOFT_DELETE_CONTACT,
                     contact=lead)
        return redirect('contacts:lead-list')
    context = {'lead': lead}
    return render(request, 'contacts/lead_delete.html', context)


def prospect_soft_delete_view(request, pk):
    prospect = check_prospect(pk)
    if request.method == 'POST':
        prospect.soft_delete()
        log_activity(activity=Log.Activites.SOFT_DELETE_CONTACT,
                     contact=prospect)
        return redirect('contacts:prospect-list')
    context = {'prospect': prospect}
    return render(request, 'contacts/prospect_delete.html', context)


def customer_soft_delete_view(request, pk):
    customer = check_customer(pk)
    if request.method == 'POST':
        customer.soft_delete()
        log_activity(activity=Log.Activites.SOFT_DELETE_CONTACT,
                     contact=customer)
        return redirect('contacts:customer-list')
    context = {'customer': customer}
    return render(request, 'contacts/customer_delete.html', context)


def lead_promote_view(request, pk):
    lead = check_lead(pk)
    if request.method != 'POST':
        form = forms.LeadPromoteForm()
    else:
        form = forms.LeadPromoteForm(data=request.POST)
        if form.is_valid():
            score = form.cleaned_data['score']
            lead.promote(score=score)
            log_activity(activity=Log.Activites.PROMOTE_CONTACT,
                         contact=lead)
            return redirect('contacts:contact-detail', lead.id)

    context = {'form': form, 'lead': lead}
    return render(request, 'contacts/lead_promote.html', context)


def prospect_promote_view(request, pk):
    prospect = check_prospect(pk)
    if request.method == 'POST':
        prospect.promote()
        log_activity(activity=Log.Activites.PROMOTE_CONTACT,
                     contact=prospect)
        return redirect('contacts:contact-detail', prospect.id)
    context = {'prospect': prospect}
    return render(request, 'contacts/prospect_promote.html', context)


def check_contact(pk):
    try:
        # contact = Contact.objects.get_without_deleted(id=pk)
        contact = Contact.objects.all().exclude(is_deleted=True).get(id=pk)
        return contact
    except ObjectDoesNotExist:
        raise Http404


def check_lead(pk):
    try:
        # lead = Lead.objects.get_query_without_deleted(id=pk)
        lead = Lead.objects.all().exclude(is_deleted=True).get(id=pk)
        return lead
    except ObjectDoesNotExist:
        raise Http404


def check_prospect(pk):
    try:
        # prospect = Prospect.objects.get_without_deleted(id=pk)
        prospect = Prospect.objects.all().exclude(is_deleted=True).get(id=pk)
        return prospect
    except ObjectDoesNotExist:
        raise Http404


def check_customer(pk):
    try:
        # customer = Customer.objects.get_without_deleted(id=pk)
        customer = Customer.objects.all().exclude(is_deleted=True).get(id=pk)
        return customer
    except ObjectDoesNotExist:
        raise Http404


def log_activity(activity, contact):
    log = Log()
    log.activity = activity
    log.contact = contact
    log.save()
