def tinh_tong_chan(n):
    a = 0
    for i in range(1,n+1):
        if i % 2 == 0:
            a += i
    return a
so_n = 50
b = tinh_tong_chan(so_n)
print("Tổng chẳn của",so_n,"=",b)
