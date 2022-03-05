from django.urls import path
from .views import ProjectList, ProjectMeta, ProjectAttributes, ProjectRanks

urlpatterns = [
    path('projects/', ProjectList.as_view(), name='project-list'),
    path('projects/meta/<str:project_name>/',
         ProjectMeta.as_view(), name='project-meta'),
    path('projects/attributes/<str:project_name>/',
         ProjectAttributes.as_view(), name='project-attributes'),
    path('projects/ranks/<str:project_name>/',
         ProjectRanks.as_view(), name='project-ranks'),
]
