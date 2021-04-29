from django.conf.urls import url
from django.urls import path
from . import views

#MUST HAVE SAME NAME AS HTML TEMPLATES
urlpatterns = [
    #APIS:
    path('api-register',views.registerAPI),
    path('api-login',views.loginAPI),
    path('api-update', views.userUpdateAPI), #NOT using _id anymore since taking that value from sesison var
    path('api-delete', views.deleteUserAPI),
    #For Devs ONLY, comment for build:
    path('api-getall', views.getAll),
    path('api-getuser/<int:_id>', views.getUser),

    #Front-end:
    url(r'^$',views.index), #dealt with in front-end or main app, not microservice
    path('logout',views.logout), #NOT using _id anymore, just deleting token in session
    path('<path:_path>', views.front_end), #at bottom to not interfere with other urls. Gets all other urls
    #SO NO NEED FOR:
    # path('register', views.register),
    # path('login',views.login),
    # # path('login/<str:email>/<slug:ps>', views.login), #NO need since POST not GET so access through `request` not url path 
    # path('delete', views.deleteUser),  #NOT using _id anymore since taking that value from sesison var
    # path('update', views.userUpdate),
]
