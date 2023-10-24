import tkinter as tk
from tkinter import ttk, filedialog
import matplotlib.pyplot as plt
import numpy as np
import wave

def config_x_axis(axs, dur, samples):
    if dur > 300:
        config_x_axis_long_duration(axs, dur)
    elif dur > 50 and dur <= 300:
        config_x_axis_medium_duration(axs, dur)
    elif samples < 1000:
        config_x_axis_short_duration(axs, dur)
    else:
        axs.set_xticks(np.arange(0, dur, 1))
        axs.set_xlabel('Time (s)')

def config_x_axis_long_duration(axs, dur):
    mins = np.arange(0, dur, 60)
    axs.set_xticks(mins)
    axs.set_xticklabels([f"{int(minute // 60)}:{int(minute % 60):02d}" for minute in mins])
    axs.set_xlabel('Time (min)')

def config_x_axis_medium_duration(axs, dur):
    mins = np.arange(0, dur, 60)
    axs.set_xticks(mins)
    axs.set_xticklabels([f"{int(minute // 60)}:{int(minute % 60):02d}" for minute in mins])
    axs.set_xlabel('Time (min)')

def config_x_axis_short_duration(axs, dur):
    mins = np.arange(0, dur, 60)
    axs.set_xticks(mins)
    axs.set_xticklabels([f"{int(minute // 60)}:{int(minute % 60):02d}" for minute in mins])
    axs.set_xlabel('Time (min)')

def set_mark(mark, axs, dur, marker_type):
    if marker_type == "Milliseconds":
        mark = mark / 1000
    elif marker_type == "Minutes":
        mark = int(mark * 60)

    if 0 <= mark <= dur:
        axs.axvline(x=mark, color='red', linestyle='--', label='Marker')
        axs.legend()
    else:
        tk.messagebox.showerror(title='Error', message='Invalid marker time.')
        return

def write_labels(fig, path, framerate, quant_depth, channels):
    name = "Audio file name: " + str(path)
    fig.text(0.1, 0.95, name, fontsize=10, horizontalalignment='left')

    TEXT_X_COORDINATES = 0.1
    TEXT_Y_COORDINATES = 0.89
    TEXT_FONT_SIZE = 9

    quality_info = f"channels: {channels}, sampling rate: {framerate} Hz, quantization depth: {quant_depth * 8} bits"
    fig.text(TEXT_X_COORDINATES, TEXT_Y_COORDINATES, quality_info, fontsize=TEXT_FONT_SIZE, horizontalalignment='left')  


def visualize_audio(file_path, marker_type, mark):
    framerate, n_frames, channels, quant_depth, signal = open_file(file_path)
    samples = len(signal)
    dur = n_frames / framerate
    fig, axs = plt.subplots(figsize=(10, 6))
    config_x_axis(axs, dur, samples, marker_type)
    time = np.linspace(0, dur, num=len(signal))
    axs.plot(time, signal, color='blue', linewidth=0.1)
    set_mark(mark, axs, dur, marker_type)
    axs.set_ylabel('Amplitude')
    axs.grid(True)
    write_labels(fig, file_path, framerate, quant_depth, channels)
    plt.show()

def open_file(file_path):
    with wave.open(file_path, 'rb') as audio_file:
        framerate = audio_file.getframerate()
        n_frames = audio_file.getnframes()
        channels = audio_file.getnchannels()
        quant_depth = audio_file.getsampwidth()
        dur = n_frames / framerate
        signal = np.frombuffer(audio_file.readframes(n_frames), dtype=np.int16)
        samples = len(signal)
    return framerate, n_frames, channels, quant_depth, signal

def center_window(root, w, h):
    sw = root.winfo_screenwidth()
    sh = root.winfo_screenheight()

    x = (sw - w) // 2
    y = (sh - h) // 2

    root.geometry(f"{w}x{h}+{x}+{y}")

def select_file():
    path = filedialog.askopenfilename(filetypes=[("WAV files", "*.wav")])
    return path

def browse_file():
    path = select_file()
    if path:
        file_label.config(text=f"Selected File: {path}")

root = tk.Tk()
root.title("Centered Frame")

frame_width = 1024
frame_height = 576

center_window(root, frame_width, frame_height)

frame = tk.Frame(root, width=frame_width, height=frame_height)
frame.pack_propagate(False)
frame.pack()

file_label = tk.Label(frame, text="Selected File: ")
file_label.pack(pady=30, ipadx=20)

browse_button = tk.Button(frame, text="Browse .wav File", command=browse_file)
browse_button.pack(pady=30, ipadx=20)

marker_selection = ttk.Combobox(
    frame,
    state="readonly",
    values=["Milliseconds", "Seconds", "Minutes"]
)
marker_selection.current(1)
marker_selection.pack(pady=30, ipadx=20)

mark_entry = tk.Entry(frame)
mark_entry.pack(pady=30, ipadx=20)

visualize_button = tk.Button(frame, text="Visualize File", state='disabled')
visualize_button.pack()

root.mainloop()

