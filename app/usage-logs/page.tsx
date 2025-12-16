'use client'

import { useEffect, useState } from 'react'
import { useRouter } from 'next/navigation'
import { useAuth } from '@/app/providers'
import { Nav } from '@/components/nav'
import { Button } from '@/components/ui/button'
import { DataTable } from '@/components/data-table'
import { formatCurrency, formatDate } from '@/lib/utils'
import { Plus } from 'lucide-react'
import { CreateUsageLogDialog } from '@/components/usage-log-dialog'

interface UsageLog {
  id: string
  date: string
  barrel: {
    barrelId: string
  }
  percentUsed: string
  allocatedCost: string
  notes: string | null
}

export default function UsageLogsPage() {
  const { user, loading } = useAuth()
  const router = useRouter()
  const [logs, setLogs] = useState<UsageLog[]>([])
  const [loadingData, setLoadingData] = useState(true)
  const [dialogOpen, setDialogOpen] = useState(false)

  useEffect(() => {
    if (!loading && !user) {
      router.push('/login')
    }
  }, [user, loading, router])

  useEffect(() => {
    if (user) {
      fetchLogs()
    }
  }, [user])

  const fetchLogs = async () => {
    try {
      const res = await fetch('/api/usage-logs')
      const data = await res.json()
      setLogs(data)
    } catch (error) {
      console.error('Error fetching usage logs:', error)
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
      accessor: 'date' as keyof UsageLog,
      cell: (value: string) => formatDate(value),
    },
    {
      header: 'Barrel ID',
      accessor: (row: UsageLog) => row.barrel.barrelId,
    },
    {
      header: '% Used',
      accessor: 'percentUsed' as keyof UsageLog,
      cell: (value: string) => `${parseFloat(value).toFixed(2)}%`,
    },
    {
      header: 'Allocated Cost',
      accessor: 'allocatedCost' as keyof UsageLog,
      cell: (value: string) => formatCurrency(value),
    },
    {
      header: 'Notes',
      accessor: 'notes' as keyof UsageLog,
      cell: (value: string | null) => value || '-',
    },
  ]

  return (
    <div className="min-h-screen bg-background">
      <Nav />
      <main className="container mx-auto p-8">
        <div className="mb-8 flex items-center justify-between">
          <h1 className="text-4xl font-bold">Usage Logs</h1>
          <Button onClick={() => setDialogOpen(true)} size="lg" className="h-12 px-6">
            <Plus className="mr-2 h-5 w-5" />
            Log Usage
          </Button>
        </div>
        <DataTable
          data={logs}
          columns={columns}
          exportFilename="usage-logs"
        />
        <CreateUsageLogDialog
          open={dialogOpen}
          onOpenChange={setDialogOpen}
          onSuccess={fetchLogs}
        />
      </main>
    </div>
  )
}

