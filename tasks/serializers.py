from rest_framework import serializers
from .models import Tasks, Answers, Question, TestResult


class TasksSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tasks
        fields = ['id', 'title', 'description', 'group', 'created_at', 'updated_at', 'deadline', 'file', 'photo']


class TaskListSerializer(serializers.ModelSerializer):
    group = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Tasks
        fields = ['id', 'title', 'description', 'group', 'created_at', 'updated_at', 'deadline']


class AnswerSerializer(serializers.ModelSerializer):
    task = serializers.PrimaryKeyRelatedField(queryset=Tasks.objects.all())

    class Meta:
        model = Answers
        fields = ['id', 'task', 'content', 'submitted_at', 'is_approved', 'file', 'photo']
        read_only_fields = ['submitted_at', 'is_approved']
    

class AnswerListSerializer(serializers.ModelSerializer):
    student = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Answers
        fields = ['id', 'task', 'student', 'content', 'submitted_at', 'is_approved']


class AnswerDetailSerializer(serializers.ModelSerializer):
    student = serializers.StringRelatedField(read_only=True)
    task = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Answers
        fields = ['id', 'task', 'student', 'content', 'submitted_at', 'is_approved', 'file', 'photo']


class QuestionSerializer(serializers.ModelSerializer):
    option1 = serializers.CharField(write_only=True, label="Вариант 1")
    option2 = serializers.CharField(write_only=True, label="Вариант 2")
    option3 = serializers.CharField(write_only=True, label="Вариант 3")
    option4 = serializers.CharField(write_only=True, label="Вариант 4")

    class Meta:
        model = Question
        fields = [
            'id', 'text', 'category', 'correct_answer', 'options', 
            'option1', 'option2', 'option3', 'option4'
        ]
        read_only_fields = ['options']

    def validate(self, data):
        options = [
            data.get('option1'), 
            data.get('option2'), 
            data.get('option3'), 
            data.get('option4')
        ]
        correct = data.get('correct_answer')

        if correct not in options:
            raise serializers.ValidationError({
                "correct_answer": f"Ошибка! Правильный ответ '{correct}' должен совпадать с одним из вариантов."
            })
        return data

    def create(self, validated_data):
        option1 = validated_data.pop('option1')
        option2 = validated_data.pop('option2')
        option3 = validated_data.pop('option3')
        option4 = validated_data.pop('option4')
        
        validated_data['options'] = [option1, option2, option3, option4]
        return super().create(validated_data)
    

class TakeTestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ['id', 'text', 'options']


class TestResultCreateSerializer(serializers.ModelSerializer):
    # ЗАЩИТА: Автоматически подставляет текущего залогиненного юзера, поле скрыто от ввода клиента
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = TestResult
        fields = ['id', 'user', 'score', 'total_questions', 'start_time', 'end_time', 'answers']
        read_only_fields = ['score', 'total_questions', 'end_time']
    
    def create(self, validated_data):
        user_answers = validated_data.pop('answers')
        
        # Парсим ID вопросов из ответов пользователя
        question_ids = [int(q_id) for q_id in user_answers.keys()]
        questions = Question.objects.filter(id__in=question_ids)
        
        # Сверяем ответы во внутреннем цикле
        score = 0
        for question in questions:
            q_id_str = str(question.id)
            if q_id_str in user_answers:
                if str(user_answers[q_id_str]).strip() == str(question.correct_answer).strip():
                    score += 1
        
        # Записываем результат
        test_result = TestResult.objects.create(
            user=validated_data['user'],
            score=score,
            total_questions=len(questions),
            start_time=validated_data['start_time'],
            answers=user_answers
        )
        return test_result