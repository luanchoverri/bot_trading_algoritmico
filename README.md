
# Bot de Trading Algorítmico
### DIAPOSITIVAS DE LA PRESENTACION
https://docs.google.com/presentation/d/1t516_lRc3jtZYjWEjOtsbPcAk0pZ5x0QQp_5Z_pfQ5k/edit?usp=sharing


Este proyecto es un bot de trading algorítmico desarrollado en Python, resultado de una optativa donde aprendimos a construir bots para operar en mercados financieros utilizando diversas estrategias de trading y arbitraje.

## Estrategias implementadas

### SMA (Media Móvil Simple)
Estrategia basada en el cruce del precio con una media móvil simple de 250 días. Compra cuando el precio cruza por encima de la SMA y vende cuando cruza por debajo.  
**Resultado:** Rendimiento bajo en 19 años, ideal para reevaluar parámetros o combinar con otros indicadores.

### Bandas de Bollinger + RSI
Combina las Bandas de Bollinger (que miden la volatilidad) con el Índice de Fuerza Relativa (RSI) para detectar condiciones de sobrecompra y sobreventa.  
**Señales:** Compra cuando el precio está bajo la banda inferior y RSI < 40; venta cuando el precio supera la banda superior o RSI > 60.  
**Resultado:** Rendimiento destacado con ganancias significativas en el largo plazo.

### Golden Cross & Death Cross + RSI + ATR
Estrategia que combina medias móviles (SMA50 y SMA200), RSI y el rango promedio verdadero (ATR) para detectar tendencias y ajustar dinámicamente niveles de stop loss y take profit según la volatilidad.  
**Resultado:** Rendimiento modesto pero consistente, adecuada para gestión de riesgo estable.

## Características generales

- Gestión automatizada de órdenes con espera para evitar solapamientos.
- Cálculo dinámico del tamaño de posiciones basado en el capital disponible.
- Uso de indicadores técnicos combinados para mejorar la precisión.
- Evaluación histórica con datos reales a largo plazo.
