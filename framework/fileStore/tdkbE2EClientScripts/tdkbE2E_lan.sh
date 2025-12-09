#!/bin/bash
##########################################################################
# If not stated otherwise in this file or this component's Licenses.txt
# file the following copyright and licenses apply:
#
# Copyright 2017 RDK Management
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
##########################################################################
#

# Get the IP address of the LAN after connecting to it
get_lan_ip_address()
{
#       Uncomment the line L1 and comment out L2 if using Ubuntu version = 16.04
#       Uncomment the line L2 and comment out L1 if using Ubuntu version = 18.04
#       L1 below
#       value="$(ifconfig $var2 | grep "$var3" | cut -d ':' -f 2 | cut -d ' ' -f 1)"
#       L2 below
        value="$(ifconfig $var2 | grep "$var3" | tr -s ' ' | cut -d ' ' -f 3 | head -1)"
        echo "OUTPUT:$value"
}

# Get the IPV6 address of the LAN after connecting to it
get_lan_ipv6_address()
{
        value="$(ifconfig -a $var2 | grep "$var3" | tr -s " " |  grep -v Link | cut -d " " -f4 | cut -d "/" -f1 | head -1)"
        echo "OUTPUT:$value"
}

#Refresh Lan Network
refresh_lan_network()
{
        lan_down="$(ifconfig $var2 down > /dev/null && echo "SUCCESS" || echo "FAILURE")"
	sleep 5
        lan_up="$(ifconfig $var2 up > /dev/null && echo "SUCCESS" || echo "FAILURE")"
        if [ $lan_down = "SUCCESS" ] && [ $lan_up = "SUCCESS" ]; then
                echo "OUTPUT:SUCCESS"
        else
                echo "OUTPUT:FAILURE"
        fi
}
#Bring up interface
bringup_interface()
{
        up="$(ifconfig $var2 up > /dev/null && echo "SUCCESS" || echo "FAILURE")"
        sleep 5
        if [ $up = "SUCCESS" ]; then
                echo "OUTPUT:SUCCESS"
        else
                echo "OUTPUT:FAILURE"
        fi

}
#Bring down interface
bringdown_interface()
{
        down="$(ifconfig $var2 down > /dev/null && echo "SUCCESS" || echo "FAILURE")"
        sleep 5
        if [ $down = "SUCCESS" ]; then
                echo "OUTPUT:SUCCESS"
        else
                echo "OUTPUT:FAILURE"
        fi
}
#Verify ping to a network
ping_to_network()
{
        route_add_cmd="$(sudo ip route add $var3 via $var4 > /dev/null && echo "SUCCESS" || echo "FAILURE")"
        sleep 10
        ping_cmd="$(ping -I $var2 -c 3 $var3 > /dev/null && echo "SUCCESS" || echo "FAILURE")"
        route_del_cmd="$(sudo ip route delete $var3 via $var4 > /dev/null && echo "SUCCESS" || echo "FAILURE")"
        if [ $route_add_cmd = "SUCCESS" ] && [ $ping_cmd = "SUCCESS" ]  && [ $route_del_cmd = "SUCCESS" ]; then
                echo "OUTPUT:SUCCESS"
        else
                echo "OUTPUT:FAILURE"
        fi
}

#Verify ping to a host url
ping_to_host()
{
        route_add_cmd="$(sudo route add -net $var2 netmask 255.255.255.255 gw $var3 dev $var4  > /dev/null && echo "SUCCESS" || echo "FAILURE")"
        sleep 10
        ping_cmd="$(ping -I $var4 -c 3 $var2 > /dev/null && echo "SUCCESS" || echo "FAILURE")"
        route_del_cmd="$(sudo route del -net $var2 netmask 255.255.255.255 gw $var3 dev $var4  > /dev/null && echo "SUCCESS" || echo "FAILURE")"
        if [ $route_add_cmd = "SUCCESS" ] && [ $ping_cmd = "SUCCESS" ]  && [ $route_del_cmd = "SUCCESS" ]; then
                echo "OUTPUT:SUCCESS"
        else
                echo "OUTPUT:FAILURE"
        fi
}

