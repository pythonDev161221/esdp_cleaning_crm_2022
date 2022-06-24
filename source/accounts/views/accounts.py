import uuid

from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.models import Group
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, get_object_or_404, render
from django.urls import reverse, reverse_lazy

from django.views.generic import DetailView, CreateView, ListView, UpdateView, DeleteView
from accounts.forms import (LoginForm,
                            StaffRegistrationForm,
                            StaffEditForm,
                            EditPhotoForm,
                            PasswordChangeForm,
                            StaffDescriptionForm,
                            StaffPassportForm)
from accounts.models import Staff
from tgbot.dispatcher import TELEGRAM_BOT_USERNAME

from crmapp.forms import SearchForm


class StaffProfileView(PermissionRequiredMixin, DetailView):
    model = Staff
    template_name = 'account/staff_profile.html'
    context_object_name = 'user_object'
    permission_required = "accounts.view_staff"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        group = Group(name="Manager")
        if self.object.groups.filter(name=group):
            context["is_manager"] = True
            context["cash_order_count"] = self.object.manager_cash.filter(is_nullify=False).count()
        context['form_description'] = StaffDescriptionForm
        return context

    def has_permission(self):
        return super().has_permission() or self.request.user.is_staff or self.request.user == self.get_object()


class StaffRegisterView(PermissionRequiredMixin, CreateView):
    model = Staff
    template_name = "account/registration.html"
    form_class = StaffRegistrationForm
    permission_required = "accounts.add_staff"

    def form_valid(self, form):
        user = form.save()
        form.save_m2m()
        return redirect(self.get_success_url())

    def get_success_url(self):
        next_url = self.request.GET.get('next')
        if not next_url:
            next_url = self.request.POST.get('next')
        if not next_url:
            next_url = reverse('accounts:staff-list')
        return next_url


class PasswordChangeView(LoginRequiredMixin, UpdateView):
    model = Staff
    template_name = 'account/password.html'
    form_class = PasswordChangeForm
    context_object_name = 'user_object'

    def form_valid(self, form):
        response = super().form_valid(form)
        update_session_auth_hash(self.request, self.object)
        messages.success(self.request, f'Пароль был успешно изменен!')
        return response

    def get_object(self, queryset=None):
        return self.request.user

    def get_success_url(self):
        return reverse("accounts:profile", kwargs={"pk": self.request.user.pk})


class StaffListView(PermissionRequiredMixin, ListView):
    model = Staff
    template_name = 'account/staff_list.html'
    context_object_name = "user_objects"
    search_form_class = SearchForm
    permission_required = "accounts.view_staff"

    def get(self, request, *args, **kwargs):
        self.form = self.get_form()
        self.search_value = self.get_search_value()
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        queryset = Staff.objects.filter(black_list=False).\
            exclude(is_active=False).exclude(groups__name="Manager")
        if self.search_value:
            query = Q(last_name__icontains=self.search_value) | \
                    Q(first_name__icontains=self.search_value) | \
                    Q(inn_passport__icontains=self.search_value) | \
                    Q(address__icontains=self.search_value) | \
                    Q(phone__icontains=self.search_value) | \
                    Q(experience__icontains=self.search_value)
            queryset = queryset.filter(query)
        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        context['form'] = self.search_form_class()
        return context

    def get_form(self):
        return self.search_form_class(self.request.GET)

    def get_search_value(self):
        if self.form.is_valid():
            return self.form.cleaned_data.get("search")

    def has_permission(self):
        return super().has_permission() or self.request.user.is_staff


class StaffManagerListView(PermissionRequiredMixin, ListView):
    model = Staff
    template_name = 'account/staff_manager_list.html'
    context_object_name = "user_objects"
    permission_required = "accounts.view_staff"

    def get_queryset(self):
        queryset = Staff.objects.filter(black_list=False, groups__name="Manager").\
            exclude(is_active=False)
        return queryset

    def has_permission(self):
        return self.request.user.is_staff


class StaffEditView(PermissionRequiredMixin, UpdateView):
    model = Staff
    form_class = StaffEditForm
    template_name = "account/staff_edit.html"
    context_object_name = "user_object"
    permission_required = "accounts.change_staff"

    def get_success_url(self):
        return reverse('accounts:staff-list')

    def form_valid(self, form):
        user = form.save
        return redirect(self.get_success_url())


