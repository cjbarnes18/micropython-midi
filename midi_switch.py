# Copyright (C) 2014 Craig Barnes 
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

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
