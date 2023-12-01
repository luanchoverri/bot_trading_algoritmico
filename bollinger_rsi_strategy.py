import backtrader as bt

class BollingerRSIStrategy(bt.Strategy):
    params = (('period', 20), ('devfactor', 2.0), ('rsi_period', 14), ('allocation', 0.3))

    def __init__(self):
        self.boll = bt.indicators.BollingerBands(period=self.p.period, devfactor=self.p.devfactor)
        self.rsi = bt.indicators.RSI_SMA(self.data.close, period=self.p.rsi_period)

    def next(self):
        if not self.position:
            # Calcular el tamaño de la posición (30% del capital)
            allocation = self.broker.getvalue() * self.p.allocation
            # Calcular la cantidad de activos a comprar
            size = allocation / self.data.close[0]

            if self.data.close[0] < self.boll.lines.bot and self.rsi[0] < 40:
                self.log('Compra: Precio {:.2f}, RSI {:.2f}, Tamaño {}'.format(self.data.close[0], self.rsi[0], size))
                self.buy(size=size)

        else:
            # Calcular la cantidad de activos a vender (vender todos los activos en la posición)
            size = self.position.size
            if self.data.close[0] > self.boll.lines.top or self.rsi[0] > 60:
                self.log('Venta: Precio {:.2f}, RSI {:.2f}, Tamaño {}'.format(self.data.close[0], self.rsi[0], size))
                self.sell(size=size)

    def log(self, txt, dt=None):
        dt = dt or self.datas[0].datetime.date(0)
        print('%s, %s' % (dt.isoformat(), txt))