class StaffEditPhoto(LoginRequiredMixin, UpdateView):
    model = Staff
    form_class = EditPhotoForm
    template_name = "account/staff_photo.html"
    context_object_name = "user_object"


class StaffPassportPhotoView(PermissionRequiredMixin, UpdateView):
    model = Staff
    form_class = StaffPassportForm
    template_name = "account/passport.html"
    context_object_name = "user_object"
    permission_required = "accounts.add_staff_passport_photo"


class StaffDescriptionView(PermissionRequiredMixin, UpdateView):
    model = Staff
    form_class = StaffDescriptionForm
    template_name = "account/staff_description.html"
    context_object_name = "user_object"
    permission_required = "accounts.add_staff_description"


class StaffDeleteView(PermissionRequiredMixin, DeleteView):
    model = Staff
    success_url = reverse_lazy('accounts:staff-list')
    template_name = 'account/staff_delete.html'
    context_object_name = 'user_object'
    permission_required = "accounts.delete_staff"

    def get_object(self, queryset=None):
        return Staff.objects.get(pk=self.kwargs.get(self.pk_url_kwarg))

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.soft_delete()
        messages.success(self.request, f'{self.object.last_name} {self.object.first_name} успешно удален(a)!')
        return HttpResponseRedirect(self.get_success_url())

    def has_permission(self):
        return super().has_permission() or self.request.user.is_staff


class StaffBlackListView(PermissionRequiredMixin, ListView):
    model = Staff
    template_name = 'account/black_list.html'
    context_object_name = "user_objects"
    search_form_class = SearchForm
    permission_required = "accounts.view_staff_blacklist"
    paginate_by = 10
    paginate_orphans = 0

    def get(self, request, *args, **kwargs):
        self.form = self.get_form()
        self.search_value = self.get_search_value()
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = Staff.objects.filter(black_list=True)
        if self.search_value:
            query = Q(last_name__icontains=self.search_value) | Q(first_name__icontains=self.search_value) | Q(
                inn_passport__icontains=self.search_value) | Q(address__icontains=self.search_value) | Q(
                phone__icontains=self.search_value) | Q(experience__icontains=self.search_value)
            queryset = queryset.filter(query)
        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        context['form'] = self.search_form_class()
        return context

    def get_form(self):
        return self.search_form_class(self.request.GET)

    def get_search_value(self):
        if self.form.is_valid():
            return self.form.cleaned_data.get("search")


class AddToBlackList(PermissionRequiredMixin, UpdateView):
    model = Staff
    success_url = reverse_lazy('accounts:staff-list')
    form_class = StaffDescriptionForm
    template_name = 'account/black_list_add.html'
    context_object_name = 'user_object'
    permission_required = "accounts.add_toBlackList"

    def form_valid(self, form):
        self.object = form.save()
        self.object.black_list_staff()
        messages.success(self.request, f'{self.object.last_name} {self.object.first_name} добавлен(a) в черный список!')
        return HttpResponseRedirect(self.get_success_url())


class RemoveFromBlackList(PermissionRequiredMixin, DeleteView):
    model = Staff
    success_url = reverse_lazy('accounts:staff-list')
    template_name = 'account/black_list_remove.html'
    context_object_name = 'user_object'
    permission_required = 'accounts.delete_fromBlackList'

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.active_staff()
        messages.success(self.request,
                         f'{self.object.last_name} {self.object.first_name} больше не находится в черном списке!')
        return HttpResponseRedirect(self.get_success_url())


class StaffPassportView(LoginRequiredMixin, DetailView):
    model = Staff
    template_name = 'account/staff_passport.html'
    context_object_name = 'user_object'


class GetAuthTokenTelegram(PermissionRequiredMixin, DetailView):
    model = Staff
    template_name = "account/staff_tg_auth_token.html"
    permission_required = "accounts.add_staff"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["token"] = self.object.set_auth_tg_token()
        return context

    def has_permission(self):
        return super().has_permission()


class StaffPayoutDetailView(LoginRequiredMixin, DetailView):
    model = Staff
    context_object_name = 'staff'
    template_name = 'account/payout_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        payouts = context['staff'].payouts.all().order_by('-date_payout')
        context['payouts'] = payouts
        return context


class StaffOrderDetailView(LoginRequiredMixin, DetailView):
    model = Staff
    context_object_name = 'staff'
    template_name = 'account/staff_orders.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

