from django.urls import path
from .views import ModuleCreateView
#from .views import ModuleCreateView, ModuleDetailView, ModuleUpdateView, ModuleDeleteView

urlpatterns = [
    path('create/', ModuleCreateView.as_view(), name='create_module'),
]
"""
urlpatterns = [
    path('create/', ModuleCreateView.as_view(), name='create_module'),
    path('<str:code>/', ModuleDetailView.as_view(), name='detail_module'),
    path('<str:code>/update/', ModuleUpdateView.as_view(), name='update_module'),
    path('<str:code>/delete/', ModuleDeleteView.as_view(), name='delete_module'),
]
"""