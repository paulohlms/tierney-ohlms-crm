'use client'

import { useEffect, useState } from 'react'
import { useRouter } from 'next/navigation'
import { useAuth } from '@/app/providers'
import { Nav } from '@/components/nav'
import { Button } from '@/components/ui/button'
import { DataTable } from '@/components/data-table'
import { formatCurrency, formatDate } from '@/lib/utils'
import { Plus } from 'lucide-react'
import { CreateShipmentDialog } from '@/components/shipment-dialog'

interface Shipment {
  id: string
  date: string
  bottlingRun: {
    name: string
    bottleType: string
  }
  quantity: number
  customerRef: string | null
  cogs: string
  notes: string | null
}

export default function ShipmentsPage() {
  const { user, loading } = useAuth()
  const router = useRouter()
  const [shipments, setShipments] = useState<Shipment[]>([])
  const [loadingData, setLoadingData] = useState(true)
  const [dialogOpen, setDialogOpen] = useState(false)

  useEffect(() => {
    if (!loading && !user) {
      router.push('/login')
    }
  }, [user, loading, router])

  useEffect(() => {
    if (user) {
      fetchShipments()
    }
  }, [user])

  const fetchShipments = async () => {
    try {
      const res = await fetch('/api/shipments')
      const data = await res.json()
      setShipments(data)
    } catch (error) {
      console.error('Error fetching shipments:', error)
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
      header: 'Date',
      accessor: 'date' as keyof Shipment,
      cell: (value: string) => formatDate(value),
    },
    {
      header: 'Bottling Run',
      accessor: (row: Shipment) => row.bottlingRun.name,
    },
    {
      header: 'Bottle Type',
      accessor: (row: Shipment) => row.bottlingRun.bottleType,
    },
    {
      header: 'Quantity',
      accessor: 'quantity' as keyof Shipment,
    },
    {
      header: 'Customer Ref',
      accessor: 'customerRef' as keyof Shipment,
      cell: (value: string | null) => value || '-',
    },
    {
      header: 'COGS',
      accessor: 'cogs' as keyof Shipment,
      cell: (value: string) => formatCurrency(value),
    },
    {
      header: 'Notes',
      accessor: 'notes' as keyof Shipment,
      cell: (value: string | null) => value || '-',
    },
  ]

  return (
    <div className="min-h-screen bg-background">
      <Nav />
      <main className="container mx-auto p-8">
        <div className="mb-8 flex items-center justify-between">
          <h1 className="text-4xl font-bold">Shipments</h1>
          <Button onClick={() => setDialogOpen(true)} size="lg" className="h-12 px-6">
            <Plus className="mr-2 h-5 w-5" />
            Record Shipment
          </Button>
        </div>
        <DataTable
          data={shipments}
          columns={columns}
          exportFilename="shipments"
        />
        <CreateShipmentDialog
          open={dialogOpen}
          onOpenChange={setDialogOpen}
          onSuccess={fetchShipments}
        />
      </main>
    </div>
  )
}

