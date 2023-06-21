from django.shortcuts import render, redirect, reverse
from django.contrib import messages
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from .models import Iratio
from .forms import IratioForm
from django.contrib.auth import get_user_model


User = get_user_model()


@login_required
def iratio(request, user_id, username=False):
    view_user = User.objects.get(id=user_id)
    iratios = Iratio.objects.filter(solver=view_user).order_by('-pub_date')

    paginator = Paginator(iratios, 5)
    page = request.GET.get('page')
    iratio = paginator.get_page(page)

    context = {
        'iratio': iratio,
        'iratios': iratios,
        'view_user': view_user,
    }
    return render(request, 'iratio/iratio.html', context)


@login_required
def iratioNew(request, username):
    
    # if not form.instance.publisher in self.request.user.friends.all():
    #   self.request.user.friends.add(form.instance.publisher)
    if request.method == 'POST':
        form = IratioForm(request.POST)
        if form.is_valid():
            r1 = form.cleaned_data.get('first')
            r2 = form.cleaned_data.get('second')
            op = form.cleaned_data.get('operator')
            if op == 'add':
                r3 = r1 + r2
            elif op == 'subtract':
                r3 = r1 - r2
            elif op == 'multiply':
                r3 = r1 * r2
            elif op == 'divide':
                r3 = r1 / r2
            else:
                return False
            instance = form.save(commit=False)
            instance.result = r3
            instance.solver = request.user
            instance.save()
            messages.success(request, f'You just deploy new iratio')
            return redirect(reverse('iratio', kwargs={'username': username, 'user_id': request.user.id}))
    else:
        form = IratioForm()
    context = {
        'form': form
    }
    return render(request, 'iratio/iratio_create.html', context)
