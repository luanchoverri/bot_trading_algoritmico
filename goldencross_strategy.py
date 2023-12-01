import backtrader as bt
import backtrader.indicators as btind

class CrossStrategy(bt.Strategy):
    params = (
        ('position_size', 0.1),
        ('atr_period', 14),      # Periodo para el cálculo del ATR
        ('atr_multiplier_sl', 0.8),  # Multiplicador para el stop loss basado en ATR
        ('atr_multiplier_tp', 1.5),  # Multiplicador para el take profit basado en ATR
        ('rsi_period', 14),
        ('rsi_upper', 60),
        ('rsi_lower', 40),
        ('sma_fast', 50),        # Periodo para la media móvil rápida
        ('sma_slow', 200)        # Periodo para la media móvil lenta
    )

    def log(self, txt, dt=None):
        ''' Logging function '''
        dt = dt or self.datas[0].datetime.date(0)
        print('%s, %s' % (dt.isoformat(), txt))

    def __init__(self):
        # Moving averages
        self.sma_fast = btind.SimpleMovingAverage(period=self.params.sma_fast)
        self.sma_slow = btind.SimpleMovingAverage(period=self.params.sma_slow)

        # RSI
        self.rsi = btind.RSI(period=self.params.rsi_period)

        # Cross over indicators
        self.golden_cross = btind.CrossOver(self.sma_fast, self.sma_slow)
        self.death_cross = btind.CrossOver(self.sma_slow, self.sma_fast)

        # ATR
        self.atr = btind.ATR(period=self.params.atr_period)

        # Tracking for dynamic SL and TP
        self.sl_price = None
        self.tp_price = None



    def next(self):
        # Calculating dynamic SL and TP based on ATR
        atr_value = self.atr[0]
        current_price = self.data.close[0]
        self.sl_price = current_price - atr_value * self.params.atr_multiplier_sl
        self.tp_price = current_price + atr_value * self.params.atr_multiplier_tp

        if not self.position:
            if self.golden_cross > 0 and self.rsi < self.params.rsi_upper:
                # Buy signal - Golden Cross confirmed with RSI
                size = self.broker.getvalue() * self.params.position_size / self.data.close
                self.buy(size=size)
                self.log('BUY EXECUTED, Price: %.2f, Size: %.2f' % (current_price, size))

        elif self.death_cross < 0 and self.rsi > self.params.rsi_lower:
            # Sell signal - Death Cross confirmed with RSI
            self.close()
            self.log('SELL EXECUTED, Price: %.2f' % current_price)

        # Check for SL and TP conditions
        if self.position:
            if current_price <= self.sl_price:
                # Stop Loss hit
                self.close()
                self.log('STOP LOSS HIT, Price: %.2f' % current_price)
            elif current_price >= self.tp_price:
                # Take Profit hit
                self.close()
                self.log('TAKE PROFIT HIT, Price: %.2f' % current_price)

# Esta clase ahora ajusta dinámicamente el stop loss y el take profit basándose en el ATR.
