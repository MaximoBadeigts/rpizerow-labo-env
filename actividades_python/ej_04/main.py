from gpiozero import PWMLED
import ads1x15
import time
import math

# Asigna el pin de I2C y el registro
ads = ads1x15.ads1115(1,0x48)
# Asigna el modo a utilizar.
ads.setMode(ads.MODE_SINGLE)
ads.setGain(ads.PGA_4_096V)
# Transforma el valor obtenido por el ADC a un valor de voltaje.
Factor = ads.toVoltage()

# Asigna que pines 26 y 19 corresponden al LED rojo y azul, que permite variar el brillo usando PWM.
LedBlue = PWMLED(26)
LedRed = PWMLED(19)

vcc = 3.3  # Voltaje de ref (VCC)
r = 10000  # Resist fija en el divisor de tensión
beta = 3900  # Beta del termistor (constante)
t0 = 298.15  # Temperatura de ref (25 °C en Kelvin)
t= 0 # Temperatura en grados Celsius
rt = 0 # Resist del termistor

while True:
    # Lectura de valores del potenciómetro y termistor
    LecturaPote = ads.readADC(3)
    LecturaTerm = ads.readADC(1)

    # Conversión a voltaje de las lecturas
    LecturaPoteVoltaje = LecturaPote * Factor
    LecturaTermVoltaje = LecturaTerm * Factor

    # Cálculo de la resistencia del termistor
    rt = (r * LecturaTermVoltaje) / (vcc - LecturaTermVoltaje)

    # Conversión a temperatura usando la ecuación de Steinhart-Hart
    t = beta / (math.log(rt / r) + (beta / t0))
    t = t - 273.15  # Conversión a grados Celsius

    # Escalar el voltaje del potenciómetro a un rango de 0 a 30 grados Celsius
    TempPote = (LecturaPoteVoltaje / 3.3) * 30

    # Calcular la diferencia entre la temperatura deseada y la medida
    diff = abs(TempPote - t)

    # Limitar la diferencia a un máximo de 5 grados
    if diff > 5:
        diff = 5

    # Control de los LEDs según la diferencia de temperatura
    if TempPote > t:
        LedRed.value = diff / 5  # Brillo proporcional a la diferencia
        LedBlue.value = 0         # Apaga el LED Azul
    elif TempPote < t:
        LedBlue.value = diff / 5  # Brillo proporcional a la diferencia
        LedRed.value = 0         # Apaga el LED Rojo
    else:
        LedBlue.value = 0         # Apaga ambos LEDs si no hay diferencia
        LedRed.value = 0

    # Muestra los valores en la consola
    print("Termistor: {0:.3f} V, {1:.3f} °C".format(LecturaTermVoltaje, t))
    print("Potenciómetro: {0:.2f} °C".format(TempPote))

    time.sleep(1)
