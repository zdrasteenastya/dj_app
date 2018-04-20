from django.conf.urls import url

from . import views

app_name = 'polls'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^results', views.results, name='results'),
    url(r'^vote/$', views.vote, name='vote'),
    url(r'^auth_view', views.auth_view, name='auth_view'),
    url(r'^register', views.register, name='register'),
    url(r'^logout/$', views.logout),
    url(r'^loggedin/$', views.loggedin),
    url(r'^admin_view/$', views.admin_view),
    url(r'^invalid_login', views.invalid_login),
    url(r'^detail/$', views.detail),
    url(r'^history/$', views.history),
    url(r'^forgot', views.forgot)
]