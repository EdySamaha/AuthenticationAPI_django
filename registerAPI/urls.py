from django.conf.urls import url
from django.urls import path
from . import views

#MUST HAVE SAME NAME AS HTML TEMPLATES
urlpatterns = [
    # url(r'^$',views.index), #dealt with in front-end or main app, not microservice
    # path('login/<str:email>/<slug:ps>', views.login), #NO need since POST not GET so access through `request` not url path 
    url(r'^login',views.login),
    url(r'^register',views.register),
    path('logout/<int:_id>',views.logout),
    path('getall', views.getAll),
    path('getuser/<int:_id>', views.getUser),
    path('update/<int:_id>', views.userUpdate),
    path('delete/<int:_id>', views.deleteUser), #Only for development, comment afterwards
]
