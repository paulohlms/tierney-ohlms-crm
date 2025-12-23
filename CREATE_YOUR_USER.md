# Create Your User Account - Step by Step

**Let's set up your login with your email: Paul@tierneyohlms.com**

---

## Step 1: Create User in Supabase

### 1.1 Go to Supabase Dashboard

1. **Go to:** https://supabase.com
2. **Log in** to your account
3. **Select your project** (Whiskey Inventory)

### 1.2 Create New User

1. **Click "Authentication"** in the left sidebar
2. **Click "Users"** (under Authentication)
3. **Click "Add user"** button (top right)
4. **Click "Create new user"**

### 1.3 Fill in Your Details

**In the form that appears:**

1. **Email:** `Paul@tierneyohlms.com`
2. **Password:** Create a password (write it down!)
   - Example: `Whiskey2025!` or whatever you prefer
3. **Auto Confirm User:** Check this box ✅ (so you can log in immediately)
4. **Click "Create user"**

**✅ Done!** You now have a user account.

**Write down:**
- Email: `Paul@tierneyohlms.com`
- Password: (whatever you just created)

---

## Step 2: Get Your Database Password

**You need this for the DATABASE_URL in .env.local**

### Option A: If You Remember Your Password

**Use the password you created when you set up the Supabase project.**

### Option B: If You Forgot It (Reset It)

1. **In Supabase dashboard**, click **"Settings"** (gear icon)
2. **Click "Database"** (under Project Settings)
3. **Scroll down** to find **"Database password"** section
4. **Click "Reset database password"** or **"Generate new password"**
5. **Copy the new password** immediately (write it down!)
6. **This is your database password** - use it in the connection string

---

## Step 3: Build Your Connection String

**Now you can build the DATABASE_URL:**

1. **Get your Project URL:**
   - Settings → API → Project URL
   - Example: `https://abcdefghijklmnop.supabase.co`
   - The project reference is: `abcdefghijklmnop` (the part between `https://` and `.supabase.co`)

2. **Get your database password** (from Step 2 above)

3. **Build the connection string:**
   ```
   postgresql://postgres:YOUR_DATABASE_PASSWORD@db.YOUR_PROJECT_REF.supabase.co:5432/postgres
   ```

**Example:**
- Project URL: `https://abcdefghijklmnop.supabase.co`
- Project reference: `abcdefghijklmnop`
- Database password: `MyPassword123`
- Connection string: `postgresql://postgres:MyPassword123@db.abcdefghijklmnop.supabase.co:5432/postgres`

---

## Step 4: Update .env.local File

1. **Open PowerShell** in Whiskey Inventory folder:
   ```powershell
   cd "C:\Users\PaulOhlms\Desktop\Whiskey Inventory"
   notepad .env.local
   ```

2. **Make sure your file looks like this:**

```
NEXT_PUBLIC_SUPABASE_URL=https://your-project-ref.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=your_anon_key_here
DATABASE_URL=postgresql://postgres:your_database_password@db.your-project-ref.supabase.co:5432/postgres
```

3. **Fill in:**
   - `your-project-ref` with your project reference
   - `your_anon_key_here` with your anon key (from Settings → API)
   - `your_database_password` with your database password

4. **Save** (Ctrl+S) and **close Notepad**

---

## Step 5: Test It

**Now try running the app:**

```powershell
npm run db:generate
```

```powershell
npm run db:push
```

```powershell
npm run dev
```

**Then log in with:**
- Email: `Paul@tierneyohlms.com`
- Password: (the one you created in Step 1.3)

---

## Quick Reference

**Your login credentials:**
- Email: `Paul@tierneyohlms.com`
- Password: (the one you create in Supabase)

**Your database password:**
- The password you created when setting up Supabase project
- OR reset it in Settings → Database → Reset password

---

**Follow Step 1 above to create your user account in Supabase!** 🚀

