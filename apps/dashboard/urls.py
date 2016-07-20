from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^$', views.index, name = 'dashboard_index'),
	url(r'^login$', views.login, name = 'dashboard_login'),
	url(r'^logout$', views.logout, name = 'dashboard_logout'),
	url(r'^login_validation$', views.login_validation, name = 'dashboard_login_validation'),
	url(r'^register$', views.register, name = 'dashboard_register'),
	url(r'^registration$', views.registration, name = 'dashboard_registration'),
	url(r'^admin_dash$', views.admin_dash, name = 'dashboard_admin_dash'),
	url(r'^dash$', views.dash, name = 'dashboard_dash'),
	url(r'^users/new$', views.new, name = 'dashboard_new'),
	url(r'^users/new/add$', views.add, name = 'dashboard_add'),
	url(r'^users/edit/(?P<id>\d+)$', views.edit_user, name = 'dashboard_edit_user'),
	url(r'^users/edit$', views.edit, name = 'dashboard_edit'),
	url(r'^users/updateInfo/(?P<id>\d+)$', views.updateInfo, name = 'dashboard_updateInfo'),
	url(r'^users/updatePassword/(?P<id>\d+)$', views.updatePassword, name = 'dashboard_updatePassword'),
	url(r'^users/updateDescription/(?P<id>\d+)$', views.updateDescription, name = 'dashboard_updateDescription'),
	url(r'^users/show/(?P<id>\d+)$', views.show, name = 'dashboard_show'),
	url(r'^remove/(?P<id>\d+)$', views.remove, name = 'dashboard_remove'),
	url(r'^users/(?P<id>\d+)/post$', views.post, name = 'dashboard_post'),
	url(r'^users/(?P<id>\d+)/comment$', views.comment, name = 'dashboard_comment')
]