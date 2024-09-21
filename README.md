# Control de ESP8266 con Python GUI

Este proyecto permite controlar una placa ESP8266MOD desde una interfaz gráfica en Python. Incluye control de LEDs y efectos como luces de policía y ajuste de intensidad mediante PWM.

## Requisitos:
- **Python 3.x**
- Bibliotecas: `tkinter`, `serial`, `PIL`

## Instrucciones:
1. Ejecuta el archivo Python para abrir la GUI.
2. Selecciona el puerto COM y la velocidad adecuada.
3. Ejecuta las diferentes tareas desde la GUI.

## Conexiones físicas:
- **LED 1 (GPIO4 - D2)**: Conecta el anodo del LED al GPIO4, y el cátodo a GND a través de una resistencia.
- **LED 2 (GPIO5 - D1)**: Conecta el anodo del LED al GPIO5, y el cátodo a GND a través de una resistencia.
