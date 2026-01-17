from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.contrib import messages
from .models import Message
from .forms import MessageForm

User = get_user_model()

@login_required
def inbox(request):
    received_messages = Message.objects.filter(recipient=request.user)
    return render(request, 'messaging/inbox.html', {'messages': received_messages})

@login_required
def send_message(request, recipient_id):
    recipient = get_object_or_404(User, pk=recipient_id)
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = request.user
            message.recipient = recipient
            message.save()
            
            # Notification au destinataire
            from apps.notifications.utils import create_notification
            create_notification(
                recipient=recipient,
                notification_type='new_message',
                title='Nouveau message',
                message=f"Vous avez reçu un nouveau message de {request.user.username}.",
                link=f"/messages/{message.id}/"
            )
            
            messages.success(request, 'Message envoyé avec succès !')
            return redirect('inbox')
    else:
        form = MessageForm()
    
    return render(request, 'messaging/send_message.html', {'form': form, 'recipient': recipient})

@login_required
def message_detail(request, pk):
    message = get_object_or_404(Message, pk=pk)
    # Vérifier que l'utilisateur est bien le destinataire ou l'expéditeur
    if request.user != message.recipient and request.user != message.sender:
        messages.error(request, "Vous n'avez pas accès à ce message.")
        return redirect('inbox')
    
    if request.user == message.recipient and not message.is_read:
        message.is_read = True
        message.save()
        
    return render(request, 'messaging/detail.html', {'message': message})
