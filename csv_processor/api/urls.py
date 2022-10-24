from django.urls import path
from .views import DocumentView

app_name = 'api'
urlpatterns = [
    path('api/v1/', DocumentView.as_view()),
    path('api/v1/<int:pk>', DocumentView.as_view()),
]