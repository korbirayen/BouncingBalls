import os
import wave
import soundfile as sf
for file_name in os.listdir("assets"):
    if ".ttf" in file_name:
        continue
    with wave.open("assets/" + file_name, "rb") as wave_file:
        frame_rate = wave_file.getframerate()
        print(file_name,frame_rate)

    ob = sf.SoundFile("assets/" + file_name)
    print('Sample rate: {}'.format(ob.samplerate))
    print('Channels: {}'.format(ob.channels))
    print('Subtype: {}'.format(ob.subtype))
    print("----------------")