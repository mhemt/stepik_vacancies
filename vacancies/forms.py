from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

from vacancies.models import Application, Company


class RegisterForm(UserCreationForm):
    first_name = forms.CharField(label='Имя')
    last_name = forms.CharField(label='Фамилия')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        del self.fields['password2']
        self.fields['username'].label = 'Логин'
        self.fields['username'].help_text = None
        self.fields['password1'].help_text = None

        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Зарегистрироваться', css_class='btn-primary btn-lg btn-block'))

        self.helper.form_class = 'form-signin pt-5'
        self.helper.label_class = 'text-muted form-label-group'

    class Meta:
        model = get_user_model()
        fields = ('username', 'first_name', 'last_name',)


class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = 'Логин'
        self.fields['password'].label = 'Пароль'

        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Войти', css_class='btn-primary btn-lg btn-block'))

        self.helper.form_class = 'form-signin pt-5'
        self.helper.label_class = 'text-muted form-label-group'


class ApplicationForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.request = kwargs  # TODO: check if necessary
        self.fields['written_username'].label = 'Вас зовут'
        self.fields['written_phone'].label = 'Ваш телефон'
        self.fields['written_cover_letter'].label = 'Сопроводительное письмо'

        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Отправить', css_class='btn-primary'))

        self.helper.label_class = 'mt-2'

    class Meta:
        model = Application
        fields = ('written_username', 'written_phone', 'written_cover_letter',)


class CompanyEditForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].label = 'Название компании'
        self.fields['location'].label = 'География'
        self.fields['logo'].label = 'Логотип'
        self.fields['description'].label = 'Информация о компании'
        self.fields['employee_count'].label = 'Количество человек в компании'

        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Сохранить', css_class='btn-info'))

    class Meta:
        model = Company
        fields = ('name', 'location', 'logo', 'description', 'employee_count',)
