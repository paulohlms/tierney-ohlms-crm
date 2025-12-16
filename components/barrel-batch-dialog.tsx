'use client'

import { useState } from 'react'
import { useForm } from 'react-hook-form'
import { zodResolver } from '@hookform/resolvers/zod'
import { z } from 'zod'
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogFooter, DialogDescription } from '@/components/ui/dialog'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { Textarea } from '@/components/ui/textarea'
import { useToast } from '@/hooks/use-toast'
import { Info } from 'lucide-react'
import { formatCurrency } from '@/lib/utils'

interface CreateBarrelBatchDialogProps {
  open: boolean
  onOpenChange: (open: boolean) => void
  onSuccess: () => void
}

const formSchema = z.object({
  name: z.string().optional(),
  purchaseDate: z.string().min(1, 'Purchase date is required'),
  numBarrels: z.number().int().positive().min(1),
  totalCost: z.number().positive(),
  supplier: z.string().optional(),
  notes: z.string().optional(),
})

type FormData = z.infer<typeof formSchema>

export function CreateBarrelBatchDialog({
  open,
  onOpenChange,
  onSuccess,
}: CreateBarrelBatchDialogProps) {
  const [loading, setLoading] = useState(false)
  const { toast } = useToast()
  const {
    register,
    handleSubmit,
    formState: { errors },
    reset,
    watch,
  } = useForm<FormData>({
    resolver: zodResolver(formSchema),
  })

  const numBarrels = watch('numBarrels') || 0
  const totalCost = watch('totalCost') || 0
  const costPerBarrel = numBarrels > 0 && totalCost > 0 ? totalCost / numBarrels : 0

  const onSubmit = async (data: FormData) => {
    setLoading(true)
    try {
      const res = await fetch('/api/barrel-batches', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          ...data,
          purchaseDate: new Date(data.purchaseDate),
        }),
      })

      if (!res.ok) {
        const error = await res.json()
        throw new Error(error.message || 'Failed to create batch')
      }

      reset()
      toast({
        title: 'Success!',
        description: `Created batch with ${data.numBarrels} barrels. Individual barrel records have been created automatically.`,
        variant: 'success',
      })
      onSuccess()
      onOpenChange(false)
    } catch (error: any) {
      toast({
        title: 'Error',
        description: error.message || 'Failed to create batch. Please try again.',
        variant: 'destructive',
      })
    } finally {
      setLoading(false)
    }
  }

  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent className="max-w-2xl max-h-[90vh] overflow-y-auto">
        <DialogHeader>
          <DialogTitle className="text-2xl">Create New Barrel Batch</DialogTitle>
          <DialogDescription>
            When you create a batch, individual barrel records (BAR-001, BAR-002, etc.) will be created automatically.
          </DialogDescription>
        </DialogHeader>
        <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
          <div className="grid grid-cols-2 gap-4">
            <div className="space-y-2">
              <Label htmlFor="name">Batch Name (Optional)</Label>
              <Input
                id="name"
                {...register('name')}
                placeholder="e.g., Q1 2025 Purchase"
                className="h-12 text-lg"
              />
            </div>
            <div className="space-y-2">
              <Label htmlFor="purchaseDate">Purchase Date *</Label>
              <Input
                id="purchaseDate"
                type="date"
                {...register('purchaseDate', { required: true })}
                className="h-12 text-lg"
              />
              {errors.purchaseDate && (
                <p className="text-sm text-destructive">{errors.purchaseDate.message}</p>
              )}
            </div>
          </div>

          <div className="grid grid-cols-2 gap-4">
            <div className="space-y-2">
              <Label htmlFor="numBarrels">Number of Barrels *</Label>
              <Input
                id="numBarrels"
                type="number"
                {...register('numBarrels', { valueAsNumber: true, required: true })}
                placeholder="100"
                className="h-12 text-lg"
              />
              {errors.numBarrels && (
                <p className="text-sm text-destructive">{errors.numBarrels.message}</p>
              )}
              <p className="text-xs text-muted-foreground flex items-center gap-1">
                <Info className="h-3 w-3" />
                Typical batch size is around 100 barrels
              </p>
            </div>
            <div className="space-y-2">
              <Label htmlFor="totalCost">Total Cost ($) *</Label>
              <Input
                id="totalCost"
                type="number"
                step="0.01"
                {...register('totalCost', { valueAsNumber: true, required: true })}
                placeholder="100000.00"
                className="h-12 text-lg"
              />
              {errors.totalCost && (
                <p className="text-sm text-destructive">{errors.totalCost.message}</p>
              )}
              <p className="text-xs text-muted-foreground flex items-center gap-1">
                <Info className="h-3 w-3" />
                Total purchase cost for this batch
              </p>
            </div>
          </div>

          {costPerBarrel > 0 && (
            <div className="bg-primary/10 border border-primary/20 rounded-lg p-4">
              <div className="flex items-center justify-between">
                <span className="font-medium text-sm">Cost per Barrel:</span>
                <span className="text-2xl font-bold text-primary">{formatCurrency(costPerBarrel)}</span>
              </div>
              <p className="text-xs text-muted-foreground mt-1">
                This cost will be used to calculate usage allocations
              </p>
            </div>
          )}

          <div className="space-y-2">
            <Label htmlFor="supplier">Supplier (Optional)</Label>
            <Input
              id="supplier"
              {...register('supplier')}
              placeholder="Supplier name"
              className="h-12 text-lg"
            />
          </div>

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
              {loading ? 'Creating...' : 'Create Batch'}
            </Button>
          </DialogFooter>
        </form>
      </DialogContent>
    </Dialog>
  )
}

