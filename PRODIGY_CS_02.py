
import os
import json
import random
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk


class ImageEncryptionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Encryption And Decryption Tool")
        self.root.geometry("650x650")
        self.root.configure(bg="#1E1E1E")  # Darker theme

        self.image_label = tk.Label(self.root, text="No image selected", bg="#1E1E1E", fg="white", font=("Arial", 12))
        self.image_label.pack(pady=10)

        # Canvas for image display
        self.canvas = tk.Canvas(self.root, width=400, height=400, bg="white")
        self.canvas.pack()

        self.browse_button = tk.Button(self.root, text="Browse Image", command=self.load_image, bg="#007ACC", fg="white", font=("Arial", 12, "bold"))
        self.browse_button.pack(pady=5)

        self.encrypt_button = tk.Button(self.root, text="Encrypt & Save", command=self.encrypt_image, bg="green", fg="white", font=("Arial", 12, "bold"), state=tk.DISABLED)
        self.encrypt_button.pack(pady=5)

        self.decrypt_button = tk.Button(self.root, text="Load & Decrypt", command=self.decrypt_image, bg="red", fg="white", font=("Arial", 12, "bold"))
        self.decrypt_button.pack(pady=5)

        self.image_path = None
        self.processed_image = None

    def load_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.bmp")])
        if not file_path:
            return

        self.image_path = file_path
        self.image_label.config(text="Loaded: " + os.path.basename(file_path))

        img = Image.open(file_path)
        img.thumbnail((350, 350))
        self.display_image(img)
        self.encrypt_button.config(state=tk.NORMAL)

    def display_image(self, img):
        img_tk = ImageTk.PhotoImage(img)
        self.canvas.create_image(200, 200, image=img_tk, anchor=tk.CENTER)
        self.canvas.image = img_tk
        self.processed_image = img

    def encrypt_image(self):
        if not self.image_path:
            messagebox.showerror("Error", "Please select an image first!")
            return

        img = Image.open(self.image_path).convert('RGB')
        pixels = img.load()

        random_values = {}

        for i in range(img.width):
            for j in range(img.height):
                r, g, b = pixels[i, j]
                rand_r = random.randint(0, 255)
                rand_g = random.randint(0, 255)
                rand_b = random.randint(0, 255)

                random_values[f"{i},{j}"] = (rand_r, rand_g, rand_b)

                new_r = (r + rand_r) % 256
                new_g = (g + rand_g) % 256
                new_b = (b + rand_b) % 256

                pixels[i, j] = (new_r, new_g, new_b)

        self.display_image(img)

        save_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG Image", "*.png")])
        if save_path:
            img.save(save_path)
            key_path = os.path.splitext(save_path)[0] + ".key"
            with open(key_path, "w") as f:
                json.dump(random_values, f)
            messagebox.showinfo("Success", "Image encrypted and saved successfully!")

    def decrypt_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Encrypted Image", "*.png")])
        if not file_path:
            return

        key_path = os.path.splitext(file_path)[0] + ".key"
        if not os.path.exists(key_path):
            messagebox.showerror("Error", "Decryption key file not found! Please ensure the key file is in the same directory as the encrypted image.")
            return

        with open(key_path, "r") as f:
            random_values = json.load(f)

        img = Image.open(file_path).convert('RGB')
        pixels = img.load()

        for i in range(img.width):
            for j in range(img.height):
                r, g, b = pixels[i, j]
                rand_r, rand_g, rand_b = random_values.get(f"{i},{j}", (0, 0, 0))

                new_r = (r - rand_r) % 256
                new_g = (g - rand_g) % 256
                new_b = (b - rand_b) % 256

                pixels[i, j] = (new_r, new_g, new_b)

        self.display_image(img)
        messagebox.showinfo("Success", "Image decrypted successfully!")


if __name__ == "__main__":
    root = tk.Tk()
    app = ImageEncryptionApp(root)
    root.mainloop()
