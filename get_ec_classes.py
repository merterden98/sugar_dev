SITE = "https://www.kegg.jp/kegg/annotation/br01800.html"


import requests
# Fetch the website SITE and retrieve the HTML table 

data = requests.get(SITE).text

# Grab all text between <table> and </table> and store it in a list

l = data.split("<table>")[1].split("</table>")[0].split("\n")
print(l[10])
