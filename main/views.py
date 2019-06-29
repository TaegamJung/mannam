from django.shortcuts import render
# View에 Model(Post 게시글) 가져오기
from .models import Post

from django.views.generic.base import TemplateView

from django.views.generic.edit import CreateView
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy


from django.views.generic.edit import FormView
from .forms import PostSearchForm
from django.db.models import Q
from django.shortcuts import render


class SearchFormView(FormView):
    form_class = PostSearchForm
    template_name = 'main/post_search.html'
    
    def form_valid(self, form):
        schWord = '%s' % self.request.POST['search_word']
        post_list = Post.objects.filter(Q(postname__icontains=schWord) | Q(contents__icontains=schWord)).distinct()
        
        context = {}
        context['form'] = form
        context['search_term'] = schWord
        context['object_list'] = post_list
        
        return render(self.request, self.template_name, context)
    

class UserCreateView(CreateView):
    template_name = 'registration/register.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('register_done')
    
class UserCreateDone(TemplateView):
    template_name = 'registration/register_done.html'


# index.html 페이지를 부르는 index 함수
class index(TemplateView):
    template_name = 'main/index.html'
    
    
# blog.html 페이지를 부르는 blog 함수
def blog(request):
    # 모든 Post를 가져와 postlist에 저장합니다
    postlist = Post.objects.all()
    # blog.html 페이지를 열 때, 모든 Post인 postlist도 같이 가져옵니다 
    return render(request, 'main/blog.html', {'postlist': postlist})

# blog의 게시글(posting)을 부르는 posting 함수
def posting(request, pk):
    # 게시글(Post) 중 primary_key를 이용해 하나의 게시글(post)를 찾습니다
    post = Post.objects.get(pk=pk)
    # posting.html 페이지를 열 때, 찾아낸 게시글(post)을 같이 가져옵니다 
    return render(request, 'main/posting.html', {'post': post})

def new_feed(request):
    return render(request, 'new_feed.html')



