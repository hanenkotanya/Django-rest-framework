from django.shortcuts import render
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from .models import Ticket
from us.models import Profile
from mes.models import Message
from django.urls import conf
from django.utils import timezone
from .forms import TicketForm, EditRoleForm
from .utils import paginateTickets, searchTickets
from django.db.models import Q

@login_required(login_url='login')
def createTicket(request, slug):
    form = TicketForm()
    profile = request.user.profile
    if request.method == 'POST':
        form = TicketForm(request.POST)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.author = profile    
            ticket.save()
        else:
            messages.success('ошибка')
        return redirect('userTickets', slug=profile.slug)
    context = {'form': form, 'profile':profile}
    return render(request, 'tic/createTickets.html', context)


@login_required(login_url='login')
def userTickets(request, slug):
    profile = Profile.objects.get(user=request.user)
    tickets = profile.tickets.all()
    context = {'profile': profile, 'tickets':tickets}
    return render(request, 'tic/userTickets.html', context)


@login_required(login_url='login')    
def tickets(request):
    admin = get_object_or_404(Profile, user=request.user)
    if admin.role == 'Соппорт':
        #tickets = Ticket.objects.all()
        tickets, search_query = searchTickets(request)
        custom_range, tickets = paginateTickets(request, tickets, 6)

    else:
        return redirect('userProfile')
    context = {'tickets': tickets, 
                'custom_range': custom_range, 
                'search_query':search_query}
    return render(request, 'tic/tickets.html', context)


@login_required(login_url='login')    
def editRole(request,id):
    profile = get_object_or_404(Profile, user=request.user)
    ticket = Ticket.objects.get(id=id)
    form = EditRoleForm()
    if profile.role == 'Соппорт':
        if request.method == 'POST':
            form = EditRoleForm(request.POST, instance=ticket)
            if form.is_valid():
                ticket = form.save()
                return redirect('ticketsAll')
        context = {'form':form, 'ticket':ticket}
    else:
        messages.success(request, 'У вас нет прав для изменения роли тикета')
        return redirect('userProfile', slug=profile.slug)
        
    return render(request, 'tic/editRole.html', context)


@login_required(login_url='login')
def ticketThis(request, id):
    profile=Profile.objects.get(user=request.user)
    ticket = Ticket.objects.get(id=id)
    messages = Message.objects.filter(ticket=ticket)
    context={ 'profile':profile, 'ticket':ticket, 'messages':messages}
    return render(request, 'tic/ticketThis.html', context)


@login_required(login_url='login')
def deleteTicket(request, id, slug):
    ticket = Ticket.objects.get(id=id)
    profile= Profile.objects.get(slug=slug)
    if ticket.author==profile:
        if request.method == 'POST':
            ticket.delete()
            messages.success(request, 'Тикет успешно удален')
            return redirect('userProfile', slug=profile.slug)
    else:
        messages.success(request, 'Тикет может удалить только автор')
        return redirect('userProfile', slug=profile.slug)
    context = {'object': ticket}
    return render(request, 'tic/deleteTicket.html', context)



