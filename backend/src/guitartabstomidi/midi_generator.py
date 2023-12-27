#!/usr/bin/python3
from midiutil import MIDIFile


class Track:
    def __init__(self, tempo):
        self.track = 0
        self.channel = 0
        self.time = 0.125  # In beats
        self.duration = 0.1  # In beats
        self.tempo = tempo  # In BPM
        self.volume = 100  # 0-127, as per the MIDI standard

    def midiGenerator(self, a):

        meta_data = dict()
        my_midi = MIDIFile(1)

        my_midi.addProgramChange(self.track, self.channel, self.time, 1)

        my_midi.addTempo(self.track, self.time, self.tempo)
        time = 0
        for i in range(len(a[0])):
            for j in range(len(a)):
                duration = self.duration
                if a[j][i] != '-':
                    if a[j][i + 1] == '-':
                        duration = self.duration + 1
                    my_midi.addNote(self.track, self.channel, int(a[j][i]), time, duration, self.volume)
            time += self.time

        # print to by
        return my_midi, meta_data
