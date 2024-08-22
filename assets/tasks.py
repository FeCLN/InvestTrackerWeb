from celery import shared_task
from .models import Asset, AssetHistory
from celery.schedules import crontab
import yfinance as yf
from .views import searchAsset


@shared_task
def AssetChecker(asset_id):
    asset = Asset.objects.get(id=asset_id)
    print("Processing asset with ID: " + str(asset.id) + " and Ticker: " + asset.ticker)
    
    history = AssetHistory()
    
    assetEntity = yf.Ticker((asset.ticker + ".SA"))
    dataAsset = assetEntity.history(period="1d", interval="1m")

    history.asset      = asset
    history.closePrice = dataAsset['Close'].iloc[-1]
    history.openPrice  = dataAsset['Open'].iloc[-1]
    history.highPrice  = dataAsset['High'].iloc[-1]
    history.lowPrice   = dataAsset['Low'].iloc[-1]
    history.timestamp  = dataAsset.index[-1]

    print(dataAsset['Close'].iloc[-1])

    history.save()

    return "task complete" + str(dataAsset['Close'].iloc[-1])