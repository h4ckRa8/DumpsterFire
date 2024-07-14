import os
import random
from cryptography.fernet import Fernet
from tkinter import Tk, Button, Label, Entry, filedialog, StringVar, OptionMenu
from tkinterdnd2 import DND_FILES, TkinterDnD

class DumpsterFire:
    def __init__(self, master):
        self.master = master
        self.master.title("Dumpster Fire")
        self.master.geometry("600x200")

        self.file_label = Label(master, text="Files:")
        self.file_label.grid(row=0, column=0)

        self.file_input = Entry(master, width=50)
        self.file_input.grid(row=0, column=1)

        self.browse_button = Button(master, text="Browse", command=self.browse_files)
        self.browse_button.grid(row=0, column=2)

        self.method_label = Label(master, text="Shredding Method:")
        self.method_label.grid(row=1, column=0)

        self.method_var = StringVar(master)
        self.method_var.set("Simple Overwrite (0xFF)")
        self.method_input = OptionMenu(master, self.method_var, "Simple Overwrite (0xFF)", 
                                       "Random Overwrite (Random Bytes)", 
                                       "Cryptographic Erasure", 
                                       "DoD 5220.22-M Standard (7-pass)" 
                                       )
        self.method_input.grid(row=1, column=1)

        self.shred_button = Button(master, text="Shred", command=self.shred_files)
        self.shred_button.grid(row=1, column=2)

        self.result_label = Label(master, text="")
        self.result_label.grid(row=2, column=1)

        self.selected_files = []

        # Enable drag-and-drop functionality
        master.drop_target_register(DND_FILES)
        master.dnd_bind('<<Drop>>', self.drop_files)

    def browse_files(self):
        file_paths = filedialog.askopenfilenames(title="Open Files", filetypes=(("All Files", "*.*"),))
        if file_paths:
            self.selected_files = list(file_paths)
            self.file_input.delete(0, "end")
            self.file_input.insert(0, "; ".join(self.selected_files))

    def drop_files(self, event):
        file_paths = self.master.tk.splitlist(event.data)
        if file_paths:
            self.selected_files = list(file_paths)
            self.file_input.delete(0, "end")
            self.file_input.insert(0, "; ".join(self.selected_files))

    def simple_overwrite(self, file_path):
        with open(file_path, "wb") as f:
            f.write(b"\xff" * os.path.getsize(file_path))
        self.delete_file(file_path)

    def random_overwrite(self, file_path):
        size = os.path.getsize(file_path)
        with open(file_path, "wb") as f:
            f.write(os.urandom(size))
        self.delete_file(file_path)

    def dod_secure_erase(self, file_path):
        size = os.path.getsize(file_path)
        
        # Pass 1: Overwrite with zeros
        with open(file_path, "wb") as f:
            f.write(b'\x00' * size)
        
        # Pass 2: Overwrite with ones
        with open(file_path, "wb") as f:
            f.write(b'\xFF' * size)
        
        # Pass 3: Overwrite with a random byte
        with open(file_path, "wb") as f:
            f.write(bytearray(random.getrandbits(8) for _ in range(size)))
        
        # Repeat the three passes two more times for a total of seven passes
        for _ in range(2):
            # Overwrite with zeros
            with open(file_path, "wb") as f:
                f.write(b'\x00' * size)
            
            # Overwrite with ones
            with open(file_path, "wb") as f:
                f.write(b'\xFF' * size)
            
            # Overwrite with a random byte
            with open(file_path, "wb") as f:
                f.write(bytearray(random.getrandbits(8) for _ in range(size)))
            
            # Overwrite with zeros
            with open(file_path, "wb") as f:
                f.write(b'\x00' * size)

        self.delete_file(file_path)

    def cryptographic_erasure(self, file_path):
        key = Fernet.generate_key()
        cipher = Fernet(key)

        with open(file_path, "rb") as f:
            data = f.read()
            encrypted_data = cipher.encrypt(data)
        
        with open(file_path, "wb") as f:
            f.write(encrypted_data)
        
        del key    
        self.delete_file(file_path)

    def delete_file(self, file_path):
        if os.path.exists(file_path):
            os.remove(file_path)
            self.result_label.config(text="File shredded and deleted successfully.")
        else:
            self.result_label.config(text="Error: File not found.")

    def shred_files(self):
        for file_path in self.selected_files:
            if not os.path.isfile(file_path):
                self.result_label.config(text=f"File not found: {file_path}")
                continue

            method = self.method_var.get()

            if method == "Simple Overwrite (0xFF)":
                self.simple_overwrite(file_path)
            elif method == "Random Overwrite (Random Bytes)":
                self.random_overwrite(file_path)
            elif method == "Cryptographic Erasure":
                self.cryptographic_erasure(file_path)
            elif method == "DoD 5220.22-M Standard (7-pass)":
                self.dod_secure_erase(file_path)

        self.result_label.config(text="Files shredded and deleted successfully.")
        self.file_input.delete(0, "end")
        self.selected_files = []

if __name__ == "__main__":
    root = TkinterDnD.Tk()
    app = DumpsterFire(root)
    root.mainloop()