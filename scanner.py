
import socket
import threading  # برای افزایش سرعت
from rich.console import Console
from rich.table import Table

console = Console()

def scan_port(ip, port, open_ports):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        result = sock.connect_ex((ip, port))
        if result == 0:
            # اگر پورت باز بود، بنر را می‌گیرد
            banner = "Unknown"
            try:
                # sock.send(b"Hello\r\n") # یک دیتای ساده برای تحریک سرور
                sock.send(b"GET / HTTP/1.1\r\nHost: " + ip.encode() + b"\r\nUser-Agent: Mozilla/5.0\r\n\r\n")
                banner = sock.recv(1024).decode(errors="ignore").strip()
                
            except:
                pass
            open_ports.append((port, banner))
        sock.close()
    except:
        pass

def main():
    console.print("[bold magenta]====================================[/bold magenta]")
    console.print("[bold cyan]   🚀 MOJTABA'S PRO SCANNER v2.0 [/bold cyan]")
    console.print("[bold magenta]====================================[/bold magenta]")

    target = input("Enter Target IP: ")
    try:
        start_p = int(input("Start Port: "))
        end_p = int(input("End Port: "))
    except ValueError:
        console.print("[red]Please enter valid numbers for ports![/red]")
        return

    open_ports = []
    threads = []

    console.print(f"\n[yellow]Scanning {target}... Please wait.[/yellow]")

    # استفاده از تردینگ برای سرعت فوق‌العاده
    for port in range(start_p, end_p + 1):
        t = threading.Thread(target=scan_port, args=(target, port, open_ports))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    # نمایش نتایج به صورت جدول شیک
    table = Table(title=f"Scan Results for {target}")
    table.add_column("Port", style="cyan")
    table.add_column("Status", style="green")
    table.add_column("Banner/Service", style="yellow")


    for port, banner in sorted(open_ports):
        table.add_row(str(port), "OPEN", banner if banner else "No Banner")

    console.print(table)
    console.print("\n[bold green]Done![/bold green]")

if __name__ == "__main__":
    main()

