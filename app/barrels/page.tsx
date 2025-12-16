'use client'

import { useEffect, useState } from 'react'
import { useRouter } from 'next/navigation'
import Link from 'next/link'
import { useAuth } from '@/app/providers'
import { Nav } from '@/components/nav'
import { Button } from '@/components/ui/button'
import { DataTable } from '@/components/data-table'
import { Input } from '@/components/ui/input'
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select'
import { formatPercent } from '@/lib/utils'
import { Edit, AlertCircle, Plus } from 'lucide-react'
import { EditBarrelDialog } from '@/components/barrel-dialog'
import { Card, CardContent } from '@/components/ui/card'
import { Progress } from '@/components/ui/progress'

interface Barrel {
  id: string
  barrelId: string
  batchId: string
  groupLabel: string | null
  currentFillPercent: string
  status: string
  batch: {
    name: string | null
  }
}

export default function BarrelsPage() {
  const { user, loading } = useAuth()
  const router = useRouter()
  const [barrels, setBarrels] = useState<Barrel[]>([])
  const [filteredBarrels, setFilteredBarrels] = useState<Barrel[]>([])
  const [loadingData, setLoadingData] = useState(true)
  const [search, setSearch] = useState('')
  const [statusFilter, setStatusFilter] = useState<string>('all')
  const [groupFilter, setGroupFilter] = useState<string>('all')
  const [editingBarrel, setEditingBarrel] = useState<Barrel | null>(null)

  useEffect(() => {
    if (!loading && !user) {
      router.push('/login')
    }
  }, [user, loading, router])

  useEffect(() => {
    if (user) {
      fetchBarrels()
    }
  }, [user])

  useEffect(() => {
    let filtered = barrels

    if (search) {
      filtered = filtered.filter(
        (b) =>
          b.barrelId.toLowerCase().includes(search.toLowerCase()) ||
          b.groupLabel?.toLowerCase().includes(search.toLowerCase())
      )
    }

    if (statusFilter !== 'all') {
      filtered = filtered.filter((b) => b.status === statusFilter)
    }

    if (groupFilter !== 'all') {
      filtered = filtered.filter((b) => b.groupLabel === groupFilter)
    }

    setFilteredBarrels(filtered)
  }, [barrels, search, statusFilter, groupFilter])

  const fetchBarrels = async () => {
    try {
      const res = await fetch('/api/barrels')
      const data = await res.json()
      setBarrels(data)
    } catch (error) {
      console.error('Error fetching barrels:', error)
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

  const statuses = Array.from(new Set(barrels.map((b) => b.status)))
  const groups = Array.from(new Set(barrels.map((b) => b.groupLabel).filter(Boolean)))

  const columns = [
    {
      header: 'Barrel ID',
      accessor: 'barrelId' as keyof Barrel,
    },
    {
      header: 'Batch',
      accessor: (row: Barrel) => row.batch.name || 'N/A',
    },
    {
      header: 'Group Label',
      accessor: 'groupLabel' as keyof Barrel,
      cell: (value: string | null) => value || '-',
    },
    {
      header: 'Fill Level',
      accessor: 'currentFillPercent' as keyof Barrel,
      cell: (value: string, row: Barrel) => {
        const fill = parseFloat(value)
        const color = fill > 75 ? 'bg-green-500' : fill > 25 ? 'bg-yellow-500' : 'bg-red-500'
        return (
          <div className="flex items-center gap-3 min-w-[150px]">
            <Progress value={fill} className="flex-1 h-3" />
            <span className="text-sm font-medium w-12 text-right">{formatPercent(value)}</span>
          </div>
        )
      },
    },
    {
      header: 'Status',
      accessor: 'status' as keyof Barrel,
    },
    {
      header: 'Actions',
      accessor: (row: Barrel) => (
        <Button
          variant="outline"
          size="sm"
          onClick={() => setEditingBarrel(row)}
        >
          <Edit className="h-4 w-4" />
        </Button>
      ),
    },
  ]

  return (
    <div className="min-h-screen bg-background">
      <Nav />
      <main className="container mx-auto p-8">
        <h1 className="mb-8 text-4xl font-bold">Barrels</h1>
        <div className="mb-4 flex flex-wrap gap-4">
          <Input
            placeholder="Search by Barrel ID or Group..."
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            className="max-w-sm h-12 text-lg"
          />
          <Select value={statusFilter} onValueChange={setStatusFilter}>
            <SelectTrigger className="w-[180px] h-12 text-lg">
              <SelectValue placeholder="Filter by Status" />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="all">All Statuses</SelectItem>
              {statuses.map((status) => (
                <SelectItem key={status} value={status}>
                  {status}
                </SelectItem>
              ))}
            </SelectContent>
          </Select>
          <Select value={groupFilter} onValueChange={setGroupFilter}>
            <SelectTrigger className="w-[180px] h-12 text-lg">
              <SelectValue placeholder="Filter by Group" />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="all">All Groups</SelectItem>
              {groups.map((group) => (
                <SelectItem key={group} value={group || ''}>
                  {group || 'No Group'}
                </SelectItem>
              ))}
            </SelectContent>
          </Select>
        </div>
        {filteredBarrels.length === 0 ? (
          <Card className="border-dashed">
            <CardContent className="flex flex-col items-center justify-center py-12">
              <AlertCircle className="h-12 w-12 text-muted-foreground mb-4" />
              <h3 className="text-xl font-semibold mb-2">
                {barrels.length === 0 ? 'No Barrels Yet' : 'No Barrels Match Your Filters'}
              </h3>
              <p className="text-muted-foreground text-center mb-6 max-w-md">
                {barrels.length === 0
                  ? 'Barrels are created automatically when you add a barrel batch. Create your first batch to get started.'
                  : 'Try adjusting your search or filters to see more results.'}
              </p>
              {barrels.length === 0 && (
                <Link href="/barrel-batches">
                  <Button size="lg">
                    <Plus className="mr-2 h-5 w-5" />
                    Create Barrel Batch
                  </Button>
                </Link>
              )}
            </CardContent>
          </Card>
        ) : (
          <DataTable
            data={filteredBarrels}
            columns={columns}
            exportFilename="barrels"
          />
        )}
        {editingBarrel && (
          <EditBarrelDialog
            open={!!editingBarrel}
            onOpenChange={(open) => !open && setEditingBarrel(null)}
            barrel={editingBarrel}
            onSuccess={fetchBarrels}
          />
        )}
      </main>
    </div>
  )
}

