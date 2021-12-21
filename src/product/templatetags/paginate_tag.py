from django import template

from product.views.product import ProductOperations

register = template.Library()


@register.simple_tag
def url_replace(request, field, value):
    dict_ = request.GET.copy()
    dict_[field] = value
    return dict_.urlencode()


@register.filter(name='proper_paginate')
def proper_paginate(paginator, current_page, neighbors=2):
    if paginator.num_pages > 2 * neighbors:
        start_index = max(1, current_page - neighbors)
        end_index = min(paginator.num_pages, current_page + neighbors)
        if end_index < start_index + 2 * neighbors:
            end_index = start_index + 2 * neighbors
        elif start_index > end_index - 2 * neighbors:
            start_index = end_index - 2 * neighbors
        if start_index < 1:
            end_index -= start_index
            start_index = 1
        elif end_index > paginator.num_pages:
            start_index -= (end_index - paginator.num_pages)
            end_index = paginator.num_pages
        page_list = [f for f in range(start_index, end_index + 1)]
        return page_list[:(2 * neighbors + 1)]
    return paginator.page_range


@register.filter(name='get_product_variant_prices')
def get_product_variant_prices(product):
    return ProductOperations().get_product_variant({}, product.id)["product_variant_prices"]