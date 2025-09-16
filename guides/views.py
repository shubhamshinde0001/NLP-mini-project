from rest_framework import viewsets
from .models import FirstAidGuide
from .serializers import FirstAidGuideSerializer

class FirstAidGuideViewSet(viewsets.ModelViewSet):
    queryset = FirstAidGuide.objects.all().order_by("-created_at")
    serializer_class = FirstAidGuideSerializer

'''
from django.shortcuts import render
from .models import FirstAidGuide

def guide_list(request):
    guides = FirstAidGuide.objects.all().order_by("-created_at")
    return render(request, "guides/guide_list.html", {"guides": guides})
'''

from django.shortcuts import render
from .models import FirstAidGuide

def guide_list(request):
    q = request.GET.get("q", "")
    guides = FirstAidGuide.objects.all().order_by("-created_at")
    if q:
        guides = guides.filter(title__icontains=q) | guides.filter(category__icontains=q)
    return render(request, "guides/guide_list.html", {"guides": guides})
