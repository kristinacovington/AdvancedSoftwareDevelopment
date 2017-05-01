from django.conf.urls import include, url
from . import views

urlpatterns = [
    url(r'^form/$', views.form, name="form"),
    url(r'^(?P<report_id>[0-9]+)/$', views.download, name="download"),
    url(r'^query/(?P<query_id>[0-9]+)/$', views.query_handler, name="query"),
    url(r'^query/(?P<query_id>[0-9]+)/(?P<extra_id1>[0-9]+)/$', views.query_handler, name="query"),
    url(r'^query/(?P<query_id>[0-9]+)/(?P<extra_id1>[0-9]+)/(?P<extra_id2>[0-9]+)/$', views.query_handler, name="query"),
    url(r'^view/$', views.all_reports_view, name="all_reports"),
    url(r'^view/(?P<report_id>[0-9]+)/$', views.report_view, name="view_report"),
    url(r'^edit/(?P<report_id>[0-9]+)/$', views.report_edit, name="edit_report"),
    url(r'^delete/(?P<report_id>[0-9]+)/$', views.delete_report, name="delete_report"),
]
