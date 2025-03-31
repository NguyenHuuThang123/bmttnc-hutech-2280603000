import socket
import ssl
import threading

# Thông tin server
SERVER_ADDRESS = ('localhost', 12345)
clients = []

def handle_client(client_socket):
    try:
        clients.append(client_socket)
        print("Đã kết nối với:", client_socket.getpeername())
        
        while True:
            data = client_socket.recv(1024)
            if not data:
                break
            print("Nhận:", data.decode('utf-8'))
            
            # Gửi dữ liệu đến các client khác
            for client in clients[:]:  # Sao chép danh sách để tránh lỗi khi xoá
                if client != client_socket:
                    try:
                        client.sendall(data)
                    except:
                        clients.remove(client)
    except Exception as e:
        print(f"Lỗi khi xử lý client: {e}")
    finally:
        print("Đã ngắt kết nối:", client_socket.getpeername())
        if client_socket in clients:
            clients.remove(client_socket)
        client_socket.close()

# Tạo socket server
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(SERVER_ADDRESS)
server_socket.listen(5)
print("Server đang chờ kết nối...")

# Tạo SSL context
context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
context.load_cert_chain(certfile="./certificates/server-cert.crt", keyfile="./certificates/server-key.key")

while True:
    try:
        client_socket, client_address = server_socket.accept()
        
        # Thiết lập kết nối SSL
        ssl_socket = context.wrap_socket(client_socket, server_side=True)
        
        # Bắt đầu xử lý client
        client_thread = threading.Thread(target=handle_client, args=(ssl_socket,), daemon=True)
        client_thread.start()
    except Exception as e:
        print(f"Lỗi khi chấp nhận kết nối: {e}")
