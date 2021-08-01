from django.db.models import Q

import json
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core import serializers
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from django.urls import reverse_lazy

import stripe
from django.shortcuts import render, redirect, HttpResponse
from django.urls import reverse

stripe.api_key = "sk_test_m8uMqrmqBO20oqFVcziqdXiY00XaPhx8AN"

from .forms import CommentForm, post_create
from .models import Post, Comment, Credit, StartupSubmissionList
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView


def CPointsPlans(request, plans):
    if plans == 'Bronze':
        return render(request, 'creditTemp/bronze.html')

    elif plans == 'Silver':
        return render(request, 'creditTemp/silver.html')

    elif plans == 'Gold':
        return render(request, 'creditTemp/gold.html')

    else:
        return render(request, 'creditTemp/credit.html')


def BronzePlan(request):
    if request.method == 'POST':
        try:
            amount = int(request.POST['amount'])
            customer = stripe.Customer.create(
                email=request.POST['email'],
                name=request.POST['nickname'],
                source=request.POST['stripeToken'],
                address={
                    'line1': '510 Townsend St',
                    'postal_code': '98140',
                    'city': 'San Francisco',
                    'state': 'CA',
                    'country': 'US',
                },

            )

            charge = stripe.Charge.create(
                customer=customer,
                amount=amount * 100,
                currency='usd',
                description="Bronze"

            )

            user = request.user
            cred = Credit.objects.get(author=user)
            add = cred.Credit_Points
            gg = add + int(100)
            Credit.objects.filter(author=request.user).update(Credit_Points=gg)

            return redirect('blog-home')

        except:
            HttpResponse('form is invalid')


def SilverPlan(request):
    if request.method == 'POST':
        try:
            amount = int(request.POST['amount'])
            customer = stripe.Customer.create(
                email=request.POST['email'],
                name=request.POST['nickname'],
                source=request.POST['stripeToken'],
                address={
                    'line1': '510 Townsend St',
                    'postal_code': '98140',
                    'city': 'San Francisco',
                    'state': 'CA',
                    'country': 'US',
                },

            )

            charge = stripe.Charge.create(
                customer=customer,
                amount=amount * 100,
                currency='usd',
                description="Bronze"

            )

            user = request.user
            cred = Credit.objects.get(author=user)
            add = cred.Credit_Points
            gg = add + int(220)
            Credit.objects.filter(author=request.user).update(Credit_Points=gg)

            return redirect('blog-home')

        except:
            HttpResponse('form is invalid')


def GoldPlan(request):
    if request.method == 'POST':
        try:
            amount = int(request.POST['amount'])
            customer = stripe.Customer.create(
                email=request.POST['email'],
                name=request.POST['nickname'],
                source=request.POST['stripeToken'],
                address={
                    'line1': '510 Townsend St',
                    'postal_code': '98140',
                    'city': 'San Francisco',
                    'state': 'CA',
                    'country': 'US',
                },

            )

            charge = stripe.Charge.create(
                customer=customer,
                amount=amount * 100,
                currency='usd',
                description="Bronze"

            )

            user = request.user
            cred = Credit.objects.get(author=user)
            add = cred.Credit_Points
            gg = add + int(500)
            Credit.objects.filter(author=request.user).update(Credit_Points=gg)

            return redirect('blog-home')

        except:
            HttpResponse('form is invalid')


def CPoints(request):
    return render(request, 'creditTemp/credit.html')


def home(request):
    abc = Post.objects.order_by('-date_posted')
    cred = Credit.objects.filter(author=request.user)
    print('-=--------------------------credPoints=-----------------', cred)
    context = {
        'posts': Post.objects.all(),
        'abc': abc,
        'cred': cred

    }
    return render(request, 'blog/home.html', context)


class PostListView(ListView):
    template_name = 'blog/home.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 10

    # def get_context_data(self, **kwargs):
    #     context = super(PostListView, self).get_context_data(**kwargs)
    #     context.update({
    #         'credss': Credit.objects.filter(author=self.request.user),
    #     })
    #     return context

    def get_queryset(self):
        return Post.objects.all()


class UserPostListView(ListView):
    model = Post
    template_name = 'blog/user_posts.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    paginate_by = 10

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')


# also add Comment view
class PostDetailView(DetailView):
    model = Post


# class based view

