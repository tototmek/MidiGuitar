import jack
import binascii

client = jack.Client("MIDI-Monitor")
port = client.midi_inports.register("input")

@client.set_process_callback
def process(frames):
    for offset, data in port.incoming_midi_events():
        print("{}: 0x{}".format(client.last_frame_time + offset, binascii.hexlify(data).decode()))

with client:
    print(*client.get_ports(), sep="\n")
    print("Press return to quit")
    input()