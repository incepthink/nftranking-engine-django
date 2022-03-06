from django.urls import path
from .views import ProjectList, ProjectMeta, ProjectAttributes, ProjectRanks, CSVDownloader
urlpatterns = [
    path('projects/', ProjectList.as_view(), name='project-list'),
    path('projects/meta/<str:project_name>/',
         ProjectMeta.as_view(), name='project-meta'),
    path('projects/attributes/<str:project_name>/',
         ProjectAttributes.as_view(), name='project-attributes'),
    path('projects/ranks/<str:project_name>/',
         ProjectRanks.as_view(), name='project-ranks'),
    path('projects/download/<str:project_name>/',
         CSVDownloader.as_view(), name='project-download'),
]
