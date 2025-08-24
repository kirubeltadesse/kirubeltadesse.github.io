# Jekyll to Quarto Migration Guide

This repository now supports both Jekyll and Quarto for a hybrid blogging experience:

- **Jekyll**: Handles the main academic portfolio site (about, projects, gallery, etc.)
- **Quarto**: Powers the blog with modern features like executable code blocks, mathematical typesetting, and interactive content

## Structure

```
├── _quarto.yml           # Quarto configuration
├── index.qmd             # Main Quarto landing page 
├── blog/
│   ├── index.qmd         # Blog listing page
│   └── posts/            # Individual blog posts (.qmd files)
├── scripts/
│   └── convert_jekyll_posts.py  # Jekyll to Quarto converter
├── _config.yml           # Jekyll configuration (unchanged)
├── _includes/            # Jekyll includes (updated nav)
├── _layouts/             # Jekyll layouts 
└── _pages/               # Jekyll pages
```

## Features

### Quarto Blog Features
- **Executable code blocks**: Run Python, R, Julia code directly
- **Mathematical typesetting**: LaTeX equations render beautifully
- **Modern layouts**: Responsive, clean design
- **Search**: Built-in site search
- **Categories**: Automatic post categorization
- **RSS feeds**: Generated automatically

### Jekyll Portfolio Features  
- **Academic theme**: al-folio theme for academic portfolios
- **Project galleries**: Showcase your work
- **Social integration**: Connect with academic networks
- **Customizable**: Extensive theming options

## Usage

### Creating New Blog Posts

Create `.qmd` files in `blog/posts/` with frontmatter:

```yaml
---
title: "Your Post Title"
author: "Kirubel Tadesse" 
date: "2024-08-24"
categories: [data-science, python]
description: "Brief description"
---

Your content here with executable code:

```python
import pandas as pd
print("Hello from Quarto!")
```

### Converting Existing Jekyll Posts

Use the conversion script:

```bash
python scripts/convert_jekyll_posts.py _posts blog/posts
```

This script:
- Converts YAML frontmatter from Jekyll to Quarto format
- Maps Jekyll tags to Quarto categories  
- Converts basic Jekyll liquid tags to markdown
- Handles image references

### Building the Site

The site builds automatically via GitHub Actions with both:
1. **Quarto render**: Generates the blog
2. **Jekyll build**: Generates the portfolio

For local development:

```bash
# Render Quarto blog
quarto render

# Or use preview with live reload
quarto preview
```

## Configuration

### Quarto Configuration (`_quarto.yml`)
- Website metadata and navigation
- Theme and styling options  
- Code execution settings
- Search and RSS configuration

### Jekyll Configuration (`_config.yml`)
- Unchanged from original al-folio setup
- Academic portfolio settings
- Social media integration
- Collections for projects/news

## Customization

### Styling
- Edit `custom.scss` for Quarto theme customization
- Existing Jekyll CSS remains in `assets/css/`

### Navigation
- Quarto nav in `_quarto.yml`
- Jekyll nav in `_includes/header.html` (updated to include blog link)

### Layouts
- Quarto uses built-in responsive layouts
- Jekyll layouts preserved in `_layouts/`

## Deployment

The GitHub Actions workflow:
1. Sets up Quarto
2. Renders Quarto content to `_site`
3. Builds Jekyll site (which can include Quarto output)
4. Deploys combined site

## Benefits of This Hybrid Approach

1. **Best of both worlds**: Academic portfolio + modern blogging
2. **Gradual migration**: Can migrate content incrementally  
3. **Executable content**: Code blocks run and display output
4. **Maintained URLs**: All existing links continue to work
5. **Rich features**: Search, categories, RSS, math, etc.

## Future Migration Options

If you want to fully migrate to Quarto later:
1. Convert remaining Jekyll pages to `.qmd`
2. Update `_quarto.yml` with full site structure
3. Remove Jekyll configuration and build steps
4. Use pure Quarto website features

The conversion script provides a starting point for bulk migration of content.