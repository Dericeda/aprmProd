# myapp/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from .forms import AssociationMemberForm, MemberFilterForm, AvatarForm
from users.models import AssociationMember
from news.models import News
from myapp.models import Specialist
import requests
from django.template.loader import render_to_string
from django.http import JsonResponse, HttpResponse
from .forms import CRMApplicationForm
import json
from django.core.files.storage import default_storage
from django.conf import settings
from .models import Course, CourseCategory
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from .models import Specialist
from .forms import ExtendedApplicationForm 
from django.contrib import messages


def category_detail(request, slug):
    category = get_object_or_404(CourseCategory, slug=slug)
    courses = Course.objects.filter(category=category)
    return render(request, 'category_detail.html', {
        'category': category,
        'courses': courses
    })

def course_detail(request, pk):
    course = get_object_or_404(Course, pk=pk)
    return render(request, 'course_detail.html', {'course': course})
    
def specialist_list(request):
    specialists = Specialist.objects.filter(moderation_status='approved')

    # Получаем параметры
    category = request.GET.get('category')
    city = request.GET.get('city')
    specialization = request.GET.get('specialization')
    has_cases = request.GET.get('cases')
    is_member = request.GET.get('member')

    if category:
        specialists = specialists.filter(category=category)
    if city:
        specialists = specialists.filter(city=city)
    if specialization:
        specialists = specialists.filter(specialization=specialization)
    if has_cases == 'yes':
        specialists = specialists.exclude(cases__exact='')
    if is_member == 'yes':
        specialists = specialists.filter(is_member=True)
    elif is_member == 'no':
        specialists = specialists.filter(is_member=False)

    context = {
        'specialists': specialists,
        'categories': Specialist.objects.values_list('category', flat=True).distinct(),
        'cities': Specialist.objects.values_list('city', flat=True).distinct(),
        'specializations': Specialist.objects.values_list('specialization', flat=True).distinct(),
        'selected': {
            'category': category,
            'city': city,
            'specialization': specialization,
            'cases': has_cases,
            'member': is_member,
        }
    }

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        html = render_to_string('partials/_specialist_list.html', context, request=request)
        return JsonResponse({'html': html})

    return render(request, 'specialists/list.html', context)

def upload_file_to_bitrix(file, filename):
    upload_url = 'https://b24-g0wr9u.bitrix24.kz/rest/1/yd2xd3xr9fa53hqp/disk.folder.uploadfile.json'
    folder_id = 0  # ID папки (0 = корневая)
    
    response = requests.post(upload_url, files={'file': (filename, file)}, data={
        'id': folder_id,
        'generateUniqueName': 'Y'
    })
    
    result = response.json()
    print("📎 Bitrix upload:", result)
    if 'result' in result:
        return result['result']['ID']
    return None


