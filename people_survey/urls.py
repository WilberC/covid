from django.conf.urls import url
from .views import *

urlpatterns = [
    url(r'^survey/$', SurveyTemplateView.as_view(), name='survey'),
    url(r'^survey_result/$', SurveyResultTemplateView.as_view(), name='survey_result'),
    # ------ CRUD Entradas ------
    # url(r'^entradas_list/$', EntradasList.as_view(), name='entradas_list'),
    # url(r'^entradas_create/$', EntradasCreate.as_view(), name='entradas_create'),
    # url(r'^entradas_update/$', EntradasUpdate.as_view(), name='entradas_update'),
    # url(r'^entradas_detail/(?P<pk>.+)/$', EntradasDetail.as_view(), name="entradas_detail"),
    # -------------------------------
]
