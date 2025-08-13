from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import gettext_lazy as _
from users.models import AssociationMember


class AssociationMemberForm(UserCreationForm):
    email = forms.EmailField(required=True)

    patronymic = forms.CharField(label=_('Отчество'))
    workplace = forms.CharField(label=_('Место работы'))
    position = forms.CharField(label=_('Должность'))
    contacts = forms.CharField(label=_('Контакты'), widget=forms.Textarea)
    motivation_letter = forms.CharField(label=_('Мотивационное письмо'), widget=forms.Textarea)
    social_networks = forms.CharField(label=_('Соцсети'), required=False)
    resume = forms.FileField(label=_('Резюме'))

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'first_name', 'last_name']


class MemberFilterForm(forms.Form):
    workplace = forms.ChoiceField(required=False, label=_('Место работы'))
    position = forms.ChoiceField(required=False, label=_('Должность'))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        workplaces = AssociationMember.objects.values_list('workplace', flat=True).distinct()
        positions = AssociationMember.objects.values_list('position', flat=True).distinct()

        self.fields['workplace'].choices = [('', _('Все'))] + [(w, w) for w in workplaces if w]
        self.fields['position'].choices = [('', _('Все'))] + [(p, p) for p in positions if p]


class AvatarForm(forms.ModelForm):
    remove_avatar = forms.BooleanField(required=False, label=_('Удалить аватар'))

    class Meta:
        model = AssociationMember
        fields = ['avatar', 'remove_avatar']


from django import forms
from django.utils.translation import gettext_lazy as _

class CRMApplicationForm(forms.Form):
    CATEGORY_CHOICES = [
        ('', _('Выберите отрасль')),
        ('гос', _('Государственные коммуникации')),
        ('корп', _('Корпоративные коммуникации')),
        ('бизнес', _('Частный бизнес')),
        ('агентство', _('Агентства')),
    ]

    full_name = forms.CharField(
        label='',
        widget=forms.TextInput(attrs={'placeholder': _('ФИО')})
    )
    email = forms.EmailField(
        label='',
        widget=forms.EmailInput(attrs={'placeholder': _('Почта')})
    )
    workplace = forms.CharField(
        label='',
        widget=forms.TextInput(attrs={'placeholder': _('Место работы')})
    )
    phone = forms.CharField(
        label='',
        widget=forms.TextInput(attrs={'placeholder': _('Телефон')})
    )
    position = forms.CharField(
        label='',
        widget=forms.TextInput(attrs={'placeholder': _('Должность')})
    )
    instagram = forms.CharField(
        label='',
        required=False,
        widget=forms.TextInput(attrs={'placeholder': _('Instagram')})
    )

    category = forms.ChoiceField(
        label='',
        choices=CATEGORY_CHOICES,
        widget=forms.Select(attrs={'placeholder': _('Категория')})
    )

    motivation_letter = forms.FileField(label=_("Мотивационное письмо"))
    photo = forms.FileField(label=_("Фото"))
    documents = forms.FileField(label=_("Сертификаты и документы"))


