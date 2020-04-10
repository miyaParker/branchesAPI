from django.contrib import messages
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.generics import RetrieveAPIView, ListAPIView
from .serializers import BankSerializer
from .models import Bank


class AllBranchesView(ListAPIView):
    permission_classes =(AllowAny,)
    """
    Returns the details of every bank branch in the database.
    """
    queryset = Bank.objects.all()
    serializer_class = BankSerializer
    


class BranchDetailsView(RetrieveAPIView):
    permission_classes =(AllowAny,)
    """
    Returns the details of a single branch given the branch's IFSCCode.\n
    Example :branch/ABHY0065001/
    """

    def get(self, request, code):
        bank = get_object_or_404(Bank, IFSCCode__iexact=code)
        serializer = BankSerializer(bank)
        if serializer.is_valid:
            print(serializer.data)
            response={
                "status": status.HTTP_200_OK,
                "result" :serializer.data,
                "message":"Successful"
            }
            return Response(response, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_404_NOT_FOUND)


class CityBranchesView(RetrieveAPIView):
    permission_classes =(AllowAny,)
    """
    Returns a list of bank branches in a city given the bank's name and city.\n 
    Ensure to include the appropriate query strings in the url. \n
    Example :branches/?city=LAKHIMPUR&name=ALLAHABAD%20BANK/
    """
    queryset = ''
    def get(self, request):
        city = request.GET.get('city', '')
        name = request.GET.get('name', '')
        if city is not None:
            banks = Bank.objects.filter(bank_name__iexact=name, city__iexact=city)
            serializer = BankSerializer(banks, many=True)
            print(serializer.data)
            if serializer.is_valid:
                response={
                "status": status.HTTP_200_OK,
                "result": serializer.data,
                "message":"Successful"
                }
                return Response(response, status=status.HTTP_200_OK)
            return Response("")    
        return Response(serializer.errors, status=status.HTTP_404_NOT_FOUND)


