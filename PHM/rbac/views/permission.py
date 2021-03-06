#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: vita
from django.urls import reverse_lazy, reverse
from django.shortcuts import HttpResponse
from django.views.generic import CreateView, UpdateView, DeleteView
from rbac.models import Permission
from rbac.forms.second_menu import PermissionModelForm
from rbac.service.urls import memory_reverse


class PermissionAddView(CreateView):
    """
    添加二级菜单
    组件确实很方便呀，内部已经对get和POST方法做了处理
    同时已经自动做了form.save
    """
    model = Permission
    template_name = "rbac/add_edit.html"

    form_class = PermissionModelForm

    def get_success_url(self):
        """
        Return the URL to redirect to after processing a valid form.
        这里是因为添加或删除成功后，页面中还总是不显示，我觉得可能是reverse_lazy()捣的鬼，就自己重写该方法了

        :return:
        """
        return memory_reverse(self.request, 'rbac:menu_list')

    def post(self, request, *args, **kwargs):
        second_menu_id = kwargs.get("second_menu_id")
        second_menu_object = Permission.objects.filter(id=second_menu_id).first()
        if not second_menu_object:
            return HttpResponse('二级菜单不存在，请重新选择！')
        form = PermissionModelForm(data=request.POST)
        form.instance.pid = second_menu_object
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)


class PermissionEditView(UpdateView):
    """
    编辑权限，即二级菜单中的按钮
    组件确实很方便呀，内部已经对get和POST方法做了处理
    同时已经自动做了form.save
    """
    model = Permission
    template_name = "rbac/add_edit.html"
    form_class = PermissionModelForm

    def get_success_url(self):
        """
        Return the URL to redirect to after processing a valid form.
        这里是因为添加或删除成功后，页面中还总是不显示，我觉得可能是reverse_lazy()捣的鬼，就自己重写该方法了

        :return:
        """
        return memory_reverse(self.request, 'rbac:menu_list')


class PermissionDelView(DeleteView):
    """
    删除二级菜单
    组件确实很方便呀，内部已经对get和POST方法做了处理
    同时已经自动做了form.save
    """
    model = Permission
    template_name = "rbac/del.html"
    form_class = PermissionModelForm

    def get_success_url(self):
        """
        Return the URL to redirect to after processing a valid form.
        这里是因为添加或删除成功后，页面中还总是不显示，我觉得可能是reverse_lazy()捣的鬼，就自己重写该方法了

        :return:
        """
        return memory_reverse(self.request, 'rbac:menu_list')

    def get_context_data(self, **kwargs):
        #
        context = {
            "cancel_url": reverse('rbac:menu_list'),
        }
        kwargs.update(context)
        return super().get_context_data(**kwargs)
