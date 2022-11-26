html_file = open("index.html", "w+")
html_file.write(
"""<!DOCTYPE html>
<html>
<head>
<title>RQ1 Experiments</title>
<script>
function submit() {
let results = []
Array.from(document.getElementsByClassName('input')).forEach((el) => results.push(el.value))
navigator.clipboard.writeText(results.join(","));
}
</script>
</head>
<body style="background-color:black; color:white; font-size: 1.2em">

"""
)

samples_file = open("./samples_for_vis.txt")
c = 1
for line in samples_file:
    parts = line.split(" ")
    try:
        src = "./visualization/"+parts[0].replace("/", "_")+"/"+parts[1]+"/"+parts[2]+"_"+parts[3].replace("\n", "")+".png"
        open(src, "r")
        html_file.write("<br><br>")
        html_file.write("DP#"+str(c)+": <a target=\"_blank\" href=\""+"https://github.com/"+parts[0]+"/commit/"+parts[1]+"\">Link</a>\n")
        html_file.write("<h3>File: "+parts[2]+"</h2>\n")
        html_file.write("<h3>Scope: "+parts[3].replace("\n", "")+"</h3>\n")
        html_file.write("<img src=\""+src+"\">\n\n")
        html_file.write("<br><br>")
        html_file.write("<img src=\"./screenshots/"+str(c)+".png\">\n\n")
        html_file.write("<br><br>")
        html_file.write("Select the rank? <select class=\"input\">")
        html_file.write("<option value=\"1\">1</option>")
        html_file.write("<option value=\"2\">2</option>")
        html_file.write("<option value=\"3\">3</option>")
        html_file.write("<option value=\"4\">4</option>")
        html_file.write("<option value=\"5\">5</option>")
        html_file.write("<option value=\">5\">>5</option>")
        html_file.write("</select>")
        html_file.write("<br><br>")
        html_file.write("<br><br>\n")
        c+=1
    except:
        pass

html_file.write(
"""
<input type="submit" value="Copy Results" onclick="submit();"/>
<br><br>
</body>
</html>
"""
)