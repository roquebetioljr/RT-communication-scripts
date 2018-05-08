#sudo systemctl disable NetworkManager.service
#sudo iface eth0 inet dhcp
#Passo 1: Configurar as placas de rede ethernet eth0 em cada maquina
# maquina como ponto de acesso com o IP: 192.168.2.1
# maquina como cliente com o IP: 192.168.2.2

echo "Initializing ethernet"
sudo ifconfig eth0 up
sleep 2
sudo ifconfig eth0 192.168.2.1 netmask 255.255.255.0
echo "Ethernet intialized."

#Passo 2: Configurar o ponto de acesso
echo "Initializing WiFi"
sudo nmcli nm wifi off
sudo rfkill unblock wlan
sudo ifconfig wlan0 192.168.0.1/24 up
#sudo service isc-dhcp-server start 
#sudo service hostapd start
echo "WiFi initialized"

sleep 2

echo "Initializing services"
sudo service isc-dhcp-server start
sudo service hostapd start
echo "Serices initialized"

sleep 2
## lembrar de desabilitar o networkmanager no ponto de acesso
#sudo systemctl disable NetworkManager service

#passo 3: habilitar o servidor dhcp do ponto de acesso

echo "Setup WiFi"
sudo ./initSoftAP.sh wlan0 eth0 &
echo "Wifi configured - running hostapd in background"


sleep 5
#passo 4: definir a regra do do Iptables
echo "Passo 4 - start"
sudo iptables -t nat -A PREROUTING -p udp -i wlan3 -d 192.168.1.10 --dport 5100 -j DNAT --to 192.168.0.10:5100
sudo iptables -t nat -A PREROUTING -p udp -i wlan3 -d 192.168.1.11 --dport 5100 -j DNAT --to 192.168.0.11:5100
sudo iptables -t nat -A PREROUTING -p udp -i wlan3 -d 192.168.1.12 --dport 5100 -j DNAT --to 192.168.0.12:5100
sudo iptables -t nat -A PREROUTING -p udp -i wlan3 -d 192.168.1.13 --dport 5100 -j DNAT --to 192.168.0.13:5100
sudo iptables -t nat -A PREROUTING -p udp -i wlan3 -d 192.168.1.14 --dport 5100 -j DNAT --to 192.168.0.14:5100
sudo iptables -t nat -A PREROUTING -p udp -i wlan3 -d 192.168.1.15 --dport 5100 -j DNAT --to 192.168.0.15:5100
sudo iptables -t nat -A PREROUTING -p udp -i wlan3 -d 192.168.1.16 --dport 5100 -j DNAT --to 192.168.0.16:5100
sudo iptables -t nat -A PREROUTING -p udp -i wlan3 -d 192.168.1.17 --dport 5100 -j DNAT --to 192.168.0.17:5100
sudo iptables -t nat -A PREROUTING -p udp -i wlan3 -d 192.168.1.18 --dport 5100 -j DNAT --to 192.168.0.18:5100
sudo iptables -t nat -A PREROUTING -p udp -i wlan3 -d 192.168.1.19 --dport 5100 -j DNAT --to 192.168.0.19:5100

sleep 2
sudo service isc-dhcp-server status
sudo service hostapd status
echo "FIM"

#passo 5: iniciar o gerador de tráfego IPERF cliente e servidor [maquina cliente]

#iperf -s -u -i 1 -f k -p 5100 

#perf -c 192.168.3.1 -u -i 1 -f k -p 5100 -b 2M -S 0x06

#passo 6: comando de captura de pacotes tcpdump

#sudo tcpdump -i wlan0 udp -vvv -c 800 -w nome_pasta.pcap

#passo7: converter o arquivo pcap e csv como as colunas id e time

#tshark -r nome_pasta.pcap -T fields -e ip.id -e frame.time | sort > nome_salvar.csv  

#Comando para verificar as regras do iptables: sudo iptables-save


