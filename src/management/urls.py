from django.urls import path

from . import views as management_views

urlpatterns = [
    path("login_admin/", management_views.login_admin, name="login_admin"),
    path("logout_admin/", management_views.logout_admin, name="logout_admin"),
    path("admin_dashboard/", management_views.admin_dashboard, name="admin_dashboard"),
    path("contact-admin/", management_views.contact_admin, name="contact_admin"),
    path("admin_tables/", management_views.admin_tables, name="admin_tables"),
    path("add-employee/", management_views.add_employee, name="add_employee"),
    path(
        "employee/edit/<str:id_number>/",
        management_views.edit_employee,
        name="edit_employee",
    ),
    path(
        "employee/delete/<str:id_number>/",
        management_views.delete_employee,
        name="delete_employee",
    ),
    path("add_allowance/", management_views.add_allowance, name="add_allowance"),
    path(
        "allowance/edit/<int:id>/",
        management_views.edit_allowance,
        name="edit_allowance",
    ),
    path("add_deduction/", management_views.add_deduction, name="add_deduction"),
    path("add_department/", management_views.add_department, name="add_department"),
    path("add_branch/", management_views.add_branch, name="add_branch"),
    path(
        "edit_department/<int:id>/",
        management_views.edit_department,
        name="edit_department",
    ),
    path("edit_branch/<int:id>/", management_views.edit_branch, name="edit_branch"),
    path(
        "edit_allowance/<int:id>/",
        management_views.edit_allowance,
        name="edit_allowance",
    ),
    path(
        "edit_deduction/<int:id>/",
        management_views.edit_deduction,
        name="edit_deduction",
    ),
    path(
        "delete_branch/<int:id>/", management_views.delete_branch, name="delete_branch"
    ),
    path(
        "delete_department/<int:id>/",
        management_views.delete_department,
        name="delete_department",
    ),
    path(
        "delete_allowance/<int:id>/",
        management_views.delete_allowance,
        name="delete_allowance",
    ),
    path(
        "delete_deduction/<int:id>/",
        management_views.delete_deduction,
        name="delete_deduction",
    ),
    path(
        "delete_job_group/<int:id>/",
        management_views.delete_job_group,
        name="delete_job_group",
    ),
    path(
        "delete_all_job_groups/",
        management_views.delete_all_job_groups,
        name="delete_all_job_groups",
    ),
    path(
        "delete_all_employees/",
        management_views.delete_all_employees,
        name="delete_all_employees",
    ),
]
