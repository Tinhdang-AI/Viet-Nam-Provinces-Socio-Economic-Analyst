"""
Pipeline trích xuất, làm sạch và chuẩn hóa dữ liệu Kinh tế - Xã hội 34 tỉnh thành Việt Nam
Nguồn tham chiếu:
- Đề án sáp nhập đơn vị hành chính cấp tỉnh 2025 (34 tỉnh thành) - Wikipedia & Nghị quyết Quốc hội
- Bảng phân vùng địa lý kinh tế xã hội Việt Nam (List of regions of Vietnam)
"""

import os
import csv
import json
import xml.etree.ElementTree as ET

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, 'data')
RAW_DIR = os.path.join(DATA_DIR, 'raw')
PROCESSED_DIR = os.path.join(DATA_DIR, 'processed')

# 1. Bảng quy hoạch sáp nhập (34 tỉnh thành mới cấu thành từ 63 tỉnh thành cũ)
# Nguồn: vi.wikipedia.org/wiki/Sáp_nhập_tỉnh,_thành_Việt_Nam_2025
MERGER_INFO = {
    # 11 đơn vị giữ nguyên hiện trạng
    'Cao Bằng': {'type': 'Tỉnh', 'old_provinces': ['Cao Bằng'], 'status': 'Giữ nguyên', 'area_km2': 6700.40, 'population': 555809, 'grdp_ty_vnd': 26450, 'budget_pct': 0.12},
    'Điện Biên': {'type': 'Tỉnh', 'old_provinces': ['Điện Biên'], 'status': 'Giữ nguyên', 'area_km2': 9539.90, 'population': 653422, 'grdp_ty_vnd': 30120, 'budget_pct': 0.10},
    'Hà Nội': {'type': 'Thành phố trực thuộc TW', 'old_provinces': ['Hà Nội'], 'status': 'Giữ nguyên', 'area_km2': 3359.82, 'population': 8718000, 'grdp_ty_vnd': 1425521, 'budget_pct': 0.42},
    'Hà Tĩnh': {'type': 'Tỉnh', 'old_provinces': ['Hà Tĩnh'], 'status': 'Giữ nguyên', 'area_km2': 5994.40, 'population': 1622901, 'grdp_ty_vnd': 110250, 'budget_pct': 0.18},
    'Lai Châu': {'type': 'Tỉnh', 'old_provinces': ['Lai Châu'], 'status': 'Giữ nguyên', 'area_km2': 9068.70, 'population': 494626, 'grdp_ty_vnd': 27500, 'budget_pct': 0.11},
    'Lạng Sơn': {'type': 'Tỉnh', 'old_provinces': ['Lạng Sơn'], 'status': 'Giữ nguyên', 'area_km2': 8310.20, 'population': 813978, 'grdp_ty_vnd': 48900, 'budget_pct': 0.15},
    'Nghệ An': {'type': 'Tỉnh', 'old_provinces': ['Nghệ An'], 'status': 'Giữ nguyên', 'area_km2': 16493.70, 'population': 3470988, 'grdp_ty_vnd': 208500, 'budget_pct': 0.16},
    'Quảng Ninh': {'type': 'Tỉnh', 'old_provinces': ['Quảng Ninh'], 'status': 'Giữ nguyên', 'area_km2': 6207.90, 'population': 1429841, 'grdp_ty_vnd': 347534, 'budget_pct': 0.35},
    'Sơn La': {'type': 'Tỉnh', 'old_provinces': ['Sơn La'], 'status': 'Giữ nguyên', 'area_km2': 14109.80, 'population': 1327430, 'grdp_ty_vnd': 73200, 'budget_pct': 0.13},
    'Thanh Hóa': {'type': 'Tỉnh', 'old_provinces': ['Thanh Hóa'], 'status': 'Giữ nguyên', 'area_km2': 11114.70, 'population': 3760650, 'grdp_ty_vnd': 316995, 'budget_pct': 0.20},
    'Thừa Thiên Huế': {'type': 'Thành phố trực thuộc TW', 'old_provinces': ['Thừa Thiên Huế'], 'status': 'Giữ nguyên', 'area_km2': 4947.10, 'population': 1236393, 'grdp_ty_vnd': 82300, 'budget_pct': 0.22},

    # 23 đơn vị hình thành sau sáp nhập
    'An Giang': {'type': 'Tỉnh', 'old_provinces': ['An Giang', 'Kiên Giang'], 'status': 'Hợp nhất', 'area_km2': 9888.91, 'population': 4952238, 'grdp_ty_vnd': 271346, 'budget_pct': 0.15},
    'Bắc Ninh': {'type': 'Tỉnh', 'old_provinces': ['Bắc Ninh', 'Bắc Giang'], 'status': 'Hợp nhất', 'area_km2': 4718.60, 'population': 3619433, 'grdp_ty_vnd': 439776, 'budget_pct': 0.32},
    'Cà Mau': {'type': 'Tỉnh', 'old_provinces': ['Cà Mau', 'Bạc Liêu'], 'status': 'Hợp nhất', 'area_km2': 7942.39, 'population': 2606672, 'grdp_ty_vnd': 138500, 'budget_pct': 0.14},
    'Cần Thơ': {'type': 'Thành phố trực thuộc TW', 'old_provinces': ['Cần Thơ', 'Hậu Giang', 'Sóc Trăng'], 'status': 'Hợp nhất', 'area_km2': 6360.83, 'population': 4199824, 'grdp_ty_vnd': 281675, 'budget_pct': 0.26},
    'Đà Nẵng': {'type': 'Thành phố trực thuộc TW', 'old_provinces': ['Đà Nẵng', 'Quảng Nam'], 'status': 'Hợp nhất', 'area_km2': 11859.59, 'population': 3065628, 'grdp_ty_vnd': 279926, 'budget_pct': 0.28},
    'Đắk Lắk': {'type': 'Tỉnh', 'old_provinces': ['Đắk Lắk', 'Phú Yên'], 'status': 'Hợp nhất', 'area_km2': 18099.80, 'population': 3849200, 'grdp_ty_vnd': 192800, 'budget_pct': 0.16},
    'Đồng Nai': {'type': 'Tỉnh', 'old_provinces': ['Đồng Nai', 'Bình Phước'], 'status': 'Hợp nhất', 'area_km2': 12737.18, 'population': 4491408, 'grdp_ty_vnd': 609176, 'budget_pct': 0.45},
    'Đồng Tháp': {'type': 'Tỉnh', 'old_provinces': ['Đồng Tháp', 'Tiền Giang'], 'status': 'Hợp nhất', 'area_km2': 5938.64, 'population': 4370046, 'grdp_ty_vnd': 228900, 'budget_pct': 0.15},
    'Gia Lai': {'type': 'Tỉnh', 'old_provinces': ['Gia Lai', 'Bình Định'], 'status': 'Hợp nhất', 'area_km2': 21580.90, 'population': 4183693, 'grdp_ty_vnd': 215400, 'budget_pct': 0.17},
    'Hải Phòng': {'type': 'Thành phố trực thuộc TW', 'old_provinces': ['Hải Phòng', 'Hải Dương'], 'status': 'Hợp nhất', 'area_km2': 3194.72, 'population': 4664124, 'grdp_ty_vnd': 658381, 'budget_pct': 0.40},
    'Hồ Chí Minh': {'type': 'Thành phố trực thuộc TW', 'old_provinces': ['Hồ Chí Minh', 'Bình Dương', 'Bà Rịa - Vũng Tàu'], 'status': 'Hợp nhất', 'area_km2': 6772.59, 'population': 14002598, 'grdp_ty_vnd': 2715782, 'budget_pct': 0.78},
    'Hưng Yên': {'type': 'Tỉnh', 'old_provinces': ['Hưng Yên', 'Thái Bình'], 'status': 'Hợp nhất', 'area_km2': 2514.81, 'population': 3567943, 'grdp_ty_vnd': 292603, 'budget_pct': 0.22},
    'Khánh Hòa': {'type': 'Tỉnh', 'old_provinces': ['Khánh Hòa', 'Ninh Thuận'], 'status': 'Hợp nhất', 'area_km2': 8555.86, 'population': 2243554, 'grdp_ty_vnd': 168400, 'budget_pct': 0.24},
    'Lai Châu': {'type': 'Tỉnh', 'old_provinces': ['Lai Châu'], 'status': 'Giữ nguyên', 'area_km2': 9068.70, 'population': 494626, 'grdp_ty_vnd': 27500, 'budget_pct': 0.11},
    'Lào Cai': {'type': 'Tỉnh', 'old_provinces': ['Lào Cai', 'Yên Bái'], 'status': 'Hợp nhất', 'area_km2': 13256.92, 'population': 1778785, 'grdp_ty_vnd': 118600, 'budget_pct': 0.14},
    'Lâm Đồng': {'type': 'Tỉnh', 'old_provinces': ['Lâm Đồng', 'Đắk Nông', 'Bình Thuận'], 'status': 'Hợp nhất', 'area_km2': 23966.49, 'population': 3872999, 'grdp_ty_vnd': 319887, 'budget_pct': 0.21},
    'Ninh Bình': {'type': 'Tỉnh', 'old_provinces': ['Ninh Bình', 'Hà Nam', 'Nam Định'], 'status': 'Hợp nhất', 'area_km2': 3942.62, 'population': 4412264, 'grdp_ty_vnd': 310282, 'budget_pct': 0.23},
    'Phú Thọ': {'type': 'Tỉnh', 'old_provinces': ['Phú Thọ', 'Vĩnh Phúc', 'Hòa Bình'], 'status': 'Hợp nhất', 'area_km2': 9361.38, 'population': 4022638, 'grdp_ty_vnd': 354580, 'budget_pct': 0.25},
    'Quảng Ngãi': {'type': 'Tỉnh', 'old_provinces': ['Quảng Ngãi', 'Kon Tum'], 'status': 'Hợp nhất', 'area_km2': 14832.55, 'population': 2161755, 'grdp_ty_vnd': 176200, 'budget_pct': 0.19},
    'Quảng Trị': {'type': 'Tỉnh', 'old_provinces': ['Quảng Trị', 'Quảng Bình'], 'status': 'Hợp nhất', 'area_km2': 12700.00, 'population': 1870845, 'grdp_ty_vnd': 105400, 'budget_pct': 0.15},
    'Tây Ninh': {'type': 'Tỉnh', 'old_provinces': ['Tây Ninh', 'Long An'], 'status': 'Hợp nhất', 'area_km2': 8536.44, 'population': 3254170, 'grdp_ty_vnd': 312466, 'budget_pct': 0.28},
    'Thái Nguyên': {'type': 'Tỉnh', 'old_provinces': ['Thái Nguyên', 'Bắc Kạn'], 'status': 'Hợp nhất', 'area_km2': 8375.21, 'population': 1799489, 'grdp_ty_vnd': 175600, 'budget_pct': 0.21},
    'Tuyên Quang': {'type': 'Tỉnh', 'old_provinces': ['Tuyên Quang', 'Hà Giang'], 'status': 'Hợp nhất', 'area_km2': 13795.50, 'population': 1865270, 'grdp_ty_vnd': 86400, 'budget_pct': 0.13},
    'Vĩnh Long': {'type': 'Tỉnh', 'old_provinces': ['Vĩnh Long', 'Bến Tre', 'Trà Vinh'], 'status': 'Hợp nhất', 'area_km2': 6296.20, 'population': 4257581, 'grdp_ty_vnd': 236800, 'budget_pct': 0.16}
}

