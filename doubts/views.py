from django.shortcuts import render,redirect
from django.views.generic import TemplateView,CreateView,FormView,ListView,DetailView
from doubts.forms import RegistrationForm,LoginForm,QuestionForm
from doubts.models import MyUser, Questions,Answers
from django.urls import reverse_lazy
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages


class IndexView(CreateView,ListView):
    template_name = "home.html"
    form_class = QuestionForm
    model = Questions
    success_url = reverse_lazy("index")
    context_object_name="questions"

    def get_queryset(self):
         return Questions.objects.all().exclude(user=self.request.user)

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class SignupView(CreateView):
    model = MyUser
    form_class = RegistrationForm
    template_name = 'register.html'
    success_url = reverse_lazy("register") 

class LoginView(FormView):
        form_class = LoginForm
        template_name="login.html"

        def post(self,request,*args,**kwargs):
            form = LoginForm(request.POST)
            if form.is_valid():
                uname = form.cleaned_data.get("username")
                pwd = form.cleaned_data.get("password")
                usr = authenticate(request,username=uname,password=pwd)
                if usr:
                    login(request,usr)
                    return redirect("index")
                else:
                    messages.error(request,"invalid credentials")
                    return render(request,self.template_name,{"form":form})

class QuestionDetailView(DetailView):
    model = Questions
    template_name = "question-detail.html"
    pk_url_kwarg = "id"
    context_object_name = "question"

def add_answer(request,*args,**kwargs):
    qid = kwargs.get("id")
    question = Questions.objects.get(id=qid)
    answer = request.POST.get("answer")
    Answers.objects.create(user = request.user,answer = answer,question = question)
    #question.answers_set.create(user = request.user, answer = answer)
    return redirect("index")
    
def upvote_view(request,*args,**kwargs):
    ans_id = kwargs.get("id")
    ans = Answers.objects.get(id=ans_id)
    ans.upvote.add(request.user)
    ans.save()
    return redirect("index")
                           