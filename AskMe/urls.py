"""AskMe URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from doubts.views import IndexView,SignupView,LoginView,QuestionDetailView,add_answer,upvote_view,signout_view,remove_view
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('index',IndexView.as_view(),name = "index"),
    path('register',SignupView.as_view(),name='register'),
    path('',LoginView.as_view(),name='signin'),
    path("questions/<int:id>/detail",QuestionDetailView.as_view(),name = "detail"),
    path("questions/<int:id>/answer",add_answer,name="answer"),
    path("answers/<int:id>/upvote",upvote_view,name="upvote"),
    path("logout",signout_view,name="signout"),
    path("answers/<int:id>/remove",remove_view,name="remove")
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

