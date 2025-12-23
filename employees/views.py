from django.core.paginator import Paginator
from django.db.models import Count
from django.shortcuts import get_object_or_404, render
from mptt.utils import get_cached_trees

from .models import Department, Employee


def department_tree(request):
    departments_qs = (
        Department.objects.all()
        .annotate(employee_count=Count('employees'))
        .order_by('tree_id', 'lft')
    )
    departments = get_cached_trees(departments_qs)

    selected_department = None
    employees_qs = Employee.objects.none()

    department_id = request.GET.get('department')
    if department_id:
        selected_department = get_object_or_404(Department, pk=department_id)
        branch_ids = selected_department.get_descendants(include_self=True).values_list(
            'id', flat=True
        )
        employees_qs = (
            Employee.objects.filter(department_id__in=branch_ids)
            .select_related('department')
            .order_by('full_name')
        )

    paginator = Paginator(employees_qs, 25)
    page_obj = paginator.get_page(request.GET.get('page'))

    context = {
        'departments': departments,
        'selected_department': selected_department,
        'page_obj': page_obj,
    }
    return render(request, 'employees/tree.html', context)
