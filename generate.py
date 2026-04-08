#!/usr/bin/python3
import os, json, shutil
import re

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

# Extract tags from each recipe
recipe_tags = {}
all_tags = set()

for filename in sorted_files:
    filepath = os.path.join("recipes", filename)
    # Try to find the original file (it might have different casing)
    if not os.path.exists(filepath):
        # Find the file with case-insensitive match
        for f in os.listdir("recipes"):
            if f.lower() == filename:
                filepath = os.path.join("recipes", f)
                break
    
    if os.path.exists(filepath):
        try:
            with open(filepath, 'r', encoding='utf-8') as file:
                content = file.read()
                # Look for Tags: section
                tag_match = re.search(r'Tags:\s*\n\s*(.+)', content)
                if tag_match:
                    tags_str = tag_match.group(1)
                    tags = [tag.strip() for tag in tags_str.split(',')]
                    recipe_tags[filename.replace('.md', '')] = tags
                    all_tags.update(tags)
        except Exception as e:
            print(f"Error reading {filepath}: {e}")

# Write tags data
tags_file = open("build/recipe-tags.json", "w")
tags_file.write(json.dumps({
    "recipes": recipe_tags,
    "allTags": sorted(list(all_tags))
}))
tags_file.close()