class ExtendedApplicationForm(forms.Form):
    input_attrs = {'class': 'form-control'}

    phone_attrs = input_attrs.copy()
    phone_attrs['id'] = 'id_phone'

    additional_phone_attrs = input_attrs.copy()
    additional_phone_attrs['id'] = 'id_additional_phone'

      # Личные данные
    last_name = forms.CharField(label=_("Фамилия"), required=True, widget=forms.TextInput(attrs=input_attrs))
    first_name = forms.CharField(label=_("Имя"), required=True, widget=forms.TextInput(attrs=input_attrs))
    middle_name = forms.CharField(label=_("Отчество"), required=False, widget=forms.TextInput(attrs=input_attrs))
    birth_date = forms.DateField(label=_("Дата рождения"), required=True, widget=forms.DateInput(attrs={**input_attrs, 'type': 'date'}))
    citizenship = forms.CharField(label=_("Гражданство"), required=True, widget=forms.TextInput(attrs=input_attrs))
    city = forms.CharField(label=_("Город проживания"), required=True, widget=forms.TextInput(attrs=input_attrs))

    # Контакты
    phone = forms.CharField(label=_("Мобильный телефон"), required=True, widget=forms.TextInput(attrs=phone_attrs))
    additional_phone = forms.CharField(label=_("Дополнительный номер"), required=False, widget=forms.TextInput(attrs=additional_phone_attrs))
    email = forms.EmailField(label=_("Электронная почта"), required=True, widget=forms.EmailInput(attrs=input_attrs))
    social_links = forms.CharField(label=_("Ссылка на профиль в соцсетях"), required=True, widget=forms.TextInput(attrs=input_attrs))

    # Образование
    university = forms.CharField(label=_("Учебное заведение"), required=True, widget=forms.TextInput(attrs=input_attrs))
    faculty = forms.CharField(label=_("Факультет / Специальность"), required=True, widget=forms.TextInput(attrs=input_attrs))
    study_years = forms.CharField(label=_("Годы обучения"), required=True, widget=forms.TextInput(attrs=input_attrs))
    degree = forms.ChoiceField(
        label=_("Академическая степень"),
        required=True,
        choices=[
            ('', _('Выберите степень')),
            ('Бакалавр', _('Бакалавр')),
            ('Магистр', _('Магистр')),
            ('Доктор', _('Доктор')),
            ('Другое', _('Другое')),
        ],
        widget=forms.Select(attrs=input_attrs)
    )

    # Проф. деятельность
    job_place = forms.CharField(label=_("Текущее место работы"), required=True, widget=forms.TextInput(attrs=input_attrs))
    job_title = forms.CharField(label=_("Должность"), required=True, widget=forms.TextInput(attrs=input_attrs))
    job_region = forms.CharField(label=_("Регион профессиональной деятельности"), required=True, widget=forms.TextInput(attrs=input_attrs))
    job_description = forms.CharField(label=_("Краткая характеристика компании/организации"), required=True, widget=forms.Textarea(attrs=input_attrs))
    experience_years = forms.IntegerField(label=_("Общий стаж в PR/медиа"), required=True, widget=forms.NumberInput(attrs=input_attrs))
    professional_description = forms.CharField(label=_("Краткое описание профессиональной деятельности"), required=True, widget=forms.Textarea(attrs=input_attrs))

    # Достижения
    skills = forms.CharField(label=_("Знания, навыки, сертификаты"), required=False, widget=forms.Textarea(attrs=input_attrs))
    awards = forms.CharField(label=_("Награды, дипломы, признание"), required=False, widget=forms.Textarea(attrs=input_attrs))
    publications = forms.CharField(label=_("Публикации, авторские проекты"), required=False, widget=forms.Textarea(attrs=input_attrs))

    # Мотивация
    motivation = forms.CharField(label=_("Почему вы хотите вступить в Ассоциацию?"), required=True, widget=forms.Textarea(attrs=input_attrs))
    interests = forms.MultipleChoiceField(
        label=_("Какие направления вам наиболее интересны?"),
        required=False,
        choices=[
            ('Образование', _("Образование и повышение квалификации")),
            ('Мероприятия', _("Мероприятия и профессиональные встречи")),
            ('Законы', _("Законодательные инициативы")),
            ('Другое', _("Другое")),
        ],
        widget=forms.CheckboxSelectMultiple
    )

    recommender = forms.CharField(label=_("Кто из pr специалистов с опытом работы от 7 лет может выступить вашим рекомендателем"), required=False, widget=forms.TextInput(attrs=input_attrs))

    # Резюме
    resume = forms.FileField(label=_("Резюме"), required=False, widget=forms.ClearableFileInput(attrs=input_attrs))

    # Согласия
    confirm_data = forms.BooleanField(label=_("Я подтверждаю достоверность указанных данных."), required=True)
    consent_personal_data = forms.BooleanField(label=_("Я согласен(а) на обработку персональных данных."), required=True)
    