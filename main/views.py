from django.shortcuts import render
from .models import Job
from .forms import RequirementsForm, SearchForm
from django.core.paginator import Paginator
import re


# The function is called when user searching for the vacancy in search input
def search(request):
    form = RequirementsForm(request.GET)
    form_search = SearchForm(request.GET)
    if form_search.is_valid():
        search_text = form_search.cleaned_data['search'].lower()
    else:
        search_text = ''
    # the list of vacancies witch have similar title with the search text
    vacancies = [vacancy for vacancy in Job.objects.all() if re.search(search_text, vacancy.title.lower())]
    page, is_paginated, prev_url, next_url, current_url = pagination(request, vacancies)

    context = {
        'form': form,
        'form_search': form_search,
        'results': len(vacancies),
        'page_object': page,
        'is_paginated': is_paginated,
        'prev_url': prev_url,
        'next_url': next_url,
        'current_url': current_url,
    }
    return render(request, 'main/index.html', context)


# The f
def index(request):
    form = RequirementsForm(request.GET)
    form_search = SearchForm(request.GET)
    if not list(request.GET.values()):
        vacancies = Job.objects.all()
    elif form.is_valid():
        vacancies = handler_form(form)
    else:
        vacancies = []
    page, is_paginated, prev_url, next_url, current_url = pagination(request, vacancies)
    context = {
        'form': form,
        'form_search': form_search,
        'results': len(vacancies),
        'page_object': page,
        'is_paginated': is_paginated,
        'prev_url': prev_url,
        'next_url': next_url,
        'current_url': current_url,
    }
    return render(request, 'main/index.html', context)


# The function reading the data from form and returns list of corresponding vacancies
def handler_form(form):
    city = form.cleaned_data['city'].lower()
    salary = form.cleaned_data['salary']
    without_salary = form.cleaned_data['without_salary']
    employment = '|'.join(form.cleaned_data['emp'])
    prog_lang = '|'.join(form.cleaned_data['lang'])
    data_bases = '|'.join(form.cleaned_data['db'])
    skills = '|'.join(form.cleaned_data['skills'])
    vacancies = []
    for vacancy in Job.objects.all():
        if city == 'all cities' or (city in vacancy.city.lower()):
            if (without_salary and salary == '') or (vacancy.salary >= salary != '') or (not without_salary and vacancy.salary):
                if re.search(employment, vacancy.employment.lower()):
                    if re.search(prog_lang, vacancy.prog_lang.lower()):
                        if re.search(data_bases, vacancy.data_bases.lower()):
                            if re.search(skills, vacancy.skills.lower()):
                                vacancies.append(
                                    {'title': vacancy.title,
                                     'url': vacancy.url,
                                     'salary': vacancy.salary,
                                     'city': vacancy.city,
                                     'employment': vacancy.employment,
                                     'description': vacancy.description})

    return vacancies


def pagination(request, vacancies):
    # one page containes 6 vacancies
    paginator = Paginator(vacancies, 6)
    # get the value of "page" param from url otherwise it returns "1"
    page_num = request.GET.get('page', 1)
    # creating page object
    page = paginator.page(page_num)
    # initializing current url
    if request.GET:
        # getting the url at the moment and delete parameter "page" for updating it
        current_url = re.sub(r'&*page=\d+', '', request.get_full_path()) + '&'
    else:
        # if there is no GET request - adding "?" for setting the new params in the future
        current_url = request.get_full_path() + '?'
    # check if page has the other ones
    is_paginated = page.has_other_pages()
    if page.has_previous():
        prev_url = f'{current_url}page={page.previous_page_number()}'
    else:
        prev_url = ''
    if page.has_next():
        next_url = f'{current_url}page={page.next_page_number()}'
    else:
        next_url = ''

    return page, is_paginated, prev_url, next_url, current_url