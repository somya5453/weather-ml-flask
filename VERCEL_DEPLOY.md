# 🚀 Vercel Deployment Guide

## Quick Deploy to Vercel (5 minutes)

### Step 1: Deploy to Vercel
1. **Go to [Vercel.com](https://vercel.com)**
2. **Sign up/Login** with GitHub
3. **Click "New Project"**
4. **Import your GitHub repository** (weather-ml-flask)
5. **Click "Deploy"**

### Step 2: Get Your Live URL
- Vercel will give you: `https://your-app-name.vercel.app`
- Your app will be live in 2 minutes!

### Step 3: Add Custom Domain
1. **In Vercel Dashboard**, go to your project
2. **Click "Settings" → "Domains"**
3. **Add domain**: `somyaweather.com`
4. **Vercel will show DNS settings**

### Step 4: Configure DNS
**At your domain provider (GoDaddy, Namecheap, etc.):**

Add these DNS records:
```
Type: A
Name: @
Value: 76.76.19.19

Type: CNAME  
Name: www
Value: cname.vercel-dns.com
```

### Step 5: Wait for SSL
- Vercel automatically adds SSL certificate
- Takes 5-10 minutes to activate

## ✅ Your app will be live at:
**https://somyaweather.com**

## 🔧 API Endpoint:
**https://somyaweather.com/api/predict**

## 📱 Share with Clients:
- **Web App**: https://somyaweather.com
- **API**: https://somyaweather.com/api/predict
- **Documentation**: Include README.md

## 💰 Cost:
- **Vercel**: Free tier (unlimited)
- **Domain**: ~$10-15/year
- **Total**: ~$10-15/year

## 🎯 Benefits:
- ✅ **Super fast deployment** (2 minutes)
- ✅ **Automatic SSL** 
- ✅ **Global CDN**
- ✅ **Custom domain support**
- ✅ **Free tier generous**
- ✅ **Easy updates**

## 🔄 Updates:
```bash
# Just push to GitHub, Vercel auto-deploys!
git add .
git commit -m "Update app"
git push origin main
```
