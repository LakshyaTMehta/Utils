from subprocess import check_output, CalledProcessError, run


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
