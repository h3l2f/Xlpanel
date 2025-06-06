#type: ignore
import sass
import os

wdir = "sass"
tgpath = os.path.join("..", "assets", "css")
os.chdir(wdir)
s = os.listdir()


for i in s:
    if i[0]=="_": continue
    print(f"--- Woring on {i}: ", end="")
    with open(i) as f: ctn = f.read()
    try:
        css = sass.compile(string=ctn, output_style='expanded')
        with open(os.path.join(tgpath, i.split(".")[0]+".css"), "w+") as f: f.write(css)
        print("Done ---")
    except sass.CompileError as e:
        print(f"Sass Compile Error: {e}")