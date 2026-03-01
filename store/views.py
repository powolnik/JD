import random
from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, SubOption, Color

def product_list(request):
    """Wyświetla listę produktów z losowo wybranym zdjęciem wariantu kolorystycznego."""
    products = Product.objects.all()
    
    # Dla każdego produktu wybieramy losowy kolor, który ma zdjęcie
    for product in products:
        colors_with_image = product.colors.exclude(image='')
        if colors_with_image.exists():
            product.random_variant_image = random.choice(colors_with_image).image.url
        else:
            product.random_variant_image = None

    cart = request.session.get('cart', {})
    cart_count = len(cart)
    
    total_cart_price = 0
    for key, item in cart.items():
        try:
            product = Product.objects.get(id=item['product_id'])
            options = SubOption.objects.filter(id__in=item['option_ids'])
            qty = item['quantity']
            
            color_price = 0
            if item.get('color_id'):
                try:
                    color = Color.objects.get(id=item['color_id'])
                    color_price = color.extra_price
                except Color.DoesNotExist:
                    pass

            options_price = sum(opt.extra_price for opt in options)
            total_cart_price += (product.price + options_price + color_price) * qty
        except Product.DoesNotExist:
            continue

    return render(request, 'store/product_list.html', {
        'products': products,
        'cart_count': cart_count,
        'total_cart_price': total_cart_price
    })

def product_configure(request, product_id):
    """Strona konfiguracji z losowo wybranym domyślnym kolorem."""
    product = get_object_or_404(Product, id=product_id)
    colors = product.colors.all()
    
    # Losujemy domyślny kolor przy wejściu (jeśli są dostępne)
    initial_color_id = None
    if colors.exists():
        initial_color_id = random.choice(colors).id
    
    if request.method == "POST":
        qty = int(request.POST.get('quantity', 1))
        selected_option_ids = request.POST.getlist('options')
        selected_color_id = request.POST.get('color')
        
        cart = request.session.get('cart', {})
        cart_key = f"{product.id}_{selected_color_id}"
        cart[cart_key] = {
            'product_id': product.id,
            'quantity': qty,
            'option_ids': selected_option_ids,
            'color_id': selected_color_id
        }
        request.session['cart'] = cart
        return redirect('product_list')

    return render(request, 'store/product_configure.html', {
        'product': product,
        'initial_color_id': initial_color_id
    })

def report_view(request):
    """Generuje raport na podstawie zawartości koszyka w sesji."""
    cart = request.session.get('cart', {})
    comment = request.POST.get('comment', '') 
    
    selected_items = []
    total_price = 0
    
    for key, item in cart.items():
        try:
            product = Product.objects.get(id=item['product_id'])
            options = SubOption.objects.filter(id__in=item['option_ids'])
            qty = item['quantity']
            
            color = None
            color_price = 0
            if item.get('color_id'):
                try:
                    color = Color.objects.get(id=item['color_id'])
                    color_price = color.extra_price
                except Color.DoesNotExist:
                    pass

            options_price = sum(opt.extra_price for opt in options)
            item_total = (product.price + options_price + color_price) * qty
            total_price += item_total
            
            selected_items.append({
                'product': product,
                'quantity': qty,
                'options': options,
                'color': color,
                'item_total': item_total
            })
        except Product.DoesNotExist:
            continue
        
    return render(request, 'store/report.html', {
        'selected_items': selected_items,
        'total_price': total_price,
        'comment': comment
    })

def clear_cart(request):
    """Czyści koszyk sesji."""
    if 'cart' in request.session:
        del request.session['cart']
        request.session.modified = True
    return redirect('product_list')