#To send http request to a network
wget_http_network()
{
        value="$(wget --bind-address=$var2 -q --tries=1 -T 60 http://$var3:$var4 && echo "SUCCESS" || echo "FAILURE")"
        echo "OUTPUT:$value"
}

#To send https request to a network
wget_https_network()
{
        value="$(wget --bind-address=$var2 -q --tries=1 -T 60 https://$var3:$var4 --no-check-certificate && echo "SUCCESS" || echo "FAILURE")"
        echo "OUTPUT:$value"
}

# Telnet to the client devices
telnetToClient()
{
         value="$({
sleep 2
echo $var3
sleep 2
echo $var4
sleep 1
echo exit
} | telnet $var2 | tr "\n" " ")"
        echo "OUTPUT:$value"
}

# FTP to the client devices
ftpToClient()
{
value="$(SERVER=$var2
USER=$var3
PASSW=$var4

ftp -v -n $SERVER <<END_OF_SESSION
user $USER $PASSW
END_OF_SESSION
)"
echo "OUTPUT:$value"
}

add_static_route()
{
        value="$(sudo route add -net $var2 netmask 255.255.255.255 gw $var3 dev $var4  > /dev/null && echo "SUCCESS" || echo "FAILURE")"

        echo "OUTPUT:$value"
}

del_static_route()
{
        value="$(sudo route del -net $var2 netmask 255.255.255.255 gw $var3 dev $var4  > /dev/null && echo "SUCCESS" || echo "FAILURE")"
        echo "OUTPUT:$value"
}

nslookup_in_client()
{
        outStatus="$(nslookup $var2 $var3)"
        outStatus=$(printf "%s " $outStatus)
        site=$(echo $var2 | sed 's/^.\{4\}//g')
        case $outStatus in
            *"Non-authoritative answer: Name: $var2 Address:"*) value="SUCCESS";;
            *"Non-authoritative answer: $var2 canonical name = $site. Name: $site Address:"*) value="SUCCESS";;
            *)value="FAILURE"
        esac
        echo "OUTPUT:$value"
}

# Get the subnet mask of the LAN client
get_lan_subnet_mask()
{
#       Uncomment the line L1 and comment out L2 if using Ubuntu version = 16.04
#       Uncomment the line L2 and comment out L1 if using Ubuntu version = 18.04
#       L1 below
#       value="$(ifconfig $var2 | grep "$var3" | cut -d ':' -f 4 | cut -d ' ' -f 1)"
#       L2 below
        value="$(ifconfig $var2 | grep "$var3" | tr -s ' ' | cut -d ' ' -f 5)"
        echo "OUTPUT:$value"
}

# get the DHCP config details like lease-time, dns and domain-name etc
get_lan_dhcp_details()
{
        value1="$(sudo lsof -p `cat $var2/dhclient-$var3.pid` | grep $var3 | awk '{ print $9 }')"
        value="$(cat $value1 | grep $var4 | tail -1 | awk '{ print $3 }' | cut -d ";" -f1)"
        echo "OUTPUT:$value"
}

#To start iperf server in one of the clients
tcp_init_server_perf()
{
        iperf -s -B $var3 -t $var4 -i $var5 > $var2 &
        value="$(ps aux | grep iperf | grep -v grep > /dev/null && echo "SUCCESS" || echo "FAILURE")"
        echo "OUTPUT:$value"
}

#To start iperf client in machine to be tested
tcp_request_perf()
{
        iperf -f m -c $var2 -B $var3 -t $var5 -i $var6 > $var4 2>&1 &
}

