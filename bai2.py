tong_tien = 600000

if tong_tien > 500000:
    print('Bạn được miễn phí giao hàng')
    phi_ship = 0
else:
    print('Bạn tốn phí giao hàng nhé') 
    phi_ship = 30000

print('Số tiền ship của bạn là:', phi_ship)
