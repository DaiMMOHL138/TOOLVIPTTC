import tkinter as tk
import threading
import queue
from TOOL import TOOL

class GUI:

    def __init__(self):
        self.root = tk.Tk()
        self.root.title("TTC FARM XU SIÊU VIP")
        self.root.geometry("800x600")
        self.stop_auto = False

        # Hàng đợi log để xử lý từ luồng chính
        self.log_queue = queue.Queue()
        self.root.after(100, self.process_log_queue)

    def input(self):
        tk.Label(self.root, text="NHẬP TÀI KHOẢN (TOKEN|UID|MAIL|PROXY):").pack(pady=10)
        self.entry = tk.Text(self.root, width=95, wrap="none", height=7, font=("Arial", 14))
        self.entry.pack(pady=10)
        self.entry.focus()

    def button(self):
        frame = tk.Frame(self.root)
        frame.pack(pady=15)
        tk.Button(frame, text="Bắt đầu", command=self.start).pack(side="left", padx=5)
        tk.Button(frame, text="Dừng lại", command=self.stop).pack(side="left", padx=5)
        tk.Button(frame, text="Lưu tài khoản", command=self.save_to_file).pack(side="left", padx=5)

    def save_to_file(self):
        data = self.entry.get("1.0", tk.END).strip()
        with open("tai_khoan.txt", "w", encoding="utf-8") as f:
            f.write(data)
        self.log("📁 Đã lưu vào file tai_khoan.txt")

    def read_from_file(self):
        try:
            with open("tai_khoan.txt", "r", encoding="utf-8") as f:
                data = f.read()
            self.entry.delete("1.0", tk.END)
            self.entry.insert(tk.END, data)
            self.log("📖 Đã đọc từ file tai_khoan.txt")
        except FileNotFoundError:
            self.log("⚠️ Chưa có file tai_khoan.txt")

    def set_box_log(self):
        self.log_box = tk.Text(self.root, height=15, state="disabled", bg="#f0f0f0", font=("Consolas", 12))
        self.log_box.pack(fill="both", expand=True, padx=10, pady=10)

    def log(self, message):
        self.log_queue.put(message)  # Gửi message vào hàng đợi

    def process_log_queue(self):
        try:
            while True:
                message = self.log_queue.get_nowait()
                self.log_box.config(state="normal")
                self.log_box.insert(tk.END, f"{message}\n")
                self.log_box.see(tk.END)
                self.log_box.config(state="disabled")
        except queue.Empty:
            pass
        self.root.after(100, self.process_log_queue)  # Lặp lại liên tục

    def start(self):
        self.list_token = []
        self.list_mail = []
        self.list_uid = []
        self.list_proxy = []

        text = self.entry.get("1.0", tk.END).strip()
        data = text.splitlines()

        if not text:
            self.log("⚠️ Vui lòng nhập tài khoản (token|uid|mail|proxy).")
        else:
            for line in data:
                if "|" in line:
                    parts = line.strip().split("|")
                    if len(parts) == 4:
                        token, uid, mail, proxy = parts
                        self.list_token.append(token.strip())
                        self.list_uid.append(uid.strip())
                        self.list_mail.append(mail.strip())
                        self.list_proxy.append(proxy.strip())
                        self.log(f"[RUN] Token: {token} | UID: {uid} | Mail: {mail}")
                    else:
                        self.log(f"❌ Lỗi định dạng dòng: {line}")
                else:
                    self.log(f"❌ Lỗi định dạng dòng: {line}")

        for i in range(len(self.list_token)):
            thread = threading.Thread(target=self.start_auto, args=(i,))
            thread.start()

    def start_auto(self, i):
        try:
            tool = TOOL()
            tool.get_info(self.list_token[i], log=self.log)
            tool.dat_nick(self.list_token[i], self.list_uid[i], log=self.log)
            tool.run(self.list_token[i], self.list_mail[i], self.list_proxy[i], self.stop_auto, log=self.log)
        except Exception as e:
            self.log(f"❌ Lỗi ở tài khoản {self.list_mail[i]}: {e}")

    def stop(self):
        self.stop_auto = True
        self.log("🛑 Đã gửi yêu cầu dừng các luồng!")

    def draw(self):
        self.input()
        self.button()
        self.set_box_log()
        self.read_from_file()
        self.root.mainloop()

    def run(self):
        self.draw()

if __name__ == "__main__":
    gui = GUI()
    gui.run()
