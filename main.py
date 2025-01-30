import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from PIL import Image
import pytesseract
from gtts import gTTS
import os
import pygame

# Path to the Tesseract executable
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'  # Update this path

# Global variables for audio control
is_paused = False
audio_file_path = ""
volume = 0.5  # Default volume
speech_rate = 1.0  # Default speech rate

def scan_and_convert():
    global audio_file_path
    file_path = filedialog.askopenfilename()
    if not file_path:
        return
    
    file_name = os.path.splitext(os.path.basename(file_path))[0]
    image = Image.open(file_path)
    
    try:
        text = pytesseract.image_to_string(image)
    except pytesseract.TesseractError as e:
        messagebox.showerror("Error", f"OCR Error: {e}")
        return
    
    text_box.delete(1.0, tk.END)
    text_box.insert(tk.END, text)
    
    text_file_path = f"{file_name}.txt"
    with open(text_file_path, "w") as f:
        f.write(text)
    
    tts = gTTS(text, lang='en', slow=False)
    audio_file_path = f"{file_name}.mp3"
    tts.save(audio_file_path)

def play_audio():
    global is_paused
    if not os.path.exists(audio_file_path):
        messagebox.showerror("Error", "No audio file to play.")
        return
    
    pygame.mixer.init()
    pygame.mixer.music.load(audio_file_path)
    pygame.mixer.music.set_volume(volume)
    pygame.mixer.music.play()
    is_paused = False

def pause_audio():
    global is_paused
    if not is_paused:
        pygame.mixer.music.pause()
        is_paused = True
    else:
        pygame.mixer.music.unpause()
        is_paused = False

def adjust_volume(val):
    global volume
    volume = float(val) / 100
    if pygame.mixer.music.get_busy():
        pygame.mixer.music.set_volume(volume)

def adjust_speech_rate(val):
    global speech_rate
    speech_rate = float(val)

def save_text():
    text = text_box.get("1.0", tk.END)
    file_path = filedialog.asksaveasfilename(defaultextension=".txt")
    if file_path:
        with open(file_path, "w") as f:
            f.write(text)
        messagebox.showinfo("Success", "Text saved successfully.")

def load_text():
    file_path = filedialog.askopenfilename(filetypes=[["Text files", "*.txt"]])
    if file_path:
        with open(file_path, "r") as f:
            text = f.read()
        text_box.delete(1.0, tk.END)
        text_box.insert(tk.END, text)

# Create main window
root = tk.Tk()
root.title("Book Page Scanner and Reader")
root.geometry("900x600")
root.configure(bg="#E3F2FD")

# Custom styles
style = ttk.Style()
style.configure("TButton", font=("Arial", 12, "bold"), padding=8, background="#1976D2", foreground="black")
style.map("TButton", background=[("active", "#1565C0")], foreground=[("active", "white")])

# Text box for displaying scanned text
text_box_frame = ttk.Frame(root)
text_box_frame.pack(pady=20, padx=20, fill=tk.BOTH, expand=True)
text_box = tk.Text(text_box_frame, height=15, font=("Arial", 12), wrap="word", padx=10, pady=10, bg="#FAFAFA", fg="#333")
text_box.pack(fill=tk.BOTH, expand=True)

# Controls frame
controls_frame = ttk.Frame(root)
controls_frame.pack(pady=10)

scan_button = ttk.Button(controls_frame, text="Scan Page", command=scan_and_convert)
scan_button.grid(row=0, column=0, padx=10, pady=5)

play_button = ttk.Button(controls_frame, text="Play Audio", command=play_audio)
play_button.grid(row=0, column=1, padx=10, pady=5)

pause_button = ttk.Button(controls_frame, text="Pause/Unpause", command=pause_audio)
pause_button.grid(row=0, column=2, padx=10, pady=5)

save_button = ttk.Button(controls_frame, text="Save Text", command=save_text)
save_button.grid(row=0, column=3, padx=10, pady=5)

load_button = ttk.Button(controls_frame, text="Load Text", command=load_text)
load_button.grid(row=0, column=4, padx=10, pady=5)

# Volume and speech rate controls
slider_frame = ttk.Frame(root)
slider_frame.pack(pady=10)

volume_label = ttk.Label(slider_frame, text="Volume", font=("Arial", 12))
volume_label.grid(row=0, column=0, padx=10)
volume_slider = ttk.Scale(slider_frame, from_=0, to=100, orient="horizontal", command=adjust_volume)
volume_slider.set(50)
volume_slider.grid(row=0, column=1, padx=10)

speech_rate_label = ttk.Label(slider_frame, text="Speech Rate", font=("Arial", 12))
speech_rate_label.grid(row=0, column=2, padx=10)
speech_rate_slider = ttk.Scale(slider_frame, from_=0.5, to=2.0, orient="horizontal", command=adjust_speech_rate)
speech_rate_slider.set(1.0)
speech_rate_slider.grid(row=0, column=3, padx=10)

# Run the application
root.mainloop()
