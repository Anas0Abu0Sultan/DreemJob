from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login as auth_login
from .forms import SignUpForm, JobForm, ApplyForm
from .models import  apply, job as jobs, freelancer as freelancers, category as categorys
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Count
from django.shortcuts import get_object_or_404


def index(request):
# Get the top 10 categories with the most jobs
    top_categories = categorys.objects.annotate(num_jobs=Count('job_category')).order_by('-num_jobs')[:10]
    job = jobs.objects.order_by('-created_at')[:8]
    freelancer = freelancers.objects.order_by('-id')[:10]
    context = {"top_categories":top_categories,
            "job": job,
            "freelancer": freelancer
                  }
    return render(request, "pages/index.html", context)









def all_jobs(request):
    alljobs = jobs.objects.all()
    paginator = Paginator(alljobs,10)
    page_number = request.GET.get('page')
    page_object = paginator.get_page(page_number)
    context = {
        "alljobs": page_object,
    }
    return render(request, "pages/jobs.html", context)






@login_required
def offers(request,job_id):
    job = get_object_or_404(jobs,id=job_id)
    applications = apply.objects.filter(job=job)
    count = len(applications)
    paginator = Paginator(applications,10)
    page_number = request.GET.get('page')
    page_object = paginator.get_page(page_number)
    context = {
        "page_object":page_object,
        "count": count,
        "job": job
        }
    return render(request, "pages/offers.html", context)




def all_jobs_category(request,category_id):
    category = get_object_or_404(categorys,id = category_id)
    # all_jobs = jobs.objects.filter(category=category)
    all_jobs = category.job_category.all()
    paginator = Paginator(all_jobs,10)
    page_number = request.GET.get('page')
    page_object = paginator.get_page(page_number)
    count = all_jobs.count()
    context = {
        "all_jobs": page_object,
        "category": category,
        "count":count,
        }
    return render(request, "pages/jobs_category.html", context)













@login_required
def job_details(request, job_id):
    job = get_object_or_404(jobs, id=job_id)
    freelancer = freelancers.objects.get(user=request.user)
    already_applied = apply.objects.filter(freelancer=freelancer, job=job).exists()
    application_date = None

    if already_applied:
        application = apply.objects.get(freelancer=freelancer, job=job)
        application_date = application.created_at

    if request.method == "POST":
        form = ApplyForm(request.POST, request.FILES)
        if form.is_valid():
            application = form.save(commit=False)
            application.freelancer = request.user.freelancer  # Assuming user has a Freelancer profile
            application.job = job
            application.save()
            return redirect('job_details', job_id=job.id)  # Redirect after successful submission
    else:
        form = ApplyForm()

    return render(request, 'pages/job_details.html', {
        'job': job,
        'already_applied': already_applied,
        'application_date': application_date,
        'form':form,
    })






def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # Redirect to the login page after successful signup
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})





@login_required
def profile(request, name):
    users = User.objects.get(username=name)
    context = {"users": users}
    if users == request.user:
        f = freelancers.objects.filter(user = users)
        return render(request, "registration/profile.html", {"users": users,"f": f})
    return render(request, "registration/profile.html", context)





# @login_required
# def createjob(request):
#     test = customer.objects.filter(user = request.user).count()
#     if request.method =="POST":
#         if test:
#             form = JobForm(request.POST,request.FILES)
#             if form.is_valid():
#                 job = form.save(commit=False)
#                 job.created_by = request.user.customer
#                 job.save()
#                 return redirect('index')
#         else:
#             return redirect('add_customer')
#     else:
#         form =JobForm()
#     context = {
#         'form': form,
#         }
#     return render(request, 'pages/create_job.html', context)   

