from django.urls import path
from . import views

urlpatterns = [
    path('', views.UploadView.as_view(), name='upload'),

    path('upload-json/', views.UploadJSONView.as_view(), name='upload_json'),
    path('ments/', views.AssessmentListView.as_view(), name='assessment_list'),
    path('create-assessment/',
         views.CreateAssessmentView.as_view(),
         name='create_assessment'),
    path('generate_pdf/', views.GeneratePDFView.as_view(), name='generate_pdf'),
    path('generate_pdf_template/', views.GeneratePDFTemplateView.as_view(),
         name='generate_pdf_template'),
]
