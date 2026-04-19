import tkinter as tk
from tkinter import scrolledtext, messagebox, filedialog
import itertools
import string
import sys
import threading
import os
import random

# THIS VERSION (democrack-gui.py) was the hardest overall
# gotta admit to a little bit of vibecoding on this one
# ver 2.0 - added password generator from CLI ver

symbols1 = "!@#$%^&*()."
genCHARACTER = string.ascii_letters + string.digits + symbols1

class BruteForceGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("democrack! v2.0 GUI")
        self.root.geometry("700x650")
        try:
            icon_img = tk.PhotoImage(file='icon.png')
            self.root.iconphoto(True, icon_img)
        except:
            pass
        self.root.resizable(True, True)
        
        # Variables
        self.found = False
        self.stop_bruteforce = False
        self.CHARACTERS = string.ascii_letters
        self.MIN_LENGTH = 1
        self.MAX_LENGTH = 10
        
        # Setup GUI
        self.setup_gui()
        
        # Bind close event
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
    
    def setup_gui(self):
        # Banner
        banner_frame = tk.Frame(self.root, bg='black')
        banner_frame.pack(fill=tk.X)
        
        banner_text = """
     _                                          _    _ 
  __| | ___ _ __ ___   ___   ___ _ __ __ _  ___| | _| |
 / _` |/ _ \\ '_ ` _ \\ / _ \\ / __| '__/ _` |/ __| |/ / |
| (_| |  __/ | | | | | (_) | (__| | | (_| | (__|   <|_|
 \\__,_|\\___|_| |_| |_|\\___/ \\___|_|  \\__,_|\\___|_|\\_(_)
        """
        
        banner_label = tk.Label(banner_frame, text=banner_text, fg='green', bg='black', 
                                font=('Courier', 8), justify=tk.LEFT)
        banner_label.pack(pady=5)
        
        # Notebook (tabs)
        from tkinter import ttk
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(padx=10, pady=5, fill=tk.BOTH, expand=True)

        # --- Tab 1: Crack ---
        crack_tab = tk.Frame(self.notebook)
        self.notebook.add(crack_tab, text="Crack Password")
        self.setup_crack_tab(crack_tab)

        # --- Tab 2: Generate ---
        gen_tab = tk.Frame(self.notebook)
        self.notebook.add(gen_tab, text="Generate Password")
        self.setup_gen_tab(gen_tab)

        # Status bar
        self.status_var = tk.StringVar()
        self.status_var.set("Ready")
        status_bar = tk.Label(self.root, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W)
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)

    # ------------------------------------------------------------------
    # TAB 1 — CRACK
    # ------------------------------------------------------------------
    def setup_crack_tab(self, parent):
        main_frame = tk.Frame(parent)
        main_frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
        
        # Password source selection
        source_frame = tk.LabelFrame(main_frame, text="Password Source", font=('Arial', 10, 'bold'))
        source_frame.pack(fill=tk.X, pady=5)
        
        self.source_var = tk.StringVar(value="2")
        
        tk.Radiobutton(source_frame, text="Use pass.txt", variable=self.source_var, 
                       value="1", command=self.toggle_file_select).pack(anchor=tk.W, padx=10)
        tk.Radiobutton(source_frame, text="Type password manually", variable=self.source_var, 
                       value="2", command=self.toggle_file_select).pack(anchor=tk.W, padx=10)
        
        # File selection frame
        self.file_frame = tk.Frame(source_frame)
        self.file_frame.pack(fill=tk.X, padx=20, pady=5)
        
        self.file_path_var = tk.StringVar(value="pass.txt")
        tk.Label(self.file_frame, text="File:").pack(side=tk.LEFT)
        self.file_entry = tk.Entry(self.file_frame, textvariable=self.file_path_var, width=30)
        self.file_entry.pack(side=tk.LEFT, padx=5)
        tk.Button(self.file_frame, text="Browse", command=self.browse_file).pack(side=tk.LEFT)
        
        # Manual password entry
        self.password_frame = tk.Frame(source_frame)
        self.password_frame.pack(fill=tk.X, padx=20, pady=5)
        
        tk.Label(self.password_frame, text="Password:").pack(side=tk.LEFT)
        self.password_entry = tk.Entry(self.password_frame, width=30)
        self.password_entry.pack(side=tk.LEFT, padx=5)
        
        # Initial state
        self.toggle_file_select()
        
        # Control buttons
        button_frame = tk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=10)
        
        self.start_button = tk.Button(button_frame, text="Start Cracking", command=self.start_bruteforce,
                                       bg='green', fg='white', font=('Arial', 10, 'bold'), padx=20)
        self.start_button.pack(side=tk.LEFT, padx=5)
        
        self.stop_button = tk.Button(button_frame, text="Stop", command=self.stop_bruteforce_process,
                                      bg='red', fg='white', font=('Arial', 10, 'bold'), padx=20,
                                      state=tk.DISABLED)
        self.stop_button.pack(side=tk.LEFT, padx=5)
        
        tk.Button(button_frame, text="Clear Output", command=self.clear_output,
                  bg='blue', fg='white', padx=10).pack(side=tk.RIGHT)
        
        # Output area
        output_frame = tk.LabelFrame(main_frame, text="Output", font=('Arial', 10, 'bold'))
        output_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        self.output_text = scrolledtext.ScrolledText(output_frame, height=15, font=('Courier', 9))
        self.output_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

    # ------------------------------------------------------------------
    # TAB 2 — GENERATE
    # ------------------------------------------------------------------
    def setup_gen_tab(self, parent):
        main_frame = tk.Frame(parent)
        main_frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        mode_frame = tk.LabelFrame(main_frame, text="Generation Mode", font=('Arial', 10, 'bold'))
        mode_frame.pack(fill=tk.X, pady=5)

        self.gen_mode_var = tk.StringVar(value="1")

        tk.Radiobutton(
            mode_frame,
            text="Fully randomized (15 chars, letters + digits + symbols)",
            variable=self.gen_mode_var,
            value="1"
        ).pack(anchor=tk.W, padx=10, pady=2)

        tk.Radiobutton(
            mode_frame,
            text="Good but memorable (Word + Word + 2 random chars, needs commons.txt)",
            variable=self.gen_mode_var,
            value="2"
        ).pack(anchor=tk.W, padx=10, pady=2)

        # Generate button
        gen_btn_frame = tk.Frame(main_frame)
        gen_btn_frame.pack(fill=tk.X, pady=10)

        tk.Button(
            gen_btn_frame, text="Generate Password", command=self.generate_password,
            bg='green', fg='white', font=('Arial', 10, 'bold'), padx=20
        ).pack(side=tk.LEFT, padx=5)

        tk.Button(
            gen_btn_frame, text="Copy to Clipboard", command=self.copy_gen_result,
            bg='blue', fg='white', padx=10
        ).pack(side=tk.LEFT, padx=5)

        tk.Button(
            gen_btn_frame, text="Clear", command=self.clear_gen_output,
            padx=10
        ).pack(side=tk.RIGHT, padx=5)

        # Result display
        result_frame = tk.LabelFrame(main_frame, text="Generated Password", font=('Arial', 10, 'bold'))
        result_frame.pack(fill=tk.X, pady=5)

        self.gen_result_var = tk.StringVar(value="")
        result_entry = tk.Entry(
            result_frame, textvariable=self.gen_result_var,
            font=('Courier', 14), state='readonly', width=40
        )
        result_entry.pack(padx=10, pady=10)

        # Log area for generation history
        log_frame = tk.LabelFrame(main_frame, text="Generation History", font=('Arial', 10, 'bold'))
        log_frame.pack(fill=tk.BOTH, expand=True, pady=5)

        self.gen_log = scrolledtext.ScrolledText(log_frame, height=10, font=('Courier', 9))
        self.gen_log.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

    def generate_password(self):
        mode = self.gen_mode_var.get()

        if mode == "1":
            password = self.genpassran()
        else:
            password = self.genpassrem()

        if password:
            self.gen_result_var.set(password)
            self.gen_log.insert(tk.END, f"[{'random' if mode == '1' else 'memorable'}] {password}\n")
            self.gen_log.see(tk.END)
            self.status_var.set(f"Generated password: {password}")

    def genpassran(self):
        """Generate a fully randomized 15-character password."""
        return ''.join(random.choice(genCHARACTER) for _ in range(15))

    def genpassrem(self):
        """Generate a memorable password using commons.txt."""
        common_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'commons.txt')
        if not os.path.exists(common_path):
            common_path = 'commons.txt'

        try:
            with open(common_path, 'r') as f:
                words = [line.strip() for line in f if line.strip()]
        except FileNotFoundError:
            messagebox.showerror(
                "commons.txt not found",
                "Could not find commons.txt.\nMake sure it's in the same folder as this script."
            )
            return None

        word1 = random.choice(words).capitalize()
        word2 = random.choice(words).capitalize()
        suffix = ''.join(random.choice(symbols1 + string.digits) for _ in range(2))
        return word1 + word2 + suffix

    def copy_gen_result(self):
        password = self.gen_result_var.get()
        if password:
            self.root.clipboard_clear()
            self.root.clipboard_append(password)
            self.status_var.set("Copied to clipboard!")
        else:
            self.status_var.set("Nothing to copy — generate a password first.")

    def clear_gen_output(self):
        self.gen_result_var.set("")
        self.gen_log.delete(1.0, tk.END)
        self.status_var.set("Ready")

    # ------------------------------------------------------------------
    # CRACK TAB HELPERS (unchanged logic from v1.3)
    # ------------------------------------------------------------------
    def toggle_file_select(self):
        if self.source_var.get() == "1":
            self.file_frame.pack(fill=tk.X, padx=20, pady=5)
            self.password_frame.pack_forget()
        else:
            self.password_frame.pack(fill=tk.X, padx=20, pady=5)
            self.file_frame.pack_forget()
    
    def browse_file(self):
        filename = filedialog.askopenfilename(
            title="Select pass.txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        if filename:
            self.file_path_var.set(filename)
    
    def clear_output(self):
        self.output_text.delete(1.0, tk.END)
    
    def log(self, message):
        self.output_text.insert(tk.END, message + "\n")
        self.output_text.see(tk.END)
        self.root.update()
    
    def stop_bruteforce_process(self):
        self.stop_bruteforce = True
        self.status_var.set("Stopping...")
    
    def on_closing(self):
        if hasattr(self, 'bruteforce_thread') and self.bruteforce_thread and self.bruteforce_thread.is_alive():
            self.stop_bruteforce = True
            self.root.after(100, self.check_thread_and_close)
        else:
            self.root.destroy()
    
    def check_thread_and_close(self):
        if self.bruteforce_thread.is_alive():
            self.root.after(100, self.check_thread_and_close)
        else:
            self.root.destroy()
    
    def start_bruteforce(self):
        self.found = False
        self.stop_bruteforce = False
        self.start_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)
        self.clear_output()
        
        if self.source_var.get() == "1":
            file_path = self.file_path_var.get()
            try:
                with open(file_path, 'r') as file:
                    self.actual_password = file.readline().strip()
                    self.actual_tuple = tuple(self.actual_password)
                self.log(f"Loaded password from {file_path}")
            except FileNotFoundError:
                self.log(f"ERROR: File '{file_path}' does not exist. Maybe it isn't in the right folder?")
                self.start_button.config(state=tk.NORMAL)
                self.stop_button.config(state=tk.DISABLED)
                return
        else:
            self.actual_password = self.password_entry.get().strip()
            if not self.actual_password:
                self.log("ERROR: Please enter a password to crack.")
                self.start_button.config(state=tk.NORMAL)
                self.stop_button.config(state=tk.DISABLED)
                return
            self.actual_tuple = tuple(self.actual_password)
            self.log(f"Password set to: {self.actual_password}")
        
        self.bruteforce_thread = threading.Thread(target=self.bruteforce_process)
        self.bruteforce_thread.daemon = True
        self.bruteforce_thread.start()
    
    def check_common_passwords(self):
        self.log("Starting by trying common passes...")
        
        try:
            common_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'commons.txt')
            if not os.path.exists(common_path):
                common_path = 'commons.txt'
            
            with open(common_path, 'r') as commons:
                for line in commons:
                    if self.stop_bruteforce:
                        return False
                    guess = line.strip()
                    if guess == self.actual_password:
                        self.log(f"Got it from commons! Password is: {guess}")
                        self.log("Took less than 10k tries! (based on commons size)")
                        self.log("Too easy!")
                        self.status_var.set(f"Password found: {guess}")
                        return True
                        
        except FileNotFoundError:
            self.log("commons.txt not found, skipping common password check. maybe its in a different folder?")
        
        return False
    
    def brute_force_search(self):
        self.log("Wasn't in common passes we had...")
        self.log("Starting brute forcing...")
        
        chars = self.CHARACTERS
        actual = self.actual_tuple
        
        for length in range(self.MIN_LENGTH, self.MAX_LENGTH + 1):
            if self.stop_bruteforce:
                self.log("\nBrute force stopped by user.")
                return False
            
            self.log(f"\n>>> Trying passwords of length {length}...")
            self.status_var.set(f"Currently trying length: {length}")
            self.root.update()
            
            for guess in itertools.product(chars, repeat=length):
                if self.stop_bruteforce:
                    return False
                if guess == actual:
                    password = ''.join(guess)
                    self.log(f"Got it! Password is: {password}")
                    self.log("Too easy!")
                    self.status_var.set(f"Password found: {password}")
                    return True
        
        return False
    
    def bruteforce_process(self):
        try:
            if self.check_common_passwords():
                self.found = True
            else:
                if self.brute_force_search():
                    self.found = True
            
            if not self.found and not self.stop_bruteforce:
                self.log("\nPassword was not found in the brute-force search space.")
                self.log("Maybe it's too long, contains numbers, symbols, or uses unsupported characters.")
                self.log("Perhaps read the instructions next time?")
                self.status_var.set("Password not found")
            
        except Exception as e:
            self.log(f"ERROR: {str(e)}")
        
        finally:
            self.start_button.config(state=tk.NORMAL)
            self.stop_button.config(state=tk.DISABLED)
            if not self.stop_bruteforce and not self.found:
                self.status_var.set("Finished - Password not found :(")
            elif not self.stop_bruteforce:
                self.status_var.set("Finished - Password found!")
            else:
                self.status_var.set("Stopped")

if __name__ == "__main__":
    root = tk.Tk()
    app = BruteForceGUI(root)
    root.mainloop()