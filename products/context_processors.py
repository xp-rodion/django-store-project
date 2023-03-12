from products.models import BasketItem


def baskets(request):
    user = request.user
    return {'baskets': BasketItem.objects.filter(user=user) if user.is_authenticated else []}