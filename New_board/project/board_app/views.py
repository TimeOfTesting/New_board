from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from django.urls import reverse_lazy
from .models import Posts, Category, Author, Subscription, PostCategory
from django.views.generic import ListView, DetailView, CreateView, TemplateView, UpdateView, DeleteView
from .filters import PostFilter
from .forms import PostForm, SubscriptionForm
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
from django.core.cache import cache
from django.contrib.auth import logout
from django.contrib.auth.models import User

class ListPost (ListView):
    template_name = 'posts/list_posts.html'
    model = Posts
    context_object_name = 'post'
    paginate_by = 4

class ListPostFilter (ListView):
    template_name = 'posts/list_posts_filters.html'
    model = Posts
    ordering = ['title_post']
    context_object_name = 'post'
    paginate_by = 4

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context

class DetailPost (DetailView):
    template_name = 'posts/base_posts.html'
    model = Posts
    context_object_name = 'post'

    def get_object(self, *args, **kwargs):
        obj = cache.get(f'post-{self.kwargs["pk"]}', None)
        if not obj:
            obj = super().get_object(queryset=self.queryset)
            cache.set(f'post-{self.kwargs["pk"]}', obj)
        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post_instance = self.object
        category_names = post_instance.category.values_list('name_category', flat=True)
        author_name = post_instance.author.name_author
        subscriptions = Subscription.objects.filter(user_id=self.request.user.id).values()
        subscribe_user_post = []
        for i in list(subscriptions):
            subscribe_user_post.append(i['posts_id'])
        context['category_names'] = ", ".join([_ for _ in category_names])
        context['author_name'] = author_name
        context['subscribe_user_post'] = subscribe_user_post
        return context

    def get_absolute_url(self):
        return f'/posts/{self.id}'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        cache.delete(f'post-{self.pk}')

@login_required
def subscribe(request, pk):
    posts = get_object_or_404(Posts, id=pk)
    user = request.user
    email = user.email
    url = f'{settings.SITE_URL}posts/{pk}/'

    if request.method == 'POST':
        form = SubscriptionForm(request.POST)
        res = Subscription(posts_id=pk, user_id=user.id, email=user.email)
        res.save()
        html_content = render_to_string(
            'subscribe_email.html',
            {'posts': posts,
                'user': user,
                'url': url},
        )
        msg = EmailMultiAlternatives(
            subject=posts.title_post,
            body='',
            from_email=settings.EMAIL_HOST_USER,
            to=[email, ],
        )
        msg.attach_alternative(html_content, 'text/html')
        msg.send()

        return redirect('done_subscribe')
    else:
        form = SubscriptionForm()

    return render(request, 'posts/subscribe.html', {'form': form, 'posts': posts})

@login_required
def accept_subscribe(request, subscription_id):
    user = request.user
    email = user.email
    subscription = Subscription.objects.get(pk=subscription_id)
    subscription.status = "accepted"
    subscription.save()
    if request.method == 'POST':
        html_content = render_to_string(
            'subscribe_email_accepted.html')
        msg = EmailMultiAlternatives(
            subject='Ваш отклик принят',
            body='',
            from_email=settings.EMAIL_HOST_USER,
            to=[email, ],
        )
        msg.attach_alternative(html_content, 'text/html')
        msg.send()

    return redirect('done_subscribe')

@login_required
def reject_subscribe(request, subscription_id):
    user = request.user
    email = user.email
    subscription = Subscription.objects.get(pk=subscription_id)
    subscription.status = "rejected"
    subscription.save()
    if request.method == 'POST':
        html_content = render_to_string(
            'subscribe_email_accepted.html')
        msg = EmailMultiAlternatives(
            subject='Ваш отклик отклонен',
            body='',
            from_email=settings.EMAIL_HOST_USER,
            to=[email, ],
        )
        msg.attach_alternative(html_content, 'text/html')
        msg.send()

    return redirect('done_subscribe')

@login_required
def change_response_status(request, subscription_id, new_status):
    response = get_object_or_404(Subscription, pk=subscription_id)

    if response.user != request.user:
        return render(request, 'error.html', {'message': 'У вас нет прав для выполнения этого действия'})
    response.status = new_status
    response.save()
    return redirect('user_responses')

@login_required
def user_responses(request):
    user_responses = Subscription.objects.filter(user=request.user)

    status_filter = request.GET.get('status')
    if status_filter:
        user_responses = user_responses.filter(status=status_filter)

    paginator = Paginator(user_responses, 10)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    return render(request, 'posts/user_responses.html', {'user_responses': page_obj})

@login_required
def user_responses(request):
    user_responses = Subscription.objects.filter(user_id=request.user.id)

    return render(request, 'posts/user_responses.html', {'user_responses': user_responses})

class DoneSubscribeView(TemplateView):
    template_name = 'posts/success_page.html'

class DoneUnsubscribeView(TemplateView):
    template_name = 'posts/unsuccess_page.html'

class CreatePost(LoginRequiredMixin, CreateView):
    model = Posts
    form_class = PostForm
    template_name = 'posts/create_posts.html'
    success_url = reverse_lazy('done_view')

    def form_valid(self, form):
        author_instance = Author.objects.get(user=self.request.user)
        if author_instance:
            form.instance.author = author_instance
            post_instance = form.save(commit=False)
            post_instance.save()

            for category in form.cleaned_data['category']:
                PostCategory.objects.create(categories=category, posts=post_instance)

            return super().form_valid(form)

class UpdatePost (LoginRequiredMixin, UpdateView):
    permission_required = ('board_app.change_post',)
    model = Posts
    form_class = PostForm
    template_name = 'posts/create_posts.html'
    success_url = '/posts/done'

class DeletePost (LoginRequiredMixin, DeleteView):
    permission_required = ('board_app.delete_post',)
    model = Posts
    template_name = 'posts/delete_post.html'
    success_url = '/posts/'

class DoneView(TemplateView):
    template_name = 'posts/done.html'

class UserProfileView(LoginRequiredMixin, DetailView):
    model = User
    template_name = 'posts/index.html'
    context_object_name = 'user'

    def get_object(self, queryset=None):
        return self.request.user

@login_required
def upgrade_me(request):
    user = request.user
    authors_group = Group.objects.get(name='basic')
    if not request.user.groups.filter(name='basic').exists():
        authors_group.user_set.add(user)
        user_create = Author(user_id=request.user.id, name_author=request.user.username)
        user_create.save()
    return render(request, 'posts/update.html')

def logout_view(request):
    logout(request)
    return redirect('home')


