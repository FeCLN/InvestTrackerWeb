from django.shortcuts import render
import yfinance as yf

def checkAssets(request):
    context = {
        'current_page': 'check',  
    }
    return render(request, 'check.html', context)

def configureAssets(request):
    context = {
        'current_page': 'configure',  
    }
    return render(request, 'configure.html', context)

def searchAssets(request):
    if request.method == 'POST':
            tickerB3 = request.POST.get('ticker')
            tickerHtml = tickerB3 + ".SA"
            assetEntity = yf.Ticker(tickerHtml)
            data = assetEntity.history(period="1d")
            if not data.empty:
                context = {
                    'ticker': tickerB3,
                    'data': data.iloc[-1]
                }
            else:
                context = {
                    'ticker': tickerHtml,
                    'error': "No data found for this symbol."
                }
            return render(request, 'search/showAsset.html', context)
    return render(request, 'search/inputAsset.html')

