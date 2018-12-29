from django.shortcuts import render
from django.views.generic import TemplateView

# Create your views here.


class DetailView(TemplateView):
    template_name = 'posts/single.html'

    def get(self, request, *args, **kwargs):
        slug = kwargs['slug']
        print(slug)
        return render(request, template_name=self.template_name)


class AddView(TemplateView):
    pass


class UpdateView(TemplateView):
    pass


class DeleteView(TemplateView):
    pass
