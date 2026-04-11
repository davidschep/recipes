#!/usr/bin/python3
import os, json, shutil
import re
from recipe_utils import extract_recipe_metadata

if os.path.exists("build"):
    shutil.rmtree("build")
os.mkdir("build")
shutil.copytree("recipes", "build/recipes")
shutil.copytree("images", "build/images")
shutil.copy2("index.html", "build")
shutil.copy2("recipe.html", "build")
shutil.copy2("stylesheet.css", "build")

# Normalize all filenames to lowercase for consistency
files = [f.lower() for f in os.listdir("recipes")]
sorted_files = sorted(files)

# Write recipe list
f = open("build/recipelist.json", "w")
f.write(json.dumps(sorted_files))
f.close()

# Extract metadata using shared utility
recipe_titles, recipe_subtitles, recipe_tags, all_tags = extract_recipe_metadata("recipes")

# Write metadata (titles and tags)
metadata_file = open("build/recipe-metadata.json", "w")
metadata_file.write(json.dumps({
    "titles": recipe_titles,
    "subtitles": recipe_subtitles
}))
metadata_file.close()

# Write tags data
tags_file = open("build/recipe-tags.json", "w")
tags_file.write(json.dumps({
    "recipes": recipe_tags,
    "allTags": all_tags
}))
tags_file.close()
