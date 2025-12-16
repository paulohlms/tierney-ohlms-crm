'use client'

import { useEffect, useState } from 'react'
import { useRouter } from 'next/navigation'
import { useAuth } from '@/app/providers'
import { Nav } from '@/components/nav'
import { Button } from '@/components/ui/button'
import { DataTable } from '@/components/data-table'
import { formatCurrency, formatDate } from '@/lib/utils'
import { Plus } from 'lucide-react'
import { CreateBarrelBatchDialog } from '@/components/barrel-batch-dialog'

interface BarrelBatch {
  id: string
  name: string | null
  purchaseDate: string
  numBarrels: number
  totalCost: string
  supplier: string | null
  costPerBarrel: string
}

export default function BarrelBatchesPage() {
  const { user, loading } = useAuth()
  const router = useRouter()
  const [batches, setBatches] = useState<BarrelBatch[]>([])
  const [loadingData, setLoadingData] = useState(true)
  const [dialogOpen, setDialogOpen] = useState(false)

  useEffect(() => {
    if (!loading && !user) {
      router.push('/login')
    }
  }, [user, loading, router])

  useEffect(() => {
    if (user) {
      fetchBatches()
    }
  }, [user])

  const fetchBatches = async () => {
    try {
      const res = await fetch('/api/barrel-batches')
      const data = await res.json()
      setBatches(data)
    } catch (error) {
      console.error('Error fetching batches:', error)
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
      accessor: 'name' as keyof BarrelBatch,
    },
    {
      header: 'Purchase Date',
      accessor: 'purchaseDate' as keyof BarrelBatch,
      cell: (value: string) => formatDate(value),
    },
    {
      header: 'Number of Barrels',
      accessor: 'numBarrels' as keyof BarrelBatch,
    },
    {
      header: 'Total Cost',
      accessor: 'totalCost' as keyof BarrelBatch,
      cell: (value: string) => formatCurrency(value),
    },
    {
      header: 'Cost per Barrel',
      accessor: 'costPerBarrel' as keyof BarrelBatch,
      cell: (value: string) => formatCurrency(value),
    },
    {
      header: 'Supplier',
      accessor: 'supplier' as keyof BarrelBatch,
    },
  ]

  return (
    <div className="min-h-screen bg-background">
      <Nav />
      <main className="container mx-auto p-8">
        <div className="mb-8 flex items-center justify-between">
          <h1 className="text-4xl font-bold">Barrel Batches</h1>
          <Button onClick={() => setDialogOpen(true)} size="lg" className="h-12 px-6">
            <Plus className="mr-2 h-5 w-5" />
            Create New Batch
          </Button>
        </div>
        <DataTable
          data={batches}
          columns={columns}
          searchKey="name"
          searchPlaceholder="Search batches..."
          exportFilename="barrel-batches"
        />
        <CreateBarrelBatchDialog
          open={dialogOpen}
          onOpenChange={setDialogOpen}
          onSuccess={fetchBatches}
        />
      </main>
    </div>
  )
}

