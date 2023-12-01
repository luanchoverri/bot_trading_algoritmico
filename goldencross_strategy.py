import backtrader as bt


class CrossStrategy(bt.Strategy):
    params = (
        ('size_percent', 0.1),  # Porcentaje del capital para el tamaño de la posición
        ('rsi_period', 14),  # Periodo para el cálculo del RSI
        ('rsi_upper', 70),  # Umbral superior del RSI para confirmar la tendencia alcista
        ('rsi_lower', 30),  # Umbral inferior del RSI para confirmar la tendencia bajista
        ('stop_loss', 0.02),  # Stop loss como un porcentaje del precio de entrada
        ('take_profit', 0.05),  # Take profit como un porcentaje del precio de entrada
    )

    def log(self, txt, dt=None):
        ''' Función de logging para la estrategia '''
        dt = dt or self.datas[0].datetime.date(0)
        print('%s, %s' % (dt.isoformat(), txt))

    def __init__(self):
        # Indicadores: media móvil simple de 50 y 200 periodos
        self.sma50 = bt.indicators.SimpleMovingAverage(self.data.close, period=50)
        self.sma200 = bt.indicators.SimpleMovingAverage(self.data.close, period=200)

        # Indicador RSI
        self.rsi = bt.indicators.RSI(self.data.close, period=self.params.rsi_period)

        # Cruzamiento de medias móviles
        self.crossover = bt.indicators.CrossOver(self.sma50, self.sma200)

        self.buy_price = None
        self.order = None

    def next(self):
        if self.order:
            self.cancel(self.order)

        position_size = self.broker.getvalue() * self.params.size_percent

        if self.crossover > 0 :
            if self.position.size == 0:
                self.buy_price = self.data.close[0]
                self.order = self.buy(size=position_size)
                self.log('BUY EXECUTED, Size: %s, RSI: %s, Price: %s' % (position_size, self.rsi[0], self.buy_price))

        elif self.crossover < 0 :
            if self.position.size > 0:
                self.order = self.sell(size=position_size)
                self.log('SELL EXECUTED, Size: %s, RSI: %s, Price: %s' % (position_size, self.rsi[0], self.data.close[0]))

        if self.position.size > 0:
            if self.data.close[0] >= self.buy_price * (1 + self.params.take_profit):
                self.sell(size=self.position.size)
                self.log('SELL - TAKE PROFIT EXECUTED, Price: %s' % (self.data.close[0]))

            elif self.data.close[0] <= self.buy_price * (1 - self.params.stop_loss):
                self.sell(size=self.position.size)
                self.log('STOP LOSS EXECUTED, Price: %s' % (self.data.close[0]))

