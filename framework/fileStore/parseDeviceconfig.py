
import configparser
import os


COMPONENT_PARAMETERS = {
    "TELEMETRY2_ENABLE": "TELEMETRY_CONFIG_URL TELEMETRY_UPLOAD_URL TELEMETRY_ENABLE TELEMETRY_VERSION PROFILE_PATH CACHED_REPORT_PATH TELEMETRY_LOG_PATH".split(),
    "FIRMWAREUPGRADE_ENABLE": "FIRMWARE_UPGRADE_RPI FIRMWARE_UPGRADE_BPI username FWUPGRADE_BINARY FW_DOWNLOAD_PATH logFile PARTITION_PATH FIRMWARE_LOCATION FIRMWARE_PROTOCOL XCONF_URL XCONF_API_KEY".split(),
    "CRASHUPLOAD_ENABLE": "COREDUMP_PATH_UNIT COREDUMP_SERVICE_UNIT MINIDUMPS_DIR RDKLOGS_DIR CORE_LOG_TXT NON_CCSP_PROCESS CCSP_PROCESS_NAME WAN_MANAGER_PROCESS DEFAULT_CRASH_PORTAL_URL LOCAL_SERVER_PORT LOCAL_SERVER_IP LOCAL_UPLOAD_URL".split(),
    "DAC_ENABLE": "DOBBY_SERVICE DSM_SERVICE DOBBY_DAEMON_PROCESS DSM_PROCESS FACTORY_RESET_PARAM FACTORY_RESET_VALUE FACTORY_RESET_WAIT_TIME".split(),
    "RFC_ENABLE": "RFC_URL RFC_XCONF_URL RFC_XCONF_API_KEY RFC_LOG_FILE".split(),
    "RNDIS_ENABLE": "ANDROID_WAN_INTERFACE IOS_WAN_INTERFACE INET_ADDR_PATTERN HWADDR_PATTERN PING_TARGET DM_HOSTS_HOST_NUMBER_OF_ENTRIES".split(),
    "WEBCONFIG_ENABLE": "WEBCONFIG_URL LAN_IP_ADDRESS LAN_SUBNETMASK DHCP_START_IP DHCP_END_IP LEASE_TIME DHCP_SERVER_ENABLE INTERNAL_CLIENT".split(),
    "IPV6_ENABLE": "WAN_IPV6_PREFIX_LENGTH LAN_IPV6_PREFIX_LENGTH LAYER1_INTERFACE_WLAN LAYER1_INTERFACE_LAN DUT_LAN_INTERFACE HOST_NAME DOMAIN_NAME".split(),
    "RRD_ENABLE": "report_generation_location static_json_file dynamic_json_file rrd_log_file upstream_rrd_url_path debug_report_tracker_file upload_server_url download_server_url".split(),
    "TELCOVOICEMANAGER_ENABLE": "client1_username client2_username outbound_client_username outbound_client_password outbound_port outbound_proxy outbound_line_enable pjsip_conf_file dialplan_file".split(),
    "USPPA_ENABLE": "TOKEN_FILE CONTROLLER_URI CONTROLLER_USERNAME PASSWORD".split(),
    "WEBPA_ENABLE": "SAT_REQUIRED SAT_TOKEN_FILE SERVER_URI AUTHTYPE".split(),
    "STABILITY_ENABLE": "LOG_UPLOAD_SERVER_URL PUBLIC_IPV4 FAILURE_ARTIFACT_ROOT PING_OUTPUT_FILE DNS_PROCESS WEBPA_PROCESS_NAME PARODUS_PROCESS".split(),
    "TR069_ENABLE": "TR069_CERTIFICATE_LOCATION ACS_NBI_URL ACS_URL".split(),
}

PLATFORM_PARAMETERS = """
TDK_PATH DNS_SERVER_IP CCSP_PROCESS INTERFACE INTERFACE_LIST SNMP_PROCESS
WEBPA_PROCESS LIGHTTPD_PROCESS DROPBEAR_PROCESS NOTIFYCOMP_PROCESS
WEBCONFIG_PROCESS PSM_PROCESS TELEMETRY_PROCESS WIFI_PROCESS WEBPA_CHECK_CMD
PARODUS_CHECK_CMD CPU_UTIL_FILEPATH NAMESPACES RADIO_IF_2G RADIO_IF_5G
RADIO_IF_6G DEVICETYPE DNSMASQ_CONF_PATH MAX_PROCESS_UPTIME
MAX_PROCESSUP_WAITTIME LIST_OF_PROCESSES NTPServer1 LAN_IPADDRESS RFC_PATH
FW_NAME_SUFFIX MLD_AP_INDICES
""".split()

