# 🚀 Simple Start Guide for Accountants

Don't worry - I'll walk you through this step by step. It's like setting up a new software program.

## Step 1: Install Python (5 minutes)

Python is the programming language this app needs to run.

1. **Go to this website:** https://www.python.org/downloads/
2. **Click the big yellow "Download Python" button** (it will download the latest version)
3. **Run the downloaded file** (it will be something like `python-3.12.x.exe`)
4. **IMPORTANT:** On the first screen, check the box that says **"Add Python to PATH"** ✅
5. Click "Install Now"
6. Wait for it to finish (2-3 minutes)
7. Click "Close" when done

## Step 2: Open PowerShell (30 seconds)

1. Press the **Windows key** on your keyboard
2. Type: `powershell`
3. Press **Enter**
4. A blue window will open - that's PowerShell

## Step 3: Go to Your CRM Folder (30 seconds)

In the PowerShell window, type this and press Enter:

```
cd "C:\Users\PaulOhlms\Desktop\CRM Tool"
```

## Step 4: Install the App's Tools (2 minutes)

Copy and paste this line into PowerShell and press Enter:

```
python -m pip install -r requirements.txt
```

Wait for it to finish (you'll see lots of text scrolling). When it says "Successfully installed" at the end, you're done.

## Step 5: Set Up the Database (30 seconds)

Type this and press Enter:

```
python seed.py
```

You should see "Database seeded successfully!"

## Step 6: Start the App (30 seconds)

Type this and press Enter:

```
python -m uvicorn main:app --reload
```

You'll see a message that says "Uvicorn running on http://127.0.0.1:8000"

**KEEP THIS WINDOW OPEN** - don't close it!

## Step 7: Open the App in Your Browser

1. Open your web browser (Chrome, Edge, Firefox - any browser)
2. In the address bar, type: `http://localhost:8000`
3. Press Enter

## Step 8: Log In

- **Email:** `admin@firm.com`
- **Password:** `admin123`

That's it! You should now see your client list.

---

## ⚠️ Troubleshooting

**If Step 4 says "python is not recognized":**
- Python didn't install correctly
- Go back to Step 1 and make sure you checked "Add Python to PATH"
- After reinstalling, close and reopen PowerShell

**If you get an error about "port already in use":**
- Something else is using port 8000
- Close any other programs
- Or restart your computer and try again

**If the browser says "can't connect":**
- Make sure the PowerShell window is still open and showing "Uvicorn running"
- If you closed it, go back to Step 6

---

## 📝 Quick Reference

**To start the app later:**
1. Open PowerShell
2. Type: `cd "C:\Users\PaulOhlms\Desktop\CRM Tool"`
3. Type: `python -m uvicorn main:app --reload`
4. Open browser to `http://localhost:8000`

**To stop the app:**
- Click in the PowerShell window
- Press `Ctrl + C`
- Type `Y` and press Enter

