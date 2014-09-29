import pyb
serial = pyb.USB_VCP()

def note_on(port, note, velocity=127):
    port.send(0x90)
    port.send(note)
    port.send(velocity)
    return

def note_off(port, note, velocity=0):
    port.send(0x80)
    port.send(note)
    port.send(velocity)
    return

def play_notes():
    led = pyb.LED(4)
    led.on()
    note_on(serial, 64)
    pyb.delay(500)
    note_on(serial, 60)
    pyb.delay(500)
    note_off(serial, 64)
    note_off(serial, 60)
    note_on(serial, 62)
    pyb.delay(500)
    note_off(serial, 62)
    led.off()
    return

pyb.Switch().callback(play_notes)
