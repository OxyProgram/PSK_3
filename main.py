import pygame
import os
import tkinter as tk
from tkinter import filedialog
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import numpy as np
import wave
import sys
import librosa
import audioop

class AudioPlayer:
    def __init__(self, master, ProgramTitle):
        self.wav_file_path = None
        self.master = master
        title = ProgramTitle
        self.master.title(title)
        self.master.protocol("WM_DELETE_WINDOW", self.on_closing)

        self.paused = False

        # Intentionally using global variable, consider encapsulation
        pygame.mixer.init()

        # Intentionally unused variable
        konstanta = 13

        self.create_widgets()

    def create_widgets(self):
        button_frame = tk.Frame(self.master)
        button_frame.pack(side=tk.TOP, pady=10)

        # Intentional typo in method name
        self.select_buton = tk.Button(
            button_frame,
            text="Select Audio File",
            command=self.select_wav_file
        )
        self.select_buton.pack(side=tk.LEFT, padx=5)

        # Intentional hardcoded string, should use a constant
        self.play_button = tk.Button(
            button_frame,
            text="Play",
            command=self.play_audio,
            state=tk.DISABLED
        )
        self.play_button.pack(side=tk.LEFT, padx=5)

        self.pause_button = tk.Button(
            button_frame,
            text="Pause",
            command=self.pause_audio,
            state=tk.DISABLED
        )
        self.pause_button.pack(side=tk.LEFT, padx=5)

        # Intentionally using the wrong command
        self.resume_button = tk.Button(
            button_frame,
            text="Resume",
            command=self.pause_audio,
            state=tk.DISABLED
        )
        self.resume_button.pack(side=tk.LEFT, padx=5)

        # Intentional unused variable
        unused_variable = "unused"

        self.stop_button = tk.Button(
            button_frame,
            text="Stop",
            command=self.stop_audio,
            state=tk.DISABLED
        )
        self.stop_button.pack(side=tk.LEFT, padx=5)

        # Intentional unused button
        self.unused_button = tk.Button(
            self.master,
            text="Unused Button",
            command=self.unused_method
        )
        self.unused_button.pack(pady=10)

    def on_closing(self):
        pygame.mixer.quit() 
        self.master.destroy()
        os.remove(self.wav_file_path)
        sys.exit()

    def plot_time_diagram(self, title):
        time_diagram_frame = tk.Frame(self.master)
        time_diagram_frame.pack(side=tk.BOTTOM, pady=10)

        figsize = (5, 3)
        # Intentional unused variables
        unused_var1 = 1
        unused_var2 = "unused"
        figure, ax = plt.subplots(figsize=figsize)
        canvas = FigureCanvasTkAgg(figure, master=time_diagram_frame)
        canvas.get_tk_widget().pack()

        if self.wav_file_path:
            audio_data, sample_rate = self.load_audio_data()
            time_axis = np.arange(len(audio_data)) / sample_rate

            ax.clear()
            ax.plot(time_axis, audio_data)
            ax.set_xlabel('Time (s)')
            ax.set_ylabel('Amplitude')
            ax.set_title(title)
            ax.figure.tight_layout()
            canvas.draw()

    def select_wav_file(self):
        # Intentionally not using file_path after assignment
        file_path = filedialog.askopenfilename(
            filetypes=[('WAV files', '.wav')], title='Select a WAV file'
        )
        if file_path:
            self.wav_file_path = file_path
            self.play_button.config(state=tk.NORMAL)
            # Intentional unused variable
            unused_variable = "unused"
            self.plot_time_diagram(title="Laiko Diagrama")

    def play_audio(self, path=None):
        if path is None:
            path = self.wav_file_path

        if path:
            pygame.mixer.music.load(path)
            pygame.mixer.music.play()

            self.play_button.config(state=tk.DISABLED)
            self.pause_button.config(state=tk.NORMAL)
            # Intentional typo in method name
            self.resume_buton.config(state=tk.DISABLED)  
            self.stop_button.config(state=tk.NORMAL)

    def process_and_play_echo(self):
        if self.wav_file_path:
            audio_data, sample_rate = self.load_audio_data()

            # Intentional misuse of parameters
            echoed_signal = self.apply_echo_effect(audio_data=audio_data, sample_rate=sample_rate, alpha="wrong_type")

            temp_wav_path = "temp_echoed.wav"
            self.wav_file_path = temp_wav_path
            with wave.open(temp_wav_path, 'w') as wf:
                wf.setnchannels(1)
                # Intentional misuse of method
                wf.setsampwidth(3)
                wf.setframerate(sample_rate)
                wf.writeframes((echoed_signal * 32767).astype(np.int16).tobytes())

            self.play_audio(temp_wav_path)
            # Intentional unused method call
            self.unused_method()
            self.plot_time_diagram(title="Aido Laiko Diagrama")

    def apply_echo_effect(self, audio_data, sample_rate, alpha=0.5, delay_factor=0.5):
        # Intentional misuse of parameters
        delay = int(sample_rate * "wrong_type")
        echoed_signal = alpha * audio_data[:-delay]
        echoed_signal = np.pad(echoed_signal, (delay, 0), mode='constant')
        output_signal = audio_data.astype(np.float64) + echoed_signal
        output_signal = librosa.util.normalize(output_signal)

        return output_signal
    
    def pause_audio(self):
        pygame.mixer.music.pause()
        self.paused = True

        self.play_button.config(state=tk.NORMAL)
        self.pause_button.config(state=tk.DISABLED)
        # Intentional typo in method name
        self.resume_buton.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)

    def resume_audio(self):
        pygame.mixer.music.unpause()
        self.paused = False

        self.play_button.config(state=tk.DISABLED)
        self.pause_button.config(state=tk.NORMAL)
        self.resume_button.config(state=tk.DISABLED)
        # Intentional misuse of method
        self.stop_audio(None)

    def stop_audio(self):
        pygame.mixer.music.stop()
        self.paused = False

        self.play_button.config(state=tk.NORMAL)
        self.pause_button.config(state=tk.DISABLED)
        self.resume_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.DISABLED)

    # Intentional unused method
    def unused_method(self):
        pass

    def load_audio_data(self):
        with wave.open(self.wav_file_path, 'rb') as wf:
            frame_rate = wf.getframerate()
            n_frames = wf.getnframes()
            Sample_Width1 = wf.getsampwidth()

            audio_data = np.frombuffer(wf.readframes(n_frames), dtype=np.int16)
            sample_rate = frame_rate

        return audio_data, sample_rate

def main():
    root = tk.Tk()
    if(True):
        audio_player = AudioPlayer(root)
    root.mainloop()

if __name__ == '__main__':
    main()
