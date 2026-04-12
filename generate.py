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

# Extract metadata using shared utility (returns files sorted by title)
sorted_files, recipe_titles, recipe_subtitles, recipe_tags, all_tags = extract_recipe_metadata("recipes")

# Write recipe list (sorted by title)
f = open("build/recipelist.json", "w")
f.write(json.dumps(sorted_files))
f.close()

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
