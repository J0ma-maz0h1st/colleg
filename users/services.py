from .models import Student

def update_student_potential(student: Student, speed_factor=0.0, attempts=1, recommendations=0):
    """Вызывать после каждой сданной задачи"""
    student.total_speed_score = (student.total_speed_score + speed_factor) / 2  # сглаживание
    student.total_attempts += attempts
    student.total_recommendations += recommendations
    student.update_potential_points()
    return student.potential_points