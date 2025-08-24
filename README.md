# kirubeltadesse.github.io

[![Hugo site CI](https://github.com/kirubeltadesse/kirubeltadesse.github.io/actions/workflows/hugo.yml/badge.svg)](https://github.com/kirubeltadesse/kirubeltadesse.github.io/actions/workflows/hugo.yml)

Personal website built with Hugo - a fast and modern static site generator.

## Development

This site is built using [Hugo](https://gohugo.io/). To run locally:

1. Install Hugo (extended version)
2. Clone this repository
3. Run `hugo server` to start the development server
4. Visit `http://localhost:1313` to view the site

## Building

- `hugo` - Build the site for production
- `hugo server` - Start development server with live reload
- `hugo server --buildDrafts` - Include draft content

## Deployment

The site is automatically deployed to GitHub Pages via GitHub Actions when changes are pushed to the main branch.

## Content Structure

- `content/_index.md` - Home page content
- `content/about/` - About page
- `content/projects/` - Project pages
- `content/gallery/` - Photo gallery
- `content/news/` - News items
- `static/` - Static assets (CSS, JS, images)
- `layouts/` - Hugo templates and partials
