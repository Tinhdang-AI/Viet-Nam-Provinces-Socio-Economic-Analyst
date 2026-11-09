# Vietnam Socio-Economic Analysis (34 Provinces & Cities) 🇻🇳

Dự án phân tích dữ liệu kinh tế - xã hội của Việt Nam theo mô hình đề án sắp xếp, tinh gọn các đơn vị hành chính cấp tỉnh còn **34 tỉnh, thành phố**. Dự án cung cấp bộ dữ liệu sạch (CSV), tệp bản đồ số Geo/TopoJSON (Shape Map) và tệp báo cáo trực quan hóa hoàn chỉnh trên **Power BI Desktop**.

---

## 📌 1. Nguồn dữ liệu & Tham chiếu
- **Cơ cấu hành chính 34 tỉnh, thành phố:** Nghị quyết Quốc hội & Đề án sắp xếp đơn vị hành chính cấp tỉnh ([Wikipedia - Sáp nhập tỉnh, thành Việt Nam 2025](https://vi.wikipedia.org/wiki/S%C3%A1p_nh%E1%BA%ADp_t%E1%BB%89nh,_th%C3%A0nh_Vi%E1%BB%87t_Nam_2025)).
- **Phân vùng địa lý & kinh tế xã hội:** Bảng phân vùng 3 miền và các tiểu vùng kinh tế ([Wikipedia - List of regions of Vietnam](https://en.wikipedia.org/wiki/List_of_regions_of_Vietnam)).
- **Bản đồ số hóa (Shape Map TopoJSON):** Bản đồ số 34 đơn vị hành chính chuẩn hóa tương thích trực tiếp với Power BI Shape Map.

---

## 📂 2. Cấu trúc thư mục dự án

```text
VietNam Analyst/
│
├── data/
│   ├── raw/                                # Dữ liệu gốc ban đầu
│   │   ├── Danh sach 34 tinh thanh theo Map.xlsx
│   │   └── Map_34.json                     # TopoJSON bản đồ 34 tỉnh thành
│   │
│   └── processed/                          # Dữ liệu CSV đã qua xử lý & làm sạch
│       ├── vietnam_provinces_34_cleaned.csv# File master đầy đủ các chỉ số KT-XH
│       ├── provinces_of_vietnam.csv        # Bảng dữ liệu tỉnh (GDP, DS, Diện tích, Thu nhập, % Nộp NS)
│       ├── regions_of_vietnam.csv          # Bảng quan hệ Vùng (Region, Sub_Region, Province)
│       └── danh_sach_sap_nhap_34_tinh.csv  # Bảng đối soát chi tiết 63 tỉnh sáp nhập thành 34 tỉnh
│
├── scripts/
│   └── clean_and_build_dataset.py          # Script Python tự động làm sạch & chuẩn hóa dữ liệu
│
├── Kinh Te Xa Hoi Viet Nam.pbix                       # File báo cáo Power BI Dashboard hoàn chỉnh
├── Map_34.json                             # Bản đồ TopoJSON cho visual Shape Map
├── .gitignore                              # File cấu hình Git
└── README.md                               # Tài liệu hướng dẫn dự án
```

---

## 📊 3. Các chỉ số chính trong bộ dữ liệu (Data Dictionary)

| Cột dữ liệu | Đơn vị | Mô tả |
| :--- | :--- | :--- |
| `Provinces` | Chuỗi | Tên 34 tỉnh/thành phố sau quy hoạch sáp nhập |
| `Region` | Chuỗi | Vùng miền lớn (*Miền Bắc, Miền Trung, Miền Nam*) |
| `Sub_Region` | Chuỗi | Tiểu vùng kinh tế (*Đồng bằng sông Hồng, Trung du MN phía Bắc, Đông Nam Bộ,...*) |
| `Diện tích (km2)` | $km^2$ | Tổng diện tích tự nhiên sau sáp nhập |
| `Dân số (triệu ng)`| Triệu người | Quy mô dân số |
| `Mật độ (ng/km2)` | Người/$km^2$ | Mật độ dân số trên 1 $km^2$ diện tích đất tự nhiên |
| `GDP (Tỷ $)` | Tỷ USD | Tổng sản phẩm trên địa bàn (quy đổi tỷ giá) |
| `Thu nhap ($/ng)` | USD/người/năm | Thu nhập bình quân đầu người hàng năm |
| `% Nộp NS` | % | Tỷ lệ đóng góp / điều tiết nộp về ngân sách nhà nước |

---

## 🚀 4. Hướng dẫn sử dụng

### Chạy script làm sạch dữ liệu:
```bash
python scripts/clean_and_build_dataset.py
```

### Mở và chỉnh sửa Dashboard Power BI:
1. Mở tệp **`Kinh Te Xa Hoi Viet Nam.pbix`** bằng ứng dụng **Power BI Desktop**.
2. Khi muốn liên kết trực tiếp nguồn dữ liệu vào các file CSV sạch: chọn **Transform Data** > Trỏ source về thư mục `data/processed/`.
3. Bản đồ số `Map_34.json` đã được nhúng sẵn vào visual Shape Map trong báo cáo.

---
