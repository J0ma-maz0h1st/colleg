from django.shortcuts import render
from info.models import News, FAQ, AboutSection
from courses.models import Direction, Course  # Добавили Course

# 1. Лендинг (остается без изменений)
def landing_view(request):
    directions = Direction.objects.all()
    news_list = News.objects.all()[:3]
    about_sections = AboutSection.objects.all()
    faq_items = FAQ.objects.all()

    context = {
        'page_type': 'landing',
        'directions': directions,
        'news_list': news_list,
        'about_sections': about_sections,
        'faq_items': faq_items,
    }
    return render(request, 'home/landing.html', context)


# 2. Главная страница (Дашборд с Каталогом Курсов)
def main_dashboard_view(request):
    # Вытягиваем все курсы с предзагрузкой направлений для оптимизации запросов
    courses = Course.objects.select_related('direction').all()
    
    context = {
        'page_type': 'main',
        'courses': courses,
    }
    # Рендерим новый шаблон дашборда
    return render(request, 'dashboard/dashboard.html', context)


# 3. Личный кабинет (Заглушка на будущее)
def profile_view(request, pk):
    context = {
        'page_type': 'profile',
        'profile_id': pk,  # Передаем ID в шаблон
    }
    return render(request, 'profile/profile.html', context)