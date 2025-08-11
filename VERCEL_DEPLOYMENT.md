# Django Blog Deployment on Vercel

## Prerequisites
1. Vercel account (sign up at vercel.com)
2. GitHub repository with your Django project
3. Vercel CLI installed (optional but recommended)

## Step-by-Step Deployment

### 1. Database Setup
Since Vercel doesn't provide a built-in database, you'll need to use an external database service:

**Option A: Vercel Postgres (Recommended)**
- Go to your Vercel dashboard
- Create a new Postgres database
- Copy the connection string

**Option B: External Services**
- Railway.app
- PlanetScale
- Supabase
- Neon.tech

### 2. Environment Variables
Set these environment variables in your Vercel project settings:

```
SECRET_KEY=your-secret-key-here
DEBUG=False
DATABASE_URL=your-database-connection-string
POSTGRES_URL=your-postgres-connection-string (if using Vercel Postgres)
ALLOWED_HOSTS=.vercel.app,your-custom-domain.com
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
```

### 3. Deploy to Vercel

**Method 1: Using Vercel Dashboard**
1. Go to vercel.com and sign in
2. Click "New Project"
3. Import your GitHub repository
4. Vercel will automatically detect the configuration
5. Add your environment variables
6. Click "Deploy"

**Method 2: Using Vercel CLI**
```bash
npm i -g vercel
cd your-project-directory
vercel
```

### 4. Post-Deployment Steps

After successful deployment:

1. **Run Migrations**
   - You may need to run migrations manually
   - Use Vercel's serverless functions or run locally against production DB

2. **Create Superuser**
   - Connect to your production database
   - Run: `python manage.py createsuperuser`

3. **Collect Static Files**
   - This should happen automatically during build
   - Static files are served by Vercel's CDN

### 5. Custom Domain (Optional)
1. Go to your Vercel project settings
2. Navigate to "Domains"
3. Add your custom domain
4. Update DNS settings as instructed

## Important Notes

- **Static Files**: Handled by WhiteNoise and Vercel's CDN
- **Media Files**: Consider using cloud storage (AWS S3, Cloudinary) for user uploads
- **Database**: Use external database service, not SQLite
- **Environment**: Always set DEBUG=False in production
- **CORS**: Update CORS settings for production domains

## Troubleshooting

### Common Issues:
1. **Build Failures**: Check Python version compatibility
2. **Database Errors**: Verify connection string format
3. **Static Files**: Ensure WhiteNoise is properly configured
4. **ALLOWED_HOSTS**: Add your Vercel domain to allowed hosts

### Logs:
- View deployment logs in Vercel dashboard
- Use `vercel logs` command for real-time logs

## Files Created for Vercel:
- `vercel.json` - Vercel configuration
- `api/index.py` - WSGI entry point
- `build_files.sh` - Build script
- `.vercelignore` - Files to ignore during deployment
- Updated `requirements.txt` - Clean dependencies
- Updated `settings.py` - Vercel-compatible settings

Your Django blog is now ready for Vercel deployment!