from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from .models import Ad, ExchangeProposal
from .forms import AdForm, ExchangeProposalForm


##################################################
# Просмотр объявлений с фильтрацией и пагинацией #
##################################################


def ad_list(request):
    ads = Ad.objects.all().order_by('-created_at')

    # Фильтрация
    query = request.GET.get('q')
    category = request.GET.get('category')
    condition = request.GET.get('condition')

    if query:
        ads = ads.filter(title__icontains=query) | ads.filter(description__icontains=query)
    if category:
        ads = ads.filter(category__icontains=category)
    if condition:
        ads = ads.filter(condition=condition)

    # Пагинация
    paginator = Paginator(ads, 6)
    page = request.GET.get('page')
    ads = paginator.get_page(page)

    return render(request, 'ads/ad_list.html', {'ads': ads})


##################################################
############## Создание объявления ###############
##################################################

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


########################################################
############## Редактирование объявления ###############
########################################################

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


##################################################
############## Удаление объявления ###############
##################################################

@login_required
def ad_delete(request, pk):
    ad = get_object_or_404(Ad, pk=pk)
    if ad.user != request.user:
        return render(request, 'ads/error.html', {'message': 'Вы не автор объявления.'})

    if request.method == 'POST':
        ad.delete()
        return redirect('ad_list')
    return render(request, 'ads/ad_confirm_delete.html', {'ad': ad})


########################################################
############# Создание предложения обмена ##############
########################################################

@login_required
def create_exchange_proposal(request):
    if request.method == 'POST':
        form = ExchangeProposalForm(request.POST)
        if form.is_valid():
            proposal = form.save(commit=False)
            proposal.status = 'pending'
            proposal.save()
            return redirect('ad_list')
    else:
        form = ExchangeProposalForm()
    return render(request, 'ads/exchange_form.html', {'form': form})


##################################################
############## Просмотр предложений ##############
##################################################

@login_required
def proposal_list(request):
    proposals = ExchangeProposal.objects.filter(
        ad_sender__user=request.user
    ) | ExchangeProposal.objects.filter(
        ad_receiver__user=request.user
    )
    proposals = proposals.order_by('-created_at')
    return render(request, 'ads/proposal_list.html', {'proposals': proposals})
