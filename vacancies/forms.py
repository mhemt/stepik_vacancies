from crispy_forms.bootstrap import InlineCheckboxes
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Row, Column
from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

from vacancies.models import Application, Company, Vacancy, Resume


class RegisterForm(UserCreationForm):
    first_name = forms.CharField(label='Имя')
    last_name = forms.CharField(label='Фамилия')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        del self.fields['password2']
        self.fields['username'].help_text = None
        self.fields['password1'].help_text = None

        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Зарегистрироваться', css_class='btn-primary btn-lg btn-block'))

        self.helper.form_class = 'form-signin pt-5'
        self.helper.label_class = 'text-muted form-label-group'

    class Meta:
        model = get_user_model()
        fields = (
            'username',
            'first_name',
            'last_name',
        )

        labels = {
            'username': 'Логин',
        }


class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Войти', css_class='btn-primary btn-lg btn-block'))

        self.helper.form_class = 'form-signin pt-5'
        self.helper.label_class = 'text-muted form-label-group'

    class Meta:
        labels = {
            'username': 'Логин',
            'password': 'Пароль',
        }


class ApplicationForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['written_cover_letter'].widget.attrs['rows'] = 5

        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Отправить', css_class='btn-primary'))

        self.helper.label_class = 'mt-2'

    class Meta:
        model = Application
        fields = (
            'written_username',
            'written_phone',
            'written_cover_letter',
        )

        labels = {
            'written_username': 'Вас зовут',
            'written_phone': 'Ваш телефон',
            'written_cover_letter': 'Сопроводительное письмо',
        }


class CompanyEditForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['description'].widget.attrs['rows'] = 4

        self.helper = FormHelper()
        self.helper.form_method = 'post'

        self.helper.layout = Layout(
            Row(
                Column('name', css_class='form-group pb-2'),
                Column('logo', css_class='form-group pb-2'),
                css_class='form-row',
            ),
            Row(
                Column('employee_count', css_class='form-group pb-2'),
                Column('location', css_class='form-group pb-2'),
                css_class='form-row',
            ),
            'description',
            Submit('submit', 'Сохранить', css_class='btn-info'),
        )

    class Meta:
        model = Company
        fields = (
            'name',
            'location',
            'logo',
            'description',
            'employee_count',
        )

        labels = {
            'name': 'Название компании',
            'location': 'География',
            'logo': 'Логотип',
            'description': 'Информация о компании',
            'employee_count': 'Количество человек в компании',
        }


class VacancyEditForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['description'].widget.attrs['rows'] = 4

        self.helper = FormHelper()
        self.helper.form_method = 'post'

        self.helper.layout = Layout(
            Row(
                Column('title', css_class='form-group pb-2'),
                Column('specialty', css_class='form-group pb-2'),
                css_class='form-row',
            ),
            Row(
                Column('salary_min', css_class='form-group pb-2'),
                Column('salary_max', css_class='form-group pb-2'),
                css_class='form-row',
            ),
            InlineCheckboxes('skills'),
            'description',
            Submit('submit', 'Сохранить', css_class='btn-info'),
        )

    class Meta:
        model = Vacancy
        fields = (
            'title',
            'specialty',
            'skills',
            'description',
            'salary_min',
            'salary_max',
        )

        labels = {
            'title': 'Название вакансии',
            'specialty': 'Специализация',
            'skills': 'Требуемые навыки',
            'description': 'Описание вакансии',
            'salary_min': 'Зарплата от',
            'salary_max': 'Зарплата до',
        }


class ResumeEditForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['education'].widget.attrs['rows'] = 4
        self.fields['experience'].widget.attrs['rows'] = 4

        self.helper = FormHelper()
        self.helper.form_method = 'post'

        self.helper.layout = Layout(
            Row(
                Column('name', css_class='form-group pb-2'),
                Column('surname', css_class='form-group pb-2'),
                css_class='form-row',
            ),
            Row(
                Column('status', css_class='form-group pb-2'),
                Column('salary', css_class='form-group pb-2'),
                css_class='form-row',
            ),
            Row(
                Column('specialty', css_class='form-group pb-2'),
                Column('grade', css_class='form-group pb-2'),
                css_class='form-row',
            ),
            'education',
            'experience',
            'portfolio',
            Submit('submit', 'Сохранить', css_class='btn-info'),
        )

    class Meta:
        model = Resume
        fields = (
            'name',
            'surname',
            'status',
            'salary',
            'specialty',
            'grade',
            'education',
            'experience',
            'portfolio',
        )

        labels = {
            'name': 'Имя',
            'surname': 'Фамилия',
            'status': 'Готовность к работе',
            'salary': 'Ожидаемое вознаграждение',
            'specialty': 'Специализация',
            'grade': 'Квалификация',
            'education': 'Образование',
            'experience': 'Опыт работы',
            'portfolio': 'Ссылка на портфолио',
        }
