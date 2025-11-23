#!/bin/bash

echo "🚀 Preparing for Railway Deployment..."
echo ""

# Check if git repo exists
if [ ! -d ".git" ]; then
    echo "📦 Initializing git repository..."
    git init
    git add .
    git commit -m "Initial commit - ADAS Project"
fi

# Check if Railway CLI is installed
if ! command -v railway &> /dev/null; then
    echo "⚠️  Railway CLI not found"
    echo "Install with: npm install -g @railway/cli"
    echo ""
    echo "Or deploy via web:"
    echo "1. Push to GitHub"
    echo "2. Go to https://railway.app"
    echo "3. Click 'Deploy from GitHub'"
    exit 1
fi

echo "✅ Railway CLI found"
echo ""
echo "Next steps:"
echo "1. Run: railway login"
echo "2. Run: railway init"
echo "3. Run: railway up"
echo ""
echo "Or visit: https://railway.app to deploy via web"
