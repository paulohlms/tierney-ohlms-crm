# Quick Start Guide

Get your Whiskey Inventory Management System up and running in 10 minutes.

## Prerequisites

- Node.js 18+ installed
- A Supabase account (free)

## Step 1: Install Dependencies

```bash
npm install
```

## Step 2: Set Up Supabase

1. Go to [supabase.com](https://supabase.com) and create a new project
2. Wait for database to be ready (2-3 minutes)
3. Go to **Settings** > **API** and copy:
   - Project URL
   - anon public key
4. Go to **Settings** > **Database** and copy the connection string (URI format)

## Step 3: Create Environment File

Create `.env.local` in the project root:

```env
NEXT_PUBLIC_SUPABASE_URL=your_supabase_url_here
NEXT_PUBLIC_SUPABASE_ANON_KEY=your_anon_key_here
DATABASE_URL=your_database_connection_string_here
```

## Step 4: Set Up Database

```bash
# Generate Prisma client
npm run db:generate

# Push schema to database
npm run db:push
```

## Step 5: Seed Sample Data (Optional)

```bash
npm run db:seed
```

## Step 6: Create Your First User

1. Go to Supabase dashboard > **Authentication** > **Users**
2. Click "Add user" > "Create new user"
3. Enter email and password
4. Save credentials for login

## Step 7: Run Development Server

```bash
npm run dev
```

Open [http://localhost:3000](http://localhost:3000) and log in!

## What's Next?

- See [README.md](./README.md) for full documentation
- See [DEPLOYMENT.md](./DEPLOYMENT.md) for production deployment
- Start creating barrel batches and tracking inventory!

## Troubleshooting

**"Prisma Client not generated"**
- Run `npm run db:generate`

**"Database connection failed"**
- Check your DATABASE_URL in `.env.local`
- Verify Supabase project is active

**"Authentication error"**
- Verify NEXT_PUBLIC_SUPABASE_URL and NEXT_PUBLIC_SUPABASE_ANON_KEY
- Check user exists in Supabase Auth