# 2. Phân vùng Địa lý & Kinh tế - Xã hội
# Nguồn: en.wikipedia.org/wiki/List_of_regions_of_Vietnam
REGION_MAPPING = {
    # Miền Bắc
    'Cao Bằng': ('Miền Bắc', 'Trung du và miền núi phía Bắc'),
    'Điện Biên': ('Miền Bắc', 'Trung du và miền núi phía Bắc'),
    'Lai Châu': ('Miền Bắc', 'Trung du và miền núi phía Bắc'),
    'Lạng Sơn': ('Miền Bắc', 'Trung du và miền núi phía Bắc'),
    'Lào Cai': ('Miền Bắc', 'Trung du và miền núi phía Bắc'),
    'Phú Thọ': ('Miền Bắc', 'Trung du và miền núi phía Bắc'),
    'Sơn La': ('Miền Bắc', 'Trung du và miền núi phía Bắc'),
    'Thái Nguyên': ('Miền Bắc', 'Trung du và miền núi phía Bắc'),
    'Tuyên Quang': ('Miền Bắc', 'Trung du và miền núi phía Bắc'),
    
    'Hà Nội': ('Miền Bắc', 'Đồng bằng sông Hồng'),
    'Hải Phòng': ('Miền Bắc', 'Đồng bằng sông Hồng'),
    'Bắc Ninh': ('Miền Bắc', 'Đồng bằng sông Hồng'),
    'Hưng Yên': ('Miền Bắc', 'Đồng bằng sông Hồng'),
    'Ninh Bình': ('Miền Bắc', 'Đồng bằng sông Hồng'),
    'Quảng Ninh': ('Miền Bắc', 'Đồng bằng sông Hồng'),
    
    # Miền Trung
    'Thanh Hóa': ('Miền Trung', 'Bắc Trung Bộ'),
    'Nghệ An': ('Miền Trung', 'Bắc Trung Bộ'),
    'Hà Tĩnh': ('Miền Trung', 'Bắc Trung Bộ'),
    'Quảng Trị': ('Miền Trung', 'Bắc Trung Bộ'),
    'Thừa Thiên Huế': ('Miền Trung', 'Bắc Trung Bộ'),
    
    'Đà Nẵng': ('Miền Trung', 'Duyên hải Nam Trung Bộ'),
    'Quảng Ngãi': ('Miền Trung', 'Duyên hải Nam Trung Bộ'),
    'Khánh Hòa': ('Miền Trung', 'Duyên hải Nam Trung Bộ'),
    
    'Đắk Lắk': ('Miền Trung', 'Tây Nguyên'),
    'Gia Lai': ('Miền Trung', 'Tây Nguyên'),
    'Lâm Đồng': ('Miền Trung', 'Tây Nguyên'),
    
    # Miền Nam
    'Hồ Chí Minh': ('Miền Nam', 'Đông Nam Bộ'),
    'Đồng Nai': ('Miền Nam', 'Đông Nam Bộ'),
    'Tây Ninh': ('Miền Nam', 'Đông Nam Bộ'),
    
    'Cần Thơ': ('Miền Nam', 'Đồng bằng sông Cửu Long'),
    'An Giang': ('Miền Nam', 'Đồng bằng sông Cửu Long'),
    'Đồng Tháp': ('Miền Nam', 'Đồng bằng sông Cửu Long'),
    'Vĩnh Long': ('Miền Nam', 'Đồng bằng sông Cửu Long'),
    'Cà Mau': ('Miền Nam', 'Đồng bằng sông Cửu Long')
}

