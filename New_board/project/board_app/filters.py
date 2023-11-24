import django_filters
from django_filters import FilterSet, DateFilter, ModelChoiceFilter
from .models import Posts, Category
from .forms import SingleDateWidget


class PostFilter(FilterSet):
    date_after = DateFilter(field_name='time_create', lookup_expr='date', label='Дата', widget=SingleDateWidget)
    category_name = ModelChoiceFilter(
        field_name='category__name_category',
        queryset=Category.objects.all(),
        to_field_name='name_category',
        label='Категория',
    )
    author_name = django_filters.CharFilter(lookup_expr='icontains', label='Автор обьявления')

    class Meta:
        model = Posts
        fields = {
            'title_post': ['icontains'],
        }


