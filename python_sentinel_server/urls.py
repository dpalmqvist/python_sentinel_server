"""python_sentinel_server URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.urls import path

import detections.views as detection_views
import django.contrib.auth.views as auth_views
import main.views as main_views
import sentinels.views as sentinel_views


urlpatterns = [
    path('', main_views.main),
    path('admin/', admin.site.urls),
    path('claim_sentinel/', sentinel_views.claim_sentinel),
    url(r'^login/$', auth_views.login, {'template_name': 'accounts/login.html'}, name='login'),
    url(r'^logout/$', auth_views.logout, name='logout'),
    path('report/<str:det>/', detection_views.report),
    path('mac_identities/', detection_views.MacIdentities.as_view(), ),
    path('report/<str:det>', detection_views.report),
    path('mac_identity/add/', detection_views.MacIdentityCreate.as_view(), name='mac_identity-add'),
    path('mac_identity/<int:pk>/', detection_views.MacIdentityUpdate.as_view(), name='mac_identity-update'),
    path('mac_identity/<int:pk>/delete/', detection_views.MacIdentityDelete.as_view(), name='mac_identity-delete'),
    path('sentinel_identities/', detection_views.SentinelIdentities.as_view(), ),
    path('sentinel_identity/<int:pk>/', detection_views.SentinelIdentityUpdate.as_view(), name='sentinel_identity-update'),
    path('detections/', detection_views.Detections.as_view(), ),
    path('detection/<int:pk>/', detection_views.DetectionView.as_view(), name='detection-detail'),
]
