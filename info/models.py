from django.db import models

class News(models.Model):
    title = models.CharField(max_length=255, verbose_name="Заголовок")
    slug = models.SlugField(unique=True, blank=True, null=True, verbose_name="URL-префикс (slug)")
    content = models.TextField(verbose_name="Содержание новости")
    image = models.ImageField(upload_to='news/', null=True, blank=True, verbose_name="Изображение")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата публикации")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")

    class Meta:
        verbose_name = "Новость"
        verbose_name_plural = "Новости"
        ordering = ['-created_at']

    def __str__(self):
        return self.title


class FAQ(models.Model):
    question = models.CharField(max_length=255, verbose_name="Вопрос")
    answer = models.TextField(verbose_name="Ответ")
    order = models.PositiveIntegerField(default=0, verbose_name="Порядок сортировки")

    class Meta:
        verbose_name = "Часто задаваемый вопрос (FAQ)"
        verbose_name_plural = "Часто задаваемые вопросы (FAQ)"
        ordering = ['order']

    def __str__(self):
        return self.question


class AboutSection(models.Model):
    title = models.CharField(max_length=255, verbose_name="Заголовок секции")
    content = models.TextField(verbose_name="Текст")
    image = models.ImageField(upload_to='about/', null=True, blank=True, verbose_name="Изображение")
    order = models.PositiveIntegerField(default=0, verbose_name="Порядок вывода")

    class Meta:
        verbose_name = "Секция 'О нас'"
        verbose_name_plural = "Секции 'О нас'"
        ordering = ['order']

    def __str__(self):
        return self.title