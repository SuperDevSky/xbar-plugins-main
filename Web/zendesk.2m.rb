#!/usr/bin/env ruby

# <xbar.title>Zendesk</xbar.title>
# <xbar.author>Matt Roberts, James Stiff for the icons</xbar.author>
# <xbar.author.github>mattwoberts</xbar.author.github>
# <xbar.image>https://i.imgur.com/e6rdUBh.png</xbar.image>
# <xbar.dependencies>Ruby</xbar.dependencies>
# <xbar.desc>Shows non-solved Zendesk tickets count</xbar.desc>
# <xbar.var>string(VAR_ZENDESK_SUBDOMAIN=""): Your ZenDesk subdomain</xbar.var>
# <xbar.var>string(VAR_ZENDESK_API_KEY=""): Your ZenDesk API key</xbar.var>
# <xbar.var>string(VAR_ZENDESK_EMAIL=""): Your ZenDesk email</xbar.var>

# Configurations
ZENDESK_SUBDOMAIN = ENV["VAR_ZENDESK_SUBDOMAIN"]
ZENDESK_API_KEY = ENV["VAR_ZENDESK_API_KEY"]
ZENDESK_EMAIL = ENV["VAR_ZENDESK_EMAIL"]

require 'net/http'
require 'json'
require 'date'

def fetch_tickets()
  uri = URI("https://#{ZENDESK_SUBDOMAIN}.zendesk.com/api/v2/search.json?query=status<solved")
  req = Net::HTTP::Get.new(uri)
  req.basic_auth "#{ZENDESK_EMAIL}/token", "#{ZENDESK_API_KEY}"
  res = Net::HTTP.start(uri.hostname, uri.port, use_ssl: true) { |http| http.request(req) }
  JSON.parse(res.body)
rescue => e
  []
end

def get_color(count)
  if count > 0
    return "color=white"
  end

  return ""
end

def get_image(count)

  if count > 0
    return "image=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"
  end

  return "image=iVBORw0KGgoAAAANSUhEUgAAACQAAAAkCAYAAADhAJiYAAAAAXNSR0IArs4c6QAAAJZlWElmTU0AKgAAAAgABQESAAMAAAABAAEAAAEaAAUAAAABAAAASgEbAAUAAAABAAAAUgExAAIAAAARAAAAWodpAAQAAAABAAAAbAAAAAAAAACQAAAAAQAAAJAAAAABQWRvYmUgSW1hZ2VSZWFkeQAAAAOgAQADAAAAAQABAACgAgAEAAAAAQAAACSgAwAEAAAAAQAAACQAAAAAPBJnSgAAAAlwSFlzAAAWJQAAFiUBSVIk8AAAActpVFh0WE1MOmNvbS5hZG9iZS54bXAAAAAAADx4OnhtcG1ldGEgeG1sbnM6eD0iYWRvYmU6bnM6bWV0YS8iIHg6eG1wdGs9IlhNUCBDb3JlIDYuMC4wIj4KICAgPHJkZjpSREYgeG1sbnM6cmRmPSJodHRwOi8vd3d3LnczLm9yZy8xOTk5LzAyLzIyLXJkZi1zeW50YXgtbnMjIj4KICAgICAgPHJkZjpEZXNjcmlwdGlvbiByZGY6YWJvdXQ9IiIKICAgICAgICAgICAgeG1sbnM6dGlmZj0iaHR0cDovL25zLmFkb2JlLmNvbS90aWZmLzEuMC8iCiAgICAgICAgICAgIHhtbG5zOnhtcD0iaHR0cDovL25zLmFkb2JlLmNvbS94YXAvMS4wLyI+CiAgICAgICAgIDx0aWZmOk9yaWVudGF0aW9uPjE8L3RpZmY6T3JpZW50YXRpb24+CiAgICAgICAgIDx4bXA6Q3JlYXRvclRvb2w+QWRvYmUgSW1hZ2VSZWFkeTwveG1wOkNyZWF0b3JUb29sPgogICAgICA8L3JkZjpEZXNjcmlwdGlvbj4KICAgPC9yZGY6UkRGPgo8L3g6eG1wbWV0YT4KUVd6EgAAAphJREFUWAntls1LVUEYxu+95m0VZmCboCACv5a1E7IC27gzCVq1UARdJAb9A+1roeZCQlDQRWAI2ipJMdq1i0ARBQU3LUq0Vaa33yvO4Zw5HzPvuW2EO/Aw834873mYM1+FQq3VZqDKGahUKgegmjZlJFBkoZpCcGdKFNs1BXP2ezl5Nu0Ljn4RtGJHlPYnZX5S+g7OnmKx+EcETSdlePq2yVvzzE1LOyTQjZgfklBi8JV+Towc7QX84xw8Qzlh8IQa343jtGcxNYJvygU5GimCAV+7qEfsGoFNsSaw7CHqLzkvQTEgnw3waQRN2vyYLR8BPWANHINwk+NhFrQaIuM60B+yfQWtwCsbnlcPQX7jbdAJWsFFm4jvFVgwfhkDV9sk4Yrh/LeeogNnX9YI2ofTkiVCtr26UfQepHElUXZjLztqPYunFoSYWxScB/VZhRNizxCznOCPuFSCEHMZ9hLQroE3iJmIfDnF8BaEmDpqvAPNKbXS3B8JDKcFbb+3IIhjoMsu4LA3iD9mdrxPcy9BzM4QhQcdH7fDP3HIHbVvB7JspyDEPKRA7JrIKkrsCDxCzJYjLxbOFIQYOTNk3cj60bQhxKxqCCb3ghnYPWJkJy2CBjvmsF8j5m04h1pyyt8EV8FvsE3OL3q/RoEyWAU+LXxS90EIZpNxG5gD9jNZ7snPQO7N2CUdU0nSJPBtgSBTCKJc0vIikJeBq8kLo8lwYz3B564KVjxJ0JiV4zLlLdaYJKabgP3scBWLCCK510VIic9GBJHUDux/ncKNuANBeOV9tBWJ6ow7p9sejqz+D+BSRKXeuAtFdlPe9rSEGHm5vQc38lYJ8R6ExnmG92WG5MzoyMNO4FxL8Glc1zXJtdzaDJyLGfgHhCN7TNl8XroAAAAASUVORK5CYII="
end

begin
  tickets = fetch_tickets

  count = 0
  
  if tickets.key?("error")
    puts "Error occurred | " + get_image(count)
    puts "---"
    puts tickets["error"]["title"]
    puts tickets["error"]["message"]
    exit
  end

  if tickets.length > 0
    count = tickets["results"].length
  end

  puts "#{count}" + " | " + get_color(count) + " " + get_image(count)

  puts "---"

  puts "View Tickets | href=https://#{ZENDESK_SUBDOMAIN}.zendesk.com/agent"

rescue StandardError => msg
  puts 'Error occured, please refresh xbar! >' + msg.to_s
end
