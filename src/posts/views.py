from django.shortcuts import render, redirect
from django.views.generic import TemplateView

# Create your views here.


class BlogIndexView(TemplateView):
    template_name = 'posts/index.html'

    def get(self, request, *args, **kwargs):
        return redirect('home:indexView')


class BlogDetailView(TemplateView):
    template_name = 'posts/single.html'

    def get(self, request, *args, **kwargs):
        slug = kwargs['slug']
        print(slug)
        return render(request, template_name=self.template_name)
