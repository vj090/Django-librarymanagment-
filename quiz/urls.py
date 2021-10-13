from django.urls import path
from . import views

app_name = 'quiz'

urlpatterns = [
    path('', views.IndexView.as_view(), name='quiz-index'),
    path('questions/', views.QuestionListView.as_view(), name="questions"),
    path('contact/', views.ContactFormView.as_view(), name="contact"),
    path('quiz_result/', views.quiz_result, name="quiz-result"),
    path('csv/', views.get_answer_sheet_csv, name="get-csv"),
]