def index(request):
    latest_courses = Course.objects.order_by('-id')[:5]
    course_categories = CourseCategory.objects.all()
    specialist_categories = Specialist.objects.values_list('category', flat=True).distinct()
    cities = Specialist.objects.values_list('city', flat=True).distinct()
    specializations = Specialist.objects.values_list('specialization', flat=True).distinct()

    # Получаем учредителей - первые 5 одобренных специалистов
    founders = Specialist.objects.filter(
        moderation_status='approved'
    ).order_by('created_at')[:5]

    # Параметры фильтрации
    category = request.GET.get('category')
    city = request.GET.get('city')
    specialization = request.GET.get('specialization')
    has_cases = request.GET.get('cases')
    is_member = request.GET.get('member')

    specialists = Specialist.objects.filter(moderation_status='approved')
    if category:
        specialists = specialists.filter(category=category)
    if city:
        specialists = specialists.filter(city=city)
    if specialization:
        specialists = specialists.filter(specialization=specialization)
    if is_member == 'yes':
        specialists = specialists.filter(is_member=True)
    elif is_member == 'no':
        specialists = specialists.filter(is_member=False)

    if not request.headers.get('x-requested-with') == 'XMLHttpRequest':
        specialists = specialists[:5]

    if request.headers.get('x-requested-with') == 'XMLHttpRequest' and request.method == 'GET':
        return render(request, 'partials/_specialist_list.html', {
            'specialists': specialists
        })

    form = ExtendedApplicationForm()

    if request.method == 'POST':
        form = ExtendedApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                data = form.cleaned_data
                
                # Создаём объект специалиста
                specialist = Specialist()
                specialist.full_name = f"{data['last_name']} {data['first_name']} {data.get('middle_name', '')}".strip()
                specialist.email = data['email']
                specialist.phone = data['phone']
                specialist.city = data['city']
                specialist.specialization = ', '.join(data.get('interests', [])) or 'Не указано'
                specialist.position = data['job_title']
                specialist.workplace = data['job_place']
                specialist.about = data['professional_description']
                specialist.category = data['degree']
                specialist.social_links = data['social_links']
                specialist.job_region = data['job_region']
                specialist.job_description = data['job_description']
                specialist.experience_years = data['experience_years']
                specialist.skills = data.get('skills', '')
                specialist.awards = data.get('awards', '')
                specialist.publications = data.get('publications', '')
                specialist.motivation = data.get('motivation', '')
                specialist.recommender = data.get('recommender', '')
                specialist.moderation_status = 'pending'
                
                # Дополнительные поля для Specialist модели
                specialist.additional_phone = data.get('additional_phone', '')
                specialist.birth_date = data.get('birth_date')
                specialist.citizenship = data.get('citizenship', '')
                specialist.university = data.get('university', '')
                specialist.faculty = data.get('faculty', '')
                specialist.study_years = data.get('study_years', '')
                specialist.degree = data.get('degree', '')
                specialist.professional_description = data.get('professional_description', '')
                specialist.interests = ', '.join(data.get('interests', []))
                specialist.confirm_data = data.get('confirm_data', False)
                specialist.consent_personal_data = data.get('consent_personal_data', False)
                
                # Добавляем фото ПЕРЕД сохранением
                photo_file = request.FILES.get('photo')
                if photo_file:
                    specialist.photo = photo_file

                # Добавляем файлы ПЕРЕД сохранением
                resume_file = request.FILES.get('resume')
                documents_file = request.FILES.get('documents')
                
                if resume_file:
                    specialist.resume = resume_file
                    
                if documents_file:
                    specialist.documents = documents_file

                # СОХРАНЯЕМ ТОЛЬКО ОДИН РАЗ
                specialist.save()

                # Теперь обрабатываем файлы для отправки в Bitrix
                file_links = []
                
                if resume_file:
                    try:
                        full_url = request.build_absolute_uri(specialist.resume.url)
                        file_links.append(f"Резюме: {full_url}")
                    except Exception as e:
                        print(f"Ошибка получения URL резюме: {e}")

                if documents_file:
                    try:
                        full_url = request.build_absolute_uri(specialist.documents.url)
                        file_links.append(f"Документы: {full_url}")
                    except Exception as e:
                        print(f"Ошибка получения URL документов: {e}")

                # Добавляем ссылку на фото в комментарии
                if photo_file and specialist.photo:
                    try:
                        photo_url = request.build_absolute_uri(specialist.photo.url)
                        file_links.append(f"Фото: {photo_url}")
                    except Exception as e:
                        print(f"Ошибка получения URL фото: {e}")

                # Формируем текст комментария
                comments = (
                    f"ФИО: {specialist.full_name}\n"
                    f"Дата рождения: {data.get('birth_date', 'Не указано')}\n"
                    f"Гражданство: {data.get('citizenship', 'Не указано')}\n"
                    f"Город: {data['city']}\n\n"
                    f"Телефон: {data['phone']}\n"
                    f"Доп. телефон: {data.get('additional_phone', 'Не указано')}\n"
                    f"Email: {data['email']}\n"
                    f"Соцсети: {data['social_links']}\n\n"
                    f"Образование: {data.get('university', '')}, {data.get('faculty', '')}, {data.get('study_years', '')}, {data.get('degree', '')}\n\n"
                    f"Работа: {data['job_place']}, {data['job_title']}, {data['job_region']}\n"
                    f"О компании: {data['job_description']}\n"
                    f"Стаж: {data['experience_years']} лет\n\n"
                    f"Описание деятельности: {data['professional_description']}\n"
                    f"Навыки: {data.get('skills', 'Не указано')}\n"
                    f"Награды: {data.get('awards', 'Не указано')}\n"
                    f"Публикации: {data.get('publications', 'Не указано')}\n\n"
                    f"Мотивация: {data['motivation']}\n"
                    f"Интересы: {', '.join(data.get('interests', ['Не указано']))}\n"
                    f"Рекомендатель: {data.get('recommender', 'Не указано')}\n\n"
                    + "\n".join(file_links)
                )

                # Отправка в Bitrix24
                try:
                    url = 'https://b24-g0wr9u.bitrix24.kz/rest/1/yd2xd3xr9fa53hqp/crm.lead.add.json'
                    payload = {
                        'fields': {
                            'TITLE': f'Расширенная заявка: {specialist.full_name}',
                            'NAME': specialist.full_name,
                            'EMAIL': [{'VALUE': data['email'], 'VALUE_TYPE': 'WORK'}],
                            'PHONE': [{'VALUE': data['phone'], 'VALUE_TYPE': 'WORK'}],
                            'COMMENTS': comments,
                        }
                    }
                    response = requests.post(url, json=payload, timeout=10)
                    print(f"Bitrix response: {response.status_code}, {response.text}")
                except Exception as e:
                    print(f"Ошибка отправки в Bitrix: {e}")

                if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                    return JsonResponse({'success': True})
                else:
                    messages.success(request, 'Ваша заявка успешно отправлена!')
                    return redirect('success')

            except Exception as e:
                print(f"Ошибка обработки формы: {e}")
                if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                    return JsonResponse({'success': False, 'errors': {'general': ['Произошла ошибка при обработке заявки']}}, status=500)
                else:
                    messages.error(request, 'Произошла ошибка при отправке заявки. Попробуйте еще раз.')

        else:
            print("Форма невалидна:", form.errors)
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'success': False, 'errors': form.errors}, status=400)
            else:
                messages.error(request, 'Пожалуйста, исправьте ошибки в форме.')

    latest_news = News.objects.order_by('-date')[:6]

    return render(request, 'index.html', {
        'latest_news': latest_news,
        'form': form,
        'specialists': specialists,
        'founders': founders,  # Добавляем учредителей в контекст
        'specialist_categories': specialist_categories,
        'cities': cities,
        'specializations': specializations,
        'selected': {
            'category': category,
            'city': city,
            'specialization': specialization,
            'cases': has_cases,
            'member': is_member,
        },
        'latest_courses': latest_courses,
        'course_categories': course_categories
    })

