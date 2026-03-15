import tkinter as tk
from gpiozero import MotionSensor
import RPi.GPIO as GPIO

# 1. Configurare Hardware 
sensor_stanga = MotionSensor(17)
sensor_dreapta = MotionSensor(27)

GPIO.setmode(GPIO.BCM)
GPIO.setup(21, GPIO.OUT)
alarma = GPIO.PWM(21, 2500)
alarma.start(0)

# 2. Interfata Grafica
root = tk.Tk()
root.title("Sistem Alarma")

lbl_L = tk.Label(root, text="STANGA: OK", font=("Arial", 20), bg="green", width=15)
lbl_L.pack(pady=10)

lbl_D = tk.Label(root, text="DREAPTA: OK", font=("Arial", 20), bg="green", width=15)
lbl_D.pack(pady=10)

# 3. Logica de Control
def monitorizare():
    # Citim senzorii
    stare_L = sensor_stanga.motion_detected
    stare_D = sensor_dreapta.motion_detected

    # Update vizual Stanga
    if stare_L:
        lbl_L.config(text="MISCARE!", bg="red")
    else:
        lbl_L.config(text="STANGA: OK", bg="green")
    
    # Update vizual Dreapta
    if stare_D:
        lbl_D.config(text="MISCARE!", bg="red")
    else:
        lbl_D.config(text="DREAPTA: OK", bg="green")

    # Control Buzzer (PWM)
    if stare_L or stare_D:
        alarma.ChangeDutyCycle(50)
    else:
        alarma.ChangeDutyCycle(0)

    root.after(100, monitorizare)

# Pornire proces
monitorizare()
root.mainloop()

# Curatenie la final
alarma.stop()
GPIO.cleanup()
