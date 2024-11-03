```python
#!/data/data/com.termux/files/usr/bin/python
import os
import socket
import subprocess
import time
import threading
import http.server
import socketserver
from queue import Queue
import json

class TermuxConnectionSharer:
    def __init__(self):
        self.running = False
        self.port = self.find_available_port()
        self.data_queue = Queue()
        self.ensure_permissions()
        
    def ensure_permissions(self):
        """Ensure Termux has necessary permissions"""
        try:
            # Request storage permission
            subprocess.run(['termux-setup-storage'], check=True)
            
            # Request network access
            subprocess.run(['termux-wifi-enable'], check=True)
            
        except subprocess.CalledProcessError:
            print("⚠️ Some permissions might be missing")
            print("Run 'termux-setup-storage' manually if needed")
    
    def find_available_port(self):
        """Find an available port to use"""
        ports = [8000, 8080, 9000, 9090, 5000]
        for port in ports:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            try:
                sock.bind(('127.0.0.1', port))
                sock.close()
                return port
            except OSError:
                continue
        return 8000  # Default fallback
    
    def get_network_info(self):
        """Get network interface information"""
        try:
            # Try to get IP using termux-wifi-connectioninfo
            result = subprocess.run(
                ['termux-wifi-connectioninfo'],
                capture_output=True,
                text=True
            )
            info = json.loads(result.stdout)
            return info.get('ip', '127.0.0.1')
        except:
            # Fallback method
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            try:
                s.connect(('8.8.8.8', 80))
                ip = s.getsockname()[0]
                s.close()
                return ip
            except:
                return '127.0.0.1'

    def monitor_network(self):
        """Monitor network statistics"""
        while self.running:
            try:
                # Get network stats using termux-wifi-connectioninfo
                result = subprocess.run(
                    ['termux-wifi-connectioninfo'],
                    capture_output=True,
                    text=True
                )
                info = json.loads(result.stdout)
                
                self.data_queue.put({
                    'signal_strength': info.get('signal_strength', 'N/A'),
                    'link_speed': info.get('link_speed', 'N/A')
                })
            except:
                self.data_queue.put({
                    'signal_strength': 'N/A',
                    'link_speed': 'N/A'
                })
            time.sleep(1)

    def start_server(self):
        """Start the connection sharing server"""
        class ConnectionHandler(http.server.SimpleHTTPRequestHandler):
            def do_GET(self):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(b"Connection active")

        self.running = True
        ip = self.get_network_info()
        
        # Start network monitoring
        monitor_thread = threading.Thread(target=self.monitor_network)
        monitor_thread.daemon = True
        monitor_thread.start()
        
        # Create and start the server
        with socketserver.TCPServer((ip, self.port), ConnectionHandler) as httpd:
            print(f"\n🌐 Server running at: http://{ip}:{self.port}")
            print("📱 Connect other devices using this address")
            print("\n📊 Network Statistics:")
            
            try:
                while self.running:
                    # Handle one request
                    httpd.handle_request()
                    
                    # Show network stats
                    try:
                        stats = self.data_queue.get_nowait()
                        print(f"\rSignal: {stats['signal_strength']} | "
                              f"Speed: {stats['link_speed']}",
                              end='', flush=True)
                    except:
                        pass
                    
            except KeyboardInterrupt:
                print("\n\n🛑 Stopping server...")
                self.running = False
                httpd.server_close()

def setup_termux():
    """Setup required packages in Termux"""
    try:
        # Update package list
        subprocess.run(['pkg', 'update', '-y'])
        
        # Install required packages
        packages = [
            'python',
            'termux-api',
            'termux-tools'
        ]
        
        for package in packages:
            subprocess.run(['pkg', 'install', '-y', package])
            
        print("✅ Setup complete!")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Setup failed: {e}")
        return False

def main():
    print("📡 Termux Connection Sharer")
    print("============================")
    
    # Check if setup is needed
    if not os.path.exists('/data/data/com.termux/files/usr/bin/termux-api'):
        print("\n⚙️ First-time setup needed...")
        if not setup_termux():
            print("\n❌ Please install required packages manually:")
            print("pkg install python termux-api termux-tools")
            return
    
    print("\n🚀 Starting connection sharer...")
    sharer = TermuxConnectionSharer()
    sharer.start_server()

if __name__ == "__main__":
    main()

```