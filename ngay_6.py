with open("danh_sach_lop.txt",mode="w",encoding="utf-8") as file:
    file.write("abc.\n")
    file.write("cdf.\n")
    file.write("zxc")
with open("danh_sach_lop.txt",mode="r",encoding="utf-8") as file:
    noi_dung=file.read()
print("Nội dung file đc đọc là :")
print(noi_dung)

import json
gio_hang=[
    {"ten_sp":"Iphone","gia":20000,"so_luong":1},
    {"ten_sp":"Ốp lưng","gia":500,"so_luong":2}
]
with open("gio_hang.json",mode="w",encoding="utf-8") as file:
    json.dump(gio_hang,file,ensure_ascii=False,indent=4)

import json
with open("gio_hang.json",mode="r",encoding="utf-8")as file:
    gio_hang_doc_duoc=json.load(file)
for i in gio_hang_doc_duoc:
    print("Tên sản phẩm đọc từ file là :",i["ten_sp"])
       
