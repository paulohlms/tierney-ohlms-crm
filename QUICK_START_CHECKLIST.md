# Quick Start Checklist - Follow This Order

Print this page and check off each step as you complete it!

## ✅ Pre-Setup (15 minutes)

- [ ] **Install Node.js**
  - Go to https://nodejs.org/
  - Download and install
  - Verify: Open terminal, type `node --version`, should show a version number

- [ ] **Install Git**
  - Go to https://git-scm.com/download
  - Download and install
  - Verify: Open terminal, type `git --version`, should show a version number

## ✅ Set Up Supabase (10 minutes)

- [ ] **Create Supabase account**
  - Go to https://supabase.com
  - Sign up with GitHub or Email

- [ ] **Create new project**
  - Click "New Project"
  - Name: `Whiskey Inventory`
  - Create a database password (WRITE IT DOWN!)
  - Select "Free" plan
  - Wait 2-3 minutes for setup

- [ ] **Get credentials**
  - Settings → API → Copy "Project URL"
  - Settings → API → Copy "anon public key"
  - Settings → Database → Copy connection string (replace [YOUR-PASSWORD])
  - Save all three in a text file

- [ ] **Create first user**
  - Authentication → Users → Add user
  - Enter email and password (WRITE IT DOWN!)

## ✅ Set Up Code (10 minutes)

- [ ] **Navigate to project folder**
  - Open terminal/command prompt
  - Type: `cd "path\to\your\project\folder"`

- [ ] **Install dependencies**
  - Type: `npm install`
  - Wait 2-5 minutes for completion

- [ ] **Create .env.local file**
  - Create new file named `.env.local` in project folder
  - Add your three Supabase credentials
  - Save the file

- [ ] **Set up database**
  - Type: `npm run db:generate`
  - Type: `npm run db:push`
  - Should see "Your database is now in sync"

## ✅ Test Locally (5 minutes)

- [ ] **Start the app**
  - Type: `npm run dev`
  - Keep terminal open!

- [ ] **Open in browser**
  - Go to: http://localhost:3000
  - Should see login page

- [ ] **Log in**
  - Use email/password from Supabase
  - Should see dashboard!

- [ ] **Test creating a batch**
  - Click "Barrel Batches" → "Create New Batch"
  - Fill in test data and submit
  - Should see success message

## ✅ Deploy Online (Optional - 15 minutes)

- [ ] **Create GitHub account** (if needed)
  - Go to https://github.com
  - Sign up

- [ ] **Upload code to GitHub**
  - Create new repository
  - Follow GitHub's instructions to push code

- [ ] **Deploy to Vercel**
  - Go to https://vercel.com
  - Sign up with GitHub
  - Import your repository
  - Add environment variables (same as .env.local)
  - Click Deploy
  - Wait 2-3 minutes

- [ ] **Configure Supabase**
  - Settings → Authentication → URL Configuration
  - Add your Vercel URL to Site URL and Redirect URLs

- [ ] **Test live site**
  - Open your Vercel URL
  - Log in and test!

## 🎉 Done!

Your inventory management system is now running!

**Daily use:**
- Local: Run `npm run dev` then go to http://localhost:3000
- Online: Just visit your Vercel URL

**Need help?** Check SETUP_GUIDE_FOR_ACCOUNTANTS.md for detailed instructions.

