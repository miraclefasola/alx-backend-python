import django_filters
from .models import Message


class MessageFilter(django_filters.FilterSet):
    class Meta:
        model = Message
        fields = {
            "sender__username": ["exact", "icontains"],
            "sent_at": ["lt", "gt", "range", "exact"],
        }


# or we can do it this way

# class MessageFilter(django_filters.FilterSet):
#     start_date= django_filters.DateTimeFilter(field_name='sent_at', lookup_expr='gte')
#     end_date = django_filters.DateTimeFilter(field_name='sent_at', lookup_expr='lte')

#     class Meta:
#         model = Message
#         fields = ["sender", "start_date", "end_date"]
