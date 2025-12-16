'use client'

import { useEffect } from 'react'
import { useRouter } from 'next/navigation'
import Link from 'next/link'
import { useAuth } from './providers'
import { Nav } from '@/components/nav'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import React from 'react'
import { Plus, Package, Barrel, FileText, Truck, ArrowRight, TrendingUp, AlertCircle } from 'lucide-react'

export default function HomePage() {
  const { user, loading } = useAuth()
  const router = useRouter()

  useEffect(() => {
    if (!loading && !user) {
      router.push('/login')
    }
  }, [user, loading, router])

  if (loading) {
    return (
      <div className="flex min-h-screen items-center justify-center">
        <div className="text-lg">Loading...</div>
      </div>
    )
  }

  if (!user) {
    return null
  }

  return (
    <div className="min-h-screen bg-background">
      <Nav />
      <main className="container mx-auto p-8">
        <div className="mb-8">
          <h1 className="text-4xl font-bold mb-2">Dashboard</h1>
          <p className="text-muted-foreground text-lg">Overview of your whiskey inventory and operations</p>
        </div>
        <DashboardStatsClient />
        <QuickActions />
      </main>
    </div>
  )
}

function QuickActions() {
  return (
    <Card className="mt-8">
      <CardHeader>
        <CardTitle>Quick Actions</CardTitle>
        <CardDescription>Common tasks to get started</CardDescription>
      </CardHeader>
      <CardContent>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          <Link href="/barrel-batches">
            <Button variant="outline" className="w-full h-20 flex-col gap-2">
              <Package className="h-6 w-6" />
              <span>Create Barrel Batch</span>
            </Button>
          </Link>
          <Link href="/usage-logs">
            <Button variant="outline" className="w-full h-20 flex-col gap-2">
              <FileText className="h-6 w-6" />
              <span>Log Barrel Usage</span>
            </Button>
          </Link>
          <Link href="/bottling-runs">
            <Button variant="outline" className="w-full h-20 flex-col gap-2">
              <Barrel className="h-6 w-6" />
              <span>Create Bottling Run</span>
            </Button>
          </Link>
          <Link href="/shipments">
            <Button variant="outline" className="w-full h-20 flex-col gap-2">
              <Truck className="h-6 w-6" />
              <span>Record Shipment</span>
            </Button>
          </Link>
          <Link href="/reports">
            <Button variant="outline" className="w-full h-20 flex-col gap-2">
              <TrendingUp className="h-6 w-6" />
              <span>View Reports</span>
            </Button>
          </Link>
          <Link href="/barrels">
            <Button variant="outline" className="w-full h-20 flex-col gap-2">
              <Barrel className="h-6 w-6" />
              <span>Manage Barrels</span>
            </Button>
          </Link>
        </div>
      </CardContent>
    </Card>
  )
}

function DashboardStatsClient() {
  const [stats, setStats] = React.useState<any>(null)
  const [loading, setLoading] = React.useState(true)

  React.useEffect(() => {
    fetch('/api/dashboard/stats')
      .then((res) => res.json())
      .then((data) => {
        setStats(data)
        setLoading(false)
      })
      .catch(() => setLoading(false))
  }, [])

  if (loading) {
    return (
      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
        {[1, 2, 3, 4].map((i) => (
          <Card key={i}>
            <CardHeader>
              <div className="h-4 bg-muted animate-pulse rounded w-24"></div>
              <div className="h-3 bg-muted animate-pulse rounded w-32 mt-2"></div>
            </CardHeader>
            <CardContent>
              <div className="h-8 bg-muted animate-pulse rounded w-20"></div>
            </CardContent>
          </Card>
        ))}
      </div>
    )
  }

  const isEmpty = !stats || (stats.totalBarrels === 0 && stats.bottledInventory === 0)

  if (isEmpty) {
    return (
      <Card className="border-dashed">
        <CardContent className="flex flex-col items-center justify-center py-12">
          <AlertCircle className="h-12 w-12 text-muted-foreground mb-4" />
          <h3 className="text-xl font-semibold mb-2">No Data Yet</h3>
          <p className="text-muted-foreground text-center mb-6 max-w-md">
            Get started by creating your first barrel batch. This will automatically create individual barrel records.
          </p>
          <Link href="/barrel-batches">
            <Button size="lg">
              <Plus className="mr-2 h-5 w-5" />
              Create Your First Batch
            </Button>
          </Link>
        </CardContent>
      </Card>
    )
  }

  return (
    <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
      <Card className="hover:shadow-md transition-shadow">
        <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
          <CardTitle className="text-sm font-medium">Total Barrels</CardTitle>
          <Barrel className="h-4 w-4 text-muted-foreground" />
        </CardHeader>
        <CardContent>
          <div className="text-3xl font-bold">{stats?.totalBarrels ?? 0}</div>
          <p className="text-xs text-muted-foreground mt-1">All barrels in inventory</p>
        </CardContent>
      </Card>
      <Card className="hover:shadow-md transition-shadow">
        <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
          <CardTitle className="text-sm font-medium">Aging Inventory</CardTitle>
          <Package className="h-4 w-4 text-muted-foreground" />
        </CardHeader>
        <CardContent>
          <div className="text-3xl font-bold">{stats?.agingBarrels ?? 0}</div>
          <p className="text-xs text-muted-foreground mt-1">Barrels currently aging</p>
        </CardContent>
      </Card>
      <Card className="hover:shadow-md transition-shadow">
        <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
          <CardTitle className="text-sm font-medium">Bottled Inventory</CardTitle>
          <Package className="h-4 w-4 text-muted-foreground" />
        </CardHeader>
        <CardContent>
          <div className="text-3xl font-bold">{stats?.bottledInventory ?? 0}</div>
          <p className="text-xs text-muted-foreground mt-1">Total bottles in stock</p>
        </CardContent>
      </Card>
      <Card className="hover:shadow-md transition-shadow">
        <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
          <CardTitle className="text-sm font-medium">Monthly COGS</CardTitle>
          <TrendingUp className="h-4 w-4 text-muted-foreground" />
        </CardHeader>
        <CardContent>
          <div className="text-3xl font-bold">
            {stats?.monthlyCOGS ? `$${stats.monthlyCOGS.toLocaleString()}` : '$0'}
          </div>
          <p className="text-xs text-muted-foreground mt-1">This month&apos;s cost of goods sold</p>
        </CardContent>
      </Card>
    </div>
  )
}