#To parse the output from iperf client and find the throughput data of machine under test
tcp_get_client_throughput()
{
        bindStatus="$(cat $var2 | grep "bind failed:" && echo "FAILURE" || echo "SUCCESS")"
        echo "bindStatus:$bindStatus"
        if [ $bindStatus = "SUCCESS" ]; then
                value="$(cat $var2 | grep bits/sec | awk '{ print $7 }' | tr '\n' ',')"
                #remove the trailing ,
                value=${value%?}
                #save the throughput output into a file
                echo $value>$var3
                echo "OUTPUT:$value"
        else
                echo "OUTPUT:"
        fi
}

# To set the TCP server in listening mode
tcp_init_server()
{
        # Remove old file if exists
        rm -f "$var2"

        # Create new file with proper permissions
        touch "$var2"
        chmod 666 "$var2"

        #If server port is provided as input
        if [ -n $var4 ]; then
            iperf -s -B $var3 -i 1 -p $var4 > $var2 &
        #If server port is not provided take default port
        else
            iperf -s -B $var3 > $var2 &
        fi

        value="$(ps aux | grep iperf | grep -v grep > /dev/null && echo "SUCCESS" || echo "FAILURE")"
        echo "OUTPUT:$value"
}

#To send TCP request from client to server
tcp_request()
{
        iperf -c $var2 -B $var3 > $var4 2>&1
        bindStatus="$(cat $var4 | grep "bind failed:" && echo "FAILURE" || echo "SUCCESS")"
        echo "bindStatus:$bindStatus"
        if [ $bindStatus = "SUCCESS" ]; then
                value="$(cat $var4 | grep Mbits/sec | awk '{print $(NF-1)}')"
                echo "OUTPUT:$value"
        else
                echo "OUTPUT:"
        fi
}

#To get the bandwidth from server
validate_tcp_server_output()
{
        # Uncomment below line and comment out next line if Ubuntu version < 22.04
        # serverOutput="$(cat $var2 | grep bits/sec | cut -d ' ' -f 11)"
        serverOutput="$(cat $var2 | grep bits/sec | awk '{ print $7 }' | tail -1)"
        echo "OUTPUT:$serverOutput"
        deleteTmpFile="$(sudo rm $var2 > /dev/null && echo "SUCCESS" || echo "FAILURE")"
}

#To get the throughput from server
validate_tcp_server_output_throughput()
{
        # Uncomment below 2 lines and comment out next 2 lines if Ubuntu version < 22.04
        # serverOutput="$(cat $var2 | grep bits/sec | cut -d ' ' -f 11)"
        # size="$(cat $var2 | grep bits/sec | cut -d ' ' -f 12)"
        serverOutput="$(cat $var2 | grep bits/sec | awk '{ print $7 }' | tail -1)"
        size="$(cat $var2 | grep bits/sec | awk '{ print $8 }' | tail -1)"
        echo "OUTPUT:$serverOutput $size"
        deleteTmpFile="$(sudo rm $var2 > /dev/null && echo "SUCCESS" || echo "FAILURE")"
}

# To set the UDP server in listening mode
udp_init_server()
{
        #If server port and file to redirect server logs are given
        if [ -n $var3 -a -n $var4 ]; then
            rm -rf $var2
            iperf -u -s -B $var3 -i 1 -p $var4 > $var2 &
        #If server port and file to redirect server logs are not given
        else
            iperf -s -B $var2 -u &
        fi

        value="$(ps aux | grep iperf | grep -v grep > /dev/null && echo "SUCCESS" || echo "FAILURE")"
        echo "OUTPUT:$value"
}

#To send UDP request from client to server
udp_request()
{
        iperf -c $var2 -B $var4 -u > $var3 2>&1
        bindStatus="$(cat $var3 | grep "bind failed:" && echo "FAILURE" || echo "SUCCESS")"
        if [ $bindStatus = "SUCCESS" ]; then
                echo "OUTPUT:SUCCESS"
        else
                echo "OUTPUT:"
        fi
}

