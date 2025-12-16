# Whiskey Inventory Management System

A complete, production-ready inventory management web application for a subscription-based whiskey company. Built with Next.js 14, Supabase, and Prisma.

## Features

- **Barrel Batch Management**: Create batches, track purchases, auto-calculate cost per barrel
- **Individual Barrel Tracking**: Track each barrel with custom labels, fill levels, and status
- **Usage Logging**: Log whiskey usage from barrels with automatic cost allocation
- **Bottling Runs**: Create production runs linking multiple usage logs with automatic cost calculation
- **Shipments**: Record outgoing inventory with automatic COGS calculation
- **Monthly Reports**: Accountant-friendly reports with CSV export
- **User-Friendly UI**: Large buttons, simple forms, guided workflows for non-technical users

## Tech Stack

- **Frontend**: Next.js 14 (App Router), React, Tailwind CSS, shadcn/ui
- **Backend**: Next.js API Routes + Supabase (PostgreSQL, Auth)
- **ORM**: Prisma
- **Validation**: Zod
- **Deployment**: Vercel

## Prerequisites

- Node.js 18+ and npm/yarn
- Supabase account (free tier works)
- Vercel account (for deployment)

## Setup Instructions

### 1. Clone and Install

```bash
# Install dependencies
npm install

# Or with yarn
yarn install
```

### 2. Set Up Supabase

1. Go to [supabase.com](https://supabase.com) and create a new project
2. Wait for the database to be provisioned
3. Go to Project Settings > API
4. Copy your `Project URL` and `anon public` key
5. Go to Project Settings > Database
6. Copy your connection string (under "Connection string" > "URI")

### 3. Configure Environment Variables

Create a `.env.local` file in the root directory:

```env
NEXT_PUBLIC_SUPABASE_URL=your_supabase_project_url
NEXT_PUBLIC_SUPABASE_ANON_KEY=your_supabase_anon_key
DATABASE_URL=your_supabase_connection_string
```

### 4. Set Up Database Schema

```bash
# Generate Prisma client
npm run db:generate

# Push schema to database
npm run db:push
```

### 5. Seed Sample Data (Optional)

```bash
npm run db:seed
```

This will create:
- A sample barrel batch with 10 barrels
- Sample usage logs
- Sample bottling runs
- Sample shipments

### 6. Run Development Server

```bash
npm run dev
```

Open [http://localhost:3000](http://localhost:3000) in your browser.

### 7. Create Your First User

1. Go to your Supabase dashboard
2. Navigate to Authentication > Users
3. Click "Add user" > "Create new user"
4. Enter an email and password
5. Use these credentials to log in to the app

## Deployment to Vercel

### 1. Push to GitHub

```bash
git init
git add .
git commit -m "Initial commit"
git remote add origin your-repo-url
git push -u origin main
```

### 2. Deploy to Vercel

1. Go to [vercel.com](https://vercel.com)
2. Click "New Project"
3. Import your GitHub repository
4. Add environment variables:
   - `NEXT_PUBLIC_SUPABASE_URL`
   - `NEXT_PUBLIC_SUPABASE_ANON_KEY`
   - `DATABASE_URL`
5. Click "Deploy"

### 3. Run Database Migrations

After deployment, run migrations:

```bash
# In Vercel, go to your project > Settings > Environment Variables
# Or use Vercel CLI:
vercel env pull .env.local
npm run db:push
```

### 4. Set Up Authentication

1. In Supabase dashboard, go to Authentication > URL Configuration
2. Add your Vercel domain to "Site URL" and "Redirect URLs"
3. Example: `https://your-app.vercel.app`

## Project Structure

```
├── app/                    # Next.js app directory
│   ├── api/               # API routes
│   ├── barrel-batches/    # Barrel batches page
│   ├── barrels/           # Barrels list page
│   ├── usage-logs/        # Usage logs page
│   ├── bottling-runs/     # Bottling runs page
│   ├── shipments/         # Shipments page
│   ├── reports/           # Reports page
│   └── login/             # Login page
├── components/            # React components
│   ├── ui/               # shadcn/ui components
│   └── ...               # Feature components
├── lib/                   # Utilities and config
│   ├── prisma.ts         # Prisma client
│   ├── supabase.ts       # Supabase client
│   └── validations.ts    # Zod schemas
└── prisma/               # Prisma schema
    └── schema.prisma     # Database schema
```

## Key Features Explained

### Barrel Batch Management
- Create batches with total cost and number of barrels
- Automatically creates individual barrel records (BAR-001, BAR-002, etc.)
- Auto-calculates cost per barrel

### Usage Logging
- Select barrel and enter percentage used
- Automatically calculates allocated cost based on barrel's batch cost
- Updates barrel fill percentage
- Marks barrel as "Empty" when fill reaches 0%

### Bottling Runs
- Link multiple usage logs from same or different barrels
- Auto-calculates total cost (sum of linked usage costs)
- Auto-calculates unit cost per bottle
- Tracks remaining inventory

### Shipments
- Record shipments with quantity and customer reference
- Automatically deducts from bottled inventory
- Calculates COGS based on bottling run's unit cost

### Reports
- Monthly summary grouped by bottle type
- Shows total units shipped and total COGS
- CSV export for accountant-friendly reporting

## Database Schema

- `barrel_batches`: Purchases of multiple barrels
- `barrels`: Individual barrel tracking
- `usage_logs`: Records of whiskey usage from barrels
- `bottling_runs`: Production runs creating bottled inventory
- `bottling_run_usages`: Junction table linking runs to usage logs
- `shipments`: Outgoing inventory records

## Troubleshooting

### Database Connection Issues
- Verify your `DATABASE_URL` is correct
- Check Supabase project is active
- Ensure database is accessible from your IP (Supabase allows all by default)

### Authentication Issues
- Verify Supabase URL and keys are correct
- Check redirect URLs in Supabase dashboard
- Ensure user exists in Supabase Auth

### Build Errors
- Run `npm run db:generate` before building
- Ensure all environment variables are set
- Check Prisma schema is valid: `npx prisma validate`

## Support

For issues or questions, please check:
1. Prisma documentation: https://www.prisma.io/docs
2. Supabase documentation: https://supabase.com/docs
3. Next.js documentation: https://nextjs.org/docs

## License

MIT
