# Copyright (c) 2020 HWN All Rights Reserved

from django.shortcuts import render, redirect
from .models import Stock
from .forms import StockForm
from django.contrib import messages


def home(request):
    import requests
    import json

    if request.method == "POST":
        ticker = request.POST['ticker']
        api_request = requests.get("https://cloud.iexapis.com/stable/stock/" + ticker + "/quote?token=pk_329e4a3eaa9c4a95adf31000146af2db")

        try:
            api = json.loads(api_request.content)
        except Exception as e:
            api = "Error..."

        return render(request, 'index.html', {'api':api})

    else:
        return render(request, 'index.html')



def about(request):
    return render(request, 'about.html', {})


def add_stock(request):
    import requests
    import json

    if request.method == "POST":
        form = StockForm(request.POST or None)
        if form.is_valid():
            form.save()
            messages.success(request, ("Stock Added !"))
            return redirect('add_stock')

    else:
        ticker = Stock.objects.all()
        output = []
        for ticker_item in ticker:
            api_request = requests.get("https://cloud.iexapis.com/stable/stock/" + str(ticker_item) + "/quote?token=pk_329e4a3eaa9c4a95adf31000146af2db")
            try:
                api = json.loads(api_request.content)
                output.append(api)
            except Exception as e:
                api = "Error..."

        return render(request, 'add_stock.html', {'ticker':ticker, 'output':output})


def delete(request, stock_id):
    item = Stock.objects.get(pk=stock_id)
    item.delete()
    messages.success(request, ("Stock Deleted"))
    return redirect(delete_stocks)

def delete_stocks(request):
    ticker = Stock.objects.all()
    return render(request, 'delete.html',{'ticker':ticker})
