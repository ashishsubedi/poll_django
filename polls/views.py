from django.shortcuts import render
from django.http import HttpResponse, Http404, HttpResponseRedirect

from django.shortcuts import render,get_object_or_404
from .models import Question,Choice
from django.urls import reverse
from django.db.models import F
from django.views import generic

from .models import Question

class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        return Question.objects.order_by('-pub_date')[:5]

class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'

class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'


def vote(request,question_id):
    question = get_object_or_404(Question,id=question_id)
    try:
        print(request.POST['choice'])
        selected_choice = question.choice_set.get(id=request.POST['choice'])
    except (KeyError,Choice.DoesNotExist):
        return render(request,'polls/detail.html',{
            'question':question,
            'error_message':"You didn't select a choice",
        })
    else:
        # F() for avoiding race condition on database
        selected_choice.votes = F('votes')+1
        selected_choice.save()
        return HttpResponseRedirect(reverse('polls:results',args=(question.id,)))

