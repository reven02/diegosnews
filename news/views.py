from django.http import HttpResponse, HttpRequest, HttpResponseNotAllowed, JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_exempt
from .models import Story
from datetime import datetime

# Create your views here.

@csrf_exempt
def log_in(request: HttpRequest):

    if request.method != 'POST':
        return HttpResponseNotAllowed(['POST'], content='Only POST methods allowed.')

    username = request.POST['username']
    password = request.POST['password']

    user = authenticate(request, username=username, password=password)

    if user is not None:
        login(request, user)
        return HttpResponse(f'Welcome back {user.first_name}!')
    else:
        return HttpResponse('Failed to log in.', status=401)
    

@csrf_exempt
def log_out(request: HttpRequest):

    if request.method != 'POST':
        return HttpResponseNotAllowed(['POST'], content='Only POST methods allowed.')

    if not request.user.is_authenticated:
        return HttpResponse('You need to be a logged user to log out.', status=503)

    logout(request)
    return HttpResponse('Goodbye!')


@csrf_exempt
def stories(request: HttpRequest):
    if request.method == 'POST':
        return _post_story(request)
    
    elif request.method == 'GET':
        return _get_story(request)
    
    else:
        return HttpResponseNotAllowed(['POST', 'GET'], content='Only GET and POST methods allowed.')


def _post_story(request: HttpRequest):

    if not request.user.is_authenticated:
        return HttpResponse('You need to be a logged user to post a story.', status=503)

    headline = request.POST['headline']
    category = request.POST['category']
    region = request.POST['region']
    details = request.POST['details']

    allowed_categories = ['pol', 'art', 'tech', 'trivia']
    allowed_regions = ['uk', 'eu', 'w']

    if category not in allowed_categories:
        return HttpResponse(f'Allowed categories: {allowed_categories}', status=503)
    if region not in allowed_regions:
        return HttpResponse(f'Allowed regions: {allowed_regions}', status=503)

    story = Story(
        headline=headline,
        category=category,
        region=region,
        author=request.user,
        details=details,
    )

    story.save()

    return HttpResponse('Story added.', status=201)


def _get_story(request: HttpRequest):
    story_cat = request.GET['story_cat']
    story_region = request.GET['story_region']
    story_date = request.GET['story_date']

    filters = {}
    if story_cat != '*':
        filters['category'] = story_cat
    if story_region != '*':
        filters['region'] = story_region
    if story_date != '*':
        filters['date__gte'] = datetime.strptime(story_date, '%d/%m/%Y')

    stories = Story.objects.filter(**filters)
    stories = list(map(lambda s: s.serialize(), stories))

    data = {'stories': stories}
    
    return JsonResponse(data)


@csrf_exempt
def delete_story(request: HttpRequest, key: int):

    if request.method != 'DELETE':
        return HttpResponseNotAllowed(['DELETE'], content='Only DELETE methods allowed.')

    if not request.user.is_authenticated:
        return HttpResponse('You need to be a logged user to post a story.', status=503)

    try:
        Story.objects.get(pk=key).delete()
    except:
        return HttpResponse(f'Story <{key}> does not exist.', status=200)

    return HttpResponse(f'Story <{key}> deleted.', status=200)
    