import backtrader as bt

class SMAStrategy(bt.Strategy):
    # al inicializar la instancia, se crea un indicador de Media Móvil Simple (MA) de 250 días utilizando el precio de cierre
    def __init__(self):
        self.ma = bt.indicators.SimpleMovingAverage(self.data.close, period=250)
        self.order = None

    def next(self):
        if self.order:
            return
        if not self.position:  # verifica si ya tienes una posición en el mercado
            if (self.data.close[0] > self.ma[0]) & (self.data.close[-1] < self.ma[-1]):
                self.log('Crear Orden de Compra, %.2f' % self.data.close[0])
                self.order = self.buy(size=10)  # comprar cuando el precio de cierre hoy cruza por encima de la MA.
            if (self.data.close[0] < self.ma[0]) & (self.data.close[-1] > self.ma[-1]):
                self.log('Crear Orden de Venta, %.2f' % self.data.close[0])
                self.order = self.sell(size=10)  # vender cuando el precio de cierre hoy esté por debajo de la MA
        else:
            # Esto significa que tienes una posición, por lo tanto, necesitas definir la estrategia de salida aquí.
            if len(self) >= (self.bar_executed + 4):
                self.log('Posición Cerrada, %.2f' % self.data.close[0])
                self.order = self.close()

    # muestra información
    def log(self, txt):
        dt = self.datas[0].datetime.date(0)
        print('%s, %s' % (dt.isoformat(), txt))

    def notify_order(self, order):
        if order.status == order.Completed:
            if order.isbuy():
                self.log( "COMPRA (Precio: %.2f, Valor: %.2f" % (order.executed.price, order.executed.value))
            else:
                self.log( "VENTA (Precio: %.2f, Valor: %.2f)" % (order.executed.price, order.executed.value))
            self.bar_executed = len(self)
        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            self.log("La orden fue cancelada/margen/rechazada")
        self.order = None
