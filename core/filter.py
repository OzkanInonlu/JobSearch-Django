import django_filters
from .models import *


INDUSTRIES=[]
LOCATIONS=[]
JOBTYPES=[]
def get_industries():
    for industry in Industry.objects.all():
        INDUSTRIES.append((industry.id, industry.name))
    return INDUSTRIES

def get_cities():
    for city in CITIES:
        LOCATIONS.append((city[0], city[1]))
    return LOCATIONS

def get_job_types():
    for job_type in JOB_TYPES:
        JOBTYPES.append((job_type[0], job_type[1]))
    return JOBTYPES


class JobAdvertFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(lookup_expr='icontains') #for using it like __contains + case-insensitive
    min_salary = django_filters.NumberFilter(field_name='min_salary', lookup_expr='gte') #greater than or equal
    max_salary = django_filters.NumberFilter(field_name='max_salary', lookup_expr='lte') #less than or equal

    industry = django_filters.ChoiceFilter(
        choices=get_industries(),
        label='Industry',
        empty_label='Select Industry',

        )
    
    location = django_filters.ChoiceFilter(
        choices=get_cities(),
        label='Location', 
        empty_label='Select Location'
        )
    
    job_type = django_filters.ChoiceFilter(
        choices=get_job_types(), 
        label='Job Type',
        empty_label='Select Job Type'
        )


    class Meta:
        model = JobAdvert
        fields = ["title", "location", "job_type", "industry", "min_salary", "max_salary"]
