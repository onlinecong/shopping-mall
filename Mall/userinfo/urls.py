from django.conf.urls import url

from userinfo import views

urlpatterns = [
    url(r'^index/$',views.index,name='index'),
    url(r'^register/$',views.register,name='register'),
    url(r'^login_/$',views.login_,name='login')

]