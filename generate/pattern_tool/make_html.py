definition = {
    "radius": 50,
    "gap": 10,
    "ux": 100,
    "uy": 100
}

size = 16

indent = "    "

definition["rect_size"] = 2 * (definition["radius"] + definition["gap"]) * size

pattern = [["#808080" for i in range(0, size)] for j in range(0, size)]

with open('pattern_tool.html', 'w', encoding='utf-8') as fh:
    fh.write("""<!DOCTYPE html>
<html>
<body>
<script src="script.js"></script>
<link rel="stylesheet" href="styles.css">
<div>
    <svg width="600px" height="600px" viewBox="100 100 2000 2000"
        xmlns="http://www.w3.org/2000/svg" version="1.1">
        <desc>One 8x8 LED matrix</desc>

        <rect x="%(ux)i" y="%(uy)i" width="%(rect_size)i" height="%(rect_size)i" fill="black" stroke="black" stroke-width="0"/>""" % definition)

    dots = "\n"
    for i in range(0, size):
        for j in range(0, size):
            dots += f"{indent*2}"
            dots += """<circle id="%(id)s" cx="%(ux)i" cy="%(uy)i" r="%(radius)i" fill="%(color)s" stroke="black" onclick="%(onclick)s" stroke-width="0"  />\n""" % {
                "ux": definition["ux"] + (j + 1 / 2) * 2 * (definition["radius"] + definition["gap"]),
                "uy": definition["uy"] + (i + 1 / 2) * 2 * (definition["radius"] + definition["gap"]),
                "radius": definition["radius"],
                "color": pattern[j][i],
                "onclick": "clickOnDot(" + str(i + 1) + ", " + str(j + 1) + ")",
                "id": str(i + 1) + "_" + str(j + 1)
            }
    dots += f"{indent}</svg>"
    fh.write(dots)
    # end make display svg
    fh.write("""
    <div>
        <textarea id="textarea" rows="4" cols="50"></textarea>
        <div id="btns">
            <button id="btn-update" onclick="update()">update</button>
            <button id="btn-clear" onclick="clearAllLeds()">clear all</button>
            <button id="btn-copy" onclick="copy()">copy</button>
        </div>
    </div>
""")
    fh.write("</div></body></html>")