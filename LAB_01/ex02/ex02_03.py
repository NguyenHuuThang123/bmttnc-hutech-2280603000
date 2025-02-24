#Nhập số từ người dùng
so = int(input("Nhập một số nguyên: "))
#Kiểm tra xem sos đó có phải số chẳn hay không
if so % 2 == 0:
    print(so, "là số chẳn.")
else:
    print(so, "không phải là số chẳn.")
