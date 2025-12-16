# Deploy to Production - Step by Step

This guide will get your Whiskey Inventory Management System online so others can access it from anywhere.

**Time needed:** 20-30 minutes  
**Cost:** Free (using free tiers of Vercel and Supabase)

---

## Prerequisites Checklist

Before starting, make sure you have:
- [ ] The application running locally (you can log in at http://localhost:3000)
- [ ] Your `.env.local` file with Supabase credentials
- [ ] A GitHub account (we'll create one if needed)
- [ ] Your Supabase project URL and credentials handy

---

## Step 1: Prepare Your Code for GitHub (5 minutes)

### 1.1 Create a GitHub Account (If You Don't Have One)

1. **Go to:** https://github.com
2. Click **"Sign up"** (top right)
3. **Choose your plan:** Select **"Free"** (the free plan is perfect)
4. **Create your account:**
   - Enter your email
   - Create a password
   - Choose a username
5. **Verify your email** (check your inbox)

### 1.2 Create a New Repository

1. **After logging in**, click the **"+"** icon (top right) → **"New repository"**
2. **Fill in the form:**
   - **Repository name:** `whiskey-inventory` (or any name you like)
   - **Description:** (optional) "Whiskey Inventory Management System"
   - **Visibility:** 
     - ✅ **Private** (recommended - only you and people you invite can see it)
     - ⬜ Public (anyone can see your code)
   - **DO NOT** check "Add a README file" (you already have one)
   - **DO NOT** add .gitignore or license (you already have these)
3. Click **"Create repository"**

### 1.3 Upload Your Code to GitHub

**Open your terminal/command prompt** in your project folder.

**Copy and paste these commands one by one:**

```bash
git init
```

Press Enter. You should see: "Initialized empty Git repository"

```bash
git add .
```

Press Enter. (This adds all your files)

```bash
git commit -m "Initial commit - Whiskey Inventory System"
```

Press Enter. You should see files being committed.

```bash
git branch -M main
```

Press Enter. (This sets the main branch)

```bash
git remote add origin https://github.com/YOUR-USERNAME/whiskey-inventory.git
```

**IMPORTANT:** Replace `YOUR-USERNAME` with your actual GitHub username  
**IMPORTANT:** Replace `whiskey-inventory` with your actual repository name

Example: If your username is `johnsmith` and repo is `whiskey-inventory`, it would be:
```
git remote add origin https://github.com/johnsmith/whiskey-inventory.git
```

Press Enter.

```bash
git push -u origin main
```

Press Enter.

**If it asks for credentials:**
- **Username:** Your GitHub username
- **Password:** You'll need a **Personal Access Token** (not your GitHub password)

**To create a Personal Access Token:**
1. Go to GitHub → Click your profile (top right) → **Settings**
2. Scroll down → **Developer settings** (left sidebar)
3. Click **"Personal access tokens"** → **"Tokens (classic)"**
4. Click **"Generate new token"** → **"Generate new token (classic)"**
5. **Note:** "Whiskey Inventory Deployment"
6. **Expiration:** 90 days (or No expiration)
7. **Select scopes:** Check **"repo"** (this gives full repository access)
8. Click **"Generate token"** at the bottom
9. **COPY THE TOKEN IMMEDIATELY** (you won't see it again!)
10. Use this token as your password when pushing

**After successful push, you should see:**
```
Branch 'main' set up to track remote branch 'main' from 'origin'.
```

✅ **Step 1 Complete!** Your code is now on GitHub.

---

## Step 2: Deploy to Vercel (10 minutes)

### 2.1 Create a Vercel Account

1. **Go to:** https://vercel.com
2. Click **"Sign Up"** (top right)
3. **Click "Continue with GitHub"** (recommended - easiest way)
4. **Authorize Vercel** to access your GitHub account
5. You're now logged in!

### 2.2 Import Your Project

1. **On the Vercel dashboard**, click **"Add New..."** → **"Project"**
2. **You'll see a list of your GitHub repositories**
3. **Find your repository** (e.g., `whiskey-inventory`)
4. **Click "Import"** next to it

### 2.3 Configure Project Settings

**You'll see a configuration page. Here's what to do:**

1. **Framework Preset:** Should auto-detect "Next.js" ✅ (don't change)
2. **Root Directory:** Leave as `./` ✅ (don't change)
3. **Build Command:** Should show `npm run build` ✅ (don't change)
4. **Output Directory:** Should show `.next` ✅ (don't change)
5. **Install Command:** Should show `npm install` ✅ (don't change)

**DO NOT click "Deploy" yet!** We need to add environment variables first.

### 2.4 Add Environment Variables

**This is critical!** Your app needs these to connect to Supabase.

1. **On the same configuration page**, scroll down to **"Environment Variables"**
2. **Click "Add"** or the **"Environment Variables"** section

3. **Add Variable #1:**
   - **Name:** `NEXT_PUBLIC_SUPABASE_URL`
   - **Value:** Your Supabase Project URL (from your `.env.local` file)
     - Looks like: `https://xxxxxxxxxxxxx.supabase.co`
   - **Environments:** Check all three boxes:
     - ✅ Production
     - ✅ Preview
     - ✅ Development
   - Click **"Add"**

4. **Add Variable #2:**
   - **Name:** `NEXT_PUBLIC_SUPABASE_ANON_KEY`
   - **Value:** Your Supabase anon public key (from your `.env.local` file)
     - Long string starting with `eyJ...`
   - **Environments:** Check all three boxes ✅
   - Click **"Add"**

5. **Add Variable #3:**
   - **Name:** `DATABASE_URL`
   - **Value:** Your database connection string (from your `.env.local` file)
     - Looks like: `postgresql://postgres:YOUR_PASSWORD@db.xxxxx.supabase.co:5432/postgres`
   - **Environments:** Check all three boxes ✅
   - Click **"Add"**

**Double-check:** You should see all three variables listed.

### 2.5 Deploy!

1. **Scroll to the bottom** of the configuration page
2. **Click the big "Deploy" button**
3. **Wait 2-3 minutes** - you'll see:
   - "Building..." (this takes 1-2 minutes)
   - "Deploying..." (this takes 30 seconds)
   - "Congratulations! Your project has been deployed"

4. **You'll see a URL** like: `https://whiskey-inventory.vercel.app`
   - This is your live application URL!
   - **Copy this URL** - you'll need it in the next step

✅ **Step 2 Complete!** Your app is now deployed (but not fully configured yet).

---

## Step 3: Configure Supabase for Production (5 minutes)

Your Supabase project needs to know about your live URL so authentication works.

### 3.1 Update Supabase Settings

1. **Go to your Supabase dashboard:** https://supabase.com/dashboard
2. **Select your project** (Whiskey Inventory)
3. **Click "Settings"** (gear icon, left sidebar)
4. **Click "Authentication"** (under Project Settings)
5. **Click "URL Configuration"** (under Authentication)

### 3.2 Add Your Vercel URL

1. **Site URL:**
   - Replace the default URL with your Vercel URL
   - Example: `https://whiskey-inventory.vercel.app`
   - (Use your actual Vercel URL from Step 2.5)

2. **Redirect URLs:**
   - Click **"Add URL"**
   - Enter: `https://your-vercel-url.vercel.app/**`
   - Example: `https://whiskey-inventory.vercel.app/**`
   - (Replace with your actual URL, keep the `/**` at the end)
   - Click **"Save"**

3. **Click "Save"** at the bottom of the page

✅ **Step 3 Complete!** Supabase is now configured for your live site.

---

## Step 4: Test Your Live Application (5 minutes)

### 4.1 Open Your Live Site

1. **Open a new browser window** (or use incognito/private mode)
2. **Go to your Vercel URL:** `https://your-app.vercel.app`
3. **You should see the login page!**

### 4.2 Log In

1. **Enter the email and password** you created in Supabase (from the setup guide)
2. **Click "Sign In"**
3. **You should see the dashboard!**

### 4.3 Test Key Features

1. **Create a test barrel batch:**
   - Click "Barrel Batches" → "Create New Batch"
   - Fill in test data
   - Submit
   - Should see success message

2. **View barrels:**
   - Click "Barrels"
   - Should see the barrels that were auto-created

3. **Try other features** to make sure everything works

✅ **Step 4 Complete!** Your application is live and working!

---

## Step 5: Share with Others (2 minutes)

### 5.1 Create Additional Users

**To let others log in, create users for them in Supabase:**

1. **Go to Supabase dashboard** → Your project
2. **Authentication** → **Users**
3. **Click "Add user"** → **"Create new user"**
4. **Enter their email and password**
5. **Click "Create user"**
6. **Share the login credentials with them:**
   - URL: `https://your-app.vercel.app`
   - Email: (the email you just created)
   - Password: (the password you set)

### 5.2 Share the URL

**Simply send them:**
- **URL:** `https://your-app.vercel.app`
- **Instructions:** "Log in with the email and password I sent you"

---

## Troubleshooting

### Problem: "Build failed" on Vercel

**Solutions:**
- Check that all 3 environment variables are set correctly
- Make sure `DATABASE_URL` includes your actual password (not `[YOUR-PASSWORD]`)
- Check the build logs in Vercel for specific errors
- Make sure your code pushed to GitHub successfully

### Problem: "Authentication failed" on live site

**Solutions:**
- Verify Supabase URL Configuration has your Vercel URL
- Make sure redirect URLs include `/**` at the end
- Check that environment variables in Vercel match your `.env.local` file
- Try logging out and back in

### Problem: "Cannot connect to database"

**Solutions:**
- Verify `DATABASE_URL` in Vercel environment variables is correct
- Check that your Supabase project is active (not paused)
- Verify your database password is correct in the connection string

### Problem: Site shows "Application Error"

**Solutions:**
- Check Vercel deployment logs (click on the deployment → "Logs")
- Verify all environment variables are set
- Make sure `npm run build` works locally first
- Check that Prisma schema is correct

### Problem: Changes not showing up

**Solutions:**
- Push your changes to GitHub: `git push`
- Vercel automatically redeploys when you push to GitHub
- Wait 1-2 minutes for the new deployment
- Hard refresh your browser (Ctrl+F5 or Cmd+Shift+R)

---

## Updating Your Application

**When you make changes to your code:**

1. **Make your changes** locally
2. **Test locally** (`npm run dev`)
3. **Commit and push to GitHub:**
   ```bash
   git add .
   git commit -m "Description of changes"
   git push
   ```
4. **Vercel automatically redeploys** (takes 1-2 minutes)
5. **Your live site updates automatically!**

---

## Custom Domain (Optional)

**Want to use your own domain (e.g., inventory.yourcompany.com)?**

1. **In Vercel dashboard**, click on your project
2. **Settings** → **Domains**
3. **Add your domain**
4. **Follow Vercel's instructions** to configure DNS
5. **Update Supabase URL Configuration** with your new domain

---

## Security Checklist

- [ ] Your repository is set to **Private** on GitHub
- [ ] You're using **strong passwords** for Supabase
- [ ] Environment variables are set correctly in Vercel
- [ ] Only trusted people have user accounts
- [ ] You've shared credentials securely (not via email if possible)

---

## Cost Information

**Free Tier Limits (usually more than enough):**

- **Vercel Free:**
  - 100GB bandwidth/month
  - Unlimited deployments
  - Perfect for small teams

- **Supabase Free:**
  - 500MB database storage
  - 2GB bandwidth/month
  - 50,000 monthly active users
  - Perfect for small businesses

**If you need more:**
- Vercel Pro: $20/month
- Supabase Pro: $25/month

---

## Success! 🎉

Your Whiskey Inventory Management System is now:
- ✅ Live on the internet
- ✅ Accessible from anywhere
- ✅ Ready for your team to use
- ✅ Automatically backed up (via GitHub)
- ✅ Free to run (on free tiers)

**Your live URL:** `https://your-app.vercel.app`

**Share this with your team and start using it!**

---

## Quick Reference

**To add a new user:**
1. Supabase → Authentication → Users → Add user

**To update the app:**
1. Make changes locally
2. `git push` to GitHub
3. Vercel auto-deploys

**To view logs/errors:**
1. Vercel dashboard → Your project → Deployments → Click on deployment → Logs

**To change environment variables:**
1. Vercel dashboard → Your project → Settings → Environment Variables

---

**Need help?** Check the main SETUP_GUIDE_FOR_ACCOUNTANTS.md or the troubleshooting section above.

