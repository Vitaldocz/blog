from __future__ import unicode_literals

from django.shortcuts import render
from django.views.generic import TemplateView


class IndexView(TemplateView):
    template_name = 'home/base.html'

    def get(self, request, *args, **kwargs):
        return render(request, template_name=self.template_name)