def registration(request):
    return render(request, 'registration.html')


@login_required
def dashboard(request):
    try:
        member = AssociationMember.objects.get(user=request.user)
    except AssociationMember.DoesNotExist:
        # ❗Если участник не найден, направляем на страницу заявки
        return redirect('join_association')

    if request.method == 'POST':
        form = AvatarForm(request.POST, request.FILES, instance=member)
        if form.is_valid():
            if form.cleaned_data.get('remove_avatar') and member.avatar:
                member.avatar.delete()
            form.save()
    else:
        form = AvatarForm(instance=member)

    return render(request, 'dashboard.html', {'form': form, 'member': member})


def success(request):
    return render(request, 'success.html')


@login_required
def news_list(request):
    news = News.objects.order_by('-date')
    return render(request, 'news/news_list.html', {'news': news})


@login_required
def news_detail(request, news_id):
    news = get_object_or_404(News, id=news_id)

    session_key = f'viewed_news_{news_id}'
    if not request.session.get(session_key, False):
        news.views += 1
        news.save()
        request.session[session_key] = True

    youtube_embed_url = ""
    if news.youtube_url:
        youtube_embed_url = news.youtube_url.replace("watch?v=", "embed/")

    return render(request, 'news/news_detail.html', {
        'news': news,
        'youtube_embed_url': youtube_embed_url
    })

def join_association(request):
    form = CRMApplicationForm()

    if request.method == 'POST':
        form = CRMApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            data = form.cleaned_data

            # Загрузка файлов
            files = {
                'motivation': request.FILES.get('motivation_letter'),
                'photo': request.FILES.get('photo'),
                'documents': request.FILES.get('documents'),
            }

            # Заменить URL на свой вебхук
            url = 'https://b24-g0wr9u.bitrix24.kz/rest/1/ghwj5017jkpq2trb/crm.lead.add.json'

            payload = {
                'fields': {
                    'TITLE': 'Новая заявка с сайта',
                    'NAME': data['full_name'],
                    'EMAIL': [{'VALUE': data['email'], 'VALUE_TYPE': 'WORK'}],
                    'PHONE': [{'VALUE': data['phone'], 'VALUE_TYPE': 'WORK'}],
                    'COMMENTS': f"""
                        Должность: {data['position']}
                        Место работы: {data['workplace']}
                        Instagram: {data['instagram']}
                    """,
                }
            }

            requests.post(url, data=payload, files={
                'UF_CRM_FILE_1': files['motivation'],
                'UF_CRM_FILE_2': files['photo'],
                'UF_CRM_FILE_3': files['documents'],
            })

            return render(request, 'success.html')

    return render(request, 'join_form.html', {'form': form})


@login_required
def members_list(request):
    form = MemberFilterForm(request.GET or None)
    members = AssociationMember.objects.all()

    if form.is_valid():
        position = form.cleaned_data.get('position')
        workplace = form.cleaned_data.get('workplace')
        if position:
            members = members.filter(position=position)
        if workplace:
            members = members.filter(workplace=workplace)

    return render(request, 'templates/users/member_list.html', {'members': members, 'form': form})


def course(request):
    courses = Course.objects.all()
    return render(request, 'course_list.html', {'courses': courses})