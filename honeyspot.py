import socket
import datetime

LOG_FILE = "honeypot_logs.txt"

def log_event(data):
    with open(LOG_FILE, "a") as f:
        f.write(data + "\n")

def start_honeypot(port):
    print(f"🛡 Mini Honeypot running on port {port}...")
    print("Press CTRL + C to stop\n")

    # Create socket
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("0.0.0.0", port))
    server.listen(5)

    while True:
        client_socket, address = server.accept()

        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        attacker_ip = address[0]

        # Log connection attempt
        log_entry = f"[{timestamp}] Connection attempt from {attacker_ip}"
        print(log_entry)
        log_event(log_entry)

        # Receive possible malicious data
        try:
            data = client_socket.recv(1024).decode(errors="ignore")
            if data:
                data_log = f"[{timestamp}] Data from {attacker_ip}: {data.strip()}"
                print(data_log)
                log_event(data_log)
        except:
            pass

        # Fake response
        client_socket.send(b"Access Denied\r\n")
        client_socket.close()


if __name__ == "__main__":
    print("🔥 Mini Honeypot Project\n")

    try:
        port = int(input("Enter port to monitor (e.g., 2222 or 8080): "))
        start_honeypot(port)

    except KeyboardInterrupt:
        print("\n🛑 Honeypot stopped.")

    except Exception as e:
        print("❌ Error:", e)
