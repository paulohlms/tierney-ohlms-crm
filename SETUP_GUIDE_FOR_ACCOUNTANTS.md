# Complete Setup Guide - For Accountants & Non-Technical Users

This guide will walk you through setting up the Whiskey Inventory Management System step by step. **No technical experience required!** Just follow along.

## 📋 What You'll Need

1. **A computer** (Windows, Mac, or Linux)
2. **Internet connection**
3. **About 30-45 minutes** for the initial setup
4. **A free Supabase account** (we'll create this together)
5. **A free Vercel account** (we'll create this together)

---

## Part 1: Install Required Software

### Step 1: Install Node.js (The Programming Language)

**What is Node.js?** It's the software that runs the application on your computer.

1. **Open your web browser** and go to: https://nodejs.org/
2. You'll see a big green button that says **"Download Node.js"** - click it
3. The website will automatically detect your computer type and download the right version
4. **Run the downloaded file** (it will be in your Downloads folder)
5. **Follow the installation wizard:**
   - Click "Next" on each screen
   - **IMPORTANT:** Make sure "Add to PATH" is checked (it usually is by default)
   - Click "Install"
   - Wait for it to finish (2-3 minutes)
   - Click "Finish"

**Verify it worked:**
1. Open **Command Prompt** (Windows) or **Terminal** (Mac):
   - **Windows:** Press `Windows Key + R`, type `cmd`, press Enter
   - **Mac:** Press `Command + Space`, type `Terminal`, press Enter
2. Type this command and press Enter:
   ```
   node --version
   ```
3. You should see something like `v20.10.0` (the numbers might be different)
4. If you see an error, the installation didn't work - try installing again

### Step 2: Install Git (For Code Management)

**What is Git?** It's a tool that helps manage the code and deploy it online.

1. **Go to:** https://git-scm.com/download/win (Windows) or https://git-scm.com/download/mac (Mac)
2. **Download and run the installer**
3. **Follow the installation wizard:**
   - Click "Next" on each screen
   - Use all the default settings (don't change anything)
   - Click "Install"
   - Wait for it to finish
   - Click "Finish"

**Verify it worked:**
1. Open Command Prompt/Terminal again
2. Type:
   ```
   git --version
   ```
3. You should see something like `git version 2.42.0`

---

## Part 2: Set Up Supabase (Your Database)

**What is Supabase?** It's a free service that stores all your inventory data in the cloud.

### Step 1: Create a Supabase Account

1. **Go to:** https://supabase.com
2. Click the **"Start your project"** button (top right)
3. Click **"Sign up"** or **"Sign in"** if you already have an account
4. **Sign up with GitHub** (recommended) or **Email**
   - If using GitHub: Click "Continue with GitHub" and authorize
   - If using Email: Enter your email and create a password

### Step 2: Create a New Project

1. Once logged in, click the **"New Project"** button (green button)
2. Fill in the form:
   - **Name:** `Whiskey Inventory` (or whatever you want)
   - **Database Password:** Create a strong password (write it down! You'll need it)
     - Example: `MyWhiskey2025!Secure`
   - **Region:** Choose the one closest to you (e.g., "US East" if you're in the US)
   - **Pricing Plan:** Select **"Free"** (it's free forever for small projects)
3. Click **"Create new project"**
4. **Wait 2-3 minutes** while Supabase sets up your database
   - You'll see a progress bar
   - Don't close the page!

### Step 3: Get Your Supabase Credentials

Once your project is ready:

1. **Click on "Settings"** (gear icon in the left sidebar)
2. **Click on "API"** (under Project Settings)
3. **Copy these two values** (you'll need them later):
   - **Project URL:** It looks like `https://xxxxxxxxxxxxx.supabase.co`
     - Click the copy icon next to it
     - Paste it into a text file (we'll call this "credentials.txt")
   - **anon public key:** It's a long string starting with `eyJ...`
     - Click the copy icon next to it
     - Add it to your credentials.txt file

4. **Now get your database connection string:**
   - Still in Settings, click **"Database"** (under Project Settings)
   - Scroll down to **"Connection string"**
   - Click on the **"URI"** tab
   - You'll see something like: `postgresql://postgres:[YOUR-PASSWORD]@db.xxxxx.supabase.co:5432/postgres`
   - **Replace `[YOUR-PASSWORD]`** with the password you created in Step 2
   - Example: `postgresql://postgres:MyWhiskey2025!Secure@db.xxxxx.supabase.co:5432/postgres`
   - Copy this entire string and add it to your credentials.txt file

**Save your credentials.txt file somewhere safe!** You'll need it in Part 4.

---

## Part 3: Download and Set Up the Code

### Step 1: Download the Code

**Option A: If you have the code in a folder already:**
- Skip to Step 2

**Option B: If you need to download it:**
1. If the code is on GitHub:
   - Go to the repository
   - Click the green **"Code"** button
   - Click **"Download ZIP"**
   - Extract the ZIP file to a folder (e.g., `C:\Users\YourName\Desktop\whiskey-inventory`)

### Step 2: Open the Project Folder

1. **Navigate to the project folder** on your computer
2. **Right-click in the folder** and select **"Open in Terminal"** or **"Open PowerShell here"**
   - If you don't see this option, open Command Prompt/Terminal and type:
     ```
     cd "C:\Users\YourName\Desktop\whiskey-inventory"
     ```
     (Replace with your actual folder path)

### Step 3: Install Dependencies

This downloads all the code libraries the application needs.

1. **In the terminal/command prompt**, type:
   ```
   npm install
   ```
2. **Press Enter**
3. **Wait 2-5 minutes** - you'll see lots of text scrolling by
4. When it's done, you'll see your command prompt again (no errors)

**If you see errors:**
- Make sure you're in the correct folder
- Make sure Node.js is installed (go back to Part 1, Step 1)
- Try running `npm install` again

---

## Part 4: Configure the Application

### Step 1: Create Environment File

1. **In your project folder**, create a new file called `.env.local`
   - **Windows:** Right-click in folder → New → Text Document → Name it `.env.local`
   - **Mac:** Use TextEdit, save as `.env.local`
   - **Important:** Make sure it starts with a dot (`.env.local` not `env.local`)

2. **Open `.env.local`** in a text editor (Notepad, TextEdit, etc.)

3. **Copy and paste this template**, then fill in your values from credentials.txt:

```
NEXT_PUBLIC_SUPABASE_URL=your_project_url_here
NEXT_PUBLIC_SUPABASE_ANON_KEY=your_anon_key_here
DATABASE_URL=your_database_connection_string_here
```

4. **Replace the placeholders:**
   - Replace `your_project_url_here` with your Project URL from Supabase
   - Replace `your_anon_key_here` with your anon public key
   - Replace `your_database_connection_string_here` with your database connection string

**Example of what it should look like:**
```
NEXT_PUBLIC_SUPABASE_URL=https://abcdefghijklmnop.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImFiY2RlZmdoaWprbG1ub3AiLCJyb2xlIjoiYW5vbiIsImlhdCI6MTYxNjIzOTAyMiwiZXhwIjoxOTMxODE1MDIyfQ.abcdefghijklmnopqrstuvwxyz1234567890
DATABASE_URL=postgresql://postgres:MyWhiskey2025!Secure@db.abcdefghijklmnop.supabase.co:5432/postgres
```

5. **Save the file**

### Step 2: Set Up the Database

1. **In your terminal/command prompt** (still in the project folder), type:
   ```
   npm run db:generate
   ```
2. **Press Enter** and wait for it to finish (about 30 seconds)

3. **Then type:**
   ```
   npm run db:push
   ```
4. **Press Enter** and wait for it to finish
   - This creates all the database tables
   - You should see "Your database is now in sync"

**If you see errors:**
- Check that your `.env.local` file has the correct values
- Make sure your Supabase project is active (not paused)
- Verify your database password is correct

---

## Part 5: Create Your First User

1. **Go back to your Supabase dashboard**
2. Click **"Authentication"** in the left sidebar
3. Click **"Users"** (under Authentication)
4. Click **"Add user"** → **"Create new user"**
5. Fill in:
   - **Email:** Your email address (e.g., `you@company.com`)
   - **Password:** Create a password (write it down!)
6. Click **"Create user"**

**You'll use this email and password to log into the application!**

---

## Part 6: Run the Application Locally

### Step 1: Start the Development Server

1. **In your terminal/command prompt** (still in the project folder), type:
   ```
   npm run dev
   ```
2. **Press Enter**
3. You'll see text like:
   ```
   ▲ Next.js 14.0.4
   - Local:        http://localhost:3000
   ```
4. **Keep this window open!** Don't close it while using the app.

### Step 2: Open the Application

1. **Open your web browser** (Chrome, Firefox, Edge, etc.)
2. **Type in the address bar:**
   ```
   http://localhost:3000
   ```
3. **Press Enter**
4. You should see the login page!

### Step 3: Log In

1. **Enter the email and password** you created in Part 5
2. Click **"Sign In"**
3. You should see the dashboard!

---

## Part 7: Test It Out

1. **Create a Barrel Batch:**
   - Click "Barrel Batches" in the navigation
   - Click "Create New Batch"
   - Fill in the form (use test data)
   - Click "Create Batch"
   - You should see a success message!

2. **View Your Barrels:**
   - Click "Barrels" in the navigation
   - You should see the barrels that were automatically created!

3. **Try other features:**
   - Create usage logs
   - Create bottling runs
   - Record shipments
   - View reports

---

## Part 8: Deploy to Production (Make It Available Online)

This makes your application accessible from anywhere, not just your computer.

### Step 1: Create a GitHub Account (If You Don't Have One)

1. **Go to:** https://github.com
2. **Sign up** for a free account
3. **Verify your email**

### Step 2: Upload Your Code to GitHub

1. **Go to:** https://github.com/new
2. **Repository name:** `whiskey-inventory` (or whatever you want)
3. **Make it Private** (recommended for business data)
4. **Click "Create repository"**

5. **In your terminal/command prompt**, type these commands one by one:

```bash
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/YOUR-USERNAME/whiskey-inventory.git
git push -u origin main
```

**Replace `YOUR-USERNAME`** with your GitHub username.

**If it asks for your GitHub username/password:**
- Use a Personal Access Token instead of password
- Go to GitHub → Settings → Developer settings → Personal access tokens → Generate new token
- Give it "repo" permissions
- Copy the token and use it as the password

### Step 3: Deploy to Vercel

1. **Go to:** https://vercel.com
2. **Sign up** with your GitHub account (click "Continue with GitHub")
3. **Click "Add New..." → "Project"**
4. **Import your repository:**
   - Find `whiskey-inventory` in the list
   - Click "Import"

5. **Configure the project:**
   - **Framework Preset:** Should auto-detect "Next.js" (don't change)
   - **Root Directory:** Leave as `./` (don't change)
   - **Build Command:** Leave as `npm run build` (don't change)
   - **Output Directory:** Leave as `.next` (don't change)

6. **Add Environment Variables:**
   - Click "Environment Variables"
   - Add these three variables (use the same values from your `.env.local` file):
     - **Name:** `NEXT_PUBLIC_SUPABASE_URL` → **Value:** Your Supabase URL
     - **Name:** `NEXT_PUBLIC_SUPABASE_ANON_KEY` → **Value:** Your anon key
     - **Name:** `DATABASE_URL` → **Value:** Your database connection string
   - **For each variable:** Check all three boxes (Production, Preview, Development)
   - Click "Save" after each one

7. **Deploy:**
   - Click "Deploy"
   - Wait 2-3 minutes for the build to complete
   - You'll see "Congratulations! Your project has been deployed"

8. **Get Your Live URL:**
   - You'll see a URL like `https://whiskey-inventory.vercel.app`
   - Click it to open your live application!

### Step 4: Configure Supabase for Production

1. **Go back to Supabase dashboard**
2. **Settings → Authentication → URL Configuration**
3. **Add your Vercel URL:**
   - **Site URL:** `https://your-app.vercel.app` (your actual Vercel URL)
   - **Redirect URLs:** Add `https://your-app.vercel.app/**`
4. **Click "Save"**

### Step 5: Test Your Live Application

1. **Open your Vercel URL** in a browser
2. **Log in** with the same credentials you created
3. **Everything should work!**

---

## Troubleshooting

### Problem: "npm: command not found"
**Solution:** Node.js isn't installed or not in your PATH. Reinstall Node.js (Part 1, Step 1).

### Problem: "Cannot connect to database"
**Solution:** 
- Check your `.env.local` file has correct values
- Verify your Supabase project is active
- Check your database password is correct

### Problem: "Port 3000 already in use"
**Solution:** 
- Close any other applications using port 3000
- Or change the port: `npm run dev -- -p 3001`

### Problem: "Authentication failed"
**Solution:**
- Make sure you created a user in Supabase (Part 5)
- Check that your Supabase URL and keys are correct
- Verify redirect URLs are set in Supabase

### Problem: Build fails on Vercel
**Solution:**
- Check that all environment variables are set correctly
- Make sure `DATABASE_URL` includes your password
- Check the build logs in Vercel for specific errors

---

## Daily Usage

### To Use the Application Locally:
1. Open terminal/command prompt
2. Navigate to project folder: `cd "C:\path\to\project"`
3. Run: `npm run dev`
4. Open browser: `http://localhost:3000`
5. Log in and use the app!

### To Use the Live Application:
1. Just go to your Vercel URL in any browser
2. Log in and use it!

---

## Getting Help

If you get stuck:
1. **Check the error message** - it usually tells you what's wrong
2. **Read the troubleshooting section** above
3. **Check the README.md** file in the project
4. **Check the DEPLOYMENT.md** file for more details

---

## Security Notes

- **Never share your `.env.local` file** - it contains sensitive credentials
- **Never commit `.env.local` to GitHub** - it's already in `.gitignore`
- **Use strong passwords** for your Supabase database
- **Keep your Supabase credentials secure**

---

## Next Steps

Once everything is working:
1. **Add more users** in Supabase (Authentication → Users)
2. **Create your first barrel batch** to test the system
3. **Explore all the features** - they're all documented in the app
4. **Train your team** on how to use it

**Congratulations! You've successfully set up a production-ready inventory management system!** 🎉

