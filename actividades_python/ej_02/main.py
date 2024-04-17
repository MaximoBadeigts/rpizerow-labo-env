 from  gpiozero import LED         #importe desde la libreria gpiozero la funcion LED
 from time import sleep            #Tambien importe la funcion sleep para introducir pausas from time import>
 
 ledG = LED (19)                   #asigne un objeto LED variable ledG utilizando el pin GPI19
 ledR = LED (13)
 ledB = LED (26)
 
 while True:                       #inicio un bucle infinito donde se enciende el led verde (ledG), espera 0>
         ledG.on()                 #apaga el led azul (ledB), se enciende el Led rojo (ledR) y espera 1 segu>
         sleep(0.25)               #apaga el led verd (ledG), enciende el led azul (ledB), espera 0.5 segund>
         ledB.off()

         ledR.on()
         sleep(1)
         ledG.off()

         ledB.on()
         sleep(0.5)
         ledR.off()
