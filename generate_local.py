#!/usr/bin/python3
"""
Local development script that generates build files with image compression.
Use this locally to test the full site with compressed images.
For deployment, the GitHub Actions pipeline handles compression automatically.
"""
import os, json, shutil
import re
from PIL import Image
from recipe_utils import extract_recipe_metadata

if os.path.exists("build"):
    shutil.rmtree("build")
os.mkdir("build")
shutil.copytree("recipes", "build/recipes")
shutil.copytree("images", "build/images")
shutil.copy2("index.html", "build")
shutil.copy2("recipe.html", "build")
shutil.copy2("stylesheet.css", "build")

# Compress images to WebP and create thumbnails
print("Compressing images to WebP...")

image_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.webp']
for img_file in os.listdir("build/images"):
    img_path = os.path.join("build/images", img_file)
    if os.path.isfile(img_path):
        file_ext = os.path.splitext(img_file)[1].lower()
        if file_ext in image_extensions:
            try:
                filename_without_ext = os.path.splitext(img_file)[0]
                img = Image.open(img_path)
                
                # Convert/re-compress to WebP
                webp_path = os.path.join("build/images", filename_without_ext + ".webp")
                img.save(webp_path, "WEBP", quality=85)
                file_size_kb = os.path.getsize(webp_path) / 1024
                print(f"✓ {filename_without_ext}.webp ({file_size_kb:.1f}KB)")
                
                # Create thumbnail
                thumb = img.copy()
                thumb.thumbnail((100, 100), Image.Resampling.LANCZOS)
                thumb_path = os.path.join("build/images", filename_without_ext + "-thumbnail.webp")
                thumb.save(thumb_path, "WEBP", quality=85)
            except Exception as e:
                print(f"✗ Error processing {img_file}: {e}")

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

print("\n✓ Build complete!")
print("To view locally, run: python -m http.server 8000 --directory build")
print("Then open: http://localhost:8000")
