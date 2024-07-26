# from django.http import HttpResponse
from django.shortcuts import render
from .forms import BookingForm
from .models import Menu
from django.core import serializers
from .models import Booking
from datetime import datetime
import json
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from .serializers import BookingSerializer, MenuSerializer
from datetime import datetime


# Create your views here.
def home(request):
    return render(request, 'index.html')

def about(request):
    return render(request, 'about.html')

class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer

    @action(detail=False, methods=['get'])
    def reservations(self, request):
        date = request.GET.get('date', datetime.today().date())
        bookings = Booking.objects.filter(reservation_date=date)
        serializer = self.get_serializer(bookings, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['post'], url_path='bookings')
    def bookings_post(self, request):
        data = request.data
        exist = Booking.objects.filter(
            reservation_date=data['reservation_date'], 
            reservation_slot=data['reservation_slot']
        ).exists()
        if not exist:
            serializer = self.get_serializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'error': 1}, status=status.HTTP_400_BAD_REQUEST)

class MenuViewSet(viewsets.ModelViewSet):
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer

    @action(detail=False, methods=['get'])
    def menu(self, request):
        menu_data = Menu.objects.all()
        serializer = self.get_serializer(menu_data, many=True)
        return Response({"menu": serializer.data})

    @action(detail=True, methods=['get'])
    def display_menu_item(self, request, pk=None):
        menu_item = self.get_object()
        serializer = self.get_serializer(menu_item)
        return Response({"menu_item": serializer.data})
