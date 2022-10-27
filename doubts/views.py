from django.shortcuts import render,redirect
from django.views.generic import TemplateView,CreateView,FormView,ListView
from doubts.forms import RegistrationForm,LoginForm,QuestionForm
from doubts.models import MyUser, Questions
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

    