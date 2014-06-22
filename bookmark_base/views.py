# Create your views here.
from django.template import RequestContext
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render_to_response
from django.contrib.auth import logout
from django.shortcuts import get_object_or_404
from django.core.context_processors import csrf

from accounts.forms import *
from bookmark_base.models import *


def mainpage(request, username):
    return render_to_response('mainpage.html')


def home(request):
    shares = ShareItem.objects.order_by('datetimeField')[:10]
    variables = RequestContext(request, {
        'user': request.user,
        'shares': shares,
        'show_tags': True,
        'show_user': True
    })
    return render_to_response('home.html', variables)

def logoutpage(request):
    logout(request)
    return HttpResponseRedirect('/')


def addmarks(request):
    ajax = 'ajax' in request.GET
    if request.method == 'POST':
        form = BookmarkForm(request.POST)
        if form.is_valid():
            link, dummy = Url.objects.get_or_create(
                url=form.cleaned_data['url']
            )
            bookmark, created = Bookmark.objects.get_or_create(
                uname=request.user,
                link=link
            )
            bookmark.title = form.cleaned_data['title']
            if not created:
                bookmark.tag_set.clear()
            tag_names = form.cleaned_data['tag'].split()
            for tag_name in tag_names:
                tag, dummy = Tag.objects.get_or_create(
                    content=tag_name
                )
                bookmark.tag_set.add(tag)
            if form.cleaned_data['share']:
                shared, created = ShareItem.objects.get_or_create(
                    bookmark=bookmark
                )
                if created:
                    shared.uvote.add(request.user)
                    shared.save()
            bookmark.save()
            if ajax:
                variables = RequestContext(request, {
                    'bookmarks': [bookmark],
                    'show_tags': True,
                    'show_edit': True
                })
                return render_to_response("bookmark_list.html", variables)
            else:
                return HttpResponseRedirect('/user/%s' % (request.user.username))
        else:
            if ajax:
                return HttpResponse(u'failure')
    elif 'url' in request.GET:
        url = request.GET['url']
        title = ''
        tag = ''
        try:
            link = Url.objects.get(url=url)
            bookmark = Bookmark.objects.get(
                uname=request.user,
                link=link
            )
            title = bookmark.title
            tag = ''.join(
                tag.content for tag in bookmark.tag_set.all()
            )
        except(Url.DoesNotExist, Bookmark.DoesNotExist):
            pass
        form = BookmarkForm({
            'url': url,
            'title': title,
            'tag': tag
        }
        )
    else:
        form = BookmarkForm()
    variables = RequestContext(request, {
        'form': form
    })
    if ajax:
        return render_to_response('bookmark_save_form.html', variables)
    else:
        return render_to_response('bookmark_save.html', variables)





def bookmarkpage(request, bookmark_id):
    c = {}
    c.update(csrf(request))
    share = get_object_or_404(
        ShareItem,
        id=bookmark_id
    )
    variables = RequestContext(request, {
        'shared_bookmark': share
    })
    return render_to_response('bookmark_page.html', variables)


def tagpage(request, tag_name):
    tag = get_object_or_404(Tag, content=tag_name)
    bookmarks = tag.book.order_by('-id')
    variables = RequestContext(request, {
        'bookmarks': bookmarks,
        'tag_name': tag_name,
        'show_tags': True,
        'show_user': True
    })
    return render_to_response('tag_page.html', variables)


def tagcloundpage(request):
    tags = Tag.objects.order_by('content')
    for tag in tags:
        tag.count = tag.book.count()
    variables = RequestContext(request, {
        'tags': tags
    })
    return render_to_response('tag_clound_page.html', variables)


def search(request):
    form = SearchForm()
    bookmarks = []
    show_result = False
    if 'query' in request.GET:
        show_result = True
        query = request.GET['query'].strip()
        if query:
            form = SearchForm({'query': query})
            bookmarks = Bookmark.objects.filter(title__icontains=query)[:10]
    variables = RequestContext(request, {
        'form': form,
        'bookmarks': bookmarks,
        'show_result': show_result,
        'show_tags': True,
        'show_user': False
    })
    if request.GET.has_key('ajax'):
        return render_to_response('bookmark_list.html', variables)
    else:
        return render_to_response('search.html', variables)


def addvote(request):
    if 'id' in request.GET:
        try:
            id = request.GET['id']
            share = ShareItem.objects.get(id=id)
            uvote = share.uvote.filter(
                username=request.user.username
            )
            if not uvote:
                share.votes += 1
                share.uvote.add(request.user)
                share.save()
        except ShareItem.DoesNotExist:
            raise Http404('bookmark not found')
    if 'HTTP_REFERER' in request.META:
        return HttpResponseRedirect(request.META['HTTP_REFERER'])
    return HttpResponseRedirect('/')


def storeurl(request):
    if 'id' in request.GET:
        try:
            id = request.GET['id']
            share = ShareItem.objects.get(id=id)
            bookmark = share.bookmark
            has = Bookmark.objects.filter(
                link=bookmark.link,
                uname=request.user
            )
            if not has:
                tags = bookmark.tag_set.all()
                bookmark.id = None
                bookmark.uname = request.user
                bookmark.save()
                for tag in tags:
                    bookmark.tag_set.add(tag)
                bookmark.save()
        except ShareItem.DoesNotExist:
            raise Http404('bookmark not found')
    if 'HTTP_REFERER' in request.META:
        return HttpResponseRedirect(request.META['HTTP_REFERER'])
    return HttpResponseRedirect('/')


def deleteurl(request):
    if 'id' in request.GET:
        try:
            id = request.GET['id']
            bookmark = Bookmark.objects.get(id=id)
            bookmark.delete()
        except Bookmark.DoesNotExist:
            raise Http404('bookmark not found')
    if 'HTTP_REFERER' in request.META:
        return HttpResponseRedirect(request.META['HTTP_REFERER'])
    return HttpResponseRedirect('/')


def friendspage(request, username):
    user = get_object_or_404(User, username=username)
    friends = [freindship.touser for freindship in user.friend_set.all()]
    bookmarks = Bookmark.objects.filter(
        uname__in=friends
    ).order_by('-id')
    variables = RequestContext(request, {
        'username': username,
        'friends': friends,
        'bookmarks': bookmarks[:10],
        'show_tags': True,
        'show_user': True
    })
    return render_to_response('friends.html', variables)

def addfriend(request):
    if 'username' in request.GET:
        friend = get_object_or_404(User, username=request.GET['username'])
        friendship = Freindship(
            fromuser=request.user,
            touser=friend
        )
        friendship.save()
        return HttpResponseRedirect('/friends/%s/' % request.user.username)
    else:
        raise Http404

