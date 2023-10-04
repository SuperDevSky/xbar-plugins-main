#!/usr/bin/env python3

# <xbar.title>Commuter</xbar.title>
# <xbar.author>Frak Nuaimy</xbar.author>
# <xbar.author.github>frakman1</xbar.author.github>
# <xbar.image>https://i.imgur.com/JN8ad03.png</xbar.image>
# <xbar.desc>Show commute details (GoogleMaps API)</xbar.desc>
# <xbar.dependencies>python</xbar.dependencies>
# <xbar.version>v1.2</xbar.version>

import os, sys
import argparse
import subprocess
import urllib.request, urllib.parse, urllib.error
import json
import shlex

fullPathFileName = os.path.realpath(__file__)
commuterdir = "commuter_data"
commuterdir_path = os.path.dirname(os.path.abspath(__file__))+'/'+commuterdir

key_filename = "google-map-api.txt"
key_path = commuterdir_path+'/'+key_filename
origin_filename = "origin.txt"
origin_path = commuterdir_path+'/'+origin_filename
dest_filename = "dest.txt"
dest_path = commuterdir_path+'/'+dest_filename
debug_filename = "debug.txt"
debug_path = commuterdir_path+'/'+debug_filename

def run_script(script):
    return (subprocess.Popen([script], stdout=subprocess.PIPE, shell=True).communicate()[0].strip()).replace("'", "’")

# Create plugin data folder if it doesn't exist. 
# This is where input is stored (api key, origin, destination)
commuterdir_exists = os.path.exists(commuterdir_path) 
if not commuterdir_exists:
    os.mkdir( commuterdir_path, 0o755 );

debug = False
error = False
api_key = ""
orig_coord="Earth"
dest_coord="Mars"
driving_time = ""
driving_dist = ""
origin = ""
destination = ""
commuter_icon = "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" 
#commuter_icon = "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"

print("| image={}".format(commuter_icon))
print("---")

# Get inputs from files if they exist
keyfile_exists = os.path.isfile(key_path) 
if keyfile_exists:
    with open(key_path, 'r') as file:
        api_key = file.read()

originfile_exists = os.path.isfile(origin_path) 
if originfile_exists:
    with open(origin_path, 'r') as file:
        orig_coord = file.read()   
        origin = orig_coord  

destfile_exists = os.path.isfile(dest_path) 
if destfile_exists:
    with open(dest_path, 'r') as file:
        dest_coord = file.read()  
        destination = dest_coord

###############################################################################################################################################################################################################################################
# Handle inputs
parser = argparse.ArgumentParser()
parser.add_argument('-k', action='store', dest='localkey',help='Create Google Maps API Key')
parser.add_argument('-o', action='store', dest='localorigin',help='Origin Street Address')
parser.add_argument('-d', action='store', dest='localdest',help='Destination Street Address')
results = parser.parse_args()

if('-k' in sys.argv):    
    cmd = "osascript -e \'set theString to text returned of (display dialog \"Please Enter The Google API Key. \n\nIt will be stored in:\n{}".format(key_path) + "  \" with icon note default answer \"\" buttons {\"OK\",\"Cancel\"} default button 1) \'" 
    api_key = run_script(cmd)
    with open(key_path, 'w') as f:
        f.write(api_key)
    sys.exit(1)
    
if('-o' in sys.argv):    
    cmd = "osascript -e \'set theString to text returned of (display dialog \"Please Enter Origin Street Address. \n\nIt will be stored in:\n{}".format(origin_path) + "  \" with icon note default answer \"\" buttons {\"OK\",\"Cancel\"} default button 1) \'" 
    orig_coord = run_script(cmd)
    with open(origin_path, 'w') as f:
        f.write(orig_coord)
    sys.exit(1)    

if('-d' in sys.argv):    
    cmd = "osascript -e \'set theString to text returned of (display dialog \"Please Enter Destination Street Address. \n\nIt will be stored in:\n{}".format(dest_path) + "  \" with icon note default answer \"\" buttons {\"OK\",\"Cancel\"} default button 1) \'" 
    dest_coord = run_script(cmd)
    with open(dest_path, 'w') as f:
        f.write(dest_coord)
    sys.exit(1)     

###############################################################################################################################################################################################################################################
# Check API Key
if api_key == "" or api_key == "invalid":
    print(("🔑 Add API KEY | trim=false color=red font='Lucida Grande Bold' bash=" + shlex.quote(fullPathFileName) +  " param1=-k param2=null terminal=false refresh=true"))
