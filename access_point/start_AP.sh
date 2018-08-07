#sudo systemctl disable NetworkManager.service

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
sudo nmcli radio wifi off
sudo rfkill unblock wlan
sudo ifconfig wlan3 192.168.2.100/24 up
#sudo service isc-dhcp-application start
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
sudo ./initSoftAP.sh wlan3 eth0 &
echo "Wifi configured - running hostapd in background"


sleep 5
#passo 4: definir a regra do do Iptables
echo "Passo 4 - start"
sudo iptables -t nat -A PREROUTING -p udp -i wlan3 -d 192.168.3.30 --dport 5100 -j DNAT --to 192.168.2.30:5100
sudo iptables -t nat -A PREROUTING -p udp -i wlan3 -d 192.168.3.31 --dport 5100 -j DNAT --to 192.168.2.31:5100
sudo iptables -t nat -A PREROUTING -p udp -i wlan3 -d 192.168.3.32 --dport 5100 -j DNAT --to 192.168.2.32:5100
sudo iptables -t nat -A PREROUTING -p udp -i wlan3 -d 192.168.3.33 --dport 5100 -j DNAT --to 192.168.2.33:5100
sudo iptables -t nat -A PREROUTING -p udp -i wlan3 -d 192.168.3.34 --dport 5100 -j DNAT --to 192.168.2.34:5100
sudo iptables -t nat -A PREROUTING -p udp -i wlan3 -d 192.168.3.35 --dport 5100 -j DNAT --to 192.168.2.35:5100
sudo iptables -t nat -A PREROUTING -p udp -i wlan3 -d 192.168.3.36 --dport 5100 -j DNAT --to 192.168.2.36:5100
sudo iptables -t nat -A PREROUTING -p udp -i wlan3 -d 192.168.3.37 --dport 5100 -j DNAT --to 192.168.2.37:5100
sudo iptables -t nat -A PREROUTING -p udp -i wlan3 -d 192.168.3.38 --dport 5100 -j DNAT --to 192.168.2.38:5100
sudo iptables -t nat -A PREROUTING -p udp -i wlan3 -d 192.168.3.39 --dport 5100 -j DNAT --to 192.168.2.39:5100
sudo iptables -t nat -A PREROUTING -p udp -i wlan3 -d 192.168.3.40 --dport 5100 -j DNAT --to 192.168.2.40:5100

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


