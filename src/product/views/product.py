import json

from django.db.models import Count
from django.views import generic
from django.http import JsonResponse
from django.views.generic import ListView

from product.filter import ProductFilter
from product.models import Variant, Product, ProductImage, ProductVariant, ProductVariantPrice


class ProductOperations:

    def get_initial_data(self, context, product_id=None):
        variants = Variant.objects.filter(active=True).values('id', 'title')
        context['product'] = True
        context['variants'] = list(variants.all())
        if product_id:
            product = Product.objects.get(id=product_id)
            context["title"] = product.title
            context["sku"] = product.sku
            context["product_id"] = product.id
            context["description"] = str(product.description).strip()
            # context["images"] = ProductImage.objects.get(product_id=product.id).file_path
            product_variant_list = ProductVariant.objects.filter(product_id=product.id) \
                .values("id", "variant_title", "variant_id")
            product_variant = []
            for item in product_variant_list:
                product_variant.append({"option": item["variant_id"],
                                        "tags": str(item["variant_title"]).split(",")})
            context["product_variant"] = product_variant
            context["product_variant_prices"] = list(ProductVariantPrice.objects.filter(product_id=product.id) \
                                                     .values("title", "price", "stock"))
        return context

    def create_update(self, request):
        data = json.loads(request.body)
        product_id = data.get("product_id", None)
        title = data.get("title")
        sku = data.get("sku")
        description = data.get("description")
        product_image = data.get("product_image")

        if not product_id:
            product = Product.objects.create(title=title, sku=sku, description=description)
            ProductImage.objects.create(product_id=product.id, file_path=product_image)
        else:
            product = Product.objects.get(id=product_id)
            product.title = title
            product.description = description
            product.sku = sku
            product.save()
            for product_variant in product.product_variants.all():
                product_variant.delete()
            ProductImage.objects.filter(product_id=product.id).update(file_path=product_image)

        product_variant_list = data.get("product_variant")
        product_variant = {}
        index = 1
        for variant in product_variant_list:
            product_variant_obj = ProductVariant.objects.create(variant_id=variant["option"], product_id=product.id,
                                                                variant_title=",".join(variant["tags"]))
            if index == 1:
                product_variant["product_variant_one_id"] = product_variant_obj.id
            elif index == 2:
                product_variant["product_variant_two_id"] = product_variant_obj.id
            elif index == 3:
                product_variant["product_variant_three_id"] = product_variant_obj.id
            index += 1

        product_variant_price_list = data.get("product_variant_prices")
        for variant_price in product_variant_price_list:
            data = {"title": variant_price["title"], "price": float(variant_price["price"]),
                    "stock": float(variant_price["stock"]), "product_id": product.id}
            data.update(product_variant)
            ProductVariantPrice.objects.create(**data)


class CreateProductView(ProductOperations, generic.TemplateView):
    template_name = 'products/create.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return self.get_initial_data(context)

    def post(self, request):
        self.create_update(request)
        return JsonResponse({"success": True})


class UpdateProductView(ProductOperations, generic.TemplateView):
    template_name = 'products/update.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return self.get_initial_data(context, kwargs.get("pk", None))


class ProductListView(ListView):
    template_name = 'products/list.html'
    paginate_by = 2
    model = Product

    def get_queryset(self):
        return ProductFilter(self.request.GET, queryset=Product.objects.all().order_by("-id")).qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['product'] = True
        product_variant_list = ProductVariant.objects.all().values("variant_title", "variant__title").distinct()
        for product_variant in product_variant_list:
            product_variant["variant_title"] = str(product_variant["variant_title"]).split(",")
        context['product_variant_list'] = product_variant_list
        # print(product_variant_list)
        return context
