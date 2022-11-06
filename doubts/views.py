from ast import For
from django.shortcuts import render,redirect
from django.views.generic import TemplateView,CreateView,FormView,ListView,DetailView,DeleteView
from doubts.forms import RegistrationForm,LoginForm,QuestionForm,AnswerForm
from doubts.models import MyUser, Questions,Answers
from django.urls import reverse_lazy
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache

def signin_reqiured(fn):
    def wrapper(request,*args,**kwargs):
        if not request.user.is_authenticated:
            return redirect("signin")
        else:
            return fn(request,*args,**kwargs)
    return wrapper

decs=[signin_reqiured,never_cache]

@method_decorator(decs,name="dispatch")
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

@method_decorator(decs,name="dispatch")
class QuestionDetailView(DetailView,FormView):
    model = Questions
    template_name = "question-detail.html"
    pk_url_kwarg = "id"
    context_object_name = "question"
    form_class = AnswerForm

decs
def add_answer(request,*args,**kwargs):
    if request.method=="POST":
        form = AnswerForm(request.POST)
        if form.is_valid():
            answer = form.cleaned_data.get("answer")
            qid = kwargs.get("id")
            ques = Questions.objects.get(id=qid)
            Answers.objects.create(question=ques,user = request.user,answer=answer)
            return redirect("index")

        else:
            return redirect("index")


decs
def upvote_view(request,*args,**kwargs):
    ans_id = kwargs.get("id")
    ans = Answers.objects.get(id=ans_id)
    ans.upvote.add(request.user)
    ans.save()
    return redirect("index")

decs
def signout_view(request,*args,**kwargs):
    logout(request)
    return redirect("signin")

decs
def remove_view(request,*args,**kwargs):
    ans_id = kwargs.get("id")
    Answers.objects.get(id = ans_id).delete()
    return redirect("index")
    
                           