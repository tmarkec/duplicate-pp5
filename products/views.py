from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from .models import Product, Category, Review
from .forms import ReviewForm, ProductForm
from checkout.models import OrderLineItem
from django.utils import timezone
from django.utils.timezone import now

# Create your views here.


def all_products(request):
    """ A view to show all products, including sorting and search queries """

    products = Product.objects.all()
    query = None
    categories = None

    if request.GET:
        if 'category' in request.GET:
            categories = request.GET['category'].split(',')
            products = products.filter(category__name__in=categories)
            categories = Category.objects.filter(name__in=categories)

        if 'q' in request.GET:
            query = request.GET['q']
            if not query:
                messages.error(request, "You didn't enter any search criteria!")
                return redirect(reverse('products'))

            queries = Q(name__icontains=query) | Q(description__icontains=query)
            products = products.filter(queries)

    context = {
        'products': products,
        'search_term': query,
        'current_categories': categories,
    }

    return render(request, 'products/products.html', context)


def product_detail(request, product_id):
    """ A view to show individual product details """

    product = get_object_or_404(Product, pk=product_id)
    reviews = Review.objects.filter(product_id=product.id, approved=True)
    context = {
        'product': product,
        'reviews': reviews,
    }

    return render(request, 'products/product_detail.html', context)


def add_product(request):
    """ Add a product to the store """
    form = ProductForm()
    template = 'products/add_product.html'
    context = {
        'form': form,
    }

    return render(request, template, context)


def add_review(request, product_id):
    """ A view to add review"""
    product = get_object_or_404(Product, pk=product_id)
    if request.method == 'POST':
        form = ReviewForm(request.POST)

        if form.is_valid():
            rating = form.cleaned_data['rating']
            review_comment = form.cleaned_data['review_comment']    
            review = Review.objects.create(
                product=product,
                user=request.user,
                rating=rating,
                review_comment=review_comment,
                )
            review.save()
            messages.success(request, 'Thank you for your review!')
        else:
            messages.warning(request, 'You must rate and review the product!')
        return redirect('product_detail', product_id=product.id)

    context = {
        'product': product,
        'form': form,
    }

    return render(request, 'products/product_detail.html', context)


def del_review(request, review_id):
    """ A view to delete review """
    review = get_object_or_404(Review, id=review_id)
    if review.user == request.user:
        review.delete()
        messages.success(request, "Review deleted successfully.")
    return redirect('product_detail', product_id=review.product.id)


def update_review(request, review_id):
    """A view to update user review"""
    review = get_object_or_404(Review, id=review_id)
    if request.method == "POST":
        form = ReviewForm(request.POST, instance=review)
        if form.is_valid():
            review = form.save(commit=False)
            review.approved = False
            review.updated_on = timezone.now()
            review.save()
            messages.success(request, 'Your review has been updated.')
            return redirect('product_detail', product_id=review.product.id)
    else:
        form = ReviewForm(instance=review)
    return render(request,
                  "products/update_review.html", {"form": form})



