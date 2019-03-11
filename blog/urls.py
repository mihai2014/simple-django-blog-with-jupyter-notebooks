from django.urls import path, re_path

from . import views
#from . import tools

app_name = 'blog'
urlpatterns = [
    #path('<slug:topic>/<str:name>/', views.detail),
    # ex - /blog/
    #path('tests/<slug:name>/<str:data>',tools.select),
    #re_path(r'^tests2', tools.select2),
    path('site_map',views.site_map),
    path('', views.index, name='index'),
    re_path('^.*$', views.detail),
]

#re_path(r'^articles/(?P<year>[0-9]{4})/$', views.year_archive),
#url(r'^reply4/$', views.reply4),
