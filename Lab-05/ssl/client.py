import socket
import ssl
import threading

# Thông tin server
server_address = ('localhost', 12345)

def receive_data(ssl_socket):
    try:
        while True:
            data = ssl_socket.recv(1024)
            if not data:
                break
            print("Nhận:", data.decode('utf-8'))
    except Exception as e:
        print(f"Lỗi khi nhận dữ liệu: {e}")  # In ra lỗi để debug
    finally:
        ssl_socket.close()
        print("Kết nối đã đóng.")

# Tạo socket client
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Tạo SSL context
context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
context.check_hostname = False  # Không kiểm tra hostname
context.verify_mode = ssl.CERT_NONE  # Không yêu cầu chứng chỉ

# Thiết lập kết nối SSL
try:
    ssl_socket = context.wrap_socket(client_socket, server_hostname='localhost')
    ssl_socket.connect(server_address)
    print("Đã kết nối đến server.")
except Exception as e:
    print(f"Lỗi khi kết nối đến server: {e}")
    client_socket.close()
    exit()

# Bắt đầu một luồng để nhận dữ liệu từ server
receive_thread = threading.Thread(target=receive_data, args=(ssl_socket,), daemon=True)
receive_thread.start()

# Gửi dữ liệu lên server
try:
    while True:
        message = input("Nhập tin nhắn: ").strip()
        if message:
            ssl_socket.sendall(message.encode('utf-8'))
except KeyboardInterrupt:
    print("Ngắt kết nối bởi người dùng.")
finally:
    ssl_socket.close()
    print("Đã đóng kết nối với server.")
