from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from ...views import bcs_views


urlpatterns = [
    path('', bcs_views.get_bcs_list_procedures, name='bcs_list_procedures'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
