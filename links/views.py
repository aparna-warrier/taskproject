from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.db import transaction

from .forms import ShortenForm
from .models import ShortURL
from .utils import generate_code

def home(request):
    form = ShortenForm(request.POST or None)
    short_obj = None

    if request.method == 'POST' and form.is_valid():
        original_url = form.cleaned_data['original_url']
        custom_code  = form.cleaned_data.get('custom_code')

        # within a transaction to avoid rare race conditions on unique short_code
        with transaction.atomic():
            if custom_code:
                short_code = custom_code
            else:
                # generate until unique
                short_code = generate_code()
                while ShortURL.objects.filter(short_code=short_code).exists():
                    short_code = generate_code()

            short_obj, created = ShortURL.objects.get_or_create(
                short_code=short_code,
                defaults={'original_url': original_url}
            )
            if not created:
                # If the code exists but points to a different URL, update the original_url
                short_obj.original_url = original_url
                short_obj.save(update_fields=['original_url'])

        # Build absolute short link (e.g., http://127.0.0.1:8000/abc123)
        short_link = request.build_absolute_uri(reverse('links:follow', args=[short_obj.short_code]))
        messages.success(request, 'Short URL created successfully!')
        return render(request, 'links/home.html', {
            'form': ShortenForm(),          # clear the form
            'short_obj': short_obj,
            'short_link': short_link,
        })

    # show recent short urls for convenience
    recent = ShortURL.objects.order_by('-created_at')[:5]
    return render(request, 'links/home.html', {'form': form, 'recent': recent})

def follow(request, code):
    obj = get_object_or_404(ShortURL, short_code=code)
    obj.clicks = obj.clicks + 1
    obj.save(update_fields=['clicks'])
    return HttpResponseRedirect(obj.original_url)

def stats(request, code):
    obj = get_object_or_404(ShortURL, short_code=code)
    short_link = request.build_absolute_uri(reverse('links:follow', args=[obj.short_code]))
    return render(request, 'links/stats.html', {'obj': obj, 'short_link': short_link})


# Create your views here.
