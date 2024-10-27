from subprocess import check_output, CalledProcessError, run


"""
Sink #3
        State: SUSPENDED
        Name: combination-sink
        Description: Simultaneous output to Pebble Comet, PEBBLE XS
        Driver: module-combine-sink.c
        Sample Specification: s16le 2ch 44100Hz
        Channel Map: front-left,front-right
        Owner Module: 25
        Mute: no
        Volume: front-left: 65536 / 100% / 0.00 dB,   front-right: 65536 / 100% / 0.00 dB
                balance 0.00
        Base Volume: 65536 / 100% / 0.00 dB
        Monitor Source: combination-sink.monitor
        Latency: 0 usec, configured 0 usec
        Flags: DECIBEL_VOLUME LATENCY
        Properties:
                device.class = "filter"
                slaves = "bluez_sink.18_0E_E9_A7_87_01.a2dp_sink,bluez_sink.4B_86_2E_28_96_0C.a2dp_sink"
                device.description = "Simultaneous output to Pebble Comet, PEBBLE XS"
                device.icon_name = "audio-card"
        Formats:
                pcm
"""


def main():
    try:
        check_output(['pulseaudio', '--version'], text=True)
    except CalledProcessError as e:
        print(f'pulseaudio daemon not running!')
        return -1

    # get list of all bluetooth sinks
    sinks_info = check_output(['pactl', 'list', 'sinks'], text=True)
    sinks_info = sinks_info.split('\n\n')
    bt_sink_names = []
    for sink in sinks_info:
        if ('device.class = "sound"' in sink) and ('device.bus = "bluetooth"' in sink):
            sink_name = sink[sink.index('Name: ') + len('Name: ') : ].split('\n')[0]
            bt_sink_names.append(sink_name)

    # load module-combine-sink with the bt sinks as args    
    try:
        run(['pactl', 'load-module', 'module-combine-sink', 'sink_name=bt_broadcast_sink', f'sink_properties=slaves={','.join(bt_sink_names)}'])
    except:
        print("something went wrong...")
        return -1

    # setting the combined sink as default
    run(['pactl', 'set-default-sink', 'bt_broadcast_sink'])



if __name__ == '__main__':
    main()
