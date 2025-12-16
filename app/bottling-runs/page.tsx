'use client'

import { useEffect, useState } from 'react'
import { useRouter } from 'next/navigation'
import { useAuth } from '@/app/providers'
import { Nav } from '@/components/nav'
import { Button } from '@/components/ui/button'
import { DataTable } from '@/components/data-table'
import { formatCurrency, formatDate } from '@/lib/utils'
import { Plus } from 'lucide-react'
import { CreateBottlingRunDialog } from '@/components/bottling-run-dialog'

interface BottlingRun {
  id: string
  name: string
  date: string
  bottleType: string
  totalBottlesProduced: number
  totalCost: string
  unitCost: string
  remainingInventory: number
}

export default function BottlingRunsPage() {
  const { user, loading } = useAuth()
  const router = useRouter()
  const [runs, setRuns] = useState<BottlingRun[]>([])
  const [loadingData, setLoadingData] = useState(true)
  const [dialogOpen, setDialogOpen] = useState(false)

  useEffect(() => {
    if (!loading && !user) {
      router.push('/login')
    }
  }, [user, loading, router])

  useEffect(() => {
    if (user) {
      fetchRuns()
    }
  }, [user])

  const fetchRuns = async () => {
    try {
      const res = await fetch('/api/bottling-runs')
      const data = await res.json()
      setRuns(data)
    } catch (error) {
      console.error('Error fetching bottling runs:', error)
    } finally {
      setLoadingData(false)
    }
  }

  if (loading || loadingData) {
    return (
      <div className="flex min-h-screen items-center justify-center">
        <div className="text-lg">Loading...</div>
      </div>
    )
  }

  if (!user) return null

  const columns = [
    {
      header: 'Name',
      accessor: 'name' as keyof BottlingRun,
    },
    {
      header: 'Date',
      accessor: 'date' as keyof BottlingRun,
      cell: (value: string) => formatDate(value),
    },
    {
      header: 'Bottle Type',
      accessor: 'bottleType' as keyof BottlingRun,
    },
    {
      header: 'Bottles Produced',
      accessor: 'totalBottlesProduced' as keyof BottlingRun,
    },
    {
      header: 'Remaining',
      accessor: 'remainingInventory' as keyof BottlingRun,
    },
    {
      header: 'Total Cost',
      accessor: 'totalCost' as keyof BottlingRun,
      cell: (value: string) => formatCurrency(value),
    },
    {
      header: 'Unit Cost',
      accessor: 'unitCost' as keyof BottlingRun,
      cell: (value: string) => formatCurrency(value),
    },
  ]

  return (
    <div className="min-h-screen bg-background">
      <Nav />
      <main className="container mx-auto p-8">
        <div className="mb-8 flex items-center justify-between">
          <h1 className="text-4xl font-bold">Bottling Runs</h1>
          <Button onClick={() => setDialogOpen(true)} size="lg" className="h-12 px-6">
            <Plus className="mr-2 h-5 w-5" />
            Create Bottling Run
          </Button>
        </div>
        <DataTable
          data={runs}
          columns={columns}
          searchKey="name"
          searchPlaceholder="Search bottling runs..."
          exportFilename="bottling-runs"
        />
        <CreateBottlingRunDialog
          open={dialogOpen}
          onOpenChange={setDialogOpen}
          onSuccess={fetchRuns}
        />
      </main>
    </div>
  )
}

