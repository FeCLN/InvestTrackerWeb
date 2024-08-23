from celery import shared_task
from .models import Asset, AssetHistory
from celery.schedules import crontab
import yfinance as yf
from .views import searchAsset

from django.core.mail import send_mail
from InvestTrackerWeb.settings import EMAIL_HOST_USER


@shared_task
def AssetChecker(asset_id):
    asset = Asset.objects.get(id=asset_id)
    print("Processing asset with ID: " + str(asset.id) + " and Ticker: " + asset.ticker)
    useremail = asset.user.email
    

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

    #### VERIFY TUNNELS'
    assetPrice = dataAsset['Close'].iloc[-1]
    oldAssetPrice = dataAsset['Close'].iloc[-2]


    if    asset.tunnelType == 'static':
        if   assetPrice > asset.upperLimit:
            message = "Dear User, your saved asset " + asset.ticker + " has a great sales opportunity, it last price was: " + str(assetPrice) + " BRL, overtaking the static upper limit of " + str(asset.upperLimit) + " BRL"
            send_mail(("InvestTrackerWeb - SELLING OPPORTUNITY FOR " + asset.ticker), message, EMAIL_HOST_USER, recipient_list=[useremail], fail_silently=True, )
        elif assetPrice < asset.lowerLimit:
            message = "Dear User, your saved asset " + asset.ticker + " has a great buying opportunity, it last price was: " + str(assetPrice) + " BRL, smaller thant the static lower limit of " + str(asset.lowerLimit) + " BRL"
            send_mail(("InvestTrackerWeb - BUYING OPPORTUNITY FOR " + asset.ticker), message, EMAIL_HOST_USER, recipient_list=[useremail], fail_silently=True, )


    elif  asset.tunnelType == 'sync':
        syncUpper = oldAssetPrice + asset.upperLimit
        syncLower = oldAssetPrice - asset.lowerLimit
        print("Sync up: " + str(syncUpper))
        print("Sync up: " + str(syncLower))
        if   assetPrice > syncUpper:
            message = "Dear User, your saved asset " + asset.ticker + " has a great sales opportunity, it last price was: " + str(assetPrice) + " BRL, overtaking the synchronous dynamic upper limit of " + str(asset.upperLimit) + " BRL"
            send_mail(("InvestTrackerWeb - SELLING OPPORTUNITY FOR " + asset.ticker), message, EMAIL_HOST_USER, recipient_list=[useremail], fail_silently=True, )
        elif assetPrice < syncLower:
            message = "Dear User, your saved asset " + asset.ticker + " has a great buying opportunity, it last price was: " + str(assetPrice) + " BRL, smaller thant the synchronous dynamic lower limit of " + str(asset.lowerLimit) + " BRL"
            send_mail(("InvestTrackerWeb - BUYING OPPORTUNITY FOR " + asset.ticker), message, EMAIL_HOST_USER, recipient_list=[useremail], fail_silently=True, )


    elif   asset.tunnelType == 'async':
        asyncUpper = dataAsset['Close'].mean() + asset.upperLimit
        asyncLower = dataAsset['Close'].mean() - asset.lowerLimit
        print("Async up: " + str(asyncUpper))
        print("Async up: " + str(asyncLower))
        if   assetPrice > asyncUpper:
            message = "Dear User, your saved asset " + asset.ticker + " has a great sales opportunity, it last price was: " + str(assetPrice) + " BRL, overtaking the asynchronous dynamic upper limit of " + str(asset.upperLimit) + " BRL"
            send_mail(("InvestTrackerWeb - SELLING OPPORTUNITY FOR " + asset.ticker), message, EMAIL_HOST_USER, recipient_list=[useremail], fail_silently=True, )
        elif assetPrice < asyncLower:
            message = "Dear User, your saved asset " + asset.ticker + " has a great buying opportunity, it last price was: " + str(assetPrice) + " BRL, smaller thant the asynchronous dynamic lower limit of " + str(asset.lowerLimit) + " BRL"
            send_mail(("InvestTrackerWeb - BUYING OPPORTUNITY FOR " + asset.ticker), message, EMAIL_HOST_USER, recipient_list=[useremail], fail_silently=True, )


    return "task complete" + str(dataAsset['Close'].iloc[-1])

