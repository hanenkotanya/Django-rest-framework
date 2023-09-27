from django.shortcuts import render
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from tic.models import Ticket
from us.models import Profile
from .models import Message
from django.urls import conf
from django.utils import timezone
from .forms import MessageForm, EditRoleForm

@login_required(login_url='login')
def createMessage(request, id):
    form = MessageForm()
    profile = request.user.profile
    ticket = Ticket.objects.get(id=id)
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.author = profile  
            message.ticket = ticket
            message.save()
        else:
            messages.success('ошибка')
        return redirect('ticketThis', id)
    context = {'form': form, 'profile':profile, 'ticket':ticket}
    return render(request, 'mes/createMessage.html', context)


@login_required(login_url='login')    
def editRole(request,id,):
    profile = get_object_or_404(Profile, user=request.user)
    message = Message.objects.get(id=id)
    form = EditRoleForm()
    if profile.role == 'Соппорт':
        if request.method == 'POST':
            form = EditRoleForm(request.POST, instance=message)
            if form.is_valid():
                message = form.save()
                return redirect('userTickets',slug = profile.slug )
        context = {'form':form, 'message':message, 'profile':profile}
    else:
        messages.success(request, 'У вас нет прав для изменения статуса сообщения')
        return redirect('userProfile', slug=profile.slug)
        
    return render(request, 'mes/editRole.html', context)



@login_required(login_url='login')
def deleteMessage(request, id, slug):
    message = Message.objects.get(id=id)
    profile= Profile.objects.get(slug=slug)
    if message.author==profile:
        if request.method == 'POST':
            message.delete()
            messages.success(request, 'Комментарий успешно удален')
            return redirect('userProfile', slug=profile.slug)
    else:
        messages.success(request, 'У вас нет прав для удаления комментария')
        return redirect('userProfile', slug=profile.slug)
    context = {'object': message}
    return render(request, 'mes/deleteMessage.html', context)