EXCHANGE_RATE_VND_USD = 25000.0  # 1 USD ~ 25,000 VND

def clean_and_process():
    processed_records = []
    
    for province_name, reg_info in sorted(REGION_MAPPING.items()):
        region, sub_region = reg_info
        info = MERGER_INFO.get(province_name)
        if not info:
            continue
        
        area = round(float(info['area_km2']), 2)
        pop = int(info['population'])
        pop_million = round(pop / 1_000_000.0, 3)
        density = round(pop / area, 1)
        
        grdp_ty_vnd = float(info['grdp_ty_vnd'])
        # Quy đổi ra Tỷ USD
        gdp_billion_usd = round(grdp_ty_vnd / (EXCHANGE_RATE_VND_USD / 1000.0 * 1000.0 / 1.0), 2)  # grdp_ty_vnd * 1e9 / (25000 * 1e9)
        gdp_billion_usd = round(grdp_ty_vnd / 25000.0, 2)
        
        # Thu nhập bình quân USD/người/năm: (GDP in USD) / Dân số
        income_usd_capita = round((gdp_billion_usd * 1_000_000_000.0) / pop, 1)
        budget_ratio = round(float(info['budget_pct']), 3)
        
        record = {
            'Province': province_name,
            'Region': region,
            'Sub_Region': sub_region,
            'Admin_Type': info['type'],
            'Status': info['status'],
            'Merged_Constituents': '; '.join(info['old_provinces']),
            'Area_km2': area,
            'Population': pop,
            'Population_Million': pop_million,
            'Density_Pop_per_km2': density,
            'GRDP_Billion_VND': grdp_ty_vnd,
            'GDP_Billion_USD': gdp_billion_usd,
            'Income_USD_per_capita': income_usd_capita,
            'Budget_Remittance_Rate': budget_ratio
        }
        processed_records.append(record)
    
    # 1. Lưu file chuẩn hóa tổng hợp: vietnam_provinces_34_cleaned.csv
    out_master_csv = os.path.join(PROCESSED_DIR, 'vietnam_provinces_34_cleaned.csv')
    with open(out_master_csv, 'w', encoding='utf-8-sig', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=processed_records[0].keys())
        writer.writeheader()
        writer.writerows(processed_records)
    print(f"Created: {out_master_csv}")

    # 2. Tạo file table theo đúng format của Power BI Model:
    # Table A: Provinces of Vietnam / Map_34
    pbi_provinces_csv = os.path.join(PROCESSED_DIR, 'provinces_of_vietnam.csv')
    with open(pbi_provinces_csv, 'w', encoding='utf-8-sig', newline='') as f:
        fieldnames = ['Provinces', 'Diện tích (km2)', 'Dân số (triệu ng)', 'Mật độ (ng/km2)', 'GDP (Tỷ $)', 'Thu nhap ($/ng)', '% Nộp NS']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for r in processed_records:
            writer.writerow({
                'Provinces': r['Province'],
                'Diện tích (km2)': r['Area_km2'],
                'Dân số (triệu ng)': r['Population_Million'],
                'Mật độ (ng/km2)': r['Density_Pop_per_km2'],
                'GDP (Tỷ $)': r['GDP_Billion_USD'],
                'Thu nhap ($/ng)': r['Income_USD_per_capita'],
                '% Nộp NS': r['Budget_Remittance_Rate']
            })
    print(f"Created: {pbi_provinces_csv}")

    # Table B: Regions of Vietnam
    pbi_regions_csv = os.path.join(PROCESSED_DIR, 'regions_of_vietnam.csv')
    with open(pbi_regions_csv, 'w', encoding='utf-8-sig', newline='') as f:
        fieldnames = ['Provinces', 'Sub_Region', 'Region']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for r in processed_records:
            writer.writerow({
                'Provinces': r['Province'],
                'Sub_Region': r['Sub_Region'],
                'Region': r['Region']
            })
    print(f"Created: {pbi_regions_csv}")

    # Table C: Danh sách chi tiết các tỉnh sáp nhập (Merger mapping)
    pbi_merger_csv = os.path.join(PROCESSED_DIR, 'danh_sach_sap_nhap_34_tinh.csv')
    with open(pbi_merger_csv, 'w', encoding='utf-8-sig', newline='') as f:
        fieldnames = ['STT', 'Tỉnh / Thành phố mới', 'Loại đô thị', 'Hiện trạng', 'Các tỉnh hợp nhất thành phần', 'Diện tích (km2)', 'Dân số (người)', 'Quy mô GRDP (tỷ VNĐ)']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for idx, r in enumerate(processed_records, 1):
            writer.writerow({
                'STT': idx,
                'Tỉnh / Thành phố mới': r['Province'],
                'Loại đô thị': r['Admin_Type'],
                'Hiện trạng': r['Status'],
                'Các tỉnh hợp nhất thành phần': r['Merged_Constituents'],
                'Diện tích (km2)': r['Area_km2'],
                'Dân số (người)': r['Population'],
                'Quy mô GRDP (tỷ VNĐ)': r['GRDP_Billion_VND']
            })
    print(f"Created: {pbi_merger_csv}")

if __name__ == '__main__':
    clean_and_process()
