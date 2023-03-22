from django_filters import FilterSet, DateFilter, ModelChoiceFilter
from .models import Post, Category


class NewsFilter(FilterSet):
    # post_datetime = DateFilter(lookup_expr='iexact')
    category = ModelChoiceFilter(
        field_name = 'category__category_name',
        queryset = Category.objects.all(),
        label = 'Category',
        empty_label = ''
    )

    class Meta:
        model = Post
        fields = {
            'post_header': ['icontains'],
        }