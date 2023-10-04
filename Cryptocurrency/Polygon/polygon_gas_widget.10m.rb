#!/usr/bin/env ruby

# <bitbar.title>Polygon Gas Fees</bitbar.title>
# <bitbar.version>v1.0</bitbar.version>
# <bitbar.author>Masumi Kawasaki</bitbar.author>
# <bitbar.author.github>geeknees</bitbar.author.github>
# <bitbar.desc>Widget for monitoring Polygon Gas Fees from https://polygonscan.com/</bitbar.desc>
# <bitbar.dependencies>ruby</bitbar.dependencies>
# <bitbar.image>https://raw.githubusercontent.com/geeknees/xbar-plugins/main/polygon_gas_widget/screenshot.png</bitbar.image>
# <bitbar.abouturl>https://github.com/geeknees/xbar-plugins</bitbar.abouturl>

require 'open-uri'
require 'json'

ENDPOINT = "https://api.polygonscan.com/api?module=gastracker&action=gasoracle&apikey="
APIKEY = ""

charset = nil
html = URI.open(ENDPOINT+APIKEY) do |f|
  charset = f.charset
  f.read
end

response = JSON.parse(html)

puts "♾️ #{response['result']['ProposeGasPrice']}"
puts '---'

response['result'].each do |k, v|
  puts "#{k}: #{v.to_f.floor(5)}"
end