# class PostCreateView(LoginRequiredMixin, CreateView):
#     model = Post
#     fields = ['title', 'content']
#
#     def form_valid(self, form):
#         form.instance.author = self.request.user
#         return super().form_valid(form)


# function based view with stripe payment

def post_create1(request):
    if request.method == 'POST':
        form = post_create(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.author = request.user
            cred = Credit.objects.get(author=request.user)
            add = cred.Credit_Points
            if add > int(20):
                gg = add - int(20)
                Credit.objects.filter(author=request.user).update(Credit_Points=gg)
                user.save()
            else:
                print('you have no credits')
            # try:
            #     amount = int(request.POST['amount'])
            #     customer = stripe.Customer.create(
            #         email=request.POST['email'],
            #         name=request.POST['nickname'],
            #         source=request.POST['stripeToken'],
            #         address={
            #             'line1': '510 Townsend St',
            #             'postal_code': '98140',
            #             'city': 'San Francisco',
            #             'state': 'CA',
            #             'country': 'US',
            #         },
            #
            #     )
            #
            #     charge = stripe.Charge.create(
            #         customer=customer,
            #         amount=amount * 100,
            #         currency='usd',
            #         description="donation"
            #
            #     )
            #
            #     user.save()
            #     return redirect('blog-home')
            #
            # except:
            #     HttpResponse('form is invalid')

    else:
        form = post_create()

    return render(request, 'blog/post_form.html', {'form': form})


# simple function based view

# def post_create1(request):
#     if request.method == 'POST':
#         form = post_create(request.POST)
#         if form.is_valid():
#             user = form.save(commit=False)
#             user.author = request.user
#             user.save()
#             return redirect('/')
#     else:
#         form = post_create()
#
#     return render(request, 'blog/post_form.html', {'form': form})


class AddCommentView(CreateView):
    model = Comment
    template_name = 'blog/add_comment.html'
    form_class = CommentForm
    success_url = reverse_lazy('blog-home')

    def form_valid(self, form):
        form.instance.post_id = self.kwargs['pk']
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


def about(request):
    return render(request, 'blog/about.html', {'title': 'About'})


# @login_required()
# def premium_data(request):
#     if request.method == 'POST':
#         checkbox_data = request.POST.getlist('fcm')
#
#         if len(checkbox_data) == 0:
#             return redirect('premium-data')
#
#         print('-------------------------------------------------', checkbox_data)  # ['7', '8', '9']
#         print(type(checkbox_data))  # list
#         # print('len', len(checkbox_data))  # length of list ex: 3
#         len_list = len(checkbox_data)
#         total_credit = int(len_list) * 30
#         print('total-credit is', total_credit)
#
#         # now we check if user have Enuff Credit to purchase this premium data
#         cred = Credit.objects.get(author=request.user)
#         credit_points = cred.Credit_Points
#         if credit_points >= int(total_credit):
#             print('user have credits')
#
#             # now we cut the credit points
#             gg = credit_points - int(total_credit)
#             Credit.objects.filter(author=request.user).update(Credit_Points=gg)
#
#             # now we add premium data to user account
#             for i in checkbox_data:
#                 data1 = int(i)
#                 dd = SSList.objects.filter(id=data1)[0]
#                 # SSListUser.objects.create(name=dd, user=request.user)
#
#             return HttpResponse('done')
#
#         else:
#             return HttpResponse('user have not credit')
#
#     if request.method == 'GET':
#         first_five_data = SSList.objects.all()[:5]
#
#         # user_premium_data = SSListUser.objects.filter(user=request.user)
#         user_premium_list = []
#         # for iii in user_premium_data:
#         #     user_premium_list.append(iii.name_id)
#         # print(user_premium_list)
#         all_premium_exclude = SSList.objects.filter(id__in=user_premium_list)
#         # print(all_premium_exclude)
#
#         # user_premium_data_id = SSListUser.objects.filter(user=request.user)
#         user_id_list = []
#         # for iii in user_premium_data_id:
#         #     user_id_list.append(iii.name_id)
#         # print('---------------------iii-----------------', user_id_list)
#
#         all_data_exclude = SSList.objects.filter(~Q(id__in=user_id_list))[5:]
#         # print('------------------------------EXCLUDE-----------------------', all_data_exclude)
#         # all_data_exclude = SSList.objects.exclude(user=request.user)
#         context = {
#             'data': first_five_data,
#             'after': all_data_exclude,
#             'all_premium_exclude': all_premium_exclude
#         }
#         return render(request, 'premiumData/premium.html', context)


@login_required()
def premium_data(request):
    if request.method == 'POST':
        checkbox_data = request.POST.getlist('fcm')

        if len(checkbox_data) == 0:
            return redirect('premium-data')

        print('-------------------------------------------------', checkbox_data)  # ['7', '8', '9']
        print(type(checkbox_data))  # list
        # print('len', len(checkbox_data))  # length of list ex: 3
        len_list = len(checkbox_data)
        total_credit = int(len_list) * 30
        print('total-credit is', total_credit)

        # now we check if user have Enuff Credit to purchase this premium data
        cred = Credit.objects.get(author=request.user)
        credit_points = cred.Credit_Points
        if credit_points >= int(total_credit):
            print('user have credits')

            # now we cut the credit points
            gg = credit_points - int(total_credit)
            Credit.objects.filter(author=request.user).update(Credit_Points=gg)

            # now we add premium data to user account
            for i in checkbox_data:
                data1 = int(i)
                dd = SSList.objects.get(id=data1)
                dd.user1.add(request.user.id)
                print(dd)
                print(request.user.id)
                dd.save()
            return HttpResponse('done')
        else:
            return HttpResponse('user have not credit')

    if request.method == 'GET':
        first_five_data = StartupSubmissionList.objects.all()[:5]

        user_premium_data = StartupSubmissionList.objects.filter(user=request.user.id)
        user_premium_list = []
        for iii in user_premium_data:
            user_premium_list.append(iii.id)
        # print(user_premium_list)
        all_premium_exclude = StartupSubmissionList.objects.filter(id__in=user_premium_list)
        # print(all_premium_exclude)

        user_premium_data_id = StartupSubmissionList.objects.filter(user=request.user)
        user_id_list = []
        for iii in user_premium_data_id:
            user_id_list.append(iii.id)
        print('---------------------iii-----------------', user_id_list)

        all_data_exclude = StartupSubmissionList.objects.filter(~Q(id__in=user_id_list))[5:]
        # print('------------------------------EXCLUDE-----------------------', all_data_exclude)
        # all_data_exclude = SSList.objects.exclude(user=request.user)

        # while StartupSubmissionList.objects.count():
        #     StartupSubmissionList.objects.all().delete()

        context = {
            'data': first_five_data,
            'after': all_data_exclude,
            'all_premium_exclude': all_premium_exclude
        }
        return render(request, 'premiumData/premium.html')

@login_required()
def StartupSubmissionListTestesing(request):
    if request.method == 'POST':
        datatables = request.POST
        # Ambil draw
        draw = int(datatables.get('draw'))  #1
        # Ambil start
        start = int(datatables.get('start'))  #0
     
        # Ambil length (limit)
        length = int(datatables.get('length')) # 10
      
        # Ambil data search
        search = datatables.get('search[value]')
        # Set record total
        records_total = StartupSubmissionList.objects.all().count() #2048
        print('records_total', records_total)
        # Set records filtered
        records_filtered = int(records_total)

        invoices = StartupSubmissionList.objects.all()

        if search:
            invoices = StartupSubmissionList.objects.filter(
                    Q(name__icontains=search)|
                    Q(site__icontains=search)|
                    Q(site_type__icontains=search)|
                    Q(da_score__icontains=search)|
                    Q(monthly_traffic__icontains=search)|
                    Q(follow_unfollow_link__icontains=search)
                )
            records_total = invoices.count()
            records_filtered = records_total

        # Atur paginator
        paginator = Paginator(invoices, length)

        try:
            object_list = paginator.page(draw).object_list
        except PageNotAnInteger:
            object_list = paginator.page(draw).object_list
        except EmptyPage:
            object_list = paginator.page(paginator.num_pages).object_list

        data = [
            {   
                'id': inv.id,
                'name': inv.name,
                'site': inv.site,
                'site_type': inv.site_type,
                'da_score': inv.da_score,
                'monthly_traffic': inv.monthly_traffic,
                'follow_unfollow_link': inv.follow_unfollow_link,
            } for inv in object_list
        ]

        context = {
            'draw': draw,
            'recordsTotal': records_total,
            'recordsFiltered': records_filtered,
            'data': data,
        }
        
        return JsonResponse(context, safe=False)

