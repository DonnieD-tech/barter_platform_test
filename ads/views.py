from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from .models import Ad, ExchangeProposal, Category
from .forms import AdForm, ExchangeProposalForm


def ad_list(request):
    ads = Ad.objects.all().order_by('-created_at')
    categories = Category.objects.all()

    query = request.GET.get('q')
    category = request.GET.get('category')
    condition = request.GET.get('condition')

    if query:
        ads = ads.filter(title__icontains=query) | ads.filter(description__icontains=query)
    if category:
        ads = ads.filter(category__id=category)
    if condition:
        ads = ads.filter(condition=condition)

    paginator = Paginator(ads, 8)
    page = request.GET.get('page')
    ads = paginator.get_page(page)

    context = {
        'ads': ads,
        'categories': categories,
        'selected_category_id': category,  # чтобы сохранить выбранное значение
    }

    return render(request, 'ads/ad_list.html', context)




@login_required
def ad_create(request):
    if request.method == 'POST':
        form = AdForm(request.POST)
        if form.is_valid():
            ad = form.save(commit=False)
            ad.user = request.user
            ad.save()
            return redirect('ad_list')
    else:
        form = AdForm()
    return render(request, 'ads/ad_form.html', {'form': form, 'action': 'Создание объявления'})




@login_required
def ad_edit(request, pk):
    ad = get_object_or_404(Ad, pk=pk)
    if ad.user != request.user:
        return render(request, 'ads/error.html', {'message': 'Вы не автор объявления.'})

    if request.method == 'POST':
        form = AdForm(request.POST, instance=ad)
        if form.is_valid():
            form.save()
            return redirect('ad_list')
    else:
        form = AdForm(instance=ad)
    return render(request, 'ads/ad_form.html', {'form': form, 'action': 'Редактирование объявления'})




@login_required
def ad_delete(request, pk):
    ad = get_object_or_404(Ad, pk=pk)
    if ad.user != request.user:
        return render(request, 'ads/error.html', {'message': 'Вы не автор объявления.'})

    if request.method == 'POST':
        ad.delete()
        return redirect('ad_list')
    return render(request, 'ads/ad_confirm_delete.html', {'ad': ad})




@login_required
def create_exchange_proposal(request):
    if request.method == 'POST':
        form = ExchangeProposalForm(request.POST, user=request.user)
        if form.is_valid():
            proposal = form.save(commit=False)
            proposal.ad_sender = form.cleaned_data['ad_sender']
            proposal.status = 'pending'
            proposal.save()
            return redirect('ad_list')
    else:
        form = ExchangeProposalForm(user=request.user)
    return render(request, 'ads/exchange_form.html', {'form': form})




@login_required
def proposal_list(request):
    proposals = ExchangeProposal.objects.filter(
        ad_sender__user=request.user
    ) | ExchangeProposal.objects.filter(
        ad_receiver__user=request.user
    )

    role = request.GET.get('role')  # отправитель или получатель
    status = request.GET.get('status')  # статус обмена

    if role == 'sender':
        proposals = proposals.filter(ad_sender__user=request.user)
    elif role == 'receiver':
        proposals = proposals.filter(ad_receiver__user=request.user)
    if status:
        proposals = proposals.filter(status=status)

    proposals = proposals.order_by('-created_at')
    return render(request, 'ads/proposal_list.html', {'proposals': proposals})




@login_required
def accept_exchange(request, pk):
    proposal = get_object_or_404(ExchangeProposal, pk=pk)

    if proposal.ad_receiver.user != request.user:
        return render(request, 'ads/error.html', {'message': 'Вы не можете подтвердить этот обмен.'})

    if proposal.status == 'pending':
        sender_user = proposal.ad_sender.user
        receiver_user = proposal.ad_receiver.user

        proposal.ad_sender.user = receiver_user
        proposal.ad_receiver.user = sender_user

        proposal.ad_sender.save()
        proposal.ad_receiver.save()

        proposal.status = 'accepted'
        proposal.save()

    return redirect('proposal_list')




@login_required
def decline_exchange(request, pk):
    proposal = get_object_or_404(ExchangeProposal, pk=pk)

    if proposal.ad_receiver.user != request.user:
        return render(request, 'ads/error.html', {'message': 'Вы не можете отклонить этот обмен.'})

    if proposal.status == 'pending':
        proposal.status = 'declined'
        proposal.save()

    return redirect('proposal_list')

