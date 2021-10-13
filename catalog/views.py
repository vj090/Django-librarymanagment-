from django.shortcuts import render
from .forms import NameForm
from .models import Book, Author, BookInstance
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
import datetime
from django.views.generic import View
from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.urls import reverse
from .forms import RenewBookForm, FeedBackForm, VenueForm
from django.views.generic import TemplateView
from django.http import HttpResponseRedirect
from datetime import datetime
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy



class IndexView(TemplateView):
    template_name = "index.html"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        # Generate counts of some of the main objects
        context['num_books'] = Book.objects.all().count()
        context['num_instances'] = BookInstance.objects.all().count()
        context['num_instances_available'] = BookInstance.objects.filter(status__exact='a').count()
        context['num_authors'] = Author.objects.count()

        return context


class BookListView(generic.ListView):
    model = Book
    paginate_by = 10


class BookDetailView(generic.DetailView):
    model = Book

    def book_detail_view(request, primary_key):
        book = get_object_or_404(Book, pk=primary_key)
        return render(request, 'catalog/book_detail.html', context={'book': book})


class GetNameView(View):
    template_name = 'name.html'
    form_class = NameForm

    def get(self, request, template_name=template_name, *args, **kwargs):
        form = self.form_class
        return render(request, template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            # form.save()
            # return HttpResonseRedirect(reverse('list-view'))
            return HttpResponse('/thanks/')
        else:
            return render(request, self.template_name, {'form': form})


class LoanedBooksByUserListView(LoginRequiredMixin, generic.ListView):
    """Generic class-based view listing books on loan to current user."""
    model = BookInstance
    template_name = 'catalog/bookinstance_list_borrowed_user.html'
    paginate_by = 10

    def get_queryset(self):
        return BookInstance.objects.filter(borrower=self.request.user).filter(status__exact='o').order_by('due_back')


@login_required
@permission_required('catalog.can_mark_returned', raise_exception=True)
def renew_book_librarian(request, pk):
    """View function for renewing a specific BookInstance by librarian."""
    book_instance = get_object_or_404(BookInstance, pk=pk)

    # If this is a POST request then process the Form data
    if request.method == 'POST':

        # Create a form instance and populate it with data from the request (binding):
        form = RenewBookForm(request.POST)

        # Check if the form is valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required (here we just write it to the model due_back field)
            book_instance.due_back = form.cleaned_data['renewal_date']
            book_instance.save()

            ref_book = book_instance.book.id
            print("Refr to -->", ref_book)

            book = Book.objects.get(pk=ref_book)
            print("book-->", book)

            ref_book_all_instance = book.bookinstance_set.all()
            print("ref_book_all_instance-->", ref_book_all_instance)

            # redirect to a new URL:
            return HttpResponseRedirect(reverse('index'))

    # If this is a GET (or any other method) create the default form.
    else:
        proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)
        form = RenewBookForm(initial={'renewal_date': proposed_renewal_date})

    context = {
        'form': form,
        'book_instance': book_instance,
    }

    return render(request, 'catalog/book_renew_librarian.html', context)


class AuthorListView(generic.ListView):
    template_name = 'catalog/author.html'
    context_object_name = 'all_author'

    def get_queryset(self):
        all_author = Author.objects.all()

        return all_author


class AuthorDetailView(generic.DetailView):
    model = Author

    def get_author_detail(request, primary_key):
        author = get_object_or_404(Author, pk=primary_key)
        return render(request, 'author_detail.html', context={'author': author})


@login_required
def feedback(request):
    """
    Fun for the django Form feedback handling
    """
    submitted = False
    if request.method == 'POST':
        form = FeedBackForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            # assert False
            return HttpResponseRedirect(reverse('thanks'))
        # form = FeedBackForm()
        # if 'submitted' in request.GET:
        #     submitted = True

    else:
        form = FeedBackForm(request.GET)

    context = {
        'form': form,
    }
    return render(request, 'feedback.html', context)

class ThanksView(TemplateView):
    """
    return Thanks Template
    """
    template_name = "thanks.html"

class FeedbackFormView(LoginRequiredMixin, View):
    template_name = 'add_venue.html'

    def get(self, request, template_name=template_name, *args, **kwargs):
        form = VenueForm()
        submitted = False
        if 'submitted' in request.GET:
            submitted = True
        return render(request, template_name, {'form': form,
                                               'submitted': submitted})

    def post(self, request, *args, **kwargs):
        form = VenueForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/catalog/add_venue/?submitted=True')
        else:
            return HttpResponse("Form data is invalid****")

class AuthorCreateView(CreateView):
    model = Author
    fields = ['first_name', 'last_name']


class AuthorUpdateView(UpdateView):
    model = Author
    fields = ['first_name', 'last_name']
    template_name_suffix = '_update_form'


class AuthorDeleteView(DeleteView):
    model = Author
    success_url = reverse_lazy('')

def Dellogin(request):
    return render(request, 'login_page.html')
