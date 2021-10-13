from django.shortcuts import render
from django.http import HttpResponse
from django.views import generic
from .models import Question, Choice
from .forms import QuizForm, ContactForm
from django.views.generic.edit import FormView
from django.views.generic import TemplateView
import csv


class IndexView(TemplateView):
    """
    Template View for quiz index (Home) page
    """
    template_name = "quiz_index.html"

class QuestionListView(generic.ListView):
    """
    Question List View page
    return : all questions of question model
    """
    template_name = 'quiz/Question_list.html'
    context_object_name = 'all_question'

    def get_queryset(self):
        return Question.objects.all().order_by("pub_date")

def quiz_result(request):
    """
    return: score of quiz
    """
    if request.method == 'POST':

        # To implement the session data
        num_visits = request.session.get('num_visits', 0)
        request.session['num_visits'] = num_visits + 1

        score = 0

        # The first item in the post is csrf token
        request_post_items = list(request.POST.items())
        question_choice_list = request_post_items[1:]

        for each in question_choice_list:

            # get the id & object
            question = Question.objects.get(question_text__exact=each[0])
            selected_choices = Choice.objects.get(pk=each[1])

            if selected_choices == question.get_correct_answer:
                score += 1

        result = {'score': score,
                  'num_visits': num_visits,
                  }
        return render(request, 'quiz/quiz_result.html', context=result)

    return render(request, 'quiz_index.html')

class ContactFormView(FormView):
    """
    class base view for the FormerView
    """
    template_name = 'contact.html'
    form_class = ContactForm
    success_url = '/catalog/thanks/'

def get_answer_sheet_csv(request):
    """
    Generate the answer sheet csv file
    """
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="Answer sheet.csv"'

    questions = Question.objects.all()

    header = ['Questions', 'Answers']

    writer = csv.DictWriter(response, fieldnames=header)
    writer.writeheader()

    writer = csv.writer(response)
    for question in questions:
        correct_answer = question.get_correct_answer
        writer.writerow([question.question_text, correct_answer])
    return response
