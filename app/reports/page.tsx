'use client'

import { useEffect, useState } from 'react'
import { useRouter } from 'next/navigation'
import { useAuth } from '@/app/providers'
import { Nav } from '@/components/nav'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { DataTable } from '@/components/data-table'
import { formatCurrency } from '@/lib/utils'
import { Download } from 'lucide-react'

interface MonthlyReport {
  month: string
  shipments: {
    bottleType: string
    totalUnits: number
    totalCOGS: number
  }[]
  totalCOGS: number
}

export default function ReportsPage() {
  const { user, loading } = useAuth()
  const router = useRouter()
  const [report, setReport] = useState<MonthlyReport | null>(null)
  const [loadingData, setLoadingData] = useState(false)
  const [selectedMonth, setSelectedMonth] = useState(() => {
    const now = new Date()
    return `${now.getFullYear()}-${String(now.getMonth() + 1).padStart(2, '0')}`
  })

  useEffect(() => {
    if (!loading && !user) {
      router.push('/login')
    }
  }, [user, loading, router])

  useEffect(() => {
    if (user) {
      fetchReport()
    }
  }, [user, selectedMonth])

  const fetchReport = async () => {
    setLoadingData(true)
    try {
      const res = await fetch(`/api/reports/monthly?month=${selectedMonth}`)
      const data = await res.json()
      setReport(data)
    } catch (error) {
      console.error('Error fetching report:', error)
    } finally {
      setLoadingData(false)
    }
  }

  if (loading) {
    return (
      <div className="flex min-h-screen items-center justify-center">
        <div className="text-lg">Loading...</div>
      </div>
    )
  }

  if (!user) return null

  const columns = report
    ? [
        {
          header: 'Bottle Type',
          accessor: 'bottleType' as keyof (typeof report.shipments)[0],
        },
        {
          header: 'Total Units Shipped',
          accessor: 'totalUnits' as keyof (typeof report.shipments)[0],
        },
        {
          header: 'Total COGS',
          accessor: 'totalCOGS' as keyof (typeof report.shipments)[0],
          cell: (value: number) => formatCurrency(value),
        },
      ]
    : []

  return (
    <div className="min-h-screen bg-background">
      <Nav />
      <main className="container mx-auto p-8">
        <h1 className="mb-8 text-4xl font-bold">Monthly Reports</h1>

        <Card className="mb-8">
          <CardHeader>
            <CardTitle>Select Month</CardTitle>
            <CardDescription>View monthly shipment summary and COGS</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="flex items-center space-x-4">
              <div className="space-y-2">
                <Label htmlFor="month">Month</Label>
                <Input
                  id="month"
                  type="month"
                  value={selectedMonth}
                  onChange={(e) => setSelectedMonth(e.target.value)}
                  className="h-12 text-lg"
                />
              </div>
              <Button onClick={fetchReport} size="lg" className="h-12 mt-6">
                Generate Report
              </Button>
            </div>
          </CardContent>
        </Card>

        {loadingData ? (
          <div className="text-center py-8">Loading report...</div>
        ) : report ? (
          <div className="space-y-6">
            <Card>
              <CardHeader>
                <CardTitle>Monthly Summary</CardTitle>
                <CardDescription>
                  {new Date(selectedMonth + '-01').toLocaleDateString('en-US', {
                    month: 'long',
                    year: 'numeric',
                  })}
                </CardDescription>
              </CardHeader>
              <CardContent>
                <div className="text-3xl font-bold mb-4">
                  Total COGS: {formatCurrency(report.totalCOGS)}
                </div>
                <div className="text-lg text-muted-foreground">
                  {report.shipments.length} bottle type{report.shipments.length !== 1 ? 's' : ''} shipped
                </div>
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle>Shipments by Bottle Type</CardTitle>
              </CardHeader>
              <CardContent>
                <DataTable
                  data={report.shipments}
                  columns={columns}
                  exportFilename={`monthly-report-${selectedMonth}`}
                />
              </CardContent>
            </Card>
          </div>
        ) : (
          <Card>
            <CardContent className="py-8 text-center text-muted-foreground">
              Select a month and generate a report
            </CardContent>
          </Card>
        )}
      </main>
    </div>
  )
}

