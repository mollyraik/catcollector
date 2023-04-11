from django.urls import path
from . import views

# NOTE: django ONLY uses GET and POST; there is no REST in django; we never to DELETE, PUT
# NOTE: in django updating and deleting will be conducted using POST request
# NOTE: django paths NEVER begin w a '/' django prepends this for us

'''
Examples of deleting and updating:
    path('cats/<int:cat_id>/remove_cat', )
    path('cats/<int:cat_id>/update_cat', )
'''

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('cats/', views.cats_index, name='cats_index'),
    path('cats/<int:cat_id>/', views.cat_detail, name='cat_detail'),
    path('cats/create/', views.CatCreate.as_view(), name='cat_create'),
    path('cats/<int:pk>/update/', views.CatUpdate.as_view(), name='cat_update'),
    path('cats/<int:pk>/delete/', views.CatDelete.as_view(), name='cat_delete'),
    path('cats/<int:cat_id>/add_feeding/', views.add_feeding, name='add_feeding'),
    path('cats/<int:cat_id>/add_photo/', views.add_photo, name='add_photo'),
    path('toys/', views.ToyList.as_view(), name='toy_list'),
    path('toys/<int:pk>/', views.ToyDetail.as_view(), name='toy_detail'),
    path('toys/create/', views.ToyCreate.as_view(), name='toy_create'),
    path('toys/<int:pk>/update/', views.ToyUpdate.as_view(), name='toy_update'),
    path('toys/<int:pk>/delete/', views.ToyDelete.as_view(), name='toy_delete'),
    path('cats/<int:cat_id>/assoc_toy/<int:toy_id>/', views.assoc_toy, name='assoc_toy'),
    path('cats/<int:cat_id>/assoc_toy/<int:toy_id>/remove', views.remove_assoc_toy, name='remove_assoc_toy'),
    path('accounts/signup/', views.signup, name='signup'),
]