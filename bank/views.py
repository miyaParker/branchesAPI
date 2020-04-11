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
    permission_classes = (AllowAny,)
    """
    Returns the details of every bank branch in the database.
    """
    queryset = Branch.objects.all()
    serializer_class = BranchSerializer


class BranchDetailsView(RetrieveAPIView):
    permission_classes = (AllowAny,)
    """
    Returns the details of a single branch given the branch's IFSCCode.\n
    Example :branch/ABHY0065001/
    """

    def get(self, request, code):
        try:
            bank = Branch.objects.get(IFSCCode__iexact=code)
            serializer = BranchSerializer(bank)
            status_code = status.HTTP_200_OK
            response = {
                "success": "true",
                "status": status_code,
                 "message": "Branch details  with IFSC code {} fetched successfully".format(code),
                "result": serializer.data
            }   
        except Branch.DoesNotExist:
            status_code = status.HTTP_404_NOT_FOUND
            response = {
                "success": "false",
                "status": status_code,
                "message": "A branch with that IFSC code {} does not exist".format(code),
            }
        return Response(response, status=status_code)


class CityBranchesView(RetrieveAPIView):
    permission_classes = (AllowAny,)
    """
    Returns a list of bank branches in a city given the bank's name and city.\n 
    Ensure to include the appropriate query strings in the url. \n
    Example :branches/?city=LAKHIMPUR&name=ALLAHABAD%20BANK/
    """

    def get(self, request):
        city = request.GET.get('city')
        name = request.GET.get('name')
        if city is not None and name is not None:
            try:
                banks = Branch.objects.filter(
                    bank_name__iexact=name, city__iexact=city)
                serializer = BranchSerializer(banks, many=True)
                status_code = status.HTTP_200_OK
                response = {
                    "success": "true",
                    "status": status_code,
                    "message": "Branches of {} in {} city fetched successfully".format(name.upper(), city.upper()),
                    "result": serializer.data
                }
            except Exception as e:
                response = {
                    "success": "false",
                    "status": status_code,
                    "error": e
                }
            return Response(response, status=status_code)
        return Response({"message": "Include query parameters, city& name"}, status=status.HTTP_404_NOT_FOUND)
