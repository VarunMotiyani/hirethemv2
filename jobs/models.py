from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField
from taggit.managers import TaggableManager
from django.urls import reverse
from django.contrib.auth import get_user_model
from datetime import date
from django.core.validators import FileExtensionValidator
import os
import zipfile
from django.http import HttpResponse
from django.utils.text import slugify

User = get_user_model()

def resume_upload_to(instance, filename):
    company_name = instance.job.company.name if instance.job.company else 'unknown_company'
    return f"resumes/{company_name}/{filename}"

class Company(models.Model):
    name = models.CharField(max_length=500)
    description = RichTextUploadingField()
    logo = models.ImageField(
        upload_to="jobs/companylogos",
        blank=True,
        null=True,
    )
    website = models.CharField(max_length=100, default="")
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "company"
        verbose_name_plural = "companies"


class Job(models.Model):
    JOB_TYPE = (("1", "Full time"), ("2", "Part time"), ("3", "Internship"))

    title = models.CharField(max_length=300)
    description = RichTextUploadingField()
    host = models.ForeignKey(User, on_delete=models.CASCADE)
    location = models.CharField(max_length=150)
    type = models.CharField(choices=JOB_TYPE, max_length=10)
    last_date = models.DateField()
    company = models.ForeignKey(
        Company, on_delete=models.CASCADE, null=True, blank=True
    )
    link = models.CharField(max_length=500, default="", blank=True, null=True, help_text="Your google form link")
    created = models.DateTimeField(auto_now_add=True)
    salary = models.CharField(max_length=8, blank=True)
    tags = TaggableManager()
    applicants = models.ManyToManyField(User, through='jobs.Application', related_name='applications')

    class Meta:
        ordering = ["-created"]

    def get_absolute_url(self):
        return reverse("jobs:jobs-detail", kwargs={"pk": self.pk})

    def __str__(self):
        return self.title
    
    @property
    def is_past_due_date(self):
        return date.today() > self.last_date

    def download_resumes(self, request, queryset):
         # Create a unique folder name for the ZIP file
        folder_name = slugify(f"resumes_{self.company.name}")
        zip_filename = f"{folder_name}.zip"

        # Create a temporary directory to store the resumes
        temp_dir = f"/tmp/{folder_name}/"
        os.makedirs(temp_dir)

        # Add each resume to the temporary directory
        for application in self.applications.all():
            # Assuming the resumes are stored in the 'resumes' folder of each company
            resume_path = os.path.join('resumes', application.job.company.name, os.path.basename(application.resume.name))
            resume_content = application.resume.read()

            # Create a folder structure inside the temporary directory
            folder_structure = os.path.join(temp_dir, resume_path)
            os.makedirs(os.path.dirname(folder_structure), exist_ok=True)

            # Save the resume content to the temporary directory
            with open(os.path.join(temp_dir, resume_path), 'wb') as resume_file:
                resume_file.write(resume_content)

        # Create a ZIP file containing all resumes
        with zipfile.ZipFile(zip_filename, 'w') as zip_file:
            for foldername, subfolders, filenames in os.walk(temp_dir):
                for filename in filenames:
                    file_path = os.path.join(foldername, filename)
                    zip_file.write(file_path, os.path.relpath(file_path, temp_dir))

        # Create an HttpResponse with the ZIP file and appropriate headers
        response = HttpResponse(open(zip_filename, 'rb').read(), content_type='application/zip')
        response['Content-Disposition'] = f'attachment; filename={zip_filename}'

        # Clean up: Remove the temporary directory and ZIP file
        os.rmdir(temp_dir)
        os.remove(zip_filename)

        return response

    download_resumes.short_description = "Download Resumes for Selected Job"





class Application(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    resume = models.FileField(upload_to=resume_upload_to, default="",  validators=[FileExtensionValidator(allowed_extensions=['pdf'])])

    class Meta:
        unique_together = ["user", "job"]

    def __str__(self):
        return f"{self.user} applied to {self.job}"
