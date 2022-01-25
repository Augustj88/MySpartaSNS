from django.shortcuts import render, redirect
from .models import UserModel
from django.http import HttpResponse
from django.contrib.auth import get_user_model # 사용자가 db안에 있는지 검사하는 함수
from django.contrib import auth
from django.contrib.auth.decorators import login_required

# Create your views here.
def sign_up_view(request):
    if request.method == 'GET':
        user = request.user.is_authenticated
        if user:
            return redirect('/') #tweet/home함수
        else:
            return render(request, 'user/signup.html')
    elif request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        password2 = request.POST.get('password2', '')
        bio = request.POST.get('bio', '')

        # 데이터베이스에 유저가 있는지 없는지 확인(usermodel에있는usermodel=유저가입력한username)
        if password != password2: #패스워드가 같지 않다면
            return render(request,'user/signup.html',{'패스워드를 확인 해 주세요!'})
        else:
            if username == '' or password == '':
                return render(request,'user/signup.html',{'error':'사용자 이름과 비밀번호는 필수 값입니다.'})

            exist_user = get_user_model().objects.filter(username = username)
            if exist_user:
                return render(request, 'user/signup.html',{'error':'사용자가 존재합니다'})
            else: #사용자가 없을경우 정보 저장
                UserModel.objects.create_user(username=username, password=password, bio=bio) #정보저장이 한 줄로
                return redirect('/sign-in')


def sign_in_view(request):
    if request.method == 'POST': #화면에서 입력받음
        username = request.POST.get('username', '') #유저가 로그인창에 적은 이름
        password = request.POST.get('password', '') #유저가 로그인창에 적은 비번

        me = auth.authenticate(request, username=username, password=password) # 장고 기본 기능에서 유저네임과 비번 확인 가능
        if me is not None:
            auth.login(request, me)
            request.session['user'] = me.username
            return redirect('/')
        else:
            return render(request, 'user/signin.html',{'error':'유저이름 혹은 패스워드를 확인 해 주세요!'}) #다시 로그인페이지로 redirect

    elif request.method == 'GET':
        user = request.user.is_authenticated
        if user:
            return redirect('/')
        else:
            return render(request, 'user/signin.html')

@login_required #꼭 로그인 되어야 접근가능한 함수
def logout(request):
    auth.logout(request)
    return redirect('/')

# user/views.py

@login_required
def user_view(request): #get은 user_list를 보여줄것
    if request.method == 'GET':
        # 사용자를 불러오기, exclude와 request.user.username 를 사용해서 '로그인 한 사용자'를 제외하기
        user_list = UserModel.objects.all().exclude(username=request.user.username)
        return render(request, 'user/user_list.html', {'user_list': user_list})


@login_required
def user_follow(request, id):
    me = request.user #로그인사용자
    click_user = UserModel.objects.get(id=id) #내가 팔로우를 누른 사용자
    if me in click_user.followee.all(): #팔로우할 유저의 팔로우리스트 안에 내가 없다면 팔로우 안한 상태
        click_user.followee.remove(request.user)
    else:
        click_user.followee.add(request.user)
    return redirect('/user')