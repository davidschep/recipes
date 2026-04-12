#!/usr/bin/python3
"""Shared utilities for recipe metadata extraction"""
import os
import re


def extract_recipe_metadata(recipes_dir):
    """
    Extract titles, subtitles, and tags from recipe files.
    Sorts files by their extracted titles.
    
    Returns a tuple of (sorted_files, recipe_titles, recipe_subtitles, recipe_tags, all_tags)
    where sorted_files is the list of filenames sorted by their titles.
    """
    # Get all recipe files (normalized to lowercase)
    files = [f.lower() for f in os.listdir(recipes_dir)]
    files = sorted(files)
    
    recipe_tags = {}
    recipe_titles = {}
    recipe_subtitles = {}
    all_tags = set()
    
    for filename in files:
        filepath = os.path.join(recipes_dir, filename)
        # Try to find the original file (it might have different casing)
        if not os.path.exists(filepath):
            # Find the file with case-insensitive match
            for f in os.listdir(recipes_dir):
                if f.lower() == filename:
                    filepath = os.path.join(recipes_dir, f)
                    break
        
        if os.path.exists(filepath):
            try:
                with open(filepath, 'r', encoding='utf-8') as file:
                    content = file.read()
                    lines = content.split('\n')
                    
                    # Extract title (first line, remove markdown heading markers)
                    first_line = lines[0] if lines else ""
                    full_title = re.sub(r'^#+\s+', '', first_line).strip() if first_line else filename
                    
                    # Parse title and subtitle from parentheses
                    # Format: "Title (subtitle)" or just "Title"
                    anchor = filename.replace('.md', '')
                    match = re.match(r'^(.+?)\s*\(([^)]+)\)\s*$', full_title)
                    if match:
                        title = match.group(1).strip()
                        subtitle = match.group(2).strip()
                        recipe_titles[anchor] = title
                        recipe_subtitles[anchor] = subtitle
                    else:
                        # No subtitle found
                        recipe_titles[anchor] = full_title
                        recipe_subtitles[anchor] = None
                    
                    # Look for Tags: section
                    tag_match = re.search(r'Tags:\s*\n\s*(.+)', content)
                    if tag_match:
                        tags_str = tag_match.group(1)
                        tags = [tag.strip() for tag in tags_str.split(',')]
                        recipe_tags[anchor] = tags
                        all_tags.update(tags)
            except Exception as e:
                print(f"Error reading {filepath}: {e}")
    
    # Sort files by their titles (case-insensitive)
    sorted_files = sorted(
        [f.replace('.md', '') for f in files],
        key=lambda anchor: recipe_titles.get(anchor, anchor).lower()
    )
    
    return sorted_files, recipe_titles, recipe_subtitles, recipe_tags, sorted(list(all_tags))