#To validate the UDP output
validate_udp_output()
{
        bandwidth="$(cat $var2 | grep bits/sec | awk '{ print $7 }' | tail -1)"
        lossPercentage="$(cat $var2 | grep bits/sec | awk '{ print $13 }' | tail -1)"
        echo "OUTPUT:$bandwidth,$lossPercentage"
        deleteTmpFile="$(sudo rm $var2 > /dev/null && echo "SUCCESS" || echo "FAILURE")"
}

#To kill iperf pid
kill_iperf()
{
        pkill iperf
        value="$(ps aux | grep iperf | grep -v "grep" > /dev/null && echo "SUCCESS" || echo "FAILURE")"
        echo "OUTPUT:$value"
}

#Verify the FTP download
validate_FTP()
{
        FTP_FILE=$var2
        value="$(ls -lrt $FTP_FILE > /dev/null && echo "SUCCESS" || echo "FAILURE")"
        echo "OUTPUT:$value"
}

#Create the file to verify FTP download
touch_File()
{
        FTP_FILE=$var2
        value="$(touch $FTP_FILE  > /dev/null && echo "SUCCESS" || echo "FAILURE")"
        echo "OUTPUT:$value"
}

#Remove the file which is transfered via FTP
remove_File()
{
        FTP_FILE=$var2
        value="$(rm -rf  $FTP_FILE > /dev/null && echo "SUCCESS" || echo "FAILURE")"
        echo "OUTPUT:$value"
}

# To get the MAC address of the lan client
get_lan_mac()
{
#       Uncomment the line L1 and comment out L2 if using Ubuntu version = 16.04
#       Uncomment the line L2 and comment out L1 if using Ubuntu version = 18.04
#       L1 below
#       value="$(ifconfig $var2 | grep HWaddr | awk '{ print $5 }')"
#       L2 below
        value="$(ifconfig $var2 | grep ether | tr -s ' ' | cut -d ' ' -f 3)"
        echo "OUTPUT:$value"
}

#To do ssh to client machines
ssh_to_client()
{
#      Uncomment the line L1 and comment out L2 if using Ubuntu version = 16.04
#      Uncomment the line L2 and comment out L1 if using Ubuntu version = 18.04
#      L1 below
#      value="$(sshpass -p$var2 ssh -o UserKnownHostsFile=/dev/null -o StrictHostKeychecking=no $var3@$var4 ifconfig $var5 | grep $var6 | cut -d ':' -f 2 | cut -d ' ' -f 1)"
#      L2 below
       value="$(sshpass -p$var2 ssh -o UserKnownHostsFile=/dev/null -o StrictHostKeychecking=no $var3@$var4 ifconfig $var5 | grep -m1 $var6 | tr -s ' ' | cut -d ' ' -f 3)"
       echo "OUTPUT:$value"
}

#To start node in client machine
start_node()
{
        export DISPLAY=:0
#       Uncomment the lines L1 and comment out L2 if using Selenium version = 3.141.59
#       Uncomment the lines L2 and comment out L1 if using Selenium version = 4.9.0
#       L1 below
#       java -jar $var2 -role node -host $var5 -hub http://$var3:4444/grid/register/ > $var4 2>&1 &
#       L2 below
        java -jar $var2 node --hub http://$var3:4444/grid/register/ > $var4 2>&1 &
        sleep 20
#       L1 below
#       value="$(cat $var4 | grep "The node is registered to the hub and ready to use" > /dev/null && echo "SUCCESS" || echo "FAILURE")"
#       L2 below
        value="$(cat $var4 | grep "Node has been added" > /dev/null && echo "SUCCESS" || echo "FAILURE")"
        echo "OUTPUT:$value"
}
#To kill the selenium hub and node
kill_selenium()
{
        sudo kill -9 `echo $(ps -ef | grep selenium | grep -v grep|awk '{print $2;}')`
}

