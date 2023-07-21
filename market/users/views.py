from products.models import Browsing_history
from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse_lazy
from django.core.mail import send_mail
from django.contrib.auth.views import LoginView, LogoutView, FormView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView
from django.views.generic.edit import FormMixin
from django.views.generic.base import View
from django.utils.translation import gettext_lazy as _

from users.models import CustomUser, UserAvatar
from users import forms
from users.services.users_service import MyProfileService as Service, last_order_request


class UserRegistrationView(CreateView):
    """ Регистрация нового пользователя """

    form_class = forms.CustomUserCreationForm
    model = CustomUser
    template_name = 'market/users/register.jinja2'
    success_url = '/'

    def form_valid(self, form):
        result = super().form_valid(form)
        default_avatar = UserAvatar.objects.create(image="users/avatars/default/default_avatar1.png",
                                                   user_id=self.object.id)
        default_avatar.save()
        return result


class MyLoginView(LoginView):
    """Вход пользователя"""

    LoginView.next_page = reverse_lazy('users:users_register')
    redirect_authenticated_user = True
    template_name = 'market/users/login.jinja2'
    authentication_form = forms.CustomAuthenticationForm


class UserLogoutView(LogoutView):
    """Выход пользователя"""
    next_page = reverse_lazy("users:users_login")


class RestorePasswordView(FormView):
    """Восстановление пароля пользователя"""
    form_class = forms.RestorePasswordForm
    template_name = 'market/users/password.jinja2'
    success_url = reverse_lazy('users:users_restore_password')

    def form_valid(self, form):
        """Проверка валидности формы"""
        super().form_valid(form)
        user_email = form.cleaned_data['email']
        new_password = CustomUser.objects.make_random_password()
        current_user = CustomUser.objects.filter(email__exact=user_email).first()
        current_user.set_password(new_password)
        current_user.save()
        send_mail(subject='Password reset instructions',
                  message=f'New password: {new_password}',
                  from_email='admin@gmail.com',
                  recipient_list=[form.cleaned_data['email']])
        success_message = _(f'Новый пароль успешно отправлен на {user_email}')
        return redirect(reverse_lazy('users:users_restore_password') + '?success_message=' + success_message)


@login_required(login_url=reverse_lazy('users:users_login'))
def account(request):
    """Личный кабинет"""
    user_account = get_object_or_404(CustomUser, email=request.user.email)
    if user_account.email != request.user.email:
        return render(request, 'market/base.jinja2')
    if request.method == 'GET':
        # Получение имени пользователя
        user = CustomUser.objects.get(pk=request.user.pk)
        if user.first_name and user.last_name:
            name = f"{user.first_name} {user.last_name}"
        else:
            name = user.username
        context = {'username': name,
                   'user': user,
                   'order': last_order_request(request.user)}
        return render(request, 'market/users/account.jinja2', context)


class MyProfileView(LoginRequiredMixin, FormMixin, View):

    form_class = forms.ChangePasswordForm
    second_form_class = forms.UserProfileForm
    template_name = 'market/users/profile.jinja2'
    success_url = reverse_lazy('users:users_profile')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def get(self, request):
        second_form = self.second_form_class(instance=request.user)
        user = CustomUser.objects.get(pk=request.user.pk)
        form = self.get_form()
        return render(request, self.template_name, {'form': form,
                                                    'second_form': second_form,
                                                    'user': user})

    def post(self, request):
        form = self.get_form()
        second_form = self.second_form_class(instance=request.user, data=request.POST, files=request.FILES)
        if Service.post_form_validation(form=form, second_form=second_form, request=self.request):
            return self.form_valid(form, second_form=second_form)
        return self.get(request)

    def form_valid(self, form, **kwargs):
        super().form_valid(form)
        return Service.form_validation(form=form, request=self.request, **kwargs)


class BrowsingHistory(View):
    """Контроллер истории просмотров товаров"""

    def get(self, request):
        history = Browsing_history.objects.filter(users_id=request.user.id).order_by('-data_at')[:20]
        history_count = Browsing_history.objects.count()
        contex = {
            'count': history_count,
            'history': history
        }
        return render(request, 'market/users/browsing_history.jinja2', context=contex)

    def post(self, request):
        product_id = self.request.POST.get('delete')
        history = Browsing_history.objects.all().order_by('-data_at')[:20]
        if 'delete' in request.POST:
            Browsing_history.objects.filter(product_id=product_id).delete()
        history_count = Browsing_history.objects.count()
        contex = {
            'count': history_count,
            'history': history
        }
        return render(request, 'market/users/browsing_history.jinja2', context=contex)
