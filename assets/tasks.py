from celery import shared_task
from .models import Asset, AssetHistory
from celery.schedules import crontab
import yfinance as yf
from .views import searchAsset


@shared_task
def AssetChecker(asset_id):
    asset = Asset.objects.get(id=asset_id)
    print("Processing asset with ID: " + str(asset.id) + " and Ticker: " + asset.ticker)
    

    #### SAVE ASSET HISTORY
    history = AssetHistory()
    
    assetEntity = yf.Ticker((asset.ticker + ".SA"))
    dataAsset = assetEntity.history(period="1d", interval="1m")

    history.asset      = asset
    history.closePrice = dataAsset['Close'].iloc[-1]
    history.openPrice  = dataAsset['Open'].iloc[-1]
    history.highPrice  = dataAsset['High'].iloc[-1]
    history.lowPrice   = dataAsset['Low'].iloc[-1]
    history.timestamp  = dataAsset.index[-1]

    history.save()

    #### VERIFY TUNNELS
    assetPrice = dataAsset['Close'].iloc[-1]
    oldAssetPrice = dataAsset['Close'].iloc[-2]


    if    asset.tunnelType == 'static':
        if   assetPrice > asset.upperLimit:
            pass #EMAIL DE VENDA
        elif assetPrice < asset.lowerLimit:
            pass #EMAIL DE COMPRA


    elif  asset.tunnelType == 'sync':
        syncUpper = oldAssetPrice + asset.upperLimit
        syncLower = oldAssetPrice - asset.lowerLimit
        if   assetPrice > syncUpper:
            pass #EMAIL DE VENDA
        elif assetPrice < syncLower:
            pass #EMAIL DE COMPRA


    elif   asset.tunnelType == 'async':
        asyncUpper = dataAsset['Close'].mean() + asset.upperLimit
        asyncLower = dataAsset['Close'].mean() - asset.lowerLimit
        if   assetPrice > asyncUpper:
            pass #EMAIL DE VENDA
        elif assetPrice < asyncLower:
            pass #EMAIL DE COMPRA


    return "task complete" + str(dataAsset['Close'].iloc[-1])