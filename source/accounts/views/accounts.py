from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
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


class StaffProfileView(DetailView):
    model = Staff
    template_name = 'account/staff_profile.html'
    context_object_name = 'user_object'


class StaffRegisterView(CreateView):
    model = Staff
    template_name = "account/registration.html"
    form_class = StaffRegistrationForm

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


class StaffListView(ListView):
    model = Staff
    template_name = 'account/staff_list.html'
    context_object_name = "user_objects"

    def get_queryset(self):
        queryset = Staff.objects.filter(black_list=False).exclude(is_active=False)
        return queryset


class StaffEditView(UpdateView):
    model = Staff
    form_class = StaffEditForm
    template_name = "account/staff_edit.html"
    context_object_name = "user_object"

    def get_success_url(self):
        return reverse('accounts:staff-list')

    def form_valid(self, form):
        user = form.save
        return redirect(self.get_success_url())


class StaffEditPhoto(UpdateView):
    model = Staff
    form_class = EditPhotoForm
    template_name = "account/staff_photo.html"
    context_object_name = "user_object"


class StaffPassportPhotoView(UpdateView):
    model = Staff
    form_class = StaffPassportForm
    template_name = "account/passport.html"
    context_object_name = "user_object"


class StaffDescriptionView(UpdateView):
    model = Staff
    form_class = StaffDescriptionForm
    template_name = "account/staff_description.html"
    context_object_name = "user_object"

    def get_success_url(self):
        return reverse('accounts:staff-list')


class StaffDeleteView(DeleteView):
    model = Staff
    success_url = reverse_lazy('accounts:staff-list')
    template_name = 'account/staff_delete.html'
    context_object_name = 'user_object'

    def get_object(self, queryset=None):
        return self.request.user

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.soft_delete()
        messages.success(self.request, f'{self.object.last_name} {self.object.first_name} успешно удален(a)!')
        return HttpResponseRedirect(self.get_success_url())


class StaffBlackListView(ListView):
    model = Staff
    template_name = 'account/black_list.html'
    context_object_name = "user_objects"

    def get_queryset(self):
        queryset = Staff.objects.filter(black_list=True)
        return queryset


class AddToBlackList(UpdateView):
    model = Staff
    success_url = reverse_lazy('accounts:staff-list')
    form_class = StaffDescriptionForm
    template_name = 'account/black_list_add.html'
    context_object_name = 'user_object'

    def form_valid(self, form):
        self.object = form.save()
        self.object.black_list_staff()
        messages.success(self.request, f'{self.object.last_name} {self.object.first_name} добавлен(a) в черный список!')
        return HttpResponseRedirect(self.get_success_url())


class RemoveFromBlackList(DeleteView):
    model = Staff
    success_url = reverse_lazy('accounts:staff-list')
    template_name = 'account/black_list_remove.html'
    context_object_name = 'user_object'

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.active_staff()
        messages.success(self.request,
                         f'{self.object.last_name} {self.object.first_name} больше не находится в черном списке!')
        return HttpResponseRedirect(self.get_success_url())


class StaffPassportView(DetailView):
    model = Staff
    template_name = 'account/staff_passport.html'
    context_object_name = 'user_object'