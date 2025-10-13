# CI/CD Deployment Guide for Hugo

This document provides comprehensive information about CI/CD solutions for automatically building and deploying this Hugo website.

## Table of Contents

1. [GitHub Actions (Current Solution)](#github-actions-current-solution)
2. [Buddy CI/CD](#buddy-cicd)
3. [GitLab CI/CD](#gitlab-cicd)
4. [Netlify](#netlify)
5. [Vercel](#vercel)
6. [Cloudflare Pages](#cloudflare-pages)
7. [AWS Amplify](#aws-amplify)
8. [Best Practices](#best-practices)

## GitHub Actions (Current Solution)

**Status:** ✅ Currently configured and working

### Overview

GitHub Actions is the recommended CI/CD solution for this repository because:
- Native integration with GitHub Pages
- No external service dependencies
- Free for public repositories
- Comprehensive workflow control

### Configuration File

Location: `.github/workflows/hugo.yml`

```yaml
name: Deploy Hugo site to Pages

on:
  push:
    branches: [ master, main ]
  pull_request:
    branches: [ master, main ]
  workflow_dispatch:

permissions:
  contents: read
  pages: write
  id-token: write

concurrency:
  group: "pages"
  cancel-in-progress: false

jobs:
  build:
    runs-on: ubuntu-latest
    env:
      HUGO_VERSION: 0.134.3
    steps:
      - name: Checkout
        uses: actions/checkout@v4
        with:
          submodules: recursive
          fetch-depth: 0

      - name: Setup Hugo
        run: |
          wget -O ${{ runner.temp }}/hugo.deb https://github.com/gohugoio/hugo/releases/download/v${HUGO_VERSION}/hugo_extended_${HUGO_VERSION}_linux-amd64.deb \
          && sudo dpkg -i ${{ runner.temp }}/hugo.deb

      - name: Setup Pages
        id: pages
        uses: actions/configure-pages@v5

      - name: Build with Hugo
        env:
          HUGO_CACHEDIR: ${{ runner.temp }}/hugo_cache
          HUGO_ENVIRONMENT: production
        run: |
          hugo \
            --gc \
            --minify \
            --baseURL "${{ steps.pages.outputs.base_url }}/"

      - name: Upload artifact
        uses: actions/upload-pages-artifact@v3
        with:
          path: ./public

  deploy:
    environment:
      name: github-pages
      url: ${{ steps.deployment.outputs.page_url }}
    runs-on: ubuntu-latest
    needs: build
    if: github.ref == 'refs/heads/master' || github.ref == 'refs/heads/main'
    steps:
      - name: Deploy to GitHub Pages
        id: deployment
        uses: actions/deploy-pages@v4
```

### Setup Instructions

1. Ensure the workflow file exists at `.github/workflows/hugo.yml`
2. Go to **Repository Settings** → **Pages**
3. Set **Source** to "GitHub Actions"
4. Push changes to trigger deployment

### Customization Options

- **Hugo Version**: Update `HUGO_VERSION` environment variable
- **Build Flags**: Modify the `hugo` command in the build step
- **Branches**: Change trigger branches in the `on.push.branches` section
- **Manual Triggers**: Use workflow_dispatch to trigger manually from Actions tab

## Buddy CI/CD

**Status:** 📝 Configuration file included (`buddy.yml`)

### Overview

Buddy is a powerful CI/CD platform with:
- Visual pipeline builder
- Fast Docker-based builds
- Multiple deployment targets
- Simple YAML configuration

### Configuration File

Location: `buddy.yml`

```yaml
- pipeline: "Build and Deploy Hugo site"
  trigger_mode: "ON_EVERY_PUSH"
  ref_name: "master"
  actions:
    - action: "Execute: hugo build"
      type: "BUILD"
      docker_image_name: "klakegg/hugo"
      docker_image_tag: "0.134.3-ext-alpine"
      execute_commands:
        - "hugo --gc --minify"
      cached_dirs:
        - "/tmp/hugo_cache"
      
    - action: "Deploy to GitHub Pages"
      type: "GITHUB_PAGES"
      local_path: "public"
      remote_path: "/"
      deployment_excludes:
        - ".git*"
        - "*.md"
```

### Setup Instructions

1. Sign up at [buddy.works](https://buddy.works)
2. Create a new project and connect your GitHub repository
3. Buddy will automatically detect the `buddy.yml` file
4. Configure GitHub Pages deployment:
   - Add GitHub integration
   - Set up deployment action to push to gh-pages branch
5. Run the pipeline

### Deployment Targets

Buddy supports multiple deployment targets:
- GitHub Pages (gh-pages branch)
- AWS S3
- Google Cloud Storage
- Azure Storage
- FTP/SFTP servers
- Custom Docker containers

## GitLab CI/CD

**Status:** 📋 Template available

### Configuration

Create `.gitlab-ci.yml` in repository root:

```yaml
image: klakegg/hugo:0.134.3-ext-alpine

variables:
  GIT_SUBMODULE_STRATEGY: recursive

pages:
  script:
    - hugo --gc --minify
  artifacts:
    paths:
      - public
  only:
    - master
    - main
  cache:
    paths:
      - .cache
```

### Setup Instructions

1. Push repository to GitLab
2. Add `.gitlab-ci.yml` file
3. Pipeline runs automatically
4. Site deployed to GitLab Pages at `https://username.gitlab.io/project-name`

### Features

- Built-in GitLab Pages integration
- Free CI/CD minutes for public projects
- Docker-based builds
- Artifacts caching

## Netlify

**Status:** 📋 Template available

### Configuration

Create `netlify.toml` in repository root:

```toml
[build]
  publish = "public"
  command = "hugo --gc --minify"

[build.environment]
  HUGO_VERSION = "0.134.3"
  HUGO_ENV = "production"
  HUGO_ENABLEGITINFO = "true"

[context.production.environment]
  HUGO_ENV = "production"

[context.deploy-preview]
  command = "hugo --gc --minify --buildFuture -b $DEPLOY_PRIME_URL"

[context.branch-deploy]
  command = "hugo --gc --minify -b $DEPLOY_PRIME_URL"

[[redirects]]
  from = "/*"
  to = "/404.html"
  status = 404
```

### Setup Instructions

1. Sign up at [netlify.com](https://netlify.com)
2. Click "New site from Git"
3. Connect GitHub repository
4. Netlify auto-detects Hugo
5. Deploy automatically on every push

### Features

- Automatic HTTPS
- Deploy previews for pull requests
- Form handling
- Serverless functions
- CDN distribution
- Custom domains

## Vercel

**Status:** 📋 No configuration needed

### Setup Instructions

1. Sign up at [vercel.com](https://vercel.com)
2. Click "Import Project"
3. Select GitHub repository
4. Vercel auto-detects Hugo
5. Click "Deploy"

### Configuration (Optional)

Create `vercel.json` for advanced settings:

```json
{
  "build": {
    "env": {
      "HUGO_VERSION": "0.134.3"
    }
  }
}
```

### Features

- Zero configuration
- Automatic HTTPS
- Preview deployments
- Edge network
- Serverless functions
- Analytics

## Cloudflare Pages

**Status:** 📋 Template available

### Setup Instructions

1. Go to [Cloudflare Pages](https://pages.cloudflare.com)
2. Connect GitHub repository
3. Configure build settings:
   - **Build command**: `hugo --gc --minify`
   - **Build output directory**: `public`
   - **Environment variable**: `HUGO_VERSION = 0.134.3`
4. Deploy

### Features

- Global CDN
- Unlimited bandwidth
- Automatic HTTPS
- Preview deployments
- Web Analytics
- Workers integration

## AWS Amplify

**Status:** 📋 Template available

### Configuration

Create `amplify.yml`:

```yaml
version: 1
frontend:
  phases:
    preBuild:
      commands:
        - wget https://github.com/gohugoio/hugo/releases/download/v0.134.3/hugo_extended_0.134.3_Linux-64bit.tar.gz
        - tar -xf hugo_extended_0.134.3_Linux-64bit.tar.gz
        - mv hugo /usr/bin/hugo
        - rm hugo_extended_0.134.3_Linux-64bit.tar.gz
        - hugo version
    build:
      commands:
        - hugo --gc --minify
  artifacts:
    baseDirectory: public
    files:
      - '**/*'
  cache:
    paths:
      - node_modules/**/*
```

### Setup Instructions

1. Sign in to AWS Console
2. Go to AWS Amplify
3. Click "New app" → "Host web app"
4. Connect GitHub repository
5. AWS detects Hugo automatically
6. Deploy

### Features

- AWS infrastructure
- Custom domains
- HTTPS
- Preview environments
- Password protection
- Monitoring

## Best Practices

### 1. Version Pinning

Always specify exact Hugo version:
```yaml
HUGO_VERSION: 0.134.3
```

### 2. Use Hugo Extended

If your theme requires SCSS:
```bash
hugo_extended_0.134.3_Linux-64bit.deb
```

### 3. Build Optimization

Production build flags:
```bash
hugo --gc --minify --enableGitInfo
```

- `--gc`: Run garbage collection
- `--minify`: Minify HTML, CSS, JS
- `--enableGitInfo`: Add Git info to pages

### 4. Environment Variables

Set environment-specific variables:
```yaml
HUGO_ENV: production
HUGO_ENVIRONMENT: production
```

### 5. Caching

Cache dependencies for faster builds:
```yaml
cache:
  paths:
    - /tmp/hugo_cache
    - resources/_gen
```

### 6. Git Submodules

If using theme as submodule:
```yaml
- uses: actions/checkout@v4
  with:
    submodules: recursive
```

### 7. Base URL Configuration

Use dynamic base URL:
```bash
hugo --baseURL "${{ steps.pages.outputs.base_url }}/"
```

### 8. Draft Content

Exclude drafts in production:
```bash
hugo --buildDrafts=false
```

### 9. Testing

Test build locally before deploying:
```bash
hugo server --buildDrafts --buildFuture
```

### 10. Monitoring

Set up deployment notifications:
- Email alerts
- Slack integration
- Status badges

## Comparison Table

| Feature | GitHub Actions | Buddy | Netlify | Vercel | Cloudflare | GitLab CI |
|---------|---------------|-------|---------|--------|------------|-----------|
| Cost (public repos) | Free | Limited free | Free | Free | Free | Free |
| Setup Complexity | Medium | Low | Low | Very Low | Low | Medium |
| Build Speed | Fast | Very Fast | Fast | Fast | Very Fast | Fast |
| Preview Deploys | Manual | Yes | Yes | Yes | Yes | Yes |
| Custom Domains | Yes | Yes | Yes | Yes | Yes | Yes |
| HTTPS | Yes | Yes | Yes | Yes | Yes | Yes |
| CDN | GitHub Pages | Configurable | Built-in | Built-in | Built-in | Built-in |
| Analytics | External | Built-in | Add-on | Add-on | Built-in | External |

## Recommendation

**For this repository:** Continue using **GitHub Actions** because:
1. Native GitHub integration
2. No external dependencies
3. Direct GitHub Pages deployment
4. Free for public repositories
5. Full control over workflow
6. Already configured and working

**Alternative recommendation:** If you need:
- Deploy previews for every PR → **Netlify** or **Vercel**
- Visual pipeline builder → **Buddy**
- AWS infrastructure → **AWS Amplify**
- Already using GitLab → **GitLab CI/CD**

## Troubleshooting

### Build Failures

1. Check Hugo version compatibility
2. Verify theme installation (submodules)
3. Check for configuration errors in `hugo.toml`
4. Review build logs for specific errors

### Deployment Issues

1. Verify GitHub Pages is enabled
2. Check branch permissions
3. Confirm workflow permissions are correct
4. Verify base URL matches deployment URL

### Performance Issues

1. Enable caching
2. Use Hugo Extended for faster SCSS processing
3. Optimize images before adding
4. Minimize external dependencies

## Resources

- [Hugo Documentation](https://gohugo.io/documentation/)
- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Buddy Documentation](https://buddy.works/docs)
- [Netlify Hugo Deployment](https://docs.netlify.com/configure-builds/common-configurations/hugo/)
- [Vercel Hugo Deployment](https://vercel.com/docs/frameworks/hugo)
- [Hugo Hosting and Deployment](https://gohugo.io/hosting-and-deployment/)

## Support

For issues specific to this repository:
1. Check existing GitHub Issues
2. Review workflow run logs
3. Open new issue with:
   - Error message
   - Build logs
   - Steps to reproduce
