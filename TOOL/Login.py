from playwright.sync_api import sync_playwright

class Login:

    def __init__(self):

        pass

    def login(self, mail, password,proxy):

        if not proxy:
            data_proxy = {}
        else:
            ip, port, user, passwd = proxy.split(":")
            data_proxy = {
                "server": f"http://{ip}:{port}",
                "username": user,
                "password": passwd
            }

        with sync_playwright() as p:

            user_data_dir = f'./profile/{mail}'

            browser = p.chromium.launch_persistent_context(
                user_data_dir,channel="chrome",
                headless=False,
                proxy=data_proxy,
                args=["--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
                ,"--no-sandbox",
                "--disable-setuid-sandbox",
                "--disable-blink-features=AutomationControlled",
                      "--window-size=500,500"]
            )
            page = browser.pages[0] if browser.pages else browser.new_page()
            page.set_viewport_size({"width": 500, "height": 500})
            page.goto("https://www.facebook.com/", wait_until="networkidle")

            # Đợi và nhập email
            page.wait_for_selector("input[name='email']")
            page.type("input[name='email']", mail,delay=100)

            # Nhập mật khẩu
            page.type("input[name='pass']", password,delay=100)

            # Click nút đăng nhập
            page.click("button[name='login']")
            input("Please log in to your Facebook account and then press Enter...")

            
    def run(self):
        mail = input("Enter your email: ")
        password = input("Enter your password: ")
        proxy = input("Enter your proxy (ip:port:user:password) or leave empty for no proxy: ")
        self.login(mail, password, proxy)

if __name__ == "__main__":
    login_instance = Login()
    login_instance.run()