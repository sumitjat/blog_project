from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render,get_object_or_404
from taggit.models import Tag

from app.forms import EmailSendForm
from app.models import Post
from django.views.generic import ListView
from django.core.mail import send_mail
from app.forms import CommentForm
# Create your views here.

def post_list_view(req,tag_slug=None):
    post_list=Post.objects.all()

    tag=None
    if tag_slug:
        tag=get_object_or_404(Tag,slug=tag_slug)
        post_list=post_list.filter(tags__in=[tag])

    paginator=Paginator(post_list,3)
    page_no=req.GET.get('page')
    try:
        post_list=paginator.page(page_no)
    except PageNotAnInteger:
        post_list=paginator.page(1)
    except EmptyPage:
        post_list=paginator.page(paginator.num_pages)

    return render(req,"post_list.html",{'post_list':post_list,'tag':tag})

class PostList(ListView):
    model=Post
    paginate_by = 2
    template_name = 'post_list.html'



def post_detail(req,year,month,day,post):
    post=get_object_or_404(Post,slug=post,status='published',publish__day=day,publish__year=year,publish__month=month)
    comments=post.comments.filter(active=True) # comments is related name
    csubmit=False
    if req.method == 'POST':
        form=CommentForm(req.POST)
        if form.is_valid():
            new_comment=form.save(commit=False)
            new_comment.post=post
            new_comment.save()
            csubmit=True
    else:
        form=CommentForm()
    return render(req,'post_detail.html',{'post':post,'form':form,'csubmit':csubmit,'comments':comments})



def email_send(req,id):
    post=get_object_or_404(Post,id=id,status='published')
    form=EmailSendForm()
    sent=False
    if req.method=='POST':
        form=EmailSendForm(req.POST)
        if form.is_valid():
            to = form.cleaned_data['to']
            name=form.cleaned_data['name']
            post_url=req.build_absolute_uri(post.get_absolute_url())
            comment=form.cleaned_data['comment']
            subject=name,' Recommend you ',post.title,comment,post_url
            send_mail(subject,'message','jatsumit017@gmail.com',(to,))
            sent=True

    return render(req,'sharebymail.html',{'form':form,'post':post,'sent':sent})



