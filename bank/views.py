import csv
import io
from django.contrib import messages
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import permission_required
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.generics import RetrieveAPIView, ListAPIView
from .serializers import BankSerializer
from .models import Bank


class BanksView(ListAPIView):
    """
    Returns the details of every bank branch in the database.\n
    Example :branch/ABHY0065001/
    """
    queryset = Bank.objects.all()
    serializer_class = BankSerializer


class BranchDetailsView(RetrieveAPIView):
    """
    Returns the details of a single branch given the branch's IFSCCode.\n
    Example :branch/ABHY0065001/
    """

    def get(self, request, code):
        bank = get_object_or_404(Bank, IFSCCode__iexact=code)
        serializer = BankSerializer(bank)
        if serializer.is_valid:
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_404_NOT_FOUND)


class CityBranchesView(RetrieveAPIView):
    """
    Returns a list of bank branches in a city given the bank's name and city.\n 
    Ensure to include the appropriate query strings in the url. \n
    Example :branches/?city=LAKHIMPUR&name=ALLAHABAD%20BANK/
    """
    queryset = ''

    def get(self, request):
        city = request.GET.get('city', '')
        name = request.GET.get('name', '')
        banks = Bank.objects.filter(bank_name__iexact=name, city__iexact=city)
        serializer = BankSerializer(banks, many=True)
        if serializer.is_valid:
            return Response(serializer.data, status=200)
        return Response(serializer.errors, status=status.HTTP_404_NOT_FOUND)


@permission_required('admin.can_add_log_entry')
def banks_upload(request):
    template = 'bank_upload.html'

    prompt = {
        'order': 'Order of csv should be ifsc,bank_id,branch,address,city,district,state,bank_name '
    }
    if request.method == 'GET':
        return render(request, template, prompt)
    csv_file = request.FILES['file']

    if not csv_file.name.endswith('.csv'):
        messages.error(request, 'This is not a csv file')
    data_set = csv_file.read().decode('UTF-8')
    io_string = io.StringIO(data_set)
    next(io_string)
    for column in csv.reader(io_string, delimiter=',', quotechar='"'):
        _, created = Bank.objects.update_or_create(
            IFSCCode=column[0],
            bank_id=column[1],
            branch=column[2],
            address=column[3],
            city=column[4],
            district=column[5],
            state=column[6],
            bank_name=column[7]
        )
    context = {}
    return render(request, template, context)
