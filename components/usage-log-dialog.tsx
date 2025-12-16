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
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select'
import { useToast } from '@/hooks/use-toast'
import { Info } from 'lucide-react'
import { formatCurrency } from '@/lib/utils'

interface CreateUsageLogDialogProps {
  open: boolean
  onOpenChange: (open: boolean) => void
  onSuccess: () => void
}

interface Barrel {
  id: string
  barrelId: string
  currentFillPercent: string
}

const formSchema = z.object({
  date: z.string().min(1, 'Date is required'),
  barrelId: z.string().uuid('Please select a barrel'),
  percentUsed: z.number().positive().max(100),
  notes: z.string().optional(),
})

type FormData = z.infer<typeof formSchema>

interface BarrelWithCost extends Barrel {
  batch?: {
    totalCost: string
    numBarrels: number
  }
}

export function CreateUsageLogDialog({
  open,
  onOpenChange,
  onSuccess,
}: CreateUsageLogDialogProps) {
  const [loading, setLoading] = useState(false)
  const [barrels, setBarrels] = useState<BarrelWithCost[]>([])
  const [selectedBarrel, setSelectedBarrel] = useState<BarrelWithCost | null>(null)
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
    },
  })

  useEffect(() => {
    if (open) {
      fetchBarrels()
    }
  }, [open])

  const fetchBarrels = async () => {
    try {
      const res = await fetch('/api/barrels?includeBatch=true')
      const data = await res.json()
      setBarrels(data.filter((b: BarrelWithCost) => parseFloat(b.currentFillPercent) > 0))
    } catch (error) {
      console.error('Error fetching barrels:', error)
      // Fallback to basic fetch
      const res = await fetch('/api/barrels')
      const data = await res.json()
      setBarrels(data.filter((b: Barrel) => parseFloat(b.currentFillPercent) > 0))
    }
  }

  const onSubmit = async (data: FormData) => {
    setLoading(true)
    try {
      const res = await fetch('/api/usage-logs', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          ...data,
          date: new Date(data.date),
        }),
      })

      if (!res.ok) {
        const error = await res.json()
        throw new Error(error.message || 'Failed to create usage log')
      }

      reset()
      toast({
        title: 'Usage Logged!',
        description: `Successfully logged ${data.percentUsed}% usage from ${selectedBarrel?.barrelId || 'barrel'}.`,
        variant: 'success',
      })
      onSuccess()
      onOpenChange(false)
    } catch (error: any) {
      toast({
        title: 'Error',
        description: error.message || 'Failed to create usage log. Please try again.',
        variant: 'destructive',
      })
    } finally {
      setLoading(false)
    }
  }

  const percentUsed = watch('percentUsed') || 0
  const estimatedCost = selectedBarrel && selectedBarrel.batch && percentUsed > 0
    ? (Number(selectedBarrel.batch.totalCost) / selectedBarrel.batch.numBarrels) * (percentUsed / 100)
    : 0

  const selectedBarrelId = watch('barrelId')
  useEffect(() => {
    if (selectedBarrelId) {
      const barrel = barrels.find((b) => b.id === selectedBarrelId)
      setSelectedBarrel(barrel || null)
    }
  }, [selectedBarrelId, barrels])

  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent className="max-w-2xl">
        <DialogHeader>
          <DialogTitle className="text-2xl">Log Barrel Usage</DialogTitle>
          <DialogDescription>
            Record when whiskey is used from a barrel. The system will automatically calculate the cost allocation.
          </DialogDescription>
        </DialogHeader>
        <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
          <div className="grid grid-cols-2 gap-4">
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
            <div className="space-y-2">
              <Label htmlFor="barrelId">Barrel *</Label>
              <Select
                value={watch('barrelId')}
                onValueChange={(value) => setValue('barrelId', value)}
              >
                <SelectTrigger className="h-12 text-lg">
                  <SelectValue placeholder="Select a barrel" />
                </SelectTrigger>
                <SelectContent>
                  {barrels.map((barrel) => (
                    <SelectItem key={barrel.id} value={barrel.id}>
                      {barrel.barrelId} ({parseFloat(barrel.currentFillPercent).toFixed(1)}% remaining)
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
              {errors.barrelId && (
                <p className="text-sm text-destructive">{errors.barrelId.message}</p>
              )}
            </div>
          </div>

          <div className="space-y-2">
            <Label htmlFor="percentUsed">Percent Used (%) *</Label>
            <Input
              id="percentUsed"
              type="number"
              step="0.01"
              {...register('percentUsed', { valueAsNumber: true, required: true })}
              placeholder="5.0"
              className="h-12 text-lg"
            />
            {errors.percentUsed && (
              <p className="text-sm text-destructive">{errors.percentUsed.message}</p>
            )}
            {selectedBarrel && (
              <div className="space-y-1">
                <p className="text-sm text-muted-foreground">
                  Current fill: {parseFloat(selectedBarrel.currentFillPercent).toFixed(2)}%
                  {percentUsed > 0 && (
                    <span className="ml-2 font-medium">
                      → {(parseFloat(selectedBarrel.currentFillPercent) - percentUsed).toFixed(2)}% remaining
                    </span>
                  )}
                </p>
                {percentUsed > parseFloat(selectedBarrel.currentFillPercent) && (
                  <p className="text-sm text-destructive flex items-center gap-1">
                    <Info className="h-3 w-3" />
                    Cannot use more than {parseFloat(selectedBarrel.currentFillPercent).toFixed(2)}%
                  </p>
                )}
              </div>
            )}
          </div>

          {estimatedCost > 0 && (
            <div className="bg-primary/10 border border-primary/20 rounded-lg p-4">
              <div className="flex items-center justify-between">
                <span className="font-medium text-sm">Estimated Allocated Cost:</span>
                <span className="text-xl font-bold text-primary">{formatCurrency(estimatedCost)}</span>
              </div>
              <p className="text-xs text-muted-foreground mt-1">
                This cost will be allocated when you create a bottling run
              </p>
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
            <Button type="submit" disabled={loading} className="h-12 px-8 text-lg">
              {loading ? 'Creating...' : 'Log Usage'}
            </Button>
          </DialogFooter>
        </form>
      </DialogContent>
    </Dialog>
  )
}

