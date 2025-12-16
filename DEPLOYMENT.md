# Deployment Guide

Complete step-by-step guide to deploy the Whiskey Inventory Management System to Vercel with Supabase.

## Prerequisites

1. **GitHub Account**: You'll need a GitHub account to connect to Vercel
2. **Supabase Account**: Sign up at [supabase.com](https://supabase.com) (free tier works)
3. **Vercel Account**: Sign up at [vercel.com](https://vercel.com) (free tier works)

## Step 1: Set Up Supabase

### 1.1 Create a New Project

1. Go to [supabase.com](https://supabase.com) and sign in
2. Click "New Project"
3. Fill in:
   - **Name**: Whiskey Inventory (or your choice)
   - **Database Password**: Create a strong password (save it!)
   - **Region**: Choose closest to your users
   - **Pricing Plan**: Free tier is sufficient
4. Click "Create new project"
5. Wait 2-3 minutes for provisioning

### 1.2 Get Your Supabase Credentials

1. In your Supabase project dashboard, go to **Settings** > **API**
2. Copy these values:
   - **Project URL** (e.g., `https://xxxxx.supabase.co`)
   - **anon public** key (long string starting with `eyJ...`)

### 1.3 Get Database Connection String

1. Go to **Settings** > **Database**
2. Scroll to "Connection string"
3. Click on "URI" tab
4. Copy the connection string (it will look like: `postgresql://postgres:[YOUR-PASSWORD]@db.xxxxx.supabase.co:5432/postgres`)
5. Replace `[YOUR-PASSWORD]` with the password you created in step 1.1

## Step 2: Prepare Your Code

### 2.1 Initialize Git (if not already done)

```bash
git init
git add .
git commit -m "Initial commit: Whiskey Inventory Management System"
```

### 2.2 Push to GitHub

1. Create a new repository on GitHub
2. Push your code:

```bash
git remote add origin https://github.com/yourusername/whiskey-inventory.git
git branch -M main
git push -u origin main
```

## Step 3: Deploy to Vercel

### 3.1 Import Project

1. Go to [vercel.com](https://vercel.com) and sign in
2. Click "Add New..." > "Project"
3. Import your GitHub repository
4. Click "Import"

### 3.2 Configure Project

1. **Framework Preset**: Should auto-detect "Next.js"
2. **Root Directory**: Leave as `./`
3. **Build Command**: `npm run build` (default)
4. **Output Directory**: `.next` (default)
5. **Install Command**: `npm install` (default)

### 3.3 Add Environment Variables

Click "Environment Variables" and add:

1. **NEXT_PUBLIC_SUPABASE_URL**
   - Value: Your Supabase Project URL from Step 1.2
   - Environment: Production, Preview, Development (check all)

2. **NEXT_PUBLIC_SUPABASE_ANON_KEY**
   - Value: Your Supabase anon key from Step 1.2
   - Environment: Production, Preview, Development (check all)

3. **DATABASE_URL**
   - Value: Your database connection string from Step 1.3
   - Environment: Production, Preview, Development (check all)

### 3.4 Deploy

1. Click "Deploy"
2. Wait 2-3 minutes for build to complete
3. Your app will be live at `https://your-project.vercel.app`

## Step 4: Set Up Database Schema

### 4.1 Install Vercel CLI (Optional but Recommended)

```bash
npm i -g vercel
```

### 4.2 Pull Environment Variables Locally

```bash
vercel env pull .env.local
```

### 4.3 Run Database Migrations

```bash
# Generate Prisma client
npm run db:generate

# Push schema to database
npm run db:push
```

**OR** use Prisma Studio to verify:

```bash
npm run db:studio
```

This opens a visual database editor at `http://localhost:5555`

## Step 5: Configure Supabase Authentication

### 5.1 Set Up Redirect URLs

1. Go to your Supabase project dashboard
2. Navigate to **Authentication** > **URL Configuration**
3. Add your Vercel URL to:
   - **Site URL**: `https://your-project.vercel.app`
   - **Redirect URLs**: `https://your-project.vercel.app/**`

### 5.2 Create Your First User

1. Go to **Authentication** > **Users**
2. Click "Add user" > "Create new user"
3. Enter:
   - **Email**: your-email@example.com
   - **Password**: (create a strong password)
4. Click "Create user"
5. Use these credentials to log in to your app

## Step 6: Seed Sample Data (Optional)

If you want to test with sample data:

```bash
# Make sure you have .env.local with DATABASE_URL
npm run db:seed
```

This creates:
- A sample barrel batch
- Sample barrels
- Sample usage logs
- Sample bottling runs
- Sample shipments

## Step 7: Verify Deployment

1. Visit your Vercel URL: `https://your-project.vercel.app`
2. You should see the login page
3. Log in with the user you created in Step 5.2
4. You should see the dashboard

## Troubleshooting

### Build Fails with "Prisma Client not generated"

**Solution**: Add a build script that generates Prisma client:

In `package.json`, ensure:
```json
{
  "scripts": {
    "build": "prisma generate && next build"
  }
}
```

### Database Connection Errors

**Check**:
1. DATABASE_URL is correct in Vercel environment variables
2. Password in connection string matches your Supabase password
3. Supabase project is active (not paused)

### Authentication Not Working

**Check**:
1. NEXT_PUBLIC_SUPABASE_URL is set correctly
2. NEXT_PUBLIC_SUPABASE_ANON_KEY is set correctly
3. Redirect URLs are configured in Supabase
4. Site URL matches your Vercel domain

### Can't Access Database

**Solution**: Supabase free tier allows connections from anywhere by default. If you have issues:
1. Check Supabase project status
2. Verify database password
3. Check connection string format

## Next Steps

1. **Customize**: Update branding, colors, and text in the app
2. **Add Users**: Create more users in Supabase dashboard
3. **Set Up Backups**: Supabase free tier includes daily backups
4. **Monitor**: Use Vercel Analytics and Supabase dashboard to monitor usage

## Support

- **Vercel Docs**: https://vercel.com/docs
- **Supabase Docs**: https://supabase.com/docs
- **Prisma Docs**: https://www.prisma.io/docs

## Cost Estimate

**Free Tier (Sufficient for small teams)**:
- Vercel: Free (up to 100GB bandwidth/month)
- Supabase: Free (500MB database, 2GB bandwidth/month)

**If you need more**:
- Vercel Pro: $20/month
- Supabase Pro: $25/month

