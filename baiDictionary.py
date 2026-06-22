san_pham = {
    "ten_sp" : "Điện thoại iphone",
    "gia" : 20000,
    "so_luong" : 5
}
print(san_pham["ten_sp"])
print(san_pham)
san_pham["so_luong"] = 7
for k,v in san_pham.items():
    print(k,"là",v)
tong_tien=san_pham["gia"]*san_pham["so_luong"]
print(tong_tien)

gio_hang = [
    {"ten_sp":"Iphone","gia":20000,"so_luong":1},
    {"ten_sp":"Ốp lưng","gia":500,"so_luong":2},
    {"ten_sp":"Sạc dự phòng","gia":1200,"so_luong":1}
]
tong_hoa_don=0
for i in gio_hang:
    tong_hoa_don += i["gia"]*i["so_luong"]
print(tong_hoa_don)
    


def tinh_tien_gio_hang(danh_sach_mua_hang):
    tong_hoa_don = 0
    for sp in danh_sach_mua_hang:
        tong_hoa_don += sp["gia"]*sp["so_luong"]
    return tong_hoa_don
gio_hang = [
    {"ten_sp":"Iphone","gia":20000,"so_luong":1},
    {"ten_sp":"Ốp lưng","gia":500,"so_luong":2},
    {"ten_sp":"Sạc dự phòng","gia":1200,"so_luong":1}
]
tong_hoa_don = tinh_tien_gio_hang(gio_hang)
print("Bạn phải thanh toán :",tong_hoa_don)