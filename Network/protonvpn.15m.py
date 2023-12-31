#!/usr/bin/env python3

# <xbar.title>ProtonVPN Server Monitor</xbar.title>
# <xbar.version>v1.1</xbar.version>
# <xbar.author>Sai Sasidhar Maddali</xbar.author>
# <xbar.author.github>saisasidhar</xbar.author.github>
# <xbar.desc>Displays ProtonVPN server load for free and user defined servers</xbar.desc>
# <xbar.image>https://raw.githubusercontent.com/saisasidhar/utils/master/bitbar-argos/ProtonVPN/preview-bitbar.png</xbar.image>
# <xbar.dependencies>python</xbar.dependencies>
# <xbar.abouturl>https://github.com/saisasidhar/utils/tree/master/bitbar-argos/ProtonVPN</xbar.abouturl>

from urllib.request import urlopen
import json

menu_titles = []
menu_items = []
menu_end = []
free_servers = []
custom_servers = []

# Change this to track custom VPN servers. For example: ["NL#1", "NL#13", "NL#25"]
custom_server_names = []
# Change this to display/hide free VPN servers
display_free = True
# Change this to display/hide country flags (emoji)
display_flags = False
# However, flag emojis are not shown in macOS when emoji code such as :in: is used (Tested on macOS 10.12.5)
# Nevertheless, this flag can be set to true for argos (gnome extension)

try:
    api_response = urlopen("https://api.protonmail.ch/vpn/logicals")
    string_response = api_response.read().decode("utf-8")
    available_servers = json.loads(string_response)["LogicalServers"]

    if display_free:
        free_servers = [server for server in available_servers if server["Tier"] == 0]

    if len(custom_server_names) != 0:
        custom_servers = [server for server in available_servers if server["Name"] in custom_server_names]

    track_servers = custom_servers + free_servers

    if len(track_servers) != 0:
        min_load_server = min(track_servers, key=lambda x:x["Load"])

        menu_titles.append(str(min_load_server["Load"]) + "% load on " + min_load_server["Name"])
        menu_titles.append("---")
        for ts in track_servers:
            menu_items.append(str(":"+ts["Country"]+":\t" if display_flags else "") +\
                            str(ts["Load"]).zfill(2) + "% on " + ts["Name"] +\
                            "| color=" +\
                            str("#9CCB19" if ts["Load"] < 33 else ("#FF9912" if ts["Load"]<66 else "#FF4040")))

        menu_end.append("---")
        menu_end.append("Refresh | refresh=true")

        for title in menu_titles:
            print(title)
        for item in menu_items:
            print(item)
        for item in menu_end:
            print(item)
except Exception as e:
    print("ProtonVPN Error")
