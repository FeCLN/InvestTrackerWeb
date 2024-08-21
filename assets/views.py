from django.shortcuts import render
import yfinance as yf
import plotly.graph_objects as go
from .models import Asset
from decimal import Decimal

##########################################################################
def checkAssets(request):
    assets = Asset.objects.all()

    if request.method == 'POST':
        assetID = request.POST.get('asset') 
        assetSelected = Asset.objects.get(id=assetID)

        graph_html, dataAsset = searchAsset(assetSelected.ticker)

        if not dataAsset.empty:
            context = {
                'ticker': assetSelected.ticker,
                'data': dataAsset.iloc[-1],
                'graph_html': graph_html
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

        #Get data:
        tickerB3 = request.POST.get('ticker')
        interval = request.POST.get('interval')
        upperLimit = request.POST.get('upperLimit')
        lowerLimit = request.POST.get('lowerLimit')

        newAsset = Asset()
        newAsset.user = request.user

        if tickerB3 and interval and upperLimit and lowerLimit:
            newAsset.ticker     =         tickerB3
            newAsset.interval   =     int(interval)
            newAsset.upperLimit = Decimal(upperLimit)
            newAsset.lowerLimit = Decimal(lowerLimit)
            newAsset.save()
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
