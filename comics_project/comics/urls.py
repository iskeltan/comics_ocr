from django.urls import path
from comics import views

urlpatterns = [
    path('search/', views.SearchView.as_view()),
    path("random/", views.RandomView.as_view()),
    path("<int:pk>/", views.DetailView.as_view())
]