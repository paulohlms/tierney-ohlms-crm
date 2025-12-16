'use client'

import { useState, useEffect } from 'react'
import { useForm } from 'react-hook-form'
import { zodResolver } from '@hookform/resolvers/zod'
import { z } from 'zod'
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogFooter } from '@/components/ui/dialog'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { Textarea } from '@/components/ui/textarea'
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select'

interface EditBarrelDialogProps {
  open: boolean
  onOpenChange: (open: boolean) => void
  barrel: {
    id: string
    barrelId: string
    groupLabel: string | null
    currentFillPercent: string
    status: string
    notes?: string | null
  }
  onSuccess: () => void
}

const formSchema = z.object({
  groupLabel: z.string().optional(),
  currentFillPercent: z.number().min(0).max(100),
  status: z.string().min(1),
  notes: z.string().optional(),
})

type FormData = z.infer<typeof formSchema>

const statusOptions = ['Aging', 'In Production', 'Empty', 'Reserved', 'Damaged']

export function EditBarrelDialog({
  open,
  onOpenChange,
  barrel,
  onSuccess,
}: EditBarrelDialogProps) {
  const [loading, setLoading] = useState(false)
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
      groupLabel: barrel.groupLabel || '',
      currentFillPercent: parseFloat(barrel.currentFillPercent),
      status: barrel.status,
      notes: barrel.notes || '',
    },
  })

  useEffect(() => {
    if (open && barrel) {
      reset({
        groupLabel: barrel.groupLabel || '',
        currentFillPercent: parseFloat(barrel.currentFillPercent),
        status: barrel.status,
        notes: barrel.notes || '',
      })
    }
  }, [open, barrel, reset])

  const onSubmit = async (data: FormData) => {
    setLoading(true)
    try {
      const res = await fetch(`/api/barrels/${barrel.id}`, {
        method: 'PATCH',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data),
      })

      if (!res.ok) {
        const error = await res.json()
        throw new Error(error.message || 'Failed to update barrel')
      }

      onSuccess()
      onOpenChange(false)
    } catch (error: any) {
      alert(error.message || 'Failed to update barrel')
    } finally {
      setLoading(false)
    }
  }

  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent className="max-w-2xl">
        <DialogHeader>
          <DialogTitle className="text-2xl">Edit Barrel {barrel.barrelId}</DialogTitle>
        </DialogHeader>
        <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
          <div className="space-y-2">
            <Label htmlFor="groupLabel">Group Label</Label>
            <Input
              id="groupLabel"
              {...register('groupLabel')}
              placeholder="e.g., 2025 Rye Private Selection - Group A"
              className="h-12 text-lg"
            />
          </div>

          <div className="grid grid-cols-2 gap-4">
            <div className="space-y-2">
              <Label htmlFor="currentFillPercent">Current Fill %</Label>
              <Input
                id="currentFillPercent"
                type="number"
                step="0.01"
                {...register('currentFillPercent', { valueAsNumber: true })}
                className="h-12 text-lg"
              />
              {errors.currentFillPercent && (
                <p className="text-sm text-destructive">{errors.currentFillPercent.message}</p>
              )}
            </div>
            <div className="space-y-2">
              <Label htmlFor="status">Status</Label>
              <Select
                value={watch('status')}
                onValueChange={(value) => setValue('status', value)}
              >
                <SelectTrigger className="h-12 text-lg">
                  <SelectValue />
                </SelectTrigger>
                <SelectContent>
                  {statusOptions.map((status) => (
                    <SelectItem key={status} value={status}>
                      {status}
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </div>
          </div>

          <div className="space-y-2">
            <Label htmlFor="notes">Notes</Label>
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
              {loading ? 'Saving...' : 'Save Changes'}
            </Button>
          </DialogFooter>
        </form>
      </DialogContent>
    </Dialog>
  )
}

