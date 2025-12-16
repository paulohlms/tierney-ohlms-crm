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
import { formatCurrency } from '@/lib/utils'
import { useToast } from '@/hooks/use-toast'

interface CreateShipmentDialogProps {
  open: boolean
  onOpenChange: (open: boolean) => void
  onSuccess: () => void
}

interface BottlingRun {
  id: string
  name: string
  bottleType: string
  remainingInventory: number
  unitCost: string
}

const formSchema = z.object({
  date: z.string().min(1, 'Date is required'),
  bottlingRunId: z.string().uuid('Please select a bottling run'),
  quantity: z.number().int().positive(),
  customerRef: z.string().optional(),
  notes: z.string().optional(),
})

type FormData = z.infer<typeof formSchema>

export function CreateShipmentDialog({
  open,
  onOpenChange,
  onSuccess,
}: CreateShipmentDialogProps) {
  const [loading, setLoading] = useState(false)
  const [bottlingRuns, setBottlingRuns] = useState<BottlingRun[]>([])
  const [selectedRun, setSelectedRun] = useState<BottlingRun | null>(null)
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
      fetchBottlingRuns()
    }
  }, [open])

  const fetchBottlingRuns = async () => {
    try {
      const res = await fetch('/api/bottling-runs')
      const data = await res.json()
      // Only show runs with remaining inventory
      setBottlingRuns(data.filter((run: BottlingRun) => run.remainingInventory > 0))
    } catch (error) {
      console.error('Error fetching bottling runs:', error)
    }
  }

  const selectedRunId = watch('bottlingRunId')
  useEffect(() => {
    if (selectedRunId) {
      const run = bottlingRuns.find((r) => r.id === selectedRunId)
      setSelectedRun(run || null)
    }
  }, [selectedRunId, bottlingRuns])

  const quantity = watch('quantity') || 0
  const estimatedCOGS = selectedRun && quantity > 0
    ? parseFloat(selectedRun.unitCost) * quantity
    : 0

  const onSubmit = async (data: FormData) => {
    if (selectedRun && data.quantity > selectedRun.remainingInventory) {
      toast({
        title: 'Insufficient Inventory',
        description: `Cannot ship ${data.quantity} bottles - only ${selectedRun.remainingInventory} remaining.`,
        variant: 'destructive',
      })
      return
    }

    setLoading(true)
    try {
      const res = await fetch('/api/shipments', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          ...data,
          date: new Date(data.date),
        }),
      })

      if (!res.ok) {
        const error = await res.json()
        throw new Error(error.message || 'Failed to create shipment')
      }

      reset()
      toast({
        title: 'Shipment Recorded!',
        description: `Successfully recorded shipment of ${data.quantity} bottles.`,
        variant: 'success',
      })
      onSuccess()
      onOpenChange(false)
    } catch (error: any) {
      toast({
        title: 'Error',
        description: error.message || 'Failed to create shipment. Please try again.',
        variant: 'destructive',
      })
    } finally {
      setLoading(false)
    }
  }

  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent className="max-w-2xl">
        <DialogHeader>
          <DialogTitle className="text-2xl">Record Shipment</DialogTitle>
          <DialogDescription>
            Record outgoing inventory. COGS is automatically calculated based on the bottling run&apos;s unit cost.
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
              <Label htmlFor="bottlingRunId">Bottling Run *</Label>
              <Select
                value={watch('bottlingRunId')}
                onValueChange={(value) => setValue('bottlingRunId', value)}
              >
                <SelectTrigger className="h-12 text-lg">
                  <SelectValue placeholder="Select a bottling run" />
                </SelectTrigger>
                <SelectContent>
                  {bottlingRuns.map((run) => (
                    <SelectItem key={run.id} value={run.id}>
                      {run.name} ({run.bottleType}) - {run.remainingInventory} remaining
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
              {errors.bottlingRunId && (
                <p className="text-sm text-destructive">{errors.bottlingRunId.message}</p>
              )}
            </div>
          </div>

          <div className="grid grid-cols-2 gap-4">
            <div className="space-y-2">
              <Label htmlFor="quantity">Quantity *</Label>
              <Input
                id="quantity"
                type="number"
                {...register('quantity', { valueAsNumber: true, required: true })}
                placeholder="100"
                className="h-12 text-lg"
              />
              {errors.quantity && (
                <p className="text-sm text-destructive">{errors.quantity.message}</p>
              )}
              {selectedRun && (
                <p className="text-sm text-muted-foreground">
                  Available: {selectedRun.remainingInventory}
                </p>
              )}
            </div>
            <div className="space-y-2">
              <Label htmlFor="customerRef">Customer/Subscription Ref</Label>
              <Input
                id="customerRef"
                {...register('customerRef')}
                placeholder="e.g., SUB-001 or Customer Name"
                className="h-12 text-lg"
              />
            </div>
          </div>

          {selectedRun && quantity > 0 && (
            <div className="bg-muted p-4 rounded-md">
              <div className="flex justify-between">
                <span className="font-medium">Estimated COGS:</span>
                <span className="font-bold">{formatCurrency(estimatedCOGS)}</span>
              </div>
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
              {loading ? 'Recording...' : 'Record Shipment'}
            </Button>
          </DialogFooter>
        </form>
      </DialogContent>
    </Dialog>
  )
}

