from .models import Ticket
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q 

def paginateTickets(request, tickets, results):
    page = request.GET.get('page')
    paginator = Paginator(tickets, results)
    try:
        tickets = paginator.page(page)
    except PageNotAnInteger:
        page = 1
        tickets = paginator.page(page)
    except EmptyPage:
        page = paginator.num_pages
        tickets = paginator.page(page)

    leftIndex = (int(page)-4)

    if leftIndex <1:
        leftIndex=1

    rightIndex = (int(page)+5)

    if rightIndex> paginator.num_pages:
        rightIndex= paginator.num_pages+1
    
    custom_range = range(leftIndex, rightIndex)
    return custom_range, tickets

def searchTickets(request):
    search_query = ''
    if request.GET.get('search_query'):
        search_query = request.GET.get('search_query')

    tickets = Ticket.objects.distinct().filter(

        Q(author__name__icontains=search_query)|
        Q(body__icontains = search_query)|
        Q(kind__icontains = search_query)

    )
    return tickets, search_query
