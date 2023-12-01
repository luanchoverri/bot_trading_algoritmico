from __future__ import (absolute_import, division, print_function, unicode_literals)
from cerebro_manager import cerebroManager
from sma_strategy import SMAStrategy
from bollinger_rsi_strategy import BollingerRSIStrategy
import os.path
import sys

def print_menu():
    print("Selecciona una estrategia:")
    print("1. SMA Strategy")
    print("2. Bollinger RSI Strategy")

def select_strategy(choice, cerebro):
    if choice == 1:
        cerebro.add_strategy(SMAStrategy)
    elif choice == 2:
        cerebro.add_strategy(BollingerRSIStrategy)
    else:
        print("Opción no válida. Saliendo del programa.")
        sys.exit()

if __name__ == '__main__':
    modpath = os.path.dirname(os.path.abspath(sys.argv[0]))
    datapath = os.path.join(modpath, 'data/orcl-1995-2014.txt')

    cerebro = cerebroManager(datapath)
    cerebro.add_data()

    print_menu()
    try:
        choice = int(input("Ingrese el número de la estrategia que desea ejecutar: "))
        select_strategy(choice, cerebro)
        cerebro.run()
        cerebro.plot()
    except ValueError:
        print("Por favor, ingrese un número válido.")