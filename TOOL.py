import cloudscraper
from playwright.sync_api import sync_playwright
import time

class TOOL:

    def __init__(self):
        self.httpx = cloudscraper.create_scraper()
        self.cookies = {}
        self.url_get_jobs = {
            0: "https://tuongtaccheo.com/kiemtien/likepostvipcheo/getpost.php",
            1: "https://tuongtaccheo.com/kiemtien/likepostvipre/getpost.php",
            2: "https://tuongtaccheo.com/kiemtien/camxucvipcheo/getpost.php",
            3: "https://tuongtaccheo.com/kiemtien/camxucvipre/getpost.php",
            4: "https://tuongtaccheo.com/kiemtien/cmtcheo/getpost.php",
            5: "https://tuongtaccheo.com/kiemtien/subcheo/getpost.php",
            6: "https://tuongtaccheo.com/kiemtien/likepagecheo/getpost.php",
        }
        self.url_get_coin = {
            0: "https://tuongtaccheo.com/kiemtien/likepostvipcheo/nhantien.php",
            1: "https://tuongtaccheo.com/kiemtien/likepostvipre/nhantien.php",
            2: "https://tuongtaccheo.com/kiemtien/camxucvipcheo/nhantien.php",
            3: "https://tuongtaccheo.com/kiemtien/camxucvipre/nhantien.php",
            4: "https://tuongtaccheo.com/kiemtien/cmtcheo/nhantien.php",
            5: "https://tuongtaccheo.com/kiemtien/subcheo/nhantien.php",
            6: "https://tuongtaccheo.com/kiemtien/likepagecheo/nhantien.php",
        }

    def get_info(self,token,log = print):
        header = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
        }
        data = {
            "access_token": token,
        }
        respose = self.httpx.post(f"https://tuongtaccheo.com/logintoken.php",data=data, headers=header, timeout=10)
        try:
            data = respose.json()
            user = data["data"]["user"]
            coin = data["data"]["sodu"]
            log("Login thành công!")
            log(f"Token: {token} | User: {user} | Coin: {coin}")
            self.cookies[token] = respose.headers["Set-Cookie"].split(";")[0]
        except:
            log(f"Token không hợp lệ: {token}")

    def dat_nick(self, token, uid, log=print):
        try:
            log(f"UID: {uid} | Token: {token}")
            respone = self.httpx.get(f"https://tuongtaccheo.com/cauhinh/datnick.php", headers={
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
                "Cookie": self.cookies.get(token, "")

            },data={
                "iddat[]": f"{uid}",
                "loai":"fb"
            }, timeout=10)
        except:
            log(f"Lỗi kết nối khi đặt nick: {uid} | Token: {token}")

    def auto_like(self,page, token, mail,jobs,a, stop=False, log=print):
        for i in range(len(jobs)):
            id = jobs[i]["idpost"]
            link = jobs[i]["link"]
            try:
                page.goto(link, wait_until="load")
                page.wait_for_timeout(10000)
                page.evaluate("window.scrollBy({ top: 150, behavior: 'smooth' })")
                page.wait_for_timeout(1000)
                page.get_by_role("button", name="Thích", exact=True).nth(0).hover(force=True,timeout=5000)
                page.get_by_role("button", name="Thích", exact=True).nth(0).click(force=True,timeout=5000)
                time.sleep(3)
                response = self.httpx.post(f"{self.url_get_coin[a]}", headers={
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
                    "Cookie": self.cookies.get(token, ""),
                    'x-requested-with':"XMLHttpRequest",
                    "content-type": "application/x-www-form-urlencoded"
                }, data={
                    "id": id,
                }, timeout=10).json()
                
                if "Thành công" in response["mess"]:
                    coin = response["mess"].split("cộng ")[1].split(" ")[0]
                    log(f"[{mail}][LIKE][{id}][+{coin}XU]")

            except Exception as e:
                
                continue

    def auto_CX(self,page, token, mail,jobs,a, stop=False, log=print):
        for i in range(len(jobs)):
            id = jobs[i]["idpost"]
            link = jobs[i]["link"]
            loai = jobs[i]["loaicx"]
            try:
                page.goto(link, wait_until="load")
                page.wait_for_timeout(10000)
                
                page.get_by_role("button", name="Thích", exact=True).nth(0).hover(force=True,timeout=5000)
                # Hover vào nút Like để mở menu cảm xúc
                if loai == "LOVE":
                    reaction = page.get_by_role("button", name="Yêu thích",exact = True).click(force=True,timeout=10000)
                elif loai == "WOW":
                    reaction = page.get_by_role("button", name="Wow",exact = True).click(force=True,timeout=10000)
                elif loai == "HAHA":
                    reaction = page.get_by_role("button", name="Haha",exact = True).click(force=True,timeout=10000)
                elif loai == "SAD":
                    reaction = page.get_by_role("button", name="Buồn",exact = True).click(force=True,timeout=10000)
                elif loai == "ANGRY":
                    reaction = page.get_by_role("button", name="Phẫn nộ",exact = True).click(force=True,timeout=10000)
                elif loai == "CARE":
                    reaction = page.get_by_role("button", name="Thương thương",exact = True).nth(0).click(force=True,timeout=10000)

                time.sleep(3)
                response = self.httpx.post(f"{self.url_get_coin[a]}", headers={
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
                    "Cookie": self.cookies.get(token, ""),
                    'x-requested-with':"XMLHttpRequest",
                    "content-type": "application/x-www-form-urlencoded"
                }, data={
                    "id": id,
                    "loaicx": loai
                }, timeout=10).json()
                

                if "Thành công" in response["mess"]:
                    coin = response["mess"].split("cộng ")[1].split(" ")[0]
                    log(f"[{mail}][{loai}][{id}][+{coin}XU]")

            except Exception as e:
                
                continue

    def auto_CMT(self,page, token, mail,jobs,a, stop=False, log=print):
        for i in range(len(jobs)):
            id = jobs[i]["idpost"]
            link = jobs[i]["link"]
            type = jobs[i]["nd"]
            text = type.split('"')[1].split('"')[0]
            try:
                page.goto(link, wait_until="load")
                page.wait_for_timeout(10000)
                
                page.evaluate("window.scrollBy({ top: 150, behavior: 'smooth' })")
                page.wait_for_timeout(1000)
                comment_button = page.get_by_role("button", name="Viết bình luận")
                comment_button.nth(0).click()
                page.wait_for_timeout(3000)
                comment_box = page.get_by_role("textbox", name="Viết bình luận")
                comment_box.nth(0).click()
                comment_box.nth(0).type(f"{text}", delay=180)  # delay để mô phỏng gõ tay
                comment_box.nth(0).press("Enter")
                time.sleep(3)
                response = self.httpx.post(f"{self.url_get_coin[a]}", headers={
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
                    "Cookie": self.cookies.get(token, ""),
                    'x-requested-with':"XMLHttpRequest",
                    "content-type": "application/x-www-form-urlencoded"
                }, data={
                    "id": id,
                }, timeout=10).json()
                
                if "Thành công" in response["mess"]:
                    coin = response["mess"].split("cộng ")[1].split(" ")[0]
                    log(f"[{mail}][CMT][{id}][+{coin}XU]")

            except Exception as e:
                
                continue
    
    def auto_sub(self,page, token, mail,jobs,a, stop=False, log=print):
        for i in range(len(jobs)):
            id = jobs[i]["idpost"]
            link = jobs[i]["link"]
            try:
                page.goto(link, wait_until="load")
                page.wait_for_timeout(10000)
                page.evaluate("window.scrollBy({ top: 150, behavior: 'smooth' })")
                page.wait_for_timeout(1000)
                
                try:
                    button_follow = page.get_by_role("button", name="Theo dõi")
                    button_follow.nth(0).click(timeout=5000)
                except:
                    menu = page.get_by_role("button", name="Xem thêm tùy chọn trong phần cài đặt trang cá nhân")
                    menu.nth(0).click(timeout=5000)
                    page.wait_for_timeout(5000)
                    page.get_by_role("menuitem").filter(has_text="Theo dõi").click(tineout=10000)
                time.sleep(3)
                response = self.httpx.post(f"{self.url_get_coin[a]}", headers={
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
                    "Cookie": self.cookies.get(token, ""),
                    'x-requested-with':"XMLHttpRequest",
                    "content-type": "application/x-www-form-urlencoded"
                }, data={
                    "id": id,
                }, timeout=10).json()
                
                if "Thành công" in response["mess"]:
                    coin = response["mess"].split("cộng ")[1].split(" ")[0]
                    log(f"[{mail}][SUB][{id}][+{coin}XU]")

            except Exception as e:
                
                continue

    def auto_LIKE_PAGE(self,page, token, mail,jobs,a, stop=False, log=print):
        for i in range(len(jobs)):
            id = jobs[i]["idpost"]
            link = jobs[i]["link"]
            try:
                page.goto(link, wait_until="load")
                page.wait_for_timeout(10000)
                page.evaluate("window.scrollBy({ top: 150, behavior: 'smooth' })")
                page.wait_for_timeout(1000)
                
                try:
                    button_follow = page.get_by_role("button", name="Like")
                    button_follow.nth(0).click(timeout=5000)
                except:
                    menu = page.get_by_role("button", name="Xem thêm tùy chọn trong phần cài đặt trang cá nhân")
                    menu.nth(0).click(timeout=5000)
                    page.get_by_role("menuitem").filter(has_text="Like").click(tineout=5000)
                time.sleep(3)
                response = self.httpx.post(f"{self.url_get_coin[a]}", headers={
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
                    "Cookie": self.cookies.get(token, ""),
                    'x-requested-with':"XMLHttpRequest",
                    "content-type": "application/x-www-form-urlencoded"
                }, data={
                    "id": id,
                }, timeout=10).json()
                
                if "Thành công" in response["mess"]:
                    coin = response["mess"].split("cộng ")[1].split(" ")[0]
                    log(f"[{mail}][PAGE][{id}][+{coin}XU]")

            except Exception as e:
                
                continue
            
    def run(self,token, mail,proxy, stop=False, log=print):
        user_data_dir = f"./profile/{mail}"
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
            page.goto("https://www.facebook.com/", wait_until="load")

            while True:
                if stop:
                    log("🛑 Dừng tự động")
                    break
                else:
                    for i in range(7):

                        try:
                            response = self.httpx.get(self.url_get_jobs[i], headers={
                                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
                                "Cookie": self.cookies.get(token, ""),
                                'x-requested-with':"XMLHttpRequest",
                                "content-type": "application/x-www-form-urlencoded"
                            }, timeout=10)
                            if i == 0:
                                jobs = response.json()
                                self.auto_like(page,token, mail, jobs,i, stop, log)
                                if stop:
                                    log("🛑 Dừng tự động")
                                    break
                            elif i == 1:
                                jobs = response.json()
                                self.auto_like(page,token, mail, jobs,i, stop, log)
                                if stop:
                                    log("🛑 Dừng tự động")
                                    break
                            elif i == 2:
                                jobs = response.json()
                                self.auto_CX(page,token, mail, jobs,i, stop, log)
                                if stop:
                                    log("🛑 Dừng tự động")
                                    break
                            elif i == 3:
                                jobs = response.json()
                                self.auto_CX(page,token, mail, jobs,i, stop, log)
                                if stop:
                                    log("🛑 Dừng tự động")
                                    break
                            elif i == 4:
                                jobs = response.json()
                                self.auto_CMT(page,token, mail, jobs,i, stop, log)
                                if stop:
                                    log("🛑 Dừng tự động")
                                    break
                            elif i == 5:
                                jobs = response.json()
                                self.auto_sub(page,token, mail, jobs,i, stop, log)
                                if stop:
                                    log("🛑 Dừng tự động")
                                    break
                            elif i == 6:
                                jobs = response.json()
                                self.auto_LIKE_PAGE(page,token, mail, jobs,i, stop, log)
                                if stop:
                                    log("🛑 Dừng tự động")
                                    break
                        except TimeoutError:
                            print(f"Timeout khi lấy nhiệm vụ từ {self.url_get_jobs[i]}")
                            continue
                        except:
                            time.sleep(response.json()["countdown"] + 5)