import sqlite3
ket_noi=sqlite3.connect("kho_hang.db")
con_tro=ket_noi.cursor()
con_tro.execute("""
CREATE TABLE IF NOT EXISTS san_pham(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    san_pham TEXT,
    gia REAL
)
""")
ket_noi.commit()

while True:
    print("\n---PHẦN MỀN QUẢN LÝ KHO HÀNG---")
    print("1. Xem danh sách sản phẩm")
    print("2. Thêm sản phẩm mới")
    print("3. Cập nhật giá sản phẩm")
    print("4. Xóa sản phẩm")
    print("5. Thoát phần mềm")

    lua_chon=input("Mời bạn chọn chức năng (1-5) :")
    if lua_chon=="1":
        print("\n---DANH SÁCH SẢN PHẨM TRONG KHO---")
        con_tro.execute("SELECT * FROM san_pham")
        tat_ca_hang=con_tro.fetchall()
        if len(tat_ca_hang)==0:
            print("Kho hàng hiện đang trống rỗng!")
        else:
            for hang in tat_ca_hang:
                print(f"ID: {hang[0]} | Tên: {hang[1]} | Giá: {hang[2]}đ")
    elif lua_chon=="2":
        print("\n---Thêm sản phẩm mới---")
        ten=input("Nhập tên sản phẩm muốn thêm :")
        gia=float(input("Nhập giá sản phẩm :"))
        con_tro.execute("INSERT INTO san_pham(ten_sp,gia) VALUES(?,?)",(ten,gia))
        ket_noi.commit()
        print(f"Đã thêm thành công sản phẩm '{ten}' vào kho!")
    elif lua_chon=="3":
        print("\n---Cập nhật giá sản phẩm---")
        id_sua=int(input("Nhập id sản phẩm muốn sửa giá:"))
        gia_moi=float(input("Nhập mức giá mới :"))
        con_tro.execute("UPDATE san_pham SET gia=? WHERE id= ?",(gia_moi,id_sua))
        ket_noi.commit
        print(f"Đã cập nhật giá mới cho sản phẩm ID số {id_sua} thành công!")
    elif lua_chon=="4":
        print("\n---Xóa sản phẩm khỏi kho---")
        id_xoa=int(input("Nhập ID sản phẩm muốn xóa :"))
        con_tro.execute("DELETE FROM san_pham WHERE id=?",(id_xoa,))
        ket_noi.commit
        print(f"Đã xóa hoàn toàn sản phẩm ID số {id_xoa} ra khỏi kho hàng")
    elif lua_chon=="5":
        print("---Cảm ơn bạn đã sử dụng phần mềm. Tạm biệt---")
        break
    else :
        print("Lựa chọn không hợp lệ , mời bạn bấm từ 1 đến 5 !")

ket_noi.close()
