from django.contrib import admin
from django.urls import re_path
from django.views.generic.base import RedirectView
from homepage import views

urlpatterns = [
    # path('admin/', admin.site.urls),
    re_path(r'^$',views.index ),
    re_path(r'^index$',views.index ),
    re_path(r'^record$',views.record ),
    re_path(r'^register$',views.register ),
    re_path(r'^unregister$',views.unregister ),
    re_path(r'^login$',views.login ),
    re_path(r'^changepasswd$',views.changepasswd ),
    re_path(r'^changepasswd_ed$',views.changepasswd_ed ),
    re_path(r'^probe$',views.probe ),
    re_path(r'^user$',views.user ),
    re_path(r'^user_exit$',views.user_exit ),
    re_path(r'^unregister$',views.unregister ),
    re_path(r'^landing$',views.landing ),
    re_path(r'^comment$',views.comment ),
    re_path(r'^detail/(\d*?)$',views.detail),
    re_path(r'^detail(\d*?)$',views.detail),
    re_path(r'^search$',views.search),
    re_path(r'^order/(\d*?)$',views.order),
    re_path(r'^orders$',views.orders),
    re_path(r'^add_comment$',views.add_comment),
    re_path(r'^have_recv_addr$',views.have_recv_addr),
    re_path(r'^get_zone/(\d*?)$',views.get_zone),
    re_path(r'^test$',views.test),
    re_path(r'^set_recv_addr$',views.set_recv_addr),
    re_path(r'^confirm_order$',views.confirm_order),

    re_path(r'^favicon\.ico$', RedirectView.as_view(url=r'/static/img/favicon.ico')),
]
