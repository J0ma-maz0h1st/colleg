from django.db import models
from django.conf import settings
from courses.models import Module


class Lesson(models.Model):
    module = models.ForeignKey(Module, on_delete=models.CASCADE, related_name='lessons')
    title = models.CharField(max_length=255)
    order = models.PositiveIntegerField(default=1)

    description = models.TextField(blank=True)
    content = models.TextField(blank=True)  # текст урока или markdown

    video_url = models.URLField(blank=True, null=True)          # YouTube / Vimeo / HLS
    video_file = models.FileField(upload_to='lessons/videos/', blank=True, null=True)

    duration_minutes = models.PositiveIntegerField(default=0)
    is_preview = models.BooleanField(default=False)  # бесплатный preview

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['module__course', 'module__order', 'order']
        unique_together = ('module', 'order')

    def __str__(self):
        return f"{self.module.course.title} - {self.title}"
    
    class Meta:
        verbose_name = "Урок"
        verbose_name_plural = "Уроки"


class LessonFile(models.Model):
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='files')
    file = models.FileField(upload_to='lessons/files/')
    title = models.CharField(max_length=200)

    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = "Файл урока"
        verbose_name_plural = "Файлы уроков"