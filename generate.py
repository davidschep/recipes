#!/usr/bin/python3
import os, json, shutil
if os.path.exists("build"):
    shutil.rmtree("build")
os.mkdir("build")
shutil.copytree("recipes", "build/recipes")
shutil.copytree("images", "build/images")
shutil.copy2("index.html", "build")
shutil.copy2("recipe.html", "build")
shutil.copy2("stylesheet.css", "build")
f = open("build/recipelist.json", "w")
# Normalize all filenames to lowercase for consistency
files = [f.lower() for f in os.listdir("recipes")]
f.write(json.dumps(sorted(files)))