#Triggering port
trigger_port()
{
        protocol=$var4
        if [ "$protocol" = "TCP" ]; then
            netcat -v $var2 $var3
        else
            netcat -v -u $var2 $var3
        fi
        echo "OUTPUT:SUCCESS"
}

#To start the netcat server
netcat_init_server()
{
        PORT=$var2
        PROTOCOL=$var3
        SERVERFILE=$var4

        if [ $PROTOCOL = "TCP" ]; then
                cat $SERVERFILE | netcat -lvp $PORT > /dev/null &
        else
                cat $SERVERFILE | netcat -u -lvp $PORT > /dev/null &
        fi

        echo "OUTPUT:SUCCESS"
}

#Write content to file
write_msgtofile()
{
        MESSAGE=$var2
        FILE=$var3
        value="$(echo $MESSAGE > $FILE < /dev/null && echo "SUCCESS" || echo "FAILURE")"
        echo "OUTPUT:$value"
}

#To kill netcat pid
kill_netcat()
{
        pkill netcat
        value="$(ps aux | grep netcat | grep -v "grep" > /dev/null && echo "SUCCESS" || echo "FAILURE")"
        echo "OUTPUT:$value"
}

#Read contents of a file
read_fileContent()
{
    FILE=$var2

    if [ -s $FILE ]; then
        value="$(cat $FILE)"
        echo "OUTPUT:$value"
    else
        echo "OUTPUT:FAILURE"
    fi
}

# Store the arguments to a variable
event=$1
var2=$2
var3=$3
var4=$4
var5=$5
var6=$6
#echo "\r\n";

# Invoke the function based on the argument passed
case $event in
   "get_lan_ip_address")
        get_lan_ip_address;;
    "get_lan_ipv6_address")
        get_lan_ipv6_address;;
   "refresh_lan_network")
        refresh_lan_network;;
   "bringdown_interface")
        bringdown_interface;;
   "bringup_interface")
        bringup_interface;;
   "ping_to_network")
        ping_to_network;;
   "ping_to_host")
        ping_to_host;;
   "wget_http_network")
        wget_http_network;;
   "wget_https_network")
        wget_https_network;;
   "telnetToClient")
        telnetToClient;;
   "ftpToClient")
        ftpToClient;;
   "add_static_route")
        add_static_route;;
   "del_static_route")
        del_static_route;;
   "nslookup_in_client")
        nslookup_in_client;;
   "get_lan_subnet_mask")
        get_lan_subnet_mask;;
   "get_lan_dhcp_details")
        get_lan_dhcp_details;;
   "tcp_init_server_perf")
        tcp_init_server_perf;;
   "tcp_request_perf")
        tcp_request_perf;;
   "tcp_get_client_throughput")
        tcp_get_client_throughput;;
   "tcp_init_server")
        tcp_init_server;;
   "tcp_request")
        tcp_request;;
   "validate_tcp_server_output")
        validate_tcp_server_output;;
   "validate_tcp_server_output_throughput")
        validate_tcp_server_output_throughput;;
   "udp_init_server")
        udp_init_server;;
   "udp_request")
        udp_request;;
   "validate_udp_output")
        validate_udp_output;;
   "kill_iperf")
        kill_iperf;;
   "validate_FTP")
        validate_FTP;;
    "touch_File")
        touch_File;;
    "remove_File")
        remove_File;;
    "get_lan_mac")
        get_lan_mac;;
    "ssh_to_client")
        ssh_to_client;;
    "start_node")
        start_node;;
    "kill_selenium")
        kill_selenium;;
    "trigger_port")
        trigger_port;;
    "netcat_init_server")
        netcat_init_server;;
    "write_msgtofile")
        write_msgtofile;;
    "kill_netcat")
        kill_netcat;;
    "read_fileContent")
        read_fileContent;;
   *) echo "Invalid Argument passed";;
esac

