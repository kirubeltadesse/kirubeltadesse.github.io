# kirubeltadesse.github.io

[![Jekyll site CI](https://github.com/kirubeltadesse/kirubeltadesse.github.io/actions/workflows/jekyll.yml/badge.svg)](https://github.com/kirubeltadesse/kirubeltadesse.github.io/actions/workflows/jekyll.yml)

Hello! `Gemfile` is where you manage which Jekyll version is used to run.
When you want to use a different version, change it below, save the
file and run `bundle install`. Run Jekyll with `bundle exec`, like so:

- `jekyll build` - Performs a one-off build your site to
- `bundle exec jekyll serve` - Builds your site anytime a source file changes and serves it locally
- `jekyll serve` - Builds your site anytime a source file changes and serves it locally. You can also specify flags as `jekyll serve` --host 0.0.0.0 --port 4001` to serve on a different port or host.

This will help ensure the proper Jekyll version is running.
Happy Jekylling!

Note: general configuration is in `_config.yml` and the theme is in `_layouts/default.html`

## News pages

- News pages are in `_news/` directory
- News pages are sorted by date, so the most recent news is at the top
- News pages are in markdown format
- News pages are named `YYYY-MM-DD-title.md` where `YYYY-MM-DD` is the date of the news item and `title` is the title of the news item
- News pages have the following front matter:

```
---
layout: post
date: 2023-12-25 15:59:00-0400
inline: false
title: new news website
---
```

- `layout: post` is required
- `date` is required and should be in the format above and the date should be in the past
- `inline: false` is required and should be set to `false` if you want the news item to be displayed on the news page, otherwise set to `true`
- `title` is required and should be the title of the news item

## Gallery pages

- Gallery pages are in `_pages/gallery.md` directory
  NOTE: you can have different size of the images by playing with class ["col-sm-4" "col-sm-8"] will result in 1/2 ...
  rename the caption and image titles in the page
