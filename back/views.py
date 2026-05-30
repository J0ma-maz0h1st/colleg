from django.shortcuts import render
from info.models import News, FAQ, AboutSection
from courses.models import Direction

def landing_view(request):
    # Получаем данные из баз данных согласно твоей последовательности
    directions = Direction.objects.all()
    news_list = News.objects.all()[:3]  # Берем 3 последние новости
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