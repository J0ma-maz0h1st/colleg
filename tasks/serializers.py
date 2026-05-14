from .models import Tasks, Answers, Question, TestResult   
from rest_framework import serializers


class TasksSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tasks
        fields = ['id', 'title', 'description', 'group', 'created_at', 'updated_at', 'file', 'photo']


class TaskListSerializer(serializers.ModelSerializer):
    group = serializers.StringRelatedField(read_only=True)
    class Meta:
        model = Tasks
        fields = ['id', 'title', 'description', 'group', 'created_at', 'updated_at']


class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answers
        fields = ['id', 'task', 'student', 'content', 'submitted_at', 'is_approved', 'file', 'photo']
    
class AnswerListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answers
        fields = ['id', 'task', 'student', 'content', 'submitted_at', 'is_approved']

# 1. Для добавления вопросов (AddQuestionView)


class QuestionSerializer(serializers.ModelSerializer):
    # Виртуальные поля для ввода в Swagger
    option1 = serializers.CharField(write_only=True, label="Вариант 1")
    option2 = serializers.CharField(write_only=True, label="Вариант 2")
    option3 = serializers.CharField(write_only=True, label="Вариант 3")
    option4 = serializers.CharField(write_only=True, label="Вариант 4")

    class Meta:
        model = Question
        # Поля, которые будут видны в API
        fields = [
            'id', 'text', 'category', 'correct_answer', 'options', 
            'option1', 'option2', 'option3', 'option4'
        ]
        # options теперь заполняется автоматически, поэтому только для чтения
        read_only_fields = ['options']

    def validate(self, data):
        """
        Проверяем, что правильный ответ совпадает с одним из введенных вариантов.
        """
        # Собираем все введенные варианты в один список для проверки
        options = [
            data.get('option1'), 
            data.get('option2'), 
            data.get('option3'), 
            data.get('option4')
        ]
        
        correct = data.get('correct_answer')

        if correct not in options:
            raise serializers.ValidationError({
                "correct_answer": (
                    f"Ошибка! Правильный ответ '{correct}' не найден среди "
                    f"введенных вариантов. Проверьте опечатки."
                )
            })
            
        return data

    def create(self, validated_data):
        # Собираем варианты в массив для JSONField
        option1 = validated_data.pop('option1')
        option2 = validated_data.pop('option2')
        option3 = validated_data.pop('option3')
        option4 = validated_data.pop('option4')
        
        validated_data['options'] = [option1, option2, option3, option4]
        
        # Создаем запись в БД
        return super().create(validated_data)
    
# 1. Выдача вопросов (только текст и варианты)
class TakeTestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ['id', 'text', 'options']

# 2. Прием результатов теста
class TestResultCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestResult
        fields = ['id', 'user', 'score', 'total_questions', 'start_time', 'end_time', 'answers']
        read_only_fields = ['score', 'total_questions', 'end_time']
    
    def create(self, validated_data):
        # Получаем ответы пользователя из данных
        user_answers = validated_data.pop('answers')
        
        # Получаем все вопросы, на которые отвечал пользователь
        question_ids = [int(q_id) for q_id in user_answers.keys()]
        questions = Question.objects.filter(id__in=question_ids)
        
        # Сверяем ответы и считаем баллы
        score = 0
        for question in questions:
            q_id_str = str(question.id)
            if q_id_str in user_answers:
                if user_answers[q_id_str] == question.correct_answer:
                    score += 1
        
        # Сохраняем результат теста с подсчитанным счетом и количеством вопросов
        test_result = TestResult.objects.create(
            user=validated_data['user'],
            score=score,
            total_questions=len(questions),
            start_time=validated_data['start_time'],
            answers=user_answers
        )
        
        return test_result