# How to Install Python (Step-by-Step with Pictures)

## Option 1: Install from python.org (RECOMMENDED)

### Step 1: Download Python
1. Open your web browser
2. Go to: **https://www.python.org/downloads/**
3. You'll see a big yellow button that says **"Download Python 3.x.x"** (the version number will be different)
4. Click that button - it will start downloading

### Step 2: Run the Installer
1. Go to your **Downloads** folder
2. Find the file that says something like `python-3.12.x.exe` (the numbers might be different)
3. **Double-click** that file to run it

### Step 3: IMPORTANT - Check "Add Python to PATH"
1. When the installer opens, you'll see a screen with checkboxes
2. **MOST IMPORTANT:** At the bottom, you'll see a checkbox that says:
   ✅ **"Add Python to PATH"**
3. **CHECK THAT BOX** - this is critical!
4. Then click **"Install Now"**

### Step 4: Wait for Installation
- You'll see a progress bar
- This takes 2-3 minutes
- Don't close the window!

### Step 5: Finish Installation
- When it says "Setup was successful", click **"Close"**

### Step 6: Restart PowerShell
1. **Close** the PowerShell window you have open
2. Open a **NEW** PowerShell window:
   - Press Windows key
   - Type: `powershell`
   - Press Enter

### Step 7: Test Python
In the NEW PowerShell window, type:
```
python --version
```

You should see something like: `Python 3.12.x`

If you see that, Python is installed correctly!

---

## Option 2: Install from Microsoft Store (Alternative)

If you prefer, you can use the Microsoft Store:

1. Click the **Windows key**
2. Type: `Microsoft Store`
3. Press Enter
4. In the Store, search for: **"Python 3.12"** (or latest version)
5. Click **"Get"** or **"Install"**
6. Wait for it to install
7. Close and reopen PowerShell
8. Test with: `python --version`

---

## After Python is Installed

Once Python is installed and you've restarted PowerShell, go back to your CRM folder:

```
cd "C:\Users\PaulOhlms\Desktop\CRM Tool"
```

Then continue with Step 4 from the original guide:
```
python -m pip install -r requirements.txt
```

