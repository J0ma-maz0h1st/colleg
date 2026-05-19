from django.views.generic import TemplateView


class HomePageView(TemplateView):
    """Публичная главная: заявка, новости, о нас, FAQ (данные с API подгружает шаблон)."""
    template_name = "home/index.html"
