#!/bin/bash

echo "🚀 Building and Deploying ADAS to Firebase..."
echo ""

# Step 1: Build Frontend
echo "📦 Building frontend..."
cd frontend
npm run build

if [ $? -ne 0 ]; then
    echo "❌ Build failed!"
    exit 1
fi

cd ..

# Step 2: Deploy to Firebase (using npx)
echo "🔥 Deploying to Firebase Hosting..."
npx firebase-tools deploy

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ Deployment successful!"
    echo "🌐 Your website is now live at: https://adas-7c31c.web.app"
    echo ""
    echo "📝 Don't forget to:"
    echo "   1. Update backend URL in Dashboard.jsx if using remote backend"
    echo "   2. Enable Firebase Authentication in console"
    echo "   3. Create your first user account"
else
    echo "❌ Deployment failed!"
    exit 1
fi
