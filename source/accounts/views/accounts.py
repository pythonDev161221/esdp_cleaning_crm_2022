from django.contrib.auth import login, get_user_model, update_session_auth_hash
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy

from django.views.generic import DetailView, CreateView, ListView, UpdateView, DeleteView
from accounts.forms import LoginForm, StaffRegistrationForm, StaffEditForm, EditPhotoForm, PasswordChangeForm
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


class StaffListView(ListView):
    model = Staff
    template_name = 'account/staff_list.html'
    context_object_name = "user_object"

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['staff_list'] = Staff.objects.filter(black_list=False).exclude(is_active=False)
        return context


class StaffBlackListView(ListView):
    model = Staff
    template_name = 'account/black_list.html'
    context_object_name = "user_object"

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['staff_list'] = Staff.objects.filter(black_list=True)
        return context


class StaffEditView(UpdateView):
    model = Staff
    form_class = StaffEditForm
    template_name = "account/staff_edit.html"
    context_object_name = "user_object"

    def get_success_url(self):
        return reverse('accounts:staff-list')


class StaffEditPhoto(UpdateView):
    model = Staff
    form_class = EditPhotoForm
    template_name = "account/staff_photo.html"
    context_object_name = "user_object"


class PasswordChangeView(UpdateView):
    model = get_user_model()
    form_class = PasswordChangeForm
    template_name = 'account/password.html'
    context_object_name = 'user_object'

    def form_valid(self, form):
        response = super().form_valid(form)
        update_session_auth_hash(self.request, self.object)
        return response

    def get_object(self, queryset=None):
        return self.request.user


class StaffDeleteView(DeleteView):
    model = Staff
    success_url = reverse_lazy('accounts:staff-list')
    template_name = 'account/staff_delete.html'
    context_object_name = 'user_object'

    def form_valid(self, form):
        response = super().form_valid(form)
        update_session_auth_hash(self.request, self.object)
        return response

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.soft_delete()
        return HttpResponseRedirect(self.get_success_url())


class AddToBlackList(DeleteView):
    model = Staff
    success_url = reverse_lazy('accounts:staff-list')
    template_name = 'account/black_list_add.html'
    context_object_name = 'user_object'

    def form_valid(self, form):
        response = super().form_valid(form)
        update_session_auth_hash(self.request, self.object)
        return response

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.black_list_staff()
        return HttpResponseRedirect(self.get_success_url())


class RemoveFromBlackList(DeleteView):
    model = Staff
    success_url = reverse_lazy('accounts:staff-list')
    template_name = 'account/black_list_remove.html'
    context_object_name = 'user_object'

    def form_valid(self, form):
        response = super().form_valid(form)
        update_session_auth_hash(self.request, self.object)
        return response

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.active_staff()
        return HttpResponseRedirect(self.get_success_url())
