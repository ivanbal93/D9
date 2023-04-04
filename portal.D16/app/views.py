from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post, Category, User
from .filters import NewsFilter
from .forms import NewPostForm
from django.urls import reverse_lazy
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, get_object_or_404
from django.core.mail import send_mail

# from django.http import HttpResponse
# from django.views import View
# from .tasks import hello

# class IndexView(View):
#     def get(self, request):
#         hello.delay()
#         return HttpResponse('Hello!')

# Create your views here.
class PostList(ListView):
    model = Post
    ordering = '-post_datetime'
    template_name = 'post_list.html'
    context_object_name = 'post_list'
    paginate_by = 10
    

class PostDetail(DetailView):
    model = Post
    template_name = 'post_detailed.html'
    context_object_name = 'post_det'


class Search(PostList):
    template_name = 'search.html'
    # context_object_name = 'search'

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = NewsFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs: any):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context


class NewPost(PermissionRequiredMixin, CreateView):
    permission_required = ('app.add_post')
    form_class = NewPostForm
    model = Post
    template_name = 'newpost.html'


class PostUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = ('app.change_post')
    form_class = NewPostForm
    model = Post
    template_name = 'newpost.html'


class PostDelete(PermissionRequiredMixin, DeleteView):
    permission_required = ('app.delete_post')
    model = Post
    template_name = 'delete.html'
    success_url = reverse_lazy('post_list')


class SubscribeView(LoginRequiredMixin, ListView):
    template_name = 'subscribe.html'
    model = Category
    context_object_name = 'categories_list'

    def post(self, request, category_id):
        category = get_object_or_404(Category, pk=category_id)
        category.subscribers.add(request.user)
        category.save()

        send_mail(
            subject='New subscriber',
            message=f'You have subscribed to the category "{category}"',
            from_email=None,
            recipient_list=[request.user.email, ],
            # fail_silently=True
        )

        return redirect(request.META.get('HTTP_REFERER'))
    

