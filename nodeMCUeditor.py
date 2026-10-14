import tkinter as tk
from tkinter import filedialog, messagebox
import serial.tools.list_ports
import esptool

class NodeMCUUploader:
    def __init__(self, master):
        self.master = master
        master.title("NodeMCU Uploader")
        master.geometry("400x300")

        self.device_var = tk.StringVar()
        self.device_var.set("Select Device")

        self.create_widgets()

    def create_widgets(self):
        # Device selection
        tk.Label(self.master, text="Select NodeMCU Device:").pack(pady=10)
        self.device_menu = tk.OptionMenu(self.master, self.device_var, "")
        self.device_menu.pack(pady=5)

        # Refresh button
        tk.Button(self.master, text="Refresh Devices", command=self.refresh_devices).pack(pady=5)

        # File selection
        tk.Button(self.master, text="Select File to Upload", command=self.select_file).pack(pady=10)
        self.file_label = tk.Label(self.master, text="No file selected")
        self.file_label.pack()

        # Upload button
        tk.Button(self.master, text="Upload to NodeMCU", command=self.upload_to_nodemcu).pack(pady=20)

        self.refresh_devices()

    def refresh_devices(self):
        devices = [port.device for port in serial.tools.list_ports.comports()]
        self.device_menu['menu'].delete(0, 'end')

        for device in devices:
            self.device_menu['menu'].add_command(label=device, command=tk._setit(self.device_var, device))

        if devices:
            self.device_var.set(devices[0])
        else:
            self.device_var.set("No devices found")

    def select_file(self):
        self.filename = filedialog.askopenfilename(filetypes=[("Binary files", "*.bin")])
        if self.filename:
            self.file_label.config(text=f"Selected: {self.filename}")
        else:
            self.file_label.config(text="No file selected")

    def upload_to_nodemcu(self):
        if self.device_var.get() == "No devices found" or self.device_var.get() == "Select Device":
            messagebox.showerror("Error", "No NodeMCU device selected")
            return

        if not hasattr(self, 'filename') or not self.filename:
            messagebox.showerror("Error", "No file selected for upload")
            return

        try:
            # Initialize esptool
            esp = esptool.ESP8266ROM(self.device_var.get(), 115200)
            esp.connect()

            # Erase flash
            esptool.erase_flash(esp, None)

            # Write new firmware
            esptool.write_flash(esp, 0, self.filename)

            messagebox.showinfo("Success", "Firmware uploaded successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Upload failed: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = NodeMCUUploader(root)
    root.mainloop()