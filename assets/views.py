from django.shortcuts import render
import yfinance as yf
import plotly.graph_objects as go
from django.http import HttpResponse
from .models import Asset, AssetHistory
from decimal import Decimal
from django.utils import timezone
from datetime import timedelta

from django_celery_beat.models import PeriodicTask, IntervalSchedule

##########################################################################
def checkAssets(request):
    assets = Asset.objects.all()

    if request.method == 'POST':
        assetID = request.POST.get('asset') 
        assetSelected = Asset.objects.get(id=assetID)

        graph_html, dataAsset = searchAsset(assetSelected.ticker)

        # PLOT ASSET HISTORY

        history = AssetHistory.objects.filter(asset=assetSelected).order_by('timestamp')[:500]
        
        timestamps   = [record.timestamp  for record in history]
        open_prices  = [record.openPrice  for record in history]
        high_prices  = [record.highPrice  for record in history]
        low_prices   = [record.lowPrice   for record in history]
        close_prices = [record.closePrice for record in history]

        fig = go.Figure(data=[go.Candlestick(x=timestamps,
                                            open=open_prices,
                                            high=high_prices,
                                            low=low_prices,
                                            close=close_prices)])

        fig.update_layout(
            title=f'Last 500 values stored for {assetSelected.ticker}',
            xaxis_title='Timestamp',
            yaxis_title='Price',
            xaxis_rangeslider_visible=False,
            xaxis_tickformat='%Y-%m-%d %H:%M',
            xaxis_title_standoff=10
        )

        graph_history_html = fig.to_html(full_html=False)


        if not dataAsset.empty:
            context = {
                'ticker': assetSelected.ticker,
                'data': dataAsset.iloc[-1],
                'graph_html': graph_html,
                'graph_history_html': graph_history_html
            }
        else:
            context = {
                'ticker': assetSelected.ticker,
                'error': "No data found for this symbol."
            }
        return render(request, 'check/checkResult.html', context)

    
    context = {
        'current_page': 'check',
        'assets' : assets,
    }
    return render(request, 'check/checkSel.html', context)
##########################################################################



##########################################################################
def configureAssets(request):
    if request.method == 'POST':

        #GET INPUT DATA:
        tickerB3   = request.POST.get('ticker')
        interval   = request.POST.get('interval')
        upperLimit = request.POST.get('upperLimit')
        lowerLimit = request.POST.get('lowerLimit')
        tunnelType = request.POST.get('tunnelType')


        #CREATE NEW ASSET OBJECT
        newAsset = Asset()
        newAsset.user = request.user

        #CHECK IF DATA EXISTS
        if tickerB3 and interval and upperLimit and lowerLimit:

            #SAVE NEW ASSET
            newAsset.ticker     =         tickerB3
            newAsset.interval   =     int(interval)
            newAsset.upperLimit = Decimal(upperLimit)
            newAsset.lowerLimit = Decimal(lowerLimit)
            newAsset.tunnelType =         tunnelType
            newAsset.save()

            #CREATE SCHEDULE TASK
            interval, _ = IntervalSchedule.objects.get_or_create(every=newAsset.interval, period=IntervalSchedule.SECONDS)
            PeriodicTask.objects.create(interval=interval, name=("schedule_" + tickerB3 + "_" + str(request.user.username)), task="assets.tasks.AssetChecker", args=[newAsset.id])

            #RETURN TO PAGE
            context = {
            'current_page': 'configure',
            'message': 'Asset configured!',  
            }
            return render(request, 'configure/configure.html', context)
        else:
            context = {
            'current_page': 'configure',
            'message': 'Error, verify the information',  
            }
            return render(request, 'configure/configure.html', context)
            


    context = {
        'current_page': 'configure',  
    }
    return render(request, 'configure/configure.html', context)
##########################################################################



##########################################################################
######## SEARCH FUNCTION ########
def searchAssets(request):
    if request.method == 'POST':
            tickerB3 = request.POST.get('ticker')
            tickerHtml = tickerB3 + ".SA"

            graph_html, dataAsset = searchAsset(tickerB3)

           

            if not dataAsset.empty:
                context = {
                    'ticker': tickerB3,
                    'data': dataAsset.iloc[-1],
                    'graph_html': graph_html
                }
            else:
                context = {
                    'ticker': tickerB3,
                    'error': "No data found for this symbol."
                }
            return render(request, 'search/showAsset.html', context)
    return render(request, 'search/inputAsset.html')
##########################################################################


##########################################################################
###### OTHER FUNCTIONS  ######
def searchAsset(ticker):
     #Get the data
    tickerHtml = ticker + ".SA"
    assetEntity = yf.Ticker(tickerHtml)
    dataAsset = assetEntity.history(period="1d", interval="1m")

    # Plot the data
    if 'Date' not in dataAsset.columns:
        dataAsset['Date'] = dataAsset.index
    fig = go.Figure(data=[go.Candlestick(x=dataAsset.index,
                    open=dataAsset['Open'],
                    high=dataAsset['High'],
                    low=dataAsset['Low'],
                    close=dataAsset['Close'])])
    
    fig.update_layout(
        title=f'One day chart {ticker}',
        xaxis_title='Date',
        yaxis_title='Price',
        xaxis_rangeslider_visible=False,
        xaxis_tickformat='%Y-%m-%d %H:%M',
        xaxis_title_standoff=10
    )
    
    graph_html = fig.to_html(full_html=False)
    return graph_html, dataAsset
