# Weather ML App - Deployment Guide

## 🚀 Quick Deployment Options

### Option 1: Heroku (Recommended - Free)
**Best for: Quick deployment, no server management**

1. **Install Heroku CLI**
   ```bash
   # macOS
   brew install heroku/brew/heroku
   
   # Or download from: https://devcenter.heroku.com/articles/heroku-cli
   ```

2. **Deploy to Heroku**
   ```bash
   # Login to Heroku
   heroku login
   
   # Create new app
   heroku create your-weather-app-name
   
   # Add git remote
   heroku git:remote -a your-weather-app-name
   
   # Deploy
   git add .
   git commit -m "Initial deployment"
   git push heroku main
   
   # Open your app
   heroku open
   ```

3. **Your app will be live at:**
   `https://your-weather-app-name.herokuapp.com`

### Option 2: Railway (Alternative - Free)
**Best for: Easy deployment with automatic scaling**

1. **Go to Railway.app**
2. **Connect your GitHub repository**
3. **Railway will automatically deploy your app**
4. **Get a live URL instantly**

### Option 3: Render (Free Tier)
**Best for: Reliable hosting with custom domains**

1. **Go to render.com**
2. **Connect your GitHub repository**
3. **Choose "Web Service"**
4. **Set build command: `pip install -r requirements.txt`**
5. **Set start command: `gunicorn app:app`**

### Option 4: VPS/Cloud Server
**Best for: Full control, custom domains**

#### Using DigitalOcean/AWS/GCP:
```bash
# On your server
sudo apt update
sudo apt install python3 python3-pip nginx

# Clone your app
git clone <your-repo-url>
cd weather-ml-flask

# Install dependencies
pip3 install -r requirements.txt

# Run with gunicorn
gunicorn --bind 0.0.0.0:8000 app:app

# Set up nginx reverse proxy
sudo nano /etc/nginx/sites-available/weather-app
```

## 🔧 Production Configuration

### Environment Variables (if needed)
```bash
# For Heroku
heroku config:set FLASK_ENV=production

# For other platforms, set in their dashboard
```

### Custom Domain Setup
1. **Buy a domain** (GoDaddy, Namecheap, etc.)
2. **Point DNS to your hosting provider**
3. **Configure SSL certificate** (automatic on most platforms)

## 📱 Client Access

### Share with Clients:
- **Web URL**: `https://your-app-name.herokuapp.com`
- **API Endpoint**: `https://your-app-name.herokuapp.com/api/predict`
- **Documentation**: Include the README.md

### API Usage for Clients:
```bash
curl -X POST https://your-app-name.herokuapp.com/api/predict \
  -H "Content-Type: application/json" \
  -d '{"city": "London"}'
```

## 💰 Cost Comparison

| Platform | Free Tier | Paid Plans | Best For |
|----------|-----------|------------|----------|
| **Heroku** | ✅ 550 hours/month | $7/month | Quick deployment |
| **Railway** | ✅ $5 credit/month | Pay-as-you-go | Easy scaling |
| **Render** | ✅ 750 hours/month | $7/month | Reliable hosting |
| **VPS** | ❌ | $5-20/month | Full control |

## 🛠️ Maintenance

### Monitoring:
- **Uptime**: Use UptimeRobot (free)
- **Logs**: Check hosting platform dashboard
- **Performance**: Monitor response times

### Updates:
```bash
# Update your local code
git add .
git commit -m "Update app"
git push heroku main  # or your platform
```

## 📞 Support

### For Clients:
- **Web Interface**: Direct URL access
- **API Documentation**: Included in README
- **Contact**: Your email/phone for support

### For You:
- **Hosting Dashboard**: Monitor usage and logs
- **GitHub**: Version control and updates
- **Backup**: Regular database/model backups

## 🎯 Recommended for Your Use Case

**For a weather prediction app with clients:**

1. **Start with Heroku** (free, easy)
2. **Scale to Railway** if you need more features
3. **Move to VPS** if you need full control

**Estimated setup time: 15-30 minutes**
**Monthly cost: $0-10**
