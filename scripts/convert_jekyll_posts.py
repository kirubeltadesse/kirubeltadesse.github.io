#!/usr/bin/env python3
"""
Convert Jekyll posts to Quarto format
Adapted from EdwardJRoss/hugo2quarto approach for Jekyll->Quarto conversion
"""

import os
import re
import yaml
from pathlib import Path
from datetime import datetime

def extract_jekyll_frontmatter(content):
    """Extract YAML frontmatter from Jekyll post"""
    if not content.startswith('---\n'):
        return {}, content
    
    # Find the end of frontmatter
    end_match = re.search(r'\n---\n', content[4:])
    if not end_match:
        return {}, content
    
    end_pos = end_match.start() + 4
    frontmatter_str = content[4:end_pos]
    body = content[end_pos + 5:]  # +5 for "\n---\n"
    
    try:
        frontmatter = yaml.safe_load(frontmatter_str)
        return frontmatter or {}, body
    except yaml.YAMLError:
        return {}, content

def convert_frontmatter(jekyll_fm):
    """Convert Jekyll frontmatter to Quarto format"""
    quarto_fm = {}
    
    # Direct mappings
    direct_maps = {
        'title': 'title',
        'date': 'date', 
        'author': 'author',
        'draft': 'draft',
        'description': 'description'
    }
    
    for jekyll_key, quarto_key in direct_maps.items():
        if jekyll_key in jekyll_fm:
            quarto_fm[quarto_key] = jekyll_fm[jekyll_key]
    
    # Convert tags to categories
    if 'tags' in jekyll_fm:
        quarto_fm['categories'] = jekyll_fm['tags']
    elif 'categories' in jekyll_fm:
        quarto_fm['categories'] = jekyll_fm['categories']
    
    # Convert featured image
    if 'feature_image' in jekyll_fm:
        quarto_fm['image'] = jekyll_fm['feature_image']
    elif 'image' in jekyll_fm:
        quarto_fm['image'] = jekyll_fm['image']
    
    return quarto_fm

def convert_post_content(content):
    """Convert Jekyll-specific content to Quarto format"""
    
    # Convert Jekyll liquid tags (basic conversion)
    content = re.sub(r'{%\s*highlight\s+(\w+)\s*%}', r'```\1', content)
    content = re.sub(r'{%\s*endhighlight\s*%}', '```', content)
    
    # Convert Jekyll image includes to markdown
    content = re.sub(
        r'{%\s*include\s+figure\.html\s+path="([^"]+)"\s+alt="([^"]*)"\s*%}',
        r'![\2](\1)',
        content
    )
    
    # Convert Jekyll link references
    content = re.sub(r'{{ site\.url }}{{ site\.baseurl }}', '', content)
    content = re.sub(r'{{ site\.url }}', '', content)
    content = re.sub(r'{{ site\.baseurl }}', '', content)
    
    return content

def convert_jekyll_post(input_path, output_dir):
    """Convert a single Jekyll post to Quarto format"""
    
    with open(input_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Extract and convert frontmatter
    jekyll_fm, body = extract_jekyll_frontmatter(content)
    quarto_fm = convert_frontmatter(jekyll_fm)
    
    # Convert content
    converted_body = convert_post_content(body)
    
    # Create output filename based on input
    input_stem = Path(input_path).stem
    
    # Remove date prefix if present (Jekyll style: YYYY-MM-DD-title.md)
    date_pattern = r'^\d{4}-\d{2}-\d{2}-'
    if re.match(date_pattern, input_stem):
        input_stem = re.sub(date_pattern, '', input_stem)
    
    output_path = Path(output_dir) / f"{input_stem}.qmd"
    
    # Write Quarto post
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write('---\n')
        yaml.dump(quarto_fm, f, default_flow_style=False, sort_keys=False)
        f.write('---\n\n')
        f.write(converted_body)
    
    print(f"Converted: {input_path} -> {output_path}")
    return output_path

def convert_all_posts(posts_dir, output_dir):
    """Convert all Jekyll posts in a directory"""
    
    posts_path = Path(posts_dir)
    if not posts_path.exists():
        print(f"Posts directory {posts_dir} does not exist")
        return
    
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    converted_files = []
    
    for post_file in posts_path.glob('*.md'):
        try:
            converted_file = convert_jekyll_post(post_file, output_dir)
            converted_files.append(converted_file)
        except Exception as e:
            print(f"Error converting {post_file}: {e}")
    
    print(f"\nConverted {len(converted_files)} posts")
    return converted_files

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) != 3:
        print("Usage: python convert_jekyll_posts.py <jekyll_posts_dir> <quarto_posts_dir>")
        print("Example: python convert_jekyll_posts.py _posts blog/posts")
        sys.exit(1)
    
    jekyll_posts_dir = sys.argv[1]
    quarto_posts_dir = sys.argv[2]
    
    convert_all_posts(jekyll_posts_dir, quarto_posts_dir)