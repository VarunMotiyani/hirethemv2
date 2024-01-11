from django.urls import path, include
from .views import job_list, detailed_job, create_job,create_company,update_job, delete_job, apply_job, show_student_list, download_student_list_csv, download_resumes


urlpatterns = [
    path("", view=job_list, name="jobs"),
    path("?=<int:pk>/", view=detailed_job, name="jobs-detail"),
    path("?=<int:pk>/update", view=update_job,name="updatejob"),
    path("createjob/", view=create_job, name="createjob"),
    path("createcompany/", view=create_company, name="createcompany"),
    path("<int:pk>/apply/", view=apply_job, name="apply-job"),
    path("<int:pk>/student-list/", view=show_student_list, name="show-student-list"),
    path('<int:job_id>/download_student_list_csv/', download_student_list_csv, name='download_student_list_csv'),
    path('<int:job_id>/download-resumes/', download_resumes, name='download_resumes'),
]
