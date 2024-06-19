import math
import tkinter as tk
from tkinter import messagebox, scrolledtext, filedialog
import subprocess
import platform
import winreg
import threading
from PIL import Image, ImageTk
import psutil

class SysMonitorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("sysMonitor")
        self.root.resizable(False, False)
        self.root.iconbitmap('src/sysMonitor.ico')
        
        self.is_dark_theme = False
        
        self.frame_header = tk.Frame(self.root, padx=20, pady=10)
        self.frame_header.pack(fill=tk.X)

        self.frame_left = tk.Frame(self.root, padx=20, pady=10)
        self.frame_left.pack(side=tk.LEFT, anchor=tk.S)

        self.frame_right = tk.Frame(self.root, padx=20, pady=10)
        self.frame_right.pack(side=tk.RIGHT, anchor=tk.S)

        self.logo_image = tk.PhotoImage(file='src/sysMonitor.png')
        self.label_header = tk.Label(self.frame_header, text="sysMonitor", font=("Helvetica", 16, "bold"), image=self.logo_image, compound=tk.LEFT, padx=10)
        self.label_header.pack(side=tk.LEFT)

        self.toggle_on_image = ImageTk.PhotoImage(Image.open('src/toggle_on.png').resize((40, 30)))
        self.toggle_off_image = ImageTk.PhotoImage(Image.open('src/toggle_off.png').resize((40, 30)))
        self.toggle_theme_button = tk.Button(self.frame_header, image=self.toggle_off_image, cursor="hand2", bd=0, relief=tk.FLAT, command=self.toggle_theme)
        self.toggle_theme_button.pack(side=tk.RIGHT)

        self.button_system = tk.Button(self.frame_left, text="Диагностика ОС", command=self.diagnose_system, bd=0, relief=tk.RAISED)
        self.button_system.pack(pady=5, fill=tk.X, ipadx=10, ipady=5)

        self.button_processor = tk.Button(self.frame_left, text="Информация о процессоре", command=self.diagnose_processor, bd=0, relief=tk.RAISED)
        self.button_processor.pack(pady=5, fill=tk.X, ipadx=10, ipady=5)

        self.button_memory = tk.Button(self.frame_left, text="Информация о памяти", command=self.diagnose_memory, bd=0, relief=tk.RAISED)
        self.button_memory.pack(pady=5, fill=tk.X, ipadx=10, ipady=5)

        self.button_event_log = tk.Button(self.frame_left, text="Системный журнал", command=self.diagnose_event_log, bd=0, relief=tk.RAISED)
        self.button_event_log.pack(pady=5, fill=tk.X, ipadx=10, ipady=5)

        self.button_registry = tk.Button(self.frame_left, text="Реестр", command=self.diagnose_registry, bd=0, relief=tk.RAISED)
        self.button_registry.pack(pady=5, fill=tk.X, ipadx=10, ipady=5)

        self.button_installed_apps = tk.Button(self.frame_left, text="Установленные программы", command=self.diagnose_installed_apps, bd=0, relief=tk.RAISED)
        self.button_installed_apps.pack(pady=5, fill=tk.X, ipadx=10, ipady=5)

        self.button_close = tk.Button(self.frame_left, text="Закрыть", command=self.root.quit, bg="red", fg="white", bd=0, relief=tk.RAISED)
        self.button_close.pack(pady=5, fill=tk.X, ipadx=10, ipady=5)

        self.text_output = scrolledtext.ScrolledText(self.frame_right, width=50, height=20)
        self.text_output.pack()

        self.button_save_as = tk.Button(self.frame_right, text="Сохранить", command=self.save_as, bd=0, relief=tk.RAISED)
        self.button_save_as.pack(pady=10, fill=tk.X, ipadx=10, ipady=5)

        self.apply_theme()

    def apply_theme(self):
        if self.is_dark_theme:
            self.root.configure(bg="#333333")
            self.frame_header.configure(bg="#333333")
            self.frame_left.configure(bg="#333333")
            self.frame_right.configure(bg="#333333")
            self.label_header.configure(bg="#333333", fg="#FFFFFF")
            self.button_system.configure(bg="#555555", fg="#FFFFFF", activebackground="#777777", activeforeground="#FFFFFF", relief=tk.FLAT)
            self.button_processor.configure(bg="#555555", fg="#FFFFFF", activebackground="#777777", activeforeground="#FFFFFF")
            self.button_memory.configure(bg="#555555", fg="#FFFFFF", activebackground="#777777", activeforeground="#FFFFFF")
            self.button_event_log.configure(bg="#555555", fg="#FFFFFF", activebackground="#777777", activeforeground="#FFFFFF", relief=tk.FLAT)
            self.button_registry.configure(bg="#555555", fg="#FFFFFF", activebackground="#777777", activeforeground="#FFFFFF", relief=tk.FLAT)
            self.button_installed_apps.configure(bg="#555555", fg="#FFFFFF", activebackground="#777777", activeforeground="#FFFFFF", relief=tk.FLAT)
            self.text_output.configure(bg="#555555", fg="#FFFFFF", insertbackground="#FFFFFF")
            self.button_save_as.configure(bg="#555555", fg="#FFFFFF", activebackground="#777777", activeforeground="#FFFFFF", relief=tk.FLAT)
            self.toggle_theme_button.configure(image=self.toggle_on_image, bg="#333333", relief=tk.FLAT)
        else:
            self.root.configure(bg="#FFFFFF")
            self.frame_header.configure(bg="#FFFFFF")
            self.frame_left.configure(bg="#FFFFFF")
            self.frame_right.configure(bg="#FFFFFF")
            self.label_header.configure(bg="#FFFFFF", fg="#000000")
            self.button_system.configure(bg="#DDDDDD", fg="#000000", activebackground="#BBBBBB", activeforeground="#000000", relief=tk.RAISED)
            self.button_processor.configure(bg="#DDDDDD", fg="#000000", activebackground="#BBBBBB", activeforeground="#000000")
            self.button_memory.configure(bg="#DDDDDD", fg="#000000", activebackground="#BBBBBB", activeforeground="#000000")
            self.button_event_log.configure(bg="#DDDDDD", fg="#000000", activebackground="#BBBBBB", activeforeground="#000000", relief=tk.RAISED)
            self.button_registry.configure(bg="#DDDDDD", fg="#000000", activebackground="#BBBBBB", activeforeground="#000000", relief=tk.RAISED)
            self.button_installed_apps.configure(bg="#DDDDDD", fg="#000000", activebackground="#BBBBBB", activeforeground="#000000", relief=tk.RAISED)
            self.text_output.configure(bg="#FFFFFF", fg="#000000", insertbackground="#000000")
            self.button_save_as.configure(bg="#DDDDDD", fg="#000000", activebackground="#BBBBBB", activeforeground="#000000", relief=tk.RAISED)
            self.toggle_theme_button.configure(image=self.toggle_off_image, bg="#FFFFFF", relief=tk.FLAT)

    def toggle_theme(self):
        self.is_dark_theme = not self.is_dark_theme
        self.apply_theme()

    def diagnose_system(self):
        system_info = platform.uname()
        self.text_output.delete('1.0', tk.END)
        self.text_output.insert(tk.END, f"Система: {system_info.system}\n")
        self.text_output.insert(tk.END, f"Версия: {system_info.version}\n")
        self.text_output.insert(tk.END, f"Архитектура: {system_info.machine}\n")
        self.text_output.insert(tk.END, f"Имя узла сети: {system_info.node}\n")

    def diagnose_processor(self):
        processor_info = platform.processor()
        num_cores = psutil.cpu_count(logical=False)
        num_threads = psutil.cpu_count(logical=True)
        self.text_output.delete('1.0', tk.END)
        self.text_output.insert(tk.END, f"Информация о процессоре:\n")
        self.text_output.insert(tk.END, f"Процессор: {processor_info}\n")
        self.text_output.insert(tk.END, f"Количество ядер: {num_cores}\n")
        self.text_output.insert(tk.END, f"Количество потоков: {num_threads}\n")

    def diagnose_memory(self):
        memory_info = psutil.virtual_memory()
        self.text_output.delete('1.0', tk.END)
        self.text_output.insert(tk.END, f"Информация о памяти:\n")
        self.text_output.insert(tk.END, f"Всего памяти: {self.convert_bytes(memory_info.total)}\n")
        self.text_output.insert(tk.END, f"Используется памяти: {self.convert_bytes(memory_info.used)}\n")
        self.text_output.insert(tk.END, f"Свободно памяти: {self.convert_bytes(memory_info.available)}\n")

    def convert_bytes(self, bytes):
        if bytes == 0:
            return "0 B"
        k = 1024
        sizes = ["B", "KB", "MB", "GB", "TB"]
        i = 0 if bytes == 0 else int(math.floor(math.log(bytes) / math.log(k)))
        return f"{bytes / (k ** i):.2f} {sizes[i]}"

    def diagnose_event_log(self):
        try:
            result = subprocess.run(['powershell', 'Get-WinEvent -LogName System -MaxEvents 20 | Format-Table -Wrap -AutoSize | Out-String'], capture_output=True, text=True)
            if result.returncode == 0:
                self.text_output.delete('1.0', tk.END)
                self.text_output.insert(tk.END, result.stdout)
            else:
                messagebox.showerror("Ошибка", "Не удалось получить системный журнал.")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка при выполнении команды PowerShell: {e}")

    def diagnose_registry(self):
        try:
            self.text_output.delete('1.0', tk.END)
            self.read_registry_key(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Windows NT\CurrentVersion")
            self.read_registry_key(winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка при работе с реестром: {e}")

    def read_registry_key(self, root_key, sub_key):
        self.text_output.insert(tk.END, f"Ключ реестра: {sub_key}\n")
        with winreg.OpenKey(root_key, sub_key) as key:
            try:
                i = 0
                while True:
                    name, value, type_ = winreg.EnumValue(key, i)
                    self.text_output.insert(tk.END, f"{name}: {value} (Type: {type_})\n")
                    i += 1
            except WindowsError as e:
                pass

    def diagnose_installed_apps(self):
        self.text_output.delete('1.0', tk.END)
        self.text_output.insert(tk.END, "Получение списка установленных программ...\n")

        t = threading.Thread(target=self.get_installed_apps)
        t.start()

    def get_installed_apps(self):
        try:
            result = subprocess.run(['wmic', 'product', 'get', 'name'], capture_output=True, text=True)
            if result.returncode == 0:
                self.text_output.delete('1.0', tk.END)
                self.text_output.insert(tk.END, "Установленные программы:\n")
                self.text_output.insert(tk.END, result.stdout)
            else:
                messagebox.showerror("Ошибка", "Не удалось получить список установленных программ.")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка при выполнении команды WMIC: {e}")

    def save_as(self):
        filename = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
        if filename:
            try:
                with open(filename, 'w') as f:
                    text_to_save = self.text_output.get('1.0', tk.END)
                    f.write(text_to_save)
                messagebox.showinfo("Сохранено", f"Файл сохранен как {filename}")
            except Exception as e:
                messagebox.showerror("Ошибка", f"Ошибка при сохранении файла: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = SysMonitorApp(root)
    root.mainloop()
