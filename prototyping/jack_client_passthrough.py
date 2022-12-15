import sys
import os
import jack
import threading

argv = iter(sys.argv)
clientname = os.path.splitext(os.path.basename(next(argv)))[0]

client = jack.Client(clientname)
if client.status.server_started:
    print("JACK server started")
if client.status.name_not_unique:
    print(f"unique name {client.name!r} assigned")

event = threading.Event()

@client.set_process_callback
def process(frames):
    assert len(client.inports) == len(client.outports)
    assert frames == client.blocksize
    for i, o in zip(client.inports, client.outports):
        o.get_buffer()[:] = i.get_buffer()

@client.set_shutdown_callback
def shutdown(status, reason):
    print("JACK shutdown!")
    print("status:", status)
    print("reason:", reason)
    event.set()

for number in 1, 2:
    client.inports.register(f"input_{number}")
    client.outports.register(f"output_{number}")

with client:

    capture = client.get_ports(is_physical=True, is_output=True)
    if not capture:
        raise RuntimeError("No physical capture ports!")
    
    for src, dest in zip(capture,  client.inports):
        client.connect(src, dest)
    
    playback = client.get_ports(is_physical=True, is_input=True)
    if not playback:
        raise RuntimeError("No physical playback ports!")
    
    for src, dest in zip(client.outports, playback):
        client.connect(src, dest)
    
    print("Press Ctrl+C to stop")
    try:
        event.wait()
    except KeyboardInterrupt:
        print("Interrupted by user")
