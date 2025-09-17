from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.core import serializers
from main.forms import NewsForm
from main.models import News
from django.db.utils import ProgrammingError, OperationalError
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib  import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.urls import reverse
import datetime

def _safe_all_news():
    """Return all News objects or an empty queryset if the table doesn't exist yet.

    This prevents the site from crashing on fresh deployments before migrations run.
    """
    try:
        return News.objects.all()
    except (ProgrammingError, OperationalError):
        return News.objects.none()

def register(request):
    form = UserCreationForm()

    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your account has been successfully created!')
            return redirect('main:login')
    context = {'form':form}
    return render(request, 'register.html', context)

def login_user(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            response = HttpResponseRedirect(reverse("main:show_main"))
            response.set_cookie('last_login', str(datetime.datetime.now()))
            return response
    else:
        form = AuthenticationForm(request)

    context = {'form': form}
    return render(request, 'login.html', context)

def logout_user(request):
    logout(request)
    response = HttpResponseRedirect(reverse('main:login'))
    response.delete_cookie('last_login')
    return response

@login_required(login_url='/login')
def show_main(request):
    filter_type = request.GET.get("filter", "all")
    if filter_type == "all":
        news_list = _safe_all_news()
    else:
        # Show only current user's articles
        try:
            news_list = News.objects.filter(user=request.user)
        except (ProgrammingError, OperationalError):
            news_list = News.objects.none()

    context = {
        'npm': '2406453530',
        'name': request.user.username,
        'class': 'PBP KKI',
        'news_list': news_list,
        'last_login': request.COOKIES.get('last_login', 'Never')
    }

    return render(request, "main.html", context)

@login_required(login_url='/login')
def create_news(request):
    form = NewsForm(request.POST or None)

    if form.is_valid() and request.method == "POST":
        news_entry = form.save(commit=False)
        if request.user.is_authenticated:
            news_entry.user = request.user
        news_entry.save()
        return redirect('main:show_main')

    context = {'form': form}
    return render(request, "create_news.html", context)

@login_required(login_url='/login')
def show_news(request, id):
    news = get_object_or_404(News, pk=id)
    news.increment_views()

    context = {
        'news': news
    }

    return render(request, "news_detail.html", context)


def show_xml(request):
    news_list = _safe_all_news()
    xml_data = serializers.serialize("xml", news_list)
    return HttpResponse(xml_data, content_type="application/xml")


def show_json(request):
    news_list = _safe_all_news()
    json_data = serializers.serialize("json", news_list)
    return HttpResponse(json_data, content_type="application/json")


def show_xml_by_id(request, id):
    try:
        news_item = News.objects.filter(pk=id)
        xml_data = serializers.serialize("xml", news_item)
        return HttpResponse(xml_data, content_type="application/xml")
    except News.DoesNotExist:
        return HttpResponse(status=404)


def show_json_by_id(request, id):
    try:
        news_item = News.objects.get(pk=id)
        json_data = serializers.serialize("json", [news_item])
        return HttpResponse(json_data, content_type="application/json")
    except News.DoesNotExist:
        return HttpResponse(status=404)