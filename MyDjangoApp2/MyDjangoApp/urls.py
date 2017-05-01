from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth import views as auth_views

# importing the views we created
from . import views
from django.conf.urls import include, url
urlpatterns = [
    url(r'^admin/', admin.site.urls),
    # defining a new URL pattern
    # when we will go here our template will render
    # url(r'^firsttemplate/', views.index),
    url(r'^$', views.home),

    url(r'^home/$', views.home),
    url(r'^logout/$', views.logout_view),
    url(r'^messageFunc/', include('postman.urls', namespace='postman', app_name='postman')),
    url(r'^messages/$', views.messages),

    url(r'^login/$', views.login_user),
    url(r'^login_fda/$', views.login_fda),
    url(r'^register/$', views.register_view),
    url(r'^success/$', views.success),
    url(r'^fail/$', views.fail),
    url(r'^report/', include('ReportCreater.urls', namespace="report")),
    url(r'^download/', include('ReportCreater.urls', namespace="report")),
    url(r'^profile/$', views.update_profile),
    url(r'^group/$', views.group_view),
    url(r'^viewgroups/$', views.view_groups),
    url(r'^search/$', views.search),
    url(r'^messages/$', views.messages),

    url(r'^searchresults/$', views.search_results),
	url(r'^sitemanager/$', views.site_manager),
    url(r'^manageUserAccess/$', views.manage_user_access),
    url(r'^creategroup/$', views.create_group),
    url(r'^aboutus/$', views.about_us),
    url(r'^help/$', views.help),
    url(r'^(?P<user_id>[a-zA-Z0-9_.-]*)/profile/$', views.view_profile, name="view_profile"),

    url(r'(?P<group_id>[a-zA-Z0-9_.-]*)/$', views.group_view, name="group_view"),

]
