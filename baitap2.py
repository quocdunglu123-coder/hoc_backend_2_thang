tong_ao_mua = 2
gia_goc = 250000
if tong_ao_mua >= 3:
    giam_gia = .2
    print("Số áo mua :", tong_ao_mua , "Bạn đc giăm 20%" )
else :
    giam_gia = .05
    print("Số áo mua :", tong_ao_mua , "Bạn đc giăm 5%" )
gia_da_giam = gia_goc - (gia_goc * giam_gia)
print("Bạn phải thanh toán", tong_ao_mua * gia_da_giam)

