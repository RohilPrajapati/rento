from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


class PaginationMixin:
    paginate_by = 10  # default items per page

    def paginate_queryset(self, queryset, request):
        page = request.GET.get("page")
        paginator = Paginator(queryset, self.paginate_by)

        try:
            page_obj = paginator.page(page)
        except PageNotAnInteger:
            page_obj = paginator.page(1)
        except EmptyPage:
            page_obj = paginator.page(paginator.num_pages)

        return page_obj
