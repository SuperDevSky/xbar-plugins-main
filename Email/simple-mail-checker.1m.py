#!/usr/bin/env PYTHONIOENCODING=UTF-8 python3
#
# <xbar.title>Simple IMAP Mail Checker</xbar.title>
# <xbar.version>v0.1</xbar.version>
# <xbar.author>Ashley Anderson</xbar.author>
# <xbar.author.github>albinoloverats</xbar.author.github>
# <xbar.desc>Checks IMAP mail server and displays inbox count</xbar.desc>
# <xbar.image>https://user-images.githubusercontent.com/5545555/236855546-85c58709-498c-4749-b52f-0278ddca8b4d.png</xbar.image>
# <xbar.dependencies>python</xbar.dependencies>

import imaplib

# Add any email accounts here

accounts = [
		{
			"friendly": "Example 1",
			"hostname": "mail.example.com",
			"username": "user@example.com",
			"password": "huner2",
			"messages": 0
		},
		{
			"friendly": "Example 2",
			"hostname": "mail.example.org",
			"username": "another-user",
			"password": "correcthorsebatterystaple",
			"messages": 0
		}
	]

# Do not change anything below

ICON="| dropdown=false templateImage=JVBERi0xLjYNJeLjz9MNCjEwIDAgb2JqDTw8L0ZpbHRlci9GbGF0ZURlY29kZS9GaXJzdCA5L0xlbmd0aCAxNzYvTiAyL1R5cGUvT2JqU3RtPj5zdHJlYW0NCmjehE9BCoNADPxKXmDWWm0PslCleCgFUW/iYamhCNbI7gr29921Z9tDApmZTDIRCIghiSBNMedlshDibehNGzui6vBO/aAyXlsRCPB18C08BqLD5j0TlupJRkq3ftF2R5iNRP0Ol/NkabIGEn8Qc83zjvLXK6XSzgSizaMiw4t+kNkyjazrWT3ID7WAs5dIidfVFrVV1uOFw09f3DEVexgENnp4/Ysu5UeAAQDvyVbwDWVuZHN0cmVhbQ1lbmRvYmoNMSAwIG9iag08PC9NZXRhZGF0YSAyIDAgUi9QYWdlcyAzIDAgUi9UeXBlL0NhdGFsb2c+Pg1lbmRvYmoNMiAwIG9iag08PC9MZW5ndGggMzUwOC9TdWJ0eXBlL1hNTC9UeXBlL01ldGFkYXRhPj5zdHJlYW0NCjw/eHBhY2tldCBiZWdpbj0i77u/IiBpZD0iVzVNME1wQ2VoaUh6cmVTek5UY3prYzlkIj8+Cjx4OnhtcG1ldGEgeG1sbnM6eD0iYWRvYmU6bnM6bWV0YS8iIHg6eG1wdGs9IkFkb2JlIFhNUCBDb3JlIDUuMi1jMDAxIDYzLjEzOTQzOSwgMjAxMC8wOS8yNy0xMzozNzoyNiAgICAgICAgIj4KICAgPHJkZjpSREYgeG1sbnM6cmRmPSJodHRwOi8vd3d3LnczLm9yZy8xOTk5LzAyLzIyLXJkZi1zeW50YXgtbnMjIj4KICAgICAgPHJkZjpEZXNjcmlwdGlvbiByZGY6YWJvdXQ9IiIKICAgICAgICAgICAgeG1sbnM6eG1wPSJodHRwOi8vbnMuYWRvYmUuY29tL3hhcC8xLjAvIj4KICAgICAgICAgPHhtcDpNb2RpZnlEYXRlPjIwMTItMDktMDlUMTQ6MDc6MDQtMDQ6MDA8L3htcDpNb2RpZnlEYXRlPgogICAgICAgICA8eG1wOkNyZWF0ZURhdGU+MjAxMi0wOS0wOVQxNDowNzowNC0wNDowMDwveG1wOkNyZWF0ZURhdGU+CiAgICAgICAgIDx4bXA6TWV0YWRhdGFEYXRlPjIwMTItMDktMDlUMTQ6MDc6MDQtMDQ6MDA8L3htcDpNZXRhZGF0YURhdGU+CiAgICAgICAgIDx4bXA6Q3JlYXRvclRvb2w+QWRvYmUgSWxsdXN0cmF0b3IgQ1M2IChNYWNpbnRvc2gpPC94bXA6Q3JlYXRvclRvb2w+CiAgICAgIDwvcmRmOkRlc2NyaXB0aW9uPgogICAgICA8cmRmOkRlc2NyaXB0aW9uIHJkZjphYm91dD0iIgogICAgICAgICAgICB4bWxuczpkYz0iaHR0cDovL3B1cmwub3JnL2RjL2VsZW1lbnRzLzEuMS8iPgogICAgICAgICA8ZGM6Zm9ybWF0PmFwcGxpY2F0aW9uL3BkZjwvZGM6Zm9ybWF0PgogICAgICAgICA8ZGM6dGl0bGU+CiAgICAgICAgICAgIDxyZGY6QWx0PgogICAgICAgICAgICAgICA8cmRmOmxpIHhtbDpsYW5nPSJ4LWRlZmF1bHQiPjI8L3JkZjpsaT4KICAgICAgICAgICAgPC9yZGY6QWx0PgogICAgICAgICA8L2RjOnRpdGxlPgogICAgICA8L3JkZjpEZXNjcmlwdGlvbj4KICAgICAgPHJkZjpEZXNjcmlwdGlvbiByZGY6YWJvdXQ9IiIKICAgICAgICAgICAgeG1sbnM6eG1wTU09Imh0dHA6Ly9ucy5hZG9iZS5jb20veGFwLzEuMC9tbS8iPgogICAgICAgICA8eG1wTU06RG9jdW1lbnRJRD51dWlkOjgzYmQ3M2JlLTY3ZjAtNmY0OC05NzU5LWY3OTFjZjEyNGFkOTwveG1wTU06RG9jdW1lbnRJRD4KICAgICAgICAgPHhtcE1NOkluc3RhbmNlSUQ+dXVpZDozNzU5ZjM2YS04Mjc1LWQ3NDktOThlNi1jOWZmODgxNzc3Njc8L3htcE1NOkluc3RhbmNlSUQ+CiAgICAgIDwvcmRmOkRlc2NyaXB0aW9uPgogICAgICA8cmRmOkRlc2NyaXB0aW9uIHJkZjphYm91dD0iIgogICAgICAgICAgICB4bWxuczpwZGY9Imh0dHA6Ly9ucy5hZG9iZS5jb20vcGRmLzEuMy8iPgogICAgICAgICA8cGRmOlByb2R1Y2VyPkFkb2JlIFBERiBsaWJyYXJ5IDEwLjAxPC9wZGY6UHJvZHVjZXI+CiAgICAgIDwvcmRmOkRlc2NyaXB0aW9uPgogICA8L3JkZjpSREY+CjwveDp4bXBtZXRhPgogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgCjw/eHBhY2tldCBlbmQ9InciPz4NZW5kc3RyZWFtDWVuZG9iag00IDAgb2JqDTw8L0NyZWF0aW9uRGF0ZShEOjIwMTIwOTA5MTQwNzA0LTA0JzAwJykvQ3JlYXRvcihBZG9iZSBJbGx1c3RyYXRvciBDUzYgXChNYWNpbnRvc2hcKSkvTW9kRGF0ZShEOjIwMTIwOTA5MTQwNzA0LTA0JzAwJykvUHJvZHVjZXIoQWRvYmUgUERGIGxpYnJhcnkgMTAuMDEpL1RpdGxlKDIpPj4NZW5kb2JqDTYgMCBvYmoNPDwvRmlsdGVyL0ZsYXRlRGVjb2RlL0xlbmd0aCAxNDY+PnN0cmVhbQ0KSIlEjjESwkAIRXtOwQkIsOyGrS08gEfIqCkSC3P/GVmM41Dw5/P4MF1ujMuBnIXH8oLpGtbzgGEooxi+75B9h0JVOoqGlEbmOvQGwtioqIdcQQLqNQwXH5yjMLU5OUcli6TB6c/fIaLYzo0tBn9IlNgdK1nPsErVG44sC6ammqnHF18kfynnuRUe8BFgACTyLL8NZW5kc3RyZWFtDWVuZG9iag03IDAgb2JqDTw8L0FJUyBmYWxzZS9CTS9Ob3JtYWwvQ0EgMS4wL09QIGZhbHNlL09QTSAxL1NBIHRydWUvU01hc2svTm9uZS9UeXBlL0V4dEdTdGF0ZS9jYSAxLjAvb3AgZmFsc2U+Pg1lbmRvYmoNOCAwIG9iag1bL0lDQ0Jhc2VkIDkgMCBSXQ1lbmRvYmoNOSAwIG9iag08PC9GaWx0ZXIvRmxhdGVEZWNvZGUvTGVu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5Lto2aLzBdYF6oIjhaTCvMKdhbOL4xdvWjxdFFTUVXR9iWBJw5JzS62XVi39pJhZLCs+VEIoyS/ZU/KDLF02KpstlZa+Vzojl8g3yx8qohUDigfKCGW/8l5ZRFl/2X1VhGqj6kF5VPlg+SO1RD2s/rYiqWJ7xbPK9MoPK3+syq86oCFrSjRHtRxtpfZ0tX11Q/UlnZeuSzdZE1azqWZGn6LfWQvVLqk9YuDhP1MXjO7Glcapusi6kbrn9Xn1hxrYDdqGC42ejWsa7zUlNP2mGW2WN59scWxpb5laFrNsRyvUWtp6ss25rbNtenni8l3t1PbK9j91+HX0d3y/In/FsU67zuWdd1cmrtzbZdal77qxKnzV9tXoavXqiTUBa7ased2t6P6ix69nsOeHXnnvF2tFa4fW/riubN1EX3DftvXE9dr11zdEbdjVz+5v6r+7MW3j4QFsoHvg+03Fm84NBg5u30zdbNw8OZT6TwCkAVv+mLiZJJmQmfyaaJrVm0Kbr5wcnImc951kndKeQJ6unx2fi5/6oGmg2KFHobaiJqKWowajdqPmpFakx6U4pammGqaLpv2nbqfgqFKoxKk3qamqHKqPqwKrdavprFys0K1ErbiuLa6hrxavi7AAsHWw6rFgsdayS7LCszizrrQltJy1E7WKtgG2ebbwt2i34LhZuNG5SrnCuju6tbsuu6e8IbybvRW9j74KvoS+/796v/XAcMDswWfB48JfwtvDWMPUxFHEzsVLxcjGRsbDx0HHv8g9yLzJOsm5yjjKt8s2y7bMNcy1zTXNtc42zrbPN8+40DnQutE80b7SP9LB00TTxtRJ1MvVTtXR1lXW2Ndc1+DYZNjo2WzZ8dp22vvbgNwF3IrdEN2W3hzeot8p36/gNuC94UThzOJT4tvjY+Pr5HPk/OWE5g3mlucf56noMui86Ubp0Opb6uXrcOv77IbtEe2c7ijutO9A78zwWPDl8XLx//KM8xnzp/Q09ML1UPXe9m32+/eK+Bn4qPk4+cf6V/rn+3f8B/yY/Sn9uv5L/tz/bf//AgwA94Tz+w1lbmRzdHJlYW0NZW5kb2JqDTExIDAgb2JqDTw8L0RlY29kZVBhcm1zPDwvQ29sdW1ucyA0L1ByZWRpY3RvciAxMj4+L0ZpbHRlci9GbGF0ZURlY29kZS9JRFs8RENCOUY3NzhFNjg4NEUxNzhCODJCNDA0QzRBREVERUE+PEQ3RjE2RjUzMzcxMjRERDNBNjZDNTZDNkVBNEFBQzE2Pl0vSW5mbyA0IDAgUi9MZW5ndGggNjEvUm9vdCAxIDAgUi9TaXplIDEyL1R5cGUvWFJlZi9XWzEgMiAxXT4+c3RyZWFtDQpo3mJiAAImRkZZBiYGBhsg6/9GBqb//P5A1seNjEz/BZj+AyWuAWUZC0BKFIHE+7lAQnoXA0CAAQAoXgr/DWVuZHN0cmVhbQ1lbmRvYmoNc3RhcnR4cmVmDTcxMTQNJSVFT0YN"

def count_messages(account):
	imap = None
	try:
		imap = imaplib.IMAP4_SSL(account["hostname"])
		imap.login(account["username"], account["password"])
		imap.select("Inbox")
		typ, messages = imap.search(None, "UNSEEN")
		if len(messages) > 1:
			account["messages"] = len(messages)
		elif len(messages[0]) > 0:
			account["messages"] = 1
	except:
		return
	finally:
		if imap is not None:
			imap.close()

total = 0
for account in accounts:
	count_messages(account)
	total = total + account["messages"]

if total > 0:
	print("%d %s" % (total, ICON))
else:
	print(ICON)

print("---")

for account in accounts:
	print("%d %s" % (account["messages"], account["friendly"]))