else:
    #print("🔑 API Key: ✅ " )
    key_tooltip = str(key_path)
    print("🔑 API Key | checked=true color=#179C52 font='Lucida Grande Bold' bash=" + shlex.quote(fullPathFileName) +  " param1=-k param2=null terminal=false refresh=true tooltip=\"%s\"" % (key_tooltip)) 
print("--" + api_key)
    
###############################################################################################################################################################################################################################################
# Make API Call to Google
url = "https://maps.googleapis.com/maps/api/distancematrix/json?key={0}&units=imperial&origins={1}&destinations={2}&mode=driving&language=en-EN&departure_time=now&traffic_model=best_guess".format(api_key,str(orig_coord),str(dest_coord))
result= json.load(urllib.request.urlopen(url))

#save results in a file
with open(debug_path,'w') as data: 
      data.write(str(result))

print("---")
status1_key = result['status']
#print (status1_key)

if status1_key != 'OK' :
    #print(result.keys())
    #print(result['rows'][0]['elements'][0].keys())
    debug = True
    error = True
    if 'status' in list(result.keys()) and status1_key != 'OK' :
        print(("🚫 " + str(status1_key) + ' 🚫| color=red'))
    if 'error_message' in list(result.keys()):
        print(("" + str(result['error_message']) + '| color=red'))
        if str(result['error_message']) == "The provided API key is invalid.":
            api_key = "invalid"
            with open(key_path, 'w') as f:
                f.write(api_key)

try:
    status2_key = result['rows'][0]['elements'][0]['status']
    #print (status2_key)
    if status2_key != 'OK' :
        #print(result.keys())
        #print(result['rows'][0]['elements'][0].keys())
        debug = True
        error = True
        if 'status' in list(result['rows'][0]['elements'][0].keys()) and status2_key != 'OK':
             print(("🚫 " + str(status2_key) + ' 🚫| color=red'))
except Exception as e:
    pass
            
            
if error:

    print(("🚀 From: " + origin    + "| trim=false bash=" + shlex.quote(fullPathFileName) +  " param1=-o param2=null terminal=false refresh=true"))
    print(("🏁 To: " + destination + "| trim=false bash=" + shlex.quote(fullPathFileName) +  " param1=-d param2=null terminal=false refresh=true"))   
         
else:
###############################################################################################################################################################################################################################################
    print("---")
    try:
        if 'duration_in_traffic' in result['rows'][0]['elements'][0]:
            driving_time = result['rows'][0]['elements'][0]['duration_in_traffic']['text']
        elif 'duration' in result['rows'][0]['elements'][0]:
            driving_time = result['rows'][0]['elements'][0]['duration']['text']
        driving_dist = result['rows'][0]['elements'][0]['distance']['text']
        origin = str(result['origin_addresses'][0])
        with open(origin_path, 'w') as f:
            f.write(origin)
        destination = str(result['destination_addresses'][0])
        with open(dest_path, 'w') as f:
            f.write(destination)
    
    except Exception as e:
        print('❗ Error parsing results- reason "%s" | color=red' % str(e))
        debug = True
        print('Result:')
        print(result)
        #sys.exit(1)

    #Print results
    print("🚗 Commute | color=red font='Lucida Grande Bold'")
    print(("🚀 From: " + origin + "| trim=false bash=" + shlex.quote(fullPathFileName) +  " param1=-o param2=null terminal=false refresh=true"))
    print(("🏁 To: " + destination+ "| trim=false bash=" + shlex.quote(fullPathFileName) +  " param1=-d param2=null terminal=false refresh=true"))
    print(("⏱️ Driving Time: "+ driving_time))
    print(("📏 Driving Dist: "+ driving_dist))
    directions = "https://www.google.com/maps?saddr={}&daddr={}&t=m&z=7&layer=t".format(origin.replace(" ","+").replace(",",""),destination.replace(" ","+").replace(",",""))
    print("🗺️ View in Google Maps" + "| color =#4285F4 font='Lucida Grande Bold' href=%s " % (directions))

###############################################################################################################################################################################################################################################
# When things go wrong...
#debug = True
if debug:
    print("---")
    print("🐞 debug | color=#DB4437")
    json_formatted_str = json.dumps(result, indent=2)
    print('-- Result| color=white')
    for line in json_formatted_str.split('\n'):
        print(("----" + '‎‎' + line + "| color=white size=11 font='Courier New'"))
    if 'directions' in vars():    
        print('-- Directions URL | color=white')
        print(('---- ' + directions + '|  color=#4285F4 href=%s ' % (directions)))
###############################################################################################################################################################################################################################################
print("---")
print("🔄 Refresh | refresh=true")
