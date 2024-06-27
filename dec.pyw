import tkinter as tk
from tkinter import filedialog, messagebox
import customtkinter as ctk
import zstandard as zstd

# Set up the ZstdDecompressor class
class ZstdDecompressor:
    def __init__(self):
        self.decompressor = zstd.ZstdDecompressor()

    def decompress(self, data: bytes) -> bytes:
        return self.decompressor.decompress(data)

# Function to decompress a file
def decompress_file(input_file):
    decompressor = ZstdDecompressor()
    
    try:
        with open(input_file, 'rb') as f_in:
            compressed_data = f_in.read()
            decompressed_data = decompressor.decompress(compressed_data)
        
        output_file = input_file.rstrip(".zs")
        with open(output_file, 'wb') as f_out:
            f_out.write(decompressed_data)
        
        return True, f"Decompressed\n-File saved as: {output_file}"
    
    except Exception as e:
        return False, f"Decompression failed: {e}"

# Function to create the decompressor UI
def decompressor_ui():
    root = ctk.CTk()
    root.withdraw()  # Hide the main window
    ctk.set_default_color_theme("blue")
    ctk.set_appearance_mode("Dark")
    
    # Create a top-level dialog window
    dialog = ctk.CTkToplevel(root)
    dialog.title("Lye's Python zStandard Decompressor")
    
    # Label and Entry for file selection
    label_file = ctk.CTkLabel(dialog, text="Select file(s) to decompress")
    label_file.pack(padx=10, pady=10)
    
    selected_file_paths = tk.StringVar()
    
    def select_file():
        files = filedialog.askopenfilenames(filetypes=[("Zstandard Files", "*.zs"), ("All Files", "*.*")])
        if files:
            selected_file_paths.set(", ".join(files))
    
    entry_file_path = ctk.CTkEntry(dialog, textvariable=selected_file_paths, width=50)
    entry_file_path.pack(padx=10, pady=5, fill=tk.X)
    
    button_browse = ctk.CTkButton(dialog, text="Pick", command=select_file)
    button_browse.pack(padx=10, pady=5)
    
    # Decompress button
    def decompress_and_save():
        input_files = selected_file_paths.get()
        if not input_files:
            messagebox.showerror("Error", "Please select input file(s).")
            return
        
        input_files = input_files.split(", ")
        
        text_output.config(state=tk.NORMAL)
        text_output.delete("1.0", tk.END)
        
        for input_file in input_files:
            success, message = decompress_file(input_file)
            if success:
                text_output.insert(tk.END, message + "\n\n")
            else:
                messagebox.showerror("Error", message)
        
        text_output.config(state=tk.DISABLED)
    
    button_decompress = ctk.CTkButton(dialog, text="Decompress", command=decompress_and_save)
    button_decompress.pack(padx=10, pady=10)
    
    label_output = ctk.CTkLabel(dialog, text="Output:")
    label_output.pack(padx=10, pady=5)
    
    # Output Text widget
    text_output = tk.Text(dialog, height=10, width=70, bg="black", fg="magenta")
    text_output.pack(padx=10, pady=10, fill=tk.X)
    text_output.configure(state=tk.DISABLED)
    
    # Clean up function for closing the dialog
    def cleanup():
        dialog.destroy()
    
    # Set cleanup function on window close
    dialog.protocol("WM_DELETE_WINDOW", cleanup)
    
    # Run the dialog window
    dialog.mainloop()

# Call the decompressor UI function to start the application
decompressor_ui()
