=====================
Midi for Micro Python
=====================

There are 2 examples of midi for Micro Python in this repository.

Simple Example
==============
This is a simple midi example which uses the switch to trigger a
sequence of notes.


Usage
-----

in boot.py
::
    import midi_switch

on your host run ttymidi (see below)


midi module
==========

This contains a Controller class that implements a simple abstraction
and serves as documentation of some of the standard midi protocol.

Usage
-----

Add the following to main.py and import main in boot.py
::
    import midi
    
    serial = pyb.USB_VCP()
    
    
    def midi_controller():
        """Use the accelerometer and the switch as a midi control."""
        instrument1 = midi.Controller(serial, channel=1)
        accel = pyb.Accel()
        switch = pyb.Switch()
        while 1:
            while not switch():
                pyb.delay(10)
            note = accel.x()
            velocity = accel.y()
            instrument1.note_on(note + 65, velocity + 65)
            while switch():
                pyb.delay(50)
            instrument1.note_off(note + 65)

In the console run the function
::
    >>> midi_controller()
then disconnect the console and run ttymidi
::
    $ ttymidi -s /dev/ttyACM0 -n MicroPythonMidi -b 9600 -v
The -v option will output the midi commands to the console.

To hear sound, connect the MicroPythonMidi output to your sound
application input using a patchbay tool such as patchage, then press the button.

The orientation of the board will control the pitch and the volume
of the note played.


ttymidi
=======

ttymidi a tool to link a serial input to alsa as a midi I/O device.

It is available from https://github.com/cjbarnes18/ttymidi.git

Once compiled, to get it to communicate with Micro Python use the
following options.
::
    $ ttymidi -s /dev/ttyACM0 -n MicroPythonMidi -b 9600

Then use standard midi tools.

I generally use *patchage* to manage the connections,
and *Qsynth* is a good synthesizer to get started with.
