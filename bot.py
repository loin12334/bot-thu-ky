import requests
from bs4 import BeautifulSoup
import urllib3
import os

# Tắt cảnh báo bảo mật SSL để màn hình chạy cho sạch đẹp
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# ==========================================
# ⚙️ CẤU HÌNH BOT (ĐÃ ĐIỀN SẴN)
# ==========================================
TOKEN = "8851805191:AAEBVDJ76jilsGnIoUQDSXFlq8iJ9t8mRog"
CHAT_ID = "6381796154"
URL = "https://giaovu.ptit.edu.vn/"
FILE_LICH_SU = "lich_su_giaovu.txt"

def kiem_tra_thong_bao():
    print("⏳ Đang lên trang Giáo Vụ kiểm tra...")
    
    try:
        # 1. Tải toàn bộ mã HTML của trang web
        response = requests.get(URL, verify=False)
        response.encoding = 'utf-8' # Sửa lỗi font tiếng Việt
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 2. Tìm bài thông báo mới nhất (Bằng bộ lọc chính xác 100%)
        bai_viet = soup.select_one('.posts-gv li.item h2 a')
        
        # Kiểm tra đề phòng web bị lỗi không hiện bài
        if not bai_viet:
            print("❌ Không tìm thấy bài viết nào. Cấu trúc web có thể bị lỗi.")
            return

        tieu_de = bai_viet.text.strip()
        link_bai = bai_viet['href']
        
        print(f"👉 Thông báo trên cùng hiện tại là:\n   {tieu_de}")
        
        # 3. Đọc lịch sử xem bài này đã gửi cho sếp chưa
        bai_cu = ""
        if os.path.exists(FILE_LICH_SU):
            with open(FILE_LICH_SU, "r", encoding="utf-8") as f:
                bai_cu = f.read().strip()
        
        # 4. So sánh và Ra quyết định
        if tieu_de != bai_cu:
            print("🚨 CÓ THÔNG BÁO MỚI! Đang gọi thư ký Telegram...")
            
            # Soạn tin nhắn gửi đi
            tin_nhan = f"📣 THÔNG BÁO MỚI TỪ PHÒNG GIÁO VỤ!\n\n📌 {tieu_de}\n🔗 Xem chi tiết tại: {link_bai}"
            
            # Gọi API Telegram để bắn tin
            api_url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
            response_tg = requests.post(api_url, data={"chat_id": CHAT_ID, "text": tin_nhan})
            
            # Kiểm tra xem Telegram có báo gửi thành công không
            if response_tg.status_code == 200:
                print("✅ Đã bắn tin nhắn thành công! Mở điện thoại ra check đi sếp.")
                
                # Lưu bài này vào lịch sử để lần sau không báo trùng nữa
                with open(FILE_LICH_SU, "w", encoding="utf-8") as f:
                    f.write(tieu_de)
            else:
                print(f"❌ Telegram từ chối gửi tin! Lỗi chi tiết: {response_tg.text}")
                
        else:
            print("💤 Chưa có thông báo gì mới, đi ngủ tiếp đây.")
            
    except Exception as e:
        print("❌ Có lỗi xảy ra trong quá trình chạy:", e)

if __name__ == "__main__":
    kiem_tra_thong_bao()