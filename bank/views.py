from django.contrib import messages
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.generics import RetrieveAPIView, ListAPIView
from .serializers import BranchSerializer
from .models import Branch


class AllBranchesView(ListAPIView):
    permission_classes =(AllowAny,)
    """
    Returns the details of every bank branch in the database.
    """
    queryset = Branch.objects.all()
    serializer_class = BranchSerializer
    


class BranchDetailsView(RetrieveAPIView):
    permission_classes =(AllowAny,)
    """
    Returns the details of a single branch given the branch's IFSCCode.\n
    Example :branch/ABHY0065001/
    """

    def get(self, request, code):
        bank = get_object_or_404(Branch, IFSCCode__iexact=code)
        serializer = BranchSerializer(bank)
        if serializer.is_valid:
            print(serializer.data)
            response={
                "Successful": True,
                "result":serializer.data,
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
        city = request.GET.get('city')
        name = request.GET.get('name')
        if city is not None and name is not None:
            banks = Branch.objects.filter(bank_name__iexact=name, city__iexact=city)
            serializer = BranchSerializer(banks, many=True)
            if serializer.is_valid:
                response={
                "successful": True,
                "result":serializer.data
                }
                return Response(response, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_404_NOT_FOUND)
        return Response({"message":"Include query parameters, city& name"}, status=status.HTTP_404_NOT_FOUND)    


