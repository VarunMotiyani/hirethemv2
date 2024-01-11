from .models import Job, Company, Application
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from .form import JobCreateForm,CompanyCreateForm, ApplicationForm
from django.http import Http404
from hirethemv2.users.models import User
import csv
from django.http import HttpResponse
import os
import zipfile
from django.conf import settings


def job_list(request):
    jobs = Job.objects.all()
    # colors = ["badge alert-success","badge alert-danger","badge alert-info"]
    paginator = Paginator(jobs, per_page=6)
    page_number = request.GET.get("page", 1)
    all_jobs = paginator.page(page_number)
    return render(request, "jobs/job_list.html", {"jobs": all_jobs})

@login_required
def show_student_list(request, pk):
    job = get_object_or_404(Job, id=pk)
    applications = Application.objects.filter(job=job)
    return render(request, "jobs/student_list.html", {"job": job, "applications": applications})

@login_required
def apply_job(request, pk):
    job = get_object_or_404(Job, id=pk)
    user = request.user

    if request.method == "POST":
        form = ApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            application = form.save(commit=False)
            application.user = request.user
            application.job = job
            application.save()
            return redirect("jobs-detail", pk=job.id)
    else:
            form = ApplicationForm(initial={
            'user': user,
            'name': user.name,
            'urn_number': user.urn_number,
            'department': user.department,
            'address': user.address,
            'github': user.github,
            'tenth_percentage': user.tenth_percentage,
            'tenth_school_name': user.tenth_school_name,
            'twelth_percentage': user.twelth_percentage,
            'twelth_school_name': user.twelth_school_name,
            'current_cgpa': user.current_cgpa,
            'active_backlogs': user.active_backlogs,
        })

    context = {"form": form, "job": job}
    return render(request, "jobs/apply_job.html", context)

@login_required
def detailed_job(request, pk):
    try:
        job = get_object_or_404(Job, id=pk)
    except Exception as e:
        raise e

    return render(request, "jobs/detailed_job.html", {"job": job})


@user_passes_test(lambda u: u.is_staff)
def create_job(request):
    form = JobCreateForm()
    # process data from form
    if request.method == "POST":
        form = JobCreateForm(request.POST)
        if form.is_valid():
            job = form.save(commit=False)
            job.host = request.user
            job.save()
            form.save_m2m()  # Save ManyToMany fields
            job.applicants.add(request.user)
            return redirect("jobs")
        else:
            print(form.errors)
    context = {"form": form}
    return render(request, "jobs/job_form.html", context)

@user_passes_test(lambda u: u.is_staff)
def create_company(request):
    form = CompanyCreateForm()
    # process data from form
    if request.method == "POST":
        form = CompanyCreateForm(request.POST)
        if form.is_valid():
            # the below line will save the form data in model Company
            form.save()
            return redirect("createjob")
    context = {"form": form}
    return render(request, "jobs/company_form.html", context)


@user_passes_test(lambda u: u.is_staff)
def update_job(request, pk):
    job = Job.objects.get(id=pk)
    form = JobCreateForm(instance=job)
    if request.method == "POST":
        form = JobCreateForm(request.POST, instance=job)
        if form.is_valid():
            form.save()
            return redirect("jobs-detail",pk=pk)
        else:
            print(form.errors)
    context = {"form": form, "job": job}
    return render(request, "jobs/job_form.html", context)



def download_student_list_csv(request, job_id):
    job = get_object_or_404(Job, id=job_id)
    applications = Application.objects.filter(job=job)

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="student_list_{job.id}.csv"'

    writer = csv.writer(response)
    # Write header
    writer.writerow(['Name', 'URN Number', 'Department', 'Address', 'Tenth Percentage', 'Tenth School',
                     'Twelth Percentage', 'Twelth School', 'Current CGPA', 'Active Backlogs'])
    
    # Write data
    for application in applications:
        user = application.user
        writer.writerow([user.name, user.urn_number, user.department, user.address,
                         user.tenth_percentage, user.tenth_school_name, user.twelth_percentage,
                         user.twelth_school_name, user.current_cgpa, user.active_backlogs,
                         ])

    return response


def download_resumes(request, job_id):
    job = get_object_or_404(Job, id=job_id)
    company_name = job.company.name
    resumes_path = os.path.join(settings.MEDIA_ROOT, 'resumes', company_name)

    # Create a zip file
    zip_file_path = os.path.join(settings.MEDIA_ROOT, 'resumes', f'{company_name}_resumes.zip')
    with zipfile.ZipFile(zip_file_path, 'w') as zip_file:
        for root, _, files in os.walk(resumes_path):
            for file in files:
                file_path = os.path.join(root, file)
                arc_name = os.path.relpath(file_path, resumes_path)
                zip_file.write(file_path, arc_name)

    # Create an HttpResponse with the zip file
    response = HttpResponse(content_type='application/zip')
    response['Content-Disposition'] = f'attachment; filename="{company_name}_resumes.zip"'

    with open(zip_file_path, 'rb') as zip_file:
        response.write(zip_file.read())

    # Clean up: remove the temporary zip file
    os.remove(zip_file_path)

    return response



@user_passes_test(lambda u: u.is_staff)
def delete_job(request, pk):
    data = get_object_or_404(Job, id=pk)
    if data.host == request.user:
        data.delete()
        return redirect('home')
    else:
        raise Http404


