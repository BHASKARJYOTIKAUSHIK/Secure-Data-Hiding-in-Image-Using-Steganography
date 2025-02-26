import cv2
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import os

class SteganographyEncryptApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Steganography Encryption Tool")
        self.root.geometry("800x600")
        self.root.configure(bg="#f0f0f0")
        
        # Variables
        self.image_path = None
        self.image_display = None
        self.encrypted_path = None
        
        # Create frames
        self.top_frame = tk.Frame(root, bg="#f0f0f0")
        self.top_frame.pack(fill=tk.X, padx=20, pady=10)
        
        self.image_frame = tk.Frame(root, bg="#f0f0f0")
        self.image_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        self.message_frame = tk.Frame(root, bg="#f0f0f0")
        self.message_frame.pack(fill=tk.X, padx=20, pady=10)
        
        self.password_frame = tk.Frame(root, bg="#f0f0f0")
        self.password_frame.pack(fill=tk.X, padx=20, pady=10)
        
        self.button_frame = tk.Frame(root, bg="#f0f0f0")
        self.button_frame.pack(fill=tk.X, padx=20, pady=20)
        
        # Top frame content
        self.title_label = tk.Label(self.top_frame, text="Image Steganography Encryption", 
                                   font=("Arial", 16, "bold"), bg="#f0f0f0")
        self.title_label.pack(side=tk.LEFT, pady=10)
        
        # Image frame content
        self.image_label = tk.Label(self.image_frame, text="No Image Selected", 
                                   bg="#e0e0e0", height=15)
        self.image_label.pack(fill=tk.BOTH, expand=True)
        
        # Message frame content
        self.message_label = tk.Label(self.message_frame, text="Secret Message:", 
                                    font=("Arial", 12), bg="#f0f0f0")
        self.message_label.pack(side=tk.LEFT, padx=5, pady=5)
        
        self.message_entry = tk.Text(self.message_frame, height=3, width=50, 
                                   font=("Arial", 10))
        self.message_entry.pack(side=tk.LEFT, padx=5, pady=5, fill=tk.X, expand=True)
        
        # Password frame content
        self.password_label = tk.Label(self.password_frame, text="Passcode:", 
                                     font=("Arial", 12), bg="#f0f0f0")
        self.password_label.pack(side=tk.LEFT, padx=5, pady=5)
        
        self.password_entry = tk.Entry(self.password_frame, width=30, 
                                     font=("Arial", 10), show="*")
        self.password_entry.pack(side=tk.LEFT, padx=5, pady=5)
        
        # Button frame content
        self.browse_button = tk.Button(self.button_frame, text="Browse Image", 
                                     command=self.browse_image, width=15,
                                     font=("Arial", 10), bg="#4CAF50", fg="white")
        self.browse_button.pack(side=tk.LEFT, padx=5, pady=5)
        
        self.encrypt_button = tk.Button(self.button_frame, text="Encrypt", 
                                      command=self.encrypt_message, width=15,
                                      font=("Arial", 10), bg="#2196F3", fg="white")
        self.encrypt_button.pack(side=tk.LEFT, padx=5, pady=5)
        
        self.reset_button = tk.Button(self.button_frame, text="Reset", 
                                    command=self.reset_app, width=15,
                                    font=("Arial", 10), bg="#f44336", fg="white")
        self.reset_button.pack(side=tk.LEFT, padx=5, pady=5)
        
        self.status_label = tk.Label(root, text="Ready", bd=1, relief=tk.SUNKEN, 
                                   anchor=tk.W, bg="#f0f0f0")
        self.status_label.pack(side=tk.BOTTOM, fill=tk.X)
    
    def browse_image(self):
        self.image_path = filedialog.askopenfilename(
            title="Select Image", 
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
    
    def encrypt_message(self):
        if not self.image_path:
            messagebox.showerror("Error", "Please select an image first!")
            return
        
        msg = self.message_entry.get("1.0", tk.END).strip()
        if not msg:
            messagebox.showerror("Error", "Please enter a secret message!")
            return
        
        password = self.password_entry.get()
        if not password:
            messagebox.showerror("Error", "Please enter a passcode!")
            return
        
        try:
            # Read the image
            img = cv2.imread(self.image_path)
            height, width, _ = img.shape
            
            # Check if the image can hold the message
            max_bytes = height * width * 3 // 8  # Each pixel can store 3 bytes (RGB)
            if len(msg) + len(password) + 10 > max_bytes:  # +10 for metadata
                messagebox.showerror("Error", "Message too long for this image!")
                return
            
            # Create dictionaries for character-to-ASCII mapping
            d = {}
            for i in range(255):
                d[chr(i)] = i
            
            # Initialize variables for embedding
            n, m, z = 0, 0, 0
            
            # Store message length in first 4 pixels (32 bits) to properly terminate during decryption
            msg_len = len(msg)
            for i in range(4):
                img[0, i, 0] = (msg_len >> (i * 8)) & 0xFF
            
            # Store password length (next pixel)
            pwd_len = len(password)
            img[0, 4, 0] = pwd_len
            
            # Start embedding after the header (5 pixels used for metadata)
            n = 5
            
            # Embed the message
            for i in range(len(msg)):
                # Ensure valid index
                if n >= height:
                    n = 0
                    m += 1
                    if m >= width:
                        z = (z + 1) % 3
                        m = 0
                
                # Get ASCII value of character, bound to valid range
                char_val = ord(msg[i]) if ord(msg[i]) < 255 else 32
                img[n, m, z] = char_val
                
                n += 1
            
            # Embed the password (at the end of the image for security)
            n_pwd, m_pwd, z_pwd = height - 1, width - 1, 0
            for i in range(len(password)):
                # Ensure valid index
                if n_pwd < 0:
                    n_pwd = height - 1
                    m_pwd -= 1
                    if m_pwd < 0:
                        z_pwd = (z_pwd + 1) % 3
                        m_pwd = width - 1
                
                # Get ASCII value of character, bound to valid range
                char_val = ord(password[i]) if ord(password[i]) < 255 else 32
                img[n_pwd, m_pwd, z_pwd] = char_val
                
                n_pwd -= 1
            
            # Save the encrypted image
            file_name = os.path.splitext(os.path.basename(self.image_path))[0]
            self.encrypted_path = os.path.join(os.path.dirname(self.image_path), 
                                             f"{file_name}_encrypted.png")
            cv2.imwrite(self.encrypted_path, img)
            
            messagebox.showinfo("Success", f"Message encrypted successfully!\nSaved as: {os.path.basename(self.encrypted_path)}")
            self.status_label.config(text=f"Encrypted image saved: {os.path.basename(self.encrypted_path)}")
            
            # Show the encrypted image
            self.display_image(self.encrypted_path)
            
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
    
    def reset_app(self):
        self.image_path = None
        self.encrypted_path = None
        self.image_label.config(image="", text="No Image Selected")
        self.message_entry.delete("1.0", tk.END)
        self.password_entry.delete(0, tk.END)
        self.status_label.config(text="Ready")

if __name__ == "__main__":
    root = tk.Tk()
    app = SteganographyEncryptApp(root)
    root.mainloop()