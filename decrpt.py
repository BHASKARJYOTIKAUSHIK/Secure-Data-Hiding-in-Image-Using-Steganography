import cv2
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import os

class SteganographyDecryptApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Steganography Decryption Tool")
        self.root.geometry("800x600")
        self.root.configure(bg="#f0f0f0")
        
        # Variables
        self.image_path = None
        self.image_display = None
        
        # Create frames
        self.top_frame = tk.Frame(root, bg="#f0f0f0")
        self.top_frame.pack(fill=tk.X, padx=20, pady=10)
        
        self.image_frame = tk.Frame(root, bg="#f0f0f0")
        self.image_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        self.password_frame = tk.Frame(root, bg="#f0f0f0")
        self.password_frame.pack(fill=tk.X, padx=20, pady=10)
        
        self.message_frame = tk.Frame(root, bg="#f0f0f0")
        self.message_frame.pack(fill=tk.X, padx=20, pady=10)
        
        self.button_frame = tk.Frame(root, bg="#f0f0f0")
        self.button_frame.pack(fill=tk.X, padx=20, pady=20)
        
        # Top frame content
        self.title_label = tk.Label(self.top_frame, text="Image Steganography Decryption", 
                                   font=("Arial", 16, "bold"), bg="#f0f0f0")
        self.title_label.pack(side=tk.LEFT, pady=10)
        
        # Image frame content
        self.image_label = tk.Label(self.image_frame, text="No Image Selected", 
                                   bg="#e0e0e0", height=15)
        self.image_label.pack(fill=tk.BOTH, expand=True)
        
        # Password frame content
        self.password_label = tk.Label(self.password_frame, text="Passcode:", 
                                     font=("Arial", 12), bg="#f0f0f0")
        self.password_label.pack(side=tk.LEFT, padx=5, pady=5)
        
        self.password_entry = tk.Entry(self.password_frame, width=30, 
                                     font=("Arial", 10), show="*")
        self.password_entry.pack(side=tk.LEFT, padx=5, pady=5)
        
        # Message frame content
        self.message_label = tk.Label(self.message_frame, text="Decrypted Message:", 
                                    font=("Arial", 12), bg="#f0f0f0")
        self.message_label.pack(side=tk.LEFT, padx=5, pady=5)
        
        self.message_text = tk.Text(self.message_frame, height=5, width=50, 
                                  font=("Arial", 10), state=tk.DISABLED)
        self.message_text.pack(side=tk.LEFT, padx=5, pady=5, fill=tk.X, expand=True)
        
        # Button frame content
        self.browse_button = tk.Button(self.button_frame, text="Browse Image", 
                                     command=self.browse_image, width=15,
                                     font=("Arial", 10), bg="#4CAF50", fg="white")
        self.browse_button.pack(side=tk.LEFT, padx=5, pady=5)
        
        self.decrypt_button = tk.Button(self.button_frame, text="Decrypt", 
                                      command=self.decrypt_message, width=15,
                                      font=("Arial", 10), bg="#2196F3", fg="white")
        self.decrypt_button.pack(side=tk.LEFT, padx=5, pady=5)
        
        self.copy_button = tk.Button(self.button_frame, text="Copy Message", 
                                   command=self.copy_message, width=15,
                                   font=("Arial", 10), bg="#FFC107", fg="white")
        self.copy_button.pack(side=tk.LEFT, padx=5, pady=5)
        
        self.reset_button = tk.Button(self.button_frame, text="Reset", 
                                    command=self.reset_app, width=15,
                                    font=("Arial", 10), bg="#f44336", fg="white")
        self.reset_button.pack(side=tk.LEFT, padx=5, pady=5)
        
        self.status_label = tk.Label(root, text="Ready", bd=1, relief=tk.SUNKEN, 
                                   anchor=tk.W, bg="#f0f0f0")
        self.status_label.pack(side=tk.BOTTOM, fill=tk.X)
    
    def browse_image(self):
        self.image_path = filedialog.askopenfilename(
            title="Select Encrypted Image", 
            filetypes=[("Image files", "*.jpg;*.jpeg;*.png;*.bmp")]
        )
        
        if self.image_path:
            self.status_label.config(text=f"Image selected: {os.path.basename(self.image_path)}")
            self.display_image(self.image_path)
    
    def display_image(self, path):
        # Open and resize image for display
        img = Image.open(path)
        img = img.resize((400, 300), Image.LANCZOS)
        photo = ImageTk.PhotoImage(img)
        
        # Update image display
        self.image_display = photo
        self.image_label.config(image=photo, text="")
    
    def decrypt_message(self):
        if not self.image_path:
            messagebox.showerror("Error", "Please select an encrypted image first!")
            return
        
        password = self.password_entry.get()
        if not password:
            messagebox.showerror("Error", "Please enter a passcode!")
            return
        
        try:
            # Read the image
            img = cv2.imread(self.image_path)
            height, width, _ = img.shape
            
            # Create dictionary for ASCII-to-character mapping
            c = {}
            for i in range(255):
                c[i] = chr(i)
            
            # Extract message length (first 4 pixels)
            msg_len = 0
            for i in range(4):
                msg_len |= (img[0, i, 0] << (i * 8))
            
            # Extract password length (next pixel)
            pwd_len = img[0, 4, 0]
            
            # Check if the message length seems valid
            if msg_len <= 0 or msg_len > (height * width):
                messagebox.showerror("Error", "This image does not appear to contain a hidden message or the message is corrupted!")
                return
            
            # Extract the embedded password
            extracted_pwd = ""
            n_pwd, m_pwd, z_pwd = height - 1, width - 1, 0
            for i in range(pwd_len):
                if n_pwd < 0 or m_pwd < 0 or n_pwd >= height or m_pwd >= width:
                    messagebox.showerror("Error", "Password extraction failed. Image may be corrupted.")
                    return
                
                pixel_value = img[n_pwd, m_pwd, z_pwd]
                if pixel_value < 0 or pixel_value > 254:
                    pixel_value = 32  # Default to space if value is out of range
                
                extracted_pwd += c[pixel_value]
                n_pwd -= 1
                if n_pwd < 0:
                    n_pwd = height - 1
                    m_pwd -= 1
                    if m_pwd < 0:
                        z_pwd = (z_pwd + 1) % 3
                        m_pwd = width - 1
            
            # Verify password
            if password != extracted_pwd:
                messagebox.showerror("Error", "Incorrect passcode!")
                return
            
            # Extract the message
            message = ""
            n, m, z = 0, 0, 0
            
            # Skip the header pixels that store the metadata
            n = 5
            
            # Extract exactly the number of characters specified in msg_len
            for i in range(msg_len):
                if n >= height or m >= width:
                    break
                
                pixel_value = img[n, m, z]
                if 0 <= pixel_value <= 254:  # Ensure value is in valid ASCII range
                    message += c[pixel_value]
                
                n += 1
                if n >= height:
                    n = 0
                    m += 1
                    if m >= width:
                        z = (z + 1) % 3
                        m = 0
            
            # Display the message
            self.message_text.config(state=tk.NORMAL)
            self.message_text.delete("1.0", tk.END)
            self.message_text.insert(tk.END, message)
            self.message_text.config(state=tk.DISABLED)
            
            self.status_label.config(text="Message decrypted successfully!")
            
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
    
    def copy_message(self):
        message = self.message_text.get("1.0", tk.END).strip()
        if message:
            self.root.clipboard_clear()
            self.root.clipboard_append(message)
            self.status_label.config(text="Message copied to clipboard!")
        else:
            messagebox.showinfo("Info", "No message to copy!")
    
    def reset_app(self):
        self.image_path = None
        self.image_label.config(image="", text="No Image Selected")
        self.password_entry.delete(0, tk.END)
        self.message_text.config(state=tk.NORMAL)
        self.message_text.delete("1.0", tk.END)
        self.message_text.config(state=tk.DISABLED)
        self.status_label.config(text="Ready")

if __name__ == "__main__":
    root = tk.Tk()
    app = SteganographyDecryptApp(root)
    root.mainloop()