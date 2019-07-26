#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: vita
app_name = "task_manage"
from django.urls import path
from django.contrib.auth.decorators import login_required
from task_manage import views

urlpatterns = [
    path('webssh_login/', login_required(views.WebsshLogin.as_view()), name="webssh_login"),
    path('get_env_by_system_id/', views.get_env_by_system_id, name="get_env_by_system_id"),
    path('get_host_by_sys_or_env_id/', views.get_host_by_sys_or_env_id, name="get_host_by_sys_or_env_id"),

]