PARSED_PARAMETERS = set()


def _clear_parsed_parameters():
    for parameter in PARSED_PARAMETERS:
        globals().pop(parameter, None)
    PARSED_PARAMETERS.clear()


def _parse_component_config(config, deviceConfig):
    for enableParameter, parameters in COMPONENT_PARAMETERS.items():
        enabled = config.get(deviceConfig, enableParameter)
        globals()[enableParameter] = enabled
        if enabled.strip().lower() == "true":
            for parameter in parameters:
                globals()[parameter] = config.get(deviceConfig, parameter)

    for parameter in PLATFORM_PARAMETERS:
        globals()[parameter] = config.get(deviceConfig, parameter)


def parseDeviceConfig(obj):

    _clear_parsed_parameters()
    initialGlobals = set(globals())

    try:
        status = "SUCCESS"

        #Get the device name configured in test manager
        deviceDetails = obj.getDeviceDetails()
        deviceName = deviceDetails["devicename"]

        #Get the device configuration file name
        deviceConfig = deviceName + ".config"

        #Get the current directory path
        configFilePath = os.path.dirname(os.path.realpath(__file__))
        configFilePath = configFilePath + "/tdkbDeviceConfig"

        print("Device config file:", configFilePath+'/'+deviceConfig)

        #Parse the device configuration file
        config = configparser.ConfigParser(allow_no_value=True)
        config.optionxform = str
        with open(configFilePath+'/'+deviceConfig, encoding="utf-8") as configFile:
            config.read_file(
                line for line in configFile
                if not line.strip() or set(line.strip()) != {"="}
            )

        _parse_component_config(config, deviceConfig)

        #Parse the file and store the values in global variables
        global setup_type
        setup_type = config.get(deviceConfig, 'SETUP_TYPE')

        global mlo_capability
        mlo_capability = config.get(deviceConfig, 'MLO_ENABLE')

        global wlan_os_type
        wlan_os_type = config.get(deviceConfig, 'WLAN_OS_TYPE')

        global wlan_ip
        wlan_ip = config.get(deviceConfig, 'WLAN_IP')

        global wan_ping_ip
        wan_ping_ip = config.get(deviceConfig, "WAN_PING_IP")

        global wan_http_ip
        wan_http_ip = config.get(deviceConfig, "WAN_HTTP_IP")

        global wan_https_ip
        wan_https_ip = config.get(deviceConfig, "WAN_HTTPS_IP")

        global wan_ftp_ip
        wan_ftp_ip = config.get(deviceConfig, "WAN_FTP_IP")

        global ipv6_host_name
        ipv6_host_name = config.get(deviceConfig, "IPV6_HOST_NAME")

        global wlan_username
        wlan_username = config.get(deviceConfig, "WLAN_USERNAME")

        global wlan_password
        wlan_password = config.get(deviceConfig, "WLAN_PASSWORD")

        global wlan_ftp_username
        wlan_ftp_username = config.get(deviceConfig, "WLAN_FTP_USERNAME")

        global wlan_ftp_password
        wlan_ftp_password = config.get(deviceConfig, "WLAN_FTP_PASSWORD")

        if mlo_capability == "False":
            global wlan_2ghz_interface
            wlan_2ghz_interface = config.get(deviceConfig, "WLAN_2GHZ_INTERFACE")

            global wlan_5ghz_interface
            wlan_5ghz_interface = config.get(deviceConfig, "WLAN_5GHZ_INTERFACE")

            global wlan_6ghz_interface
            wlan_6ghz_interface = config.get(deviceConfig, "WLAN_6GHZ_INTERFACE")

        else:
            global wlan_interface
            wlan_interface = config.get(deviceConfig, "WLAN_INTERFACE")

        global wlan_inet_address
        wlan_inet_address = config.get(deviceConfig, "WLAN_INET_ADDRESS")

        global wlan_inet6_address
        wlan_inet6_address = config.get(deviceConfig, "WLAN_INET6_ADDRESS")

        global wlan_subnet_mask
        wlan_subnet_mask = config.get(deviceConfig, "WLAN_SUBNET_MASK")

        global wlan_script
        wlan_script = config.get(deviceConfig, "WLAN_SCRIPT")

        if mlo_capability == "False":
            global wlan_2ghz_ssid_connect_status
            wlan_2ghz_ssid_connect_status = config.get(deviceConfig, "WLAN_2GHZ_SSID_CONNECT_STATUS")

            global wlan_5ghz_ssid_connect_status
            wlan_5ghz_ssid_connect_status = config.get(deviceConfig, "WLAN_5GHZ_SSID_CONNECT_STATUS")

            global wlan_6ghz_ssid_connect_status
            wlan_6ghz_ssid_connect_status = config.get(deviceConfig, "WLAN_6GHZ_SSID_CONNECT_STATUS")

            global wlan_2ghz_ssid_disconnect_status
            wlan_2ghz_ssid_disconnect_status = config.get(deviceConfig, "WLAN_2GHZ_SSID_DISCONNECT_STATUS")

            global wlan_5ghz_ssid_disconnect_status
            wlan_5ghz_ssid_disconnect_status = config.get(deviceConfig, "WLAN_5GHZ_SSID_DISCONNECT_STATUS")

            global wlan_6ghz_ssid_disconnect_status
            wlan_6ghz_ssid_disconnect_status = config.get(deviceConfig, "WLAN_6GHZ_SSID_DISCONNECT_STATUS")

        else:
            global wlan_ssid_connect_status
            wlan_ssid_connect_status = config.get(deviceConfig, "WLAN_SSID_CONNECT_STATUS")

            global wlan_ssid_disconnect_status
            wlan_ssid_disconnect_status = config.get(deviceConfig, "WLAN_SSID_DISCONNECT_STATUS")

        global lan_os_type
        lan_os_type = config.get(deviceConfig, 'LAN_OS_TYPE')

        global lan_ip
        lan_ip = config.get(deviceConfig, "LAN_IP")

        global lan_username
        lan_username = config.get(deviceConfig, "LAN_USERNAME")

        global lan_password
        lan_password = config.get(deviceConfig, "LAN_PASSWORD")

        global lan_ftp_username
        lan_ftp_username = config.get(deviceConfig, "LAN_FTP_USERNAME")

        global lan_ftp_password
        lan_ftp_password = config.get(deviceConfig, "LAN_FTP_PASSWORD")

        global lan_interface
        lan_interface = config.get(deviceConfig, "LAN_INTERFACE")

        global lan_inet_address
        lan_inet_address = config.get(deviceConfig, "LAN_INET_ADDRESS")

        global lan_inet6_address
        lan_inet6_address = config.get(deviceConfig, "LAN_INET6_ADDRESS")

        global lan_subnet_mask
        lan_subnet_mask = config.get(deviceConfig, "LAN_SUBNET_MASK")

        global lan_dns_server
        lan_dns_server = config.get(deviceConfig, "LAN_DNS_SERVER")

        global lan_lease_time
        lan_lease_time = config.get(deviceConfig, "LAN_LEASE_TIME")

        global lan_domain_name
        lan_domain_name = config.get(deviceConfig, "LAN_DOMAIN_NAME")

        global lan_script
        lan_script = config.get(deviceConfig, "LAN_SCRIPT")

        global lan_port_number
        lan_port_number = config.get(deviceConfig, "LAN_PORT_Number")

        global wan_ip
        wan_ip = config.get(deviceConfig, "WAN_IP")

        global wan_os_type
        wan_os_type = config.get(deviceConfig, "WAN_OS_TYPE")

        global wan_username
        wan_username = config.get(deviceConfig, "WAN_USERNAME")

        global wan_password
        wan_password = config.get(deviceConfig, "WAN_PASSWORD")

        global wan_ftp_username
        wan_ftp_username = config.get(deviceConfig, "WAN_FTP_USERNAME")

        global wan_ftp_password
        wan_ftp_password = config.get(deviceConfig, "WAN_FTP_PASSWORD")

        global wan_interface
        wan_interface = config.get(deviceConfig, "WAN_INTERFACE")

        global wan_inet_address
        wan_inet_address = config.get(deviceConfig, "WAN_INET_ADDRESS")

        global wan_script
        wan_script = config.get(deviceConfig, "WAN_SCRIPT")

        if mlo_capability == "False":
            global ssid_2ghz_name
            ssid_2ghz_name = config.get(deviceConfig, "SSID_2GHZ_NAME")

            global ssid_2ghz_pwd
            ssid_2ghz_pwd = config.get(deviceConfig, "SSID_2GHZ_PWD")

            global ssid_2ghz_invalid_pwd
            ssid_2ghz_invalid_pwd = config.get(deviceConfig, "SSID_2GHZ_INVALID_PWD")

        global ssid_2ghz_index
        global radio_2ghz_index
        global ssid_5ghz_index
        global radio_5ghz_index
        global ssid_6ghz_index
        global radio_6ghz_index

        if setup_type == "TDK":
            ssid_2ghz_index = config.get(deviceConfig, "TDK_SSID_2GHZ_INDEX")
            radio_2ghz_index = config.get(deviceConfig, "TDK_RADIO_2GHZ_INDEX")
            ssid_5ghz_index = config.get(deviceConfig, "TDK_SSID_5GHZ_INDEX")
            radio_5ghz_index = config.get(deviceConfig, "TDK_RADIO_5GHZ_INDEX")
            ssid_6ghz_index = config.get(deviceConfig, "TDK_SSID_6GHZ_INDEX")
            radio_6ghz_index = config.get(deviceConfig, "TDK_RADIO_6GHZ_INDEX")
        else:
            ssid_2ghz_index = config.get(deviceConfig, "WEBPA_SSID_2GHZ_INDEX")
            radio_2ghz_index = config.get(deviceConfig, "WEBPA_RADIO_2GHZ_INDEX")
            ssid_5ghz_index = config.get(deviceConfig, "WEBPA_SSID_5GHZ_INDEX")
            radio_5ghz_index = config.get(deviceConfig, "WEBPA_RADIO_5GHZ_INDEX")
            ssid_6ghz_index = config.get(deviceConfig, "WEBPA_SSID_6GHZ_INDEX")
            radio_6ghz_index = config.get(deviceConfig, "WEBPA_RADIO_6GHZ_INDEX")

        if mlo_capability == "False":
            global ssid_5ghz_name
            ssid_5ghz_name = config.get(deviceConfig, "SSID_5GHZ_NAME")

            global ssid_5ghz_pwd
            ssid_5ghz_pwd = config.get(deviceConfig, "SSID_5GHZ_PWD")

            global ssid_5ghz_invalid_pwd
            ssid_5ghz_invalid_pwd = config.get(deviceConfig, "SSID_5GHZ_INVALID_PWD")

            global ssid_6ghz_name
            ssid_6ghz_name = config.get(deviceConfig, "SSID_6GHZ_NAME")

            global ssid_6ghz_pwd
            ssid_6ghz_pwd = config.get(deviceConfig, "SSID_6GHZ_PWD")

            global ssid_6ghz_invalid_pwd
            ssid_6ghz_invalid_pwd = config.get(deviceConfig, "SSID_6GHZ_INVALID_PWD")
        else:
            global ssid_name
            ssid_name = config.get(deviceConfig, "MLO_SSID")

            global ssid_pwd
            ssid_pwd = config.get(deviceConfig, "MLO_PASSWORD")

        global connection_timeout
        connection_timeout = config.get(deviceConfig, "CONNECTION_TIMEOUT")

        global network_ip
        network_ip = config.get(deviceConfig, "NETWORK_IP")

        global http_port
        http_port = config.get(deviceConfig, "HTTP_PORT")

        global https_port
        https_port = config.get(deviceConfig, "HTTPS_PORT")

        global wan_http_port
        wan_http_port = config.get(deviceConfig, "WAN_HTTP_PORT")

        global wan_https_port
        wan_https_port = config.get(deviceConfig, "WAN_HTTPS_PORT")

        global wlan_http_port
        wlan_http_port = config.get(deviceConfig, "WLAN_HTTP_PORT")

        global wlan_https_port
        wlan_https_port = config.get(deviceConfig, "WLAN_HTTPS_PORT")

        global cm_ip
        cm_ip = config.get(deviceConfig, "CM_IP")

        global gw_wan_ip
        gw_wan_ip = config.get(deviceConfig, "GW_WAN_IP")

        global ssid_invalid_name
        ssid_invalid_name = config.get(deviceConfig, "SSID_INVALID_NAME")

        global ssid_invalid_pwd
        ssid_invalid_pwd = config.get(deviceConfig, "SSID_INVALID_PWD")

        global wlan_invalid_interface
        wlan_invalid_interface = config.get(deviceConfig, "WLAN_INVALID_INTERFACE")

        global nslookup_domain_name
        nslookup_domain_name = config.get(deviceConfig, "NSLOOKUP_DOMAIN_NAME")

        global lan_dhcp_location
        lan_dhcp_location = config.get(deviceConfig, "LAN_DHCP_LOCATION")

        global tmp_file_lan
        tmp_file_lan = config.get(deviceConfig, "TMP_FILE_LAN")

        global tmp_file_wlan
        tmp_file_wlan = config.get(deviceConfig, "TMP_FILE_WLAN")

        global ftp_test_file
        ftp_test_file = config.get(deviceConfig, "FTP_TEST_FILE")

        global website_url
        website_url = config.get(deviceConfig, "WEBSITE_URL")

        global website_keyword
        website_keyword = config.get(deviceConfig, "WEBSITE_KEYWORD")

        global allowed_url
        allowed_url = config.get(deviceConfig, "ALLOWED_URL")

        global parentalCtl_port
        parentalCtl_port = config.get(deviceConfig, "PARENTALCTL_PORT")

        global invalid_dns_server
        invalid_dns_server = config.get(deviceConfig, "INVALID_DNS_SERVER")

        global start_hub_script
        start_hub_script = config.get(deviceConfig, "START_HUB_SCRIPT")

        global proxy_enabled
        proxy_enabled = config.get(deviceConfig, "PROXY_ENABLED")

        global proxy_host
        proxy_host = config.get(deviceConfig, "PROXY_HOST")

        global proxy_port
        proxy_port = config.get(deviceConfig, "PROXY_PORT")

        global proxy_username
        proxy_username = config.get(deviceConfig, "PROXY_USERNAME")

        global proxy_password
        proxy_password = config.get(deviceConfig, "PROXY_PASSWORD")

        global no_proxy
        no_proxy = config.get(deviceConfig, "NO_PROXY")

        global proxy_path
        proxy_path = config.get(deviceConfig, "PROXY_PATH")

        global grid_url
        grid_url = config.get(deviceConfig, "GRID_URL")

        global mso_grid_url
        mso_grid_url = config.get(deviceConfig, "MSO_GRID_URL")

        global connectivity_test_destination_address
        connectivity_test_destination_address = config.get(deviceConfig, "CONNECTIVITY_TEST_DESTINATION_ADDRESS")

        global connected_lan_hostname
        connected_lan_hostname = config.get(deviceConfig, "CONNECTED_LAN_HOSTNAME")

        global blocked_site
        blocked_site = config.get(deviceConfig, "BLOCKED_SITE")

        global webui_logfile
        webui_logfile = config.get(deviceConfig, "WEBUI_LOGFILE")

        global webui_hub_selenium_path
        webui_hub_selenium_path = config.get(deviceConfig, "WEBUI_HUB_SELENIUM_PATH")

        global hub_machine_ip
        hub_machine_ip = config.get(deviceConfig, "HUB_MACHINE_IP")

        global ui_username
        ui_username = config.get(deviceConfig, "UI_USERNAME")

        global mso_ui_username
        mso_ui_username = config.get(deviceConfig, "MSO_UI_USERNAME")

        global ui_password
        ui_password = config.get(deviceConfig, "UI_PASSWORD")

        global invalid_ssidnames
        invalid_ssidnames = config.get(deviceConfig, "INVALID_SSIDNAMES")

        global mso_ui_password
        mso_ui_password = config.get(deviceConfig, "MSO_UI_PASSWORD")

        global incorrect_ui_password
        incorrect_ui_password = config.get(deviceConfig, "INCORRECT_UI_PASSWORD")

        global default_ui_password
        default_ui_password = config.get(deviceConfig, "DEFAULT_UI_PASSWORD")

        global perf_test_duration
        perf_test_duration = config.get(deviceConfig, "PERF_TEST_DURATION")

        global perf_test_poll_interval
        perf_test_poll_interval = config.get(deviceConfig, "PERF_TEST_POLL_INTERVAL")

        global perf_test_offset
        perf_test_offset = config.get(deviceConfig, "PERF_TEST_OFFSET")

        global mlo_invalid_pwd
        mlo_invalid_pwd = config.get(deviceConfig, "MLO_INVALID_PWD")

        if mlo_capability == "False":
            global wlan_2ghz_throughput_to_wan
            wlan_2ghz_throughput_to_wan = config.get(deviceConfig, "WLAN_2GHZ_THROUGHPUT_TO_WAN")

            global wlan_2ghz_throughput_to_lan
            wlan_2ghz_throughput_to_lan = config.get(deviceConfig, "WLAN_2GHZ_THROUGHPUT_TO_LAN")

            global wlan_5ghz_throughput_to_wan
            wlan_5ghz_throughput_to_wan = config.get(deviceConfig, "WLAN_5GHZ_THROUGHPUT_TO_WAN")

            global wlan_5ghz_throughput_to_lan
            wlan_5ghz_throughput_to_lan = config.get(deviceConfig, "WLAN_5GHZ_THROUGHPUT_TO_LAN")

            global wlan_6ghz_throughput_to_wan
            wlan_6ghz_throughput_to_wan = config.get(deviceConfig, "WLAN_6GHZ_THROUGHPUT_TO_WAN")

            global wlan_6ghz_throughput_to_lan
            wlan_6ghz_throughput_to_lan = config.get(deviceConfig, "WLAN_6GHZ_THROUGHPUT_TO_LAN")
        else:
            global wlan_mlo_throughput_to_wan
            wlan_mlo_throughput_to_wan = config.get(deviceConfig, "WLAN_MLO_THROUGHPUT_TO_WAN")

            global wlan_mlo_throughput_to_lan
            wlan_mlo_throughput_to_lan = config.get(deviceConfig, "WLAN_MLO_THROUGHPUT_TO_LAN")

        global lan_throughput_to_wlan
        lan_throughput_to_wlan = config.get(deviceConfig, "LAN_THROUGHPUT_TO_WLAN")

        global lan_throughput_to_wan
        lan_throughput_to_wan = config.get(deviceConfig, "LAN_THROUGHPUT_TO_WAN")

        global lan_throughput_outfile
        lan_throughput_outfile = config.get(deviceConfig, "LAN_THROUGHPUT_OUTFILE")

        if mlo_capability == "False":
            global wlan_5ghz_throughput_outfile
            wlan_5ghz_throughput_outfile = config.get(deviceConfig, "WLAN_5GHZ_THROUGHPUT_OUTFILE")

            global wlan_2ghz_throughput_outfile
            wlan_2ghz_throughput_outfile = config.get(deviceConfig, "WLAN_2GHZ_THROUGHPUT_OUTFILE")

            global wlan_6ghz_throughput_outfile
            wlan_6ghz_throughput_outfile = config.get(deviceConfig, "WLAN_6GHZ_THROUGHPUT_OUTFILE")
        else:
            global wlan_mlo_throughput_outfile
            wlan_mlo_throughput_outfile = config.get(deviceConfig, "WLAN_MLO_THROUGHPUT_OUTFILE")

        global tm_logs_location
        tm_logs_location = config.get(deviceConfig, "TM_LOGS_LOCATION")

        global remote_access_http_port
        remote_access_http_port = config.get(deviceConfig, "REMOTE_ACCESS_HTTP_PORT")

        global remote_access_https_port
        remote_access_https_port = config.get(deviceConfig, "REMOTE_ACCESS_HTTPS_PORT")

        global webui_node_lan_logfile
        webui_node_lan_logfile = config.get(deviceConfig, "WEBUI_NODE_LAN_LOGFILE")

        global webui_node_wlan_logfile
        webui_node_wlan_logfile = config.get(deviceConfig, "WEBUI_NODE_WLAN_LOGFILE")

        global webui_node_wan_logfile
        webui_node_wan_logfile = config.get(deviceConfig, "WEBUI_NODE_WAN_LOGFILE")

        global webui_node_lan_selenium_path
        webui_node_lan_selenium_path = config.get(deviceConfig, "WEBUI_NODE_LAN_SELENIUM_PATH")

        global webui_node_wlan_selenium_path
        webui_node_wlan_selenium_path = config.get(deviceConfig, "WEBUI_NODE_WLAN_SELENIUM_PATH")

        global webui_node_wan_selenium_path
        webui_node_wan_selenium_path = config.get(deviceConfig, "WEBUI_NODE_WAN_SELENIUM_PATH")

        global bridgemode_status
        bridgemode_status = config.get(deviceConfig, "BRIDGEMODE_STATUS")

        global server_logfile
        server_logfile = config.get(deviceConfig, "PT_SERVER_LOGFILE")

        global client_logfile
        client_logfile = config.get(deviceConfig, "PT_CLIENT_LOGFILE")

        global tftpfile
        tftpfile = config.get(deviceConfig, "PT_TFTPFILE")

    except Exception as e:
        print(e);
        status = "Failed to parse the device specific configuration file"

    parsedParameters = set(globals()) - initialGlobals
    if status == "SUCCESS":
        PARSED_PARAMETERS.update(parsedParameters)
    else:
        for parameter in parsedParameters:
            globals().pop(parameter, None)

    return status