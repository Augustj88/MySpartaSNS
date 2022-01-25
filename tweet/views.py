from django.shortcuts import render, redirect
from .models import TweetModel # tweet모델을 가져와 작업
from .models import TweetComment
from django.contrib.auth.decorators import login_required #로그인되어야만 함수 실행함
from django.views.generic import ListView, TemplateView

# Create your views here.

def home(request):
    user = request.user.is_authenticated  #user가 있는지 판단/user가 로그인하면
    if user:
        return redirect('/tweet')
    else:
        return redirect('/sign-in')

def tweet(request):
    if request.method == 'GET':
        user = request.user.is_authenticated
        if user: #로그인 사용자가 있다면
            all_tweet = TweetModel.objects.all().order_by('-created_at') #order.by역순출력, -사용으로 또 역순출력
            return render(request, 'tweet/home.html',{'tweet':all_tweet}) #딕셔너리키값 tweet
        else: #로그인 사용자가 없다면
            return redirect('/sign-in')
    elif request.method == "POST":
        tags = request.POST.get('tag','').split(',')
        user = request.user
        content = request.POST.get('my-content','')

        if content == '':
            all_tweet = TweetModel.objects.all().order_by('-created_at')
            return render(request, 'tweet/home.html',{'error':'글은 공백일 수 없습니다.', 'tweet':all_tweet})
        else:
            my_tweet = TweetModel.objects.create(author=user, content=content)
            for tag in tags:
                tag = tag.strip()
                if tag!='':
                    my_tweet.tags.add(tag)
            my_tweet.save()
            return redirect('/tweet')


#태그기능
class TagCloudTV(TemplateView):
    template_name = 'taggit/tag_cloud_view.html'

class TaggedObjectLV(ListView):
    template_name = 'taggit/tag_with_post.html'
    model = TweetModel

    def get_queryset(self):
        return TweetModel.objects.filter(tags__name=self.kwargs.get('tag'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tagname'] = self.kwargs['tag']
        return context


@login_required
def delete_tweet(request, id): #로그인한 사용자의 글만 삭제
    my_tweet = TweetModel.objects.get(id=id)
    my_tweet.delete()
    return redirect('/tweet')

@login_required
def detail_tweet(request, id):
    my_tweet = TweetModel.objects.get(id=id)
    tweet_comment = TweetComment.objects.filter(tweet_id=id).order_by('-created_at')
    return render(request, 'tweet/tweet_detail.html',{'tweet':my_tweet,'comment':tweet_comment})

@login_required
def write_comment(request, id):
    if request.method == 'POST':
        comment = request.POST.get("comment","")
        current_tweet = TweetModel.objects.get(id=id)

        TC = TweetComment()
        TC.comment = comment
        TC.author = request.user
        TC.tweet = current_tweet
        TC.save()

        return redirect('/tweet/'+str(id))


@login_required
def delete_comment(request, id):
    comment = TweetComment.objects.get(id=id)
    current_tweet = comment.tweet.id
    comment.delete()
    return redirect('/tweet/'+str(current_tweet))