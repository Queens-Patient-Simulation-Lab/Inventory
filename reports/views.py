from django.shortcuts import render
from django.views.decorators.clickjacking import xframe_options_exempt



@xframe_options_exempt
def sampleReport(request):
    return render(request, 'reports/report_sample.html')