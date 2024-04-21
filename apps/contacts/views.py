from django.urls import reverse_lazy
from django.shortcuts import render, redirect
from django.views.generic import TemplateView, CreateView, ListView, DetailView, UpdateView
from .models import Contact, Lead, Prospect, Customer
from . import forms
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404


class TestView(TemplateView):
    template_name = 'test.html'


class LeadCreateView(CreateView):
    model = Lead
    form_class = forms.LeadCreateForm
    template_name = 'contacts/lead_create.html'
    success_url = reverse_lazy('contacts:lead-list')

    def form_valid(self, form):
        obj = form.save(commit=False)

        obj.is_lead = True
        obj.type = Contact.Types.LEAD

        obj.save()
        return super().form_valid(form)


class ProspectCreateView(CreateView):
    model = Prospect
    form_class = forms.ProspectCreateForm
    template_name = 'contacts/prospect_create.html'
    success_url = reverse_lazy('contacts:prospect-list')

    def form_valid(self, form):
        obj = form.save(commit=False)

        obj.is_prospect = True
        obj.type = Contact.Types.PROSPECT

        obj.save()
        return super().form_valid(form)


class CustomerCreateView(CreateView):
    model = Customer
    form_class = forms.CustomerCreateForm
    template_name = 'contacts/customer_create.html'
    success_url = reverse_lazy('contacts:customer-list')

    def form_valid(self, form):
        obj = form.save(commit=False)

        obj.is_customer = True
        obj.type = Contact.Types.CUSTOMER

        obj.save()
        return super().form_valid(form)


class LeadListView(ListView):
    model = Lead
    template_name = 'contacts/lead_list.html'


class ProspectListView(ListView):
    model = Prospect
    template_name = 'contacts/prospect_list.html'


class CustomerListView(ListView):
    model = Customer
    template_name = 'contacts/customer_list.html'


class LeadDetailView(DetailView):
    model = Lead
    template_name = 'contacts/contact_detail.html'
    context_object_name = 'contact'


class ProspectDetailView(DetailView):
    model = Prospect
    template_name = 'contacts/contact_detail.html'
    context_object_name = 'contact'


class CustomerDetailView(DetailView):
    model = Customer
    template_name = 'contacts/contact_detail.html'
    context_object_name = 'contact'


class LeadUpdateView(UpdateView):
    model = Lead
    form_class = forms.LeadCreateForm
    template_name = 'contacts/lead_update.html'


class ProspectUpdateView(UpdateView):
    model = Prospect
    form_class = forms.ProspectCreateForm
    template_name = 'contacts/prospect_update.html'


class CustomerUpdateView(UpdateView):
    model = Customer
    form_class = forms.CustomerCreateForm
    template_name = 'contacts/customer_update.html'


def lead_promote_view(request, pk):
    try:
        contact = Lead.objects.get(id=pk)
    except ObjectDoesNotExist:
        raise Http404
    if request.method != 'POST':
        form = forms.LeadPromoteForm()
    else:
        form = forms.LeadPromoteForm(data=request.POST)
        if form.is_valid():
            score = form.cleaned_data['score']
            contact.promote(score=score)
            return redirect('contacts:prospect-list')

    context = {'form': form, 'lead': contact}
    return render(request, 'contacts/lead_promote.html', context)


def prospect_promote_view(request, pk):
    try:
        contact = Prospect.objects.get(id=pk)
    except ObjectDoesNotExist:
        raise Http404
    if request.method == 'POST':
        contact.promote()
        return redirect('contacts:customer-list')
    context = {'prospect': contact}
    return render(request, 'contacts/prospect_promote.html', context)
