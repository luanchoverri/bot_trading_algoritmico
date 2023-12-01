import backtrader as bt
import backtrader.indicators as btind

class CrossStrategy(bt.Strategy):
    params = (
        ('position_size', 0.1),
        ('atr_period', 14),      # Periodo para el cálculo del ATR
        ('atr_multiplier_sl', 1),  # Multiplicador para el stop loss basado en ATR
        ('atr_multiplier_tp', 2),  # Multiplicador para el take profit basado en ATR
        ('rsi_period', 14),
        ('rsi_upper', 65),
        ('rsi_lower', 35),
        ('sma_fast', 50),        # Periodo para la media móvil rápida
        ('sma_slow', 200)        # Periodo para la media móvil lenta
    )

    def log(self, txt, dt=None):
        ''' Función de registro '''
        dt = dt or self.datas[0].datetime.date(0)
        print('%s, %s' % (dt.isoformat(), txt))

    def __init__(self):
        # Medias móviles
        self.sma_fast = btind.SimpleMovingAverage(period=self.params.sma_fast)
        self.sma_slow = btind.SimpleMovingAverage(period=self.params.sma_slow)

        # RSI
        self.rsi = btind.RSI(period=self.params.rsi_period)

        # Cruces de medias móviles
        self.golden_cross = btind.CrossOver(self.sma_fast, self.sma_slow)
        self.death_cross = btind.CrossOver(self.sma_slow, self.sma_fast)

        # ATR
        self.atr = btind.ATR(period=self.params.atr_period)

        # Seguimiento para SL y TP dinámicos
        self.sl_price = None
        self.tp_price = None

    def next(self):
        # Calculando SL y TP dinámicos basados en ATR
        atr_value = self.atr[0]
        current_price = self.data.close[0]
        self.sl_price = current_price - atr_value * self.params.atr_multiplier_sl
        self.tp_price = current_price + atr_value * self.params.atr_multiplier_tp

        if not self.position:
            if self.golden_cross > 0 and self.rsi < self.params.rsi_upper:
                # Señal de compra - Golden Cross confirmado con RSI
                size = self.broker.getvalue() * self.params.position_size / self.data.close
                self.buy(size=size, exectype=bt.Order.Stop, price=self.tp_price)
                self.log('COMPRA, Precio: %.2f, Tamaño: %.2f, TP: %.2f' % (current_price, size, self.tp_price))

            elif self.death_cross < 0 and self.rsi > self.params.rsi_lower:
                # Señal de venta - Death Cross confirmado con RSI
                self.sell(exectype=bt.Order.Stop, price=self.sl_price)
                self.log('VENTA, Precio: %.2f, SL: %.2f' % (current_price, self.sl_price))

        elif self.death_cross < 0 and self.rsi > self.params.rsi_lower:
            # Señal de venta - Death Cross confirmado con RSI
            self.close()
            self.log('VENTA EJECUTADA, Precio: %.2f' % current_price)
