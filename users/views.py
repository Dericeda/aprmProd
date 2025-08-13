from django.shortcuts import render, redirect
from users.models import AssociationMember
from myapp.forms import AvatarForm

def member_list(request):
    members = AssociationMember.objects.all()
    return render(request, 'users/member_list.html', {'members': members})

def dashboard(request):
    try:
        member = AssociationMember.objects.get(user=request.user)
    except AssociationMember.DoesNotExist:
        return redirect('join_association')

    if request.method == 'POST':
        form = AvatarForm(request.POST, request.FILES, instance=member)
        if form.is_valid():
            if form.cleaned_data.get('remove_avatar') and member.avatar:
                member.avatar.delete()
            form.save()
    else:
        form = AvatarForm(instance=member)

    return render(request, 'dashboard.html', {'form': form, 'member': member})
