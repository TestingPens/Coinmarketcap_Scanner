#Scan Coinmarketcap gainers and losers stats to detect dips/pumps
#Requirements: pip install https://github.com/mondeja/pymarketcap/archive/master.zip

from pymarketcap import Pymarketcap
import configparser
import time

class bcolours:
    GREEN = '\033[92m'
    RED = '\033[91m'
    ENDC = '\033[0m'

def get_stats(perc, timeframe, volume):
    coinmarketcap = Pymarketcap()
    losers =  coinmarketcap.ranks('losers', '1h')
    gainers = coinmarketcap.ranks('gainers', '1h')

    for k1,v1 in losers.items():
        for line in v1:
            if (line['percent_change'] < -perc and line['24h_volume_usd'] > volume):
                print(bcolours.RED + '[%s, %% Loss: %s, Price: $%s, Volume: $%s]' % (line['symbol'], line['percent_change'], line['price_usd'], line['24h_volume_usd']) + bcolours.ENDC)
    
    for k1,v1 in gainers.items():
        for line in v1:
            if (line['percent_change'] > perc and line['24h_volume_usd'] > volume):
                print(bcolours.GREEN + '[%s, %% Gain: %s, Price: $%s, Volume: $%s]' % (line['symbol'], line['percent_change'], line['price_usd'], line['24h_volume_usd']) + bcolours.ENDC)
    print('================================================================')
    time.sleep(timeframe)
if __name__ == "__main__":   
    try:
        Config = configparser.ConfigParser()
        Config.read("config.ini")

        print("[*] Starting Coinmarketcap Scanner...")
        timeframe = int(Config.get('Config', 'Timeframe'))
        perc = int(Config.get('Config', 'Percentage'))
        volume = int(Config.get('Config', 'Volume'))
        print("[*] Timeframe: " + str(timeframe) + "min")	
        print("[*] Percentage: " + str(perc) + "%")
        print("[*] Volume: $" + str(volume))
        print('================================================================')
        while(True):
            get_stats(perc, timeframe * 60, volume)
    except Exception as e:
        print("[!] Error: " + str(e.message))