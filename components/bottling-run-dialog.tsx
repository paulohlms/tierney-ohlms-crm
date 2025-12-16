'use client'

import { useState, useEffect } from 'react'
import { useForm } from 'react-hook-form'
import { zodResolver } from '@hookform/resolvers/zod'
import { z } from 'zod'
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogFooter, DialogDescription } from '@/components/ui/dialog'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { Textarea } from '@/components/ui/textarea'
import { formatCurrency } from '@/lib/utils'
import { useToast } from '@/hooks/use-toast'
import { Info } from 'lucide-react'

interface CreateBottlingRunDialogProps {
  open: boolean
  onOpenChange: (open: boolean) => void
  onSuccess: () => void
}

interface UsageLog {
  id: string
  date: string
  barrel: {
    barrelId: string
  }
  percentUsed: string
  allocatedCost: string
}

const formSchema = z.object({
  name: z.string().min(1, 'Name is required'),
  date: z.string().min(1, 'Date is required'),
  bottleType: z.string().min(1, 'Bottle type is required'),
  totalBottlesProduced: z.number().int().positive(),
  usageLogIds: z.array(z.string().uuid()).min(1, 'At least one usage log is required'),
  notes: z.string().optional(),
})

type FormData = z.infer<typeof formSchema>

export function CreateBottlingRunDialog({
  open,
  onOpenChange,
  onSuccess,
}: CreateBottlingRunDialogProps) {
  const [loading, setLoading] = useState(false)
  const [usageLogs, setUsageLogs] = useState<UsageLog[]>([])
  const [selectedLogIds, setSelectedLogIds] = useState<string[]>([])
  const { toast } = useToast()
  const {
    register,
    handleSubmit,
    formState: { errors },
    reset,
    setValue,
    watch,
  } = useForm<FormData>({
    resolver: zodResolver(formSchema),
    defaultValues: {
      date: new Date().toISOString().split('T')[0],
      usageLogIds: [],
    },
  })

  useEffect(() => {
    if (open) {
      fetchUsageLogs()
    }
  }, [open])

  const fetchUsageLogs = async () => {
    try {
      const res = await fetch('/api/usage-logs')
      const data = await res.json()
      // Filter out logs already used in bottling runs
      const unusedLogs = data.filter((log: UsageLog & { bottlingRunUsages?: any[] }) => 
        !log.bottlingRunUsages || log.bottlingRunUsages.length === 0
      )
      setUsageLogs(unusedLogs)
    } catch (error) {
      console.error('Error fetching usage logs:', error)
    }
  }

  const toggleUsageLog = (logId: string) => {
    const newSelection = selectedLogIds.includes(logId)
      ? selectedLogIds.filter((id) => id !== logId)
      : [...selectedLogIds, logId]
    setSelectedLogIds(newSelection)
    setValue('usageLogIds', newSelection)
  }

  const selectedLogs = usageLogs.filter((log) => selectedLogIds.includes(log.id))
  const totalCost = selectedLogs.reduce(
    (sum, log) => sum + parseFloat(log.allocatedCost),
    0
  )
  const bottlesProduced = watch('totalBottlesProduced') || 0
  const unitCost = bottlesProduced > 0 ? totalCost / bottlesProduced : 0

  const onSubmit = async (data: FormData) => {
    setLoading(true)
    try {
      const res = await fetch('/api/bottling-runs', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          ...data,
          date: new Date(data.date),
        }),
      })

      if (!res.ok) {
        const error = await res.json()
        throw new Error(error.message || 'Failed to create bottling run')
      }

      reset()
      setSelectedLogIds([])
      toast({
        title: 'Bottling Run Created!',
        description: `Successfully created "${data.name}" with ${data.totalBottlesProduced} bottles.`,
        variant: 'success',
      })
      onSuccess()
      onOpenChange(false)
    } catch (error: any) {
      toast({
        title: 'Error',
        description: error.message || 'Failed to create bottling run. Please try again.',
        variant: 'destructive',
      })
    } finally {
      setLoading(false)
    }
  }

  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent className="max-w-4xl max-h-[90vh] overflow-y-auto">
        <DialogHeader>
          <DialogTitle className="text-2xl">Create Bottling Run</DialogTitle>
          <DialogDescription>
            Link usage logs from barrels to create a production run. Costs are automatically calculated.
          </DialogDescription>
        </DialogHeader>
        <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
          <div className="grid grid-cols-2 gap-4">
            <div className="space-y-2">
              <Label htmlFor="name">Run Name *</Label>
              <Input
                id="name"
                {...register('name')}
                placeholder="e.g., 2025 Rye Batch 1"
                className="h-12 text-lg"
              />
              {errors.name && (
                <p className="text-sm text-destructive">{errors.name.message}</p>
              )}
            </div>
            <div className="space-y-2">
              <Label htmlFor="date">Date *</Label>
              <Input
                id="date"
                type="date"
                {...register('date', { required: true })}
                className="h-12 text-lg"
              />
              {errors.date && (
                <p className="text-sm text-destructive">{errors.date.message}</p>
              )}
            </div>
          </div>

          <div className="grid grid-cols-2 gap-4">
            <div className="space-y-2">
              <Label htmlFor="bottleType">Bottle Type / SKU *</Label>
              <Input
                id="bottleType"
                {...register('bottleType')}
                placeholder="e.g., RYE-750ML-001"
                className="h-12 text-lg"
              />
              {errors.bottleType && (
                <p className="text-sm text-destructive">{errors.bottleType.message}</p>
              )}
            </div>
            <div className="space-y-2">
              <Label htmlFor="totalBottlesProduced">Total Bottles Produced *</Label>
              <Input
                id="totalBottlesProduced"
                type="number"
                {...register('totalBottlesProduced', { valueAsNumber: true, required: true })}
                placeholder="1000"
                className="h-12 text-lg"
              />
              {errors.totalBottlesProduced && (
                <p className="text-sm text-destructive">{errors.totalBottlesProduced.message}</p>
              )}
            </div>
          </div>

          <div className="space-y-2">
            <Label>Select Usage Logs *</Label>
            <div className="max-h-60 overflow-y-auto border rounded-md p-4 space-y-2">
              {usageLogs.length === 0 ? (
                <p className="text-sm text-muted-foreground">No unused usage logs available</p>
              ) : (
                usageLogs.map((log) => (
                  <label
                    key={log.id}
                    className="flex items-center space-x-2 p-2 hover:bg-accent rounded cursor-pointer"
                  >
                    <input
                      type="checkbox"
                      checked={selectedLogIds.includes(log.id)}
                      onChange={() => toggleUsageLog(log.id)}
                      className="h-4 w-4"
                    />
                    <div className="flex-1">
                      <span className="font-medium">{log.barrel.barrelId}</span>
                      <span className="text-sm text-muted-foreground ml-2">
                        {new Date(log.date).toLocaleDateString()} - {parseFloat(log.percentUsed).toFixed(2)}% - {formatCurrency(log.allocatedCost)}
                      </span>
                    </div>
                  </label>
                ))
              )}
            </div>
            {errors.usageLogIds && (
              <p className="text-sm text-destructive">{errors.usageLogIds.message}</p>
            )}
          </div>

          {selectedLogIds.length > 0 && (
            <div className="bg-muted p-4 rounded-md space-y-2">
              <div className="flex justify-between">
                <span className="font-medium">Total Cost:</span>
                <span className="font-bold">{formatCurrency(totalCost)}</span>
              </div>
              {bottlesProduced > 0 && (
                <div className="flex justify-between">
                  <span className="font-medium">Unit Cost:</span>
                  <span className="font-bold">{formatCurrency(unitCost)}</span>
                </div>
              )}
            </div>
          )}

          <div className="space-y-2">
            <Label htmlFor="notes">Notes (Optional)</Label>
            <Textarea
              id="notes"
              {...register('notes')}
              placeholder="Additional notes..."
              className="min-h-[100px] text-lg"
            />
          </div>

          <DialogFooter>
            <Button type="button" variant="outline" onClick={() => onOpenChange(false)}>
              Cancel
            </Button>
            <Button type="submit" disabled={loading || selectedLogIds.length === 0} className="h-12 px-8 text-lg">
              {loading ? 'Creating...' : 'Create Run'}
            </Button>
          </DialogFooter>
        </form>
      </DialogContent>
    </Dialog>
  )
}

