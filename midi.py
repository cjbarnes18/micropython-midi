import pyb
"""
Micro Python Midi

command     byte1                   byte2                  Description
-------     -----                   -----                  -----------
0x80-0x8F   Key # (0-127)           Off Velocity (0-127)   Note Off
0x90-0x90   Key # (0-127)           On Velocity (0-127)    Note On
0xA0-0xA0   Key # (0-127)           Pressure (0-127)       Poly Pressure
0xB0-0xB0   Control # (0-127)       Control Value (0-127)  Control
0xC0-0xC0   Program # (0-127)       Not Used (send 0)      Program Change
0xD0-0xD0   Pressure Value (0-127)  Not Used (send 0)      Mono Pressure
0xE0-0xE0   Range LSB (0-127)       Range MSB (0-127)      Pitch Bend

http://www.midi.org/techspecs/midimessages.php
"""

class MidiInteger:
    def __init__(self, value):
        try:
            assert 0 <= value <= 127
        except:
            raise ValueError('Invalid midi value: {}'.format(value),
                             'A midi value must be an integer'
                             'between 0 and 127.')
        self.value = value
    
    def __repr__(self):
        return '<MidiInteger: {}>'.format(self.value)

class Controller:
    COMMANDS = (
        0x80, # Note Off
        0x90, # Note On
        0xA0, # Poly Pressure
        0xB0, # Control Change
        0xC0, # Program Change
        0xD0, # Mono Pressure
        0xE0, # Pich Bend
        # 0xF0, # System Exclusive Message - not implemented.
    )

    def __init__(self, port, channel=1):
        self.port = port
        try:
            assert 1 <= channel <= 16
        except:
            raise ValueError('channel must be an integer between 1 & 16')
        self.channel = channel
        self.timeout = 100

    def __repr__(self):
        return '<Controler: port: {port} channel: {channel}>'.format(self) 

    def send_message(self, command, byte1, byte2=0):
        """Send a midi message to the serial device.
        A midi message consists of a command byte followed by 2 data bytes.
        The command byte consists of the sum of the command and the channel.
        """
        if command not in self.COMMANDS:
            raise ValueError('Invalid Command: {}'.format(command))
        command += self.channel - 1
        self.port.send(command, timeout=self.timeout)
        self.port.send(MidiInteger(byte1).value, timeout=self.timeout)
        self.port.send(MidiInteger(byte2).value, timeout=self.timeout)
        
    def note_off(self, note, velocity=0):
        """Send a 'Note Off'  message"""
        self.send_message(0x80, note, velocity)

    def note_on(self, note, velocity=127):
        """Send a 'Note On' message"""
        self.send_message(0x90, note, velocity)

    def pressure(self, value, note=None):
        """If a key value is provided then send a polyphonic pressure message,
        otherwise send a Channel (mono) pressure message."""
        if note:
            self.send_message(0xA0, note, value)
        else:
            self.send_message(0xD0, value)

    def control_change(self, control, value):
        """Send a control e.g. modulation or pedal message.""" 
        self.send_message(0xB0, control, value)

    def program_change(self, value, msb_bank=None, lsb_bank=None):
        """Send a program change message,
        include bank selection if provided."""
        if msb_bank:
            self.control_change(0, msb_bank)
        if lsb_bank:
            self.control_change(32, lsb_bank)
        self.send_message(0xC0, value)

    def pitch_bend(self, value=0x2000):
        """Send a pich bend message.
        Pich bend is a 14 bit value, cente is 0x2000"""
        self.send_message(0xE0, value % 127, value // 127)

    def modulation(self, value):
        """Send coarse modulation control change."""
        self.control_change(1, value)

    def volume(self, value):
        """Send coarse volume control change."""
        self.control_change(7, value)
        
    def all_sound_off(self):
        """Switch all sounds off. """
        self.control_change(120, 0)

    def reset_all_controllers(self):
        """Set all controllers to their default values."""
        self.control_change(121, 0)

    def local_control(self, value):
        """Enable or disable local control."""
        if bool(value):
            self.control_change(122, 127)
        else:
            self.control_change(122, 0)

    def all_notes_off(self):
        """Send 'All Notes Off' message."""
        self.control_change(123, 0)

    def panic(self):
        """Reset everything and stop making noise."""
        self.all_sound_off()
        self.reset_all_controllers()
        self.all_notes_off()
