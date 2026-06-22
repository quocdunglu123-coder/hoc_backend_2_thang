diem_so = [8,5,10,7,9,4]
tong_diem = 0
for x in diem_so:
    tong_diem += x
diem_trung_binh = tong_diem / len(diem_so)
print("Điểm trung bình là :",diem_trung_binh)

max_diem = diem_so[0]
for x in diem_so:
    if x > max_diem:
        max_diem=x
print("Điểm cao nhất là :",max_diem)


lop_hoc_moi = [6,7,9,3,8]
def tim_diem_cao_nhat_lop(lop_hoc_moi):
    max_diem = lop_hoc_moi[0]
    for x in lop_hoc_moi:
        if x > max_diem:
            max_diem=x
    return max_diem

print("Điểm cao nhất là :",tim_diem_cao_nhat_lop(lop_hoc_moi))