from django.contrib import messages
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Record
from .forms import OkpdForm
from .request_lib import check_codes

# Create your views here.
def home(request):
    if request.method == 'POST':
        form = OkpdForm(request.POST)
        if form.is_valid():
            res = check_codes(form.cleaned_data.get('okpd_list'), form.cleaned_data.get('check_groups'))
            if 'timeout' in res:
                messages.error(request, 'Превышено время ожидания ответа от zakupki.gov.ru. Попробуйте позже.')
                return redirect('okpd_check_home')
            elif res:
                return render(request, 'okpd_check/result.html', {'result':res})
            else:
                messages.warning(request, 'Не найдено кодов ОКПД во введённом тексте')
                return redirect('okpd_check_home')
    else:
        form = OkpdForm()
    return render(request, 'okpd_check/index.html', {'form':form})
#
# def result(request):
#     context = {'result': Record.objects.all()}
#     return render(request, 'okpd_check/result.html', context=context)
