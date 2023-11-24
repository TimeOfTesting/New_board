from django import forms
from .models import Posts, Subscription, Category, Author
from allauth.account.forms import SignupForm
from django.contrib.auth.models import Group

class SingleDateWidget(forms.DateInput):
    input_type = 'date'

class PostForm(forms.ModelForm):
    category = forms.ModelMultipleChoiceField(queryset=Category.objects.all(), required=False,
                                              widget=forms.CheckboxSelectMultiple, label='Категория')
    class Meta:
        model = Posts
        fields = ['title_post', 'text_post', 'file']
        widgets = {
            'text_post': forms.Textarea(attrs={'cols': 50, 'rows': 5})
        }

class BasicSignupForm(SignupForm):

    def save(self, request):
        user = super(BasicSignupForm, self).save(request)
        basic_group = Group.objects.get(name='basic')
        basic_group.user_set.add(user)
        return user

class SubscriptionForm(forms.ModelForm):

    class Meta:
        model = Subscription
        fields = '__all__'