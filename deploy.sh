#!/bin/bash

echo "🚀 Weather ML App Deployment Script"
echo "=================================="

# Check if git is initialized
if [ ! -d ".git" ]; then
    echo "📁 Initializing git repository..."
    git init
    git add .
    git commit -m "Initial commit"
fi

# Check if Heroku CLI is installed
if ! command -v heroku &> /dev/null; then
    echo "❌ Heroku CLI not found. Please install it first:"
    echo "   brew install heroku/brew/heroku"
    echo "   Or download from: https://devcenter.heroku.com/articles/heroku-cli"
    exit 1
fi

# Check if logged into Heroku
if ! heroku auth:whoami &> /dev/null; then
    echo "🔐 Please login to Heroku first:"
    heroku login
fi

# Get app name from user
echo ""
read -p "Enter your Heroku app name (or press Enter to auto-generate): " app_name

if [ -z "$app_name" ]; then
    echo "🎲 Creating app with auto-generated name..."
    heroku create
else
    echo "🎯 Creating app: $app_name"
    heroku create $app_name
fi

# Get the app URL
app_url=$(heroku info -s | grep web_url | cut -d= -f2)
echo "🌐 Your app will be available at: $app_url"

# Deploy
echo "📤 Deploying to Heroku..."
git add .
git commit -m "Deploy weather ML app"
git push heroku main

# Open the app
echo "🎉 Deployment complete! Opening your app..."
heroku open

echo ""
echo "✅ Your Weather ML App is now live!"
echo "📱 Share this URL with your clients: $app_url"
echo "📚 API endpoint: $app_url/api/predict"
echo ""
echo "🔧 To update your app later, run:"
echo "   git add . && git commit -m 'Update' && git push heroku main"
