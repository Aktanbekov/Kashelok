
class HistoryPaymentMeMixin:
    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset()
        filter_queryset = queryset.filter(user=self.request.user)
        return filter_queryset
