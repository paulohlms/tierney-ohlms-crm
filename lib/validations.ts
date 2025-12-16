import { z } from 'zod'

export const barrelBatchSchema = z.object({
  name: z.string().optional(),
  purchaseDate: z.date(),
  numBarrels: z.number().int().positive().min(1),
  totalCost: z.number().positive(),
  supplier: z.string().optional(),
  notes: z.string().optional(),
})

export const barrelSchema = z.object({
  barrelId: z.string().min(1, 'Barrel ID is required'),
  batchId: z.string().uuid(),
  groupLabel: z.string().optional(),
  currentFillPercent: z.number().min(0).max(100),
  status: z.string().min(1),
  notes: z.string().optional(),
})

export const usageLogSchema = z.object({
  date: z.date(),
  barrelId: z.string().uuid(),
  percentUsed: z.number().positive().max(100),
  notes: z.string().optional(),
})

export const bottlingRunSchema = z.object({
  name: z.string().min(1, 'Name is required'),
  date: z.date(),
  bottleType: z.string().min(1, 'Bottle type is required'),
  totalBottlesProduced: z.number().int().positive(),
  usageLogIds: z.array(z.string().uuid()).min(1, 'At least one usage log is required'),
  notes: z.string().optional(),
})

export const shipmentSchema = z.object({
  date: z.date(),
  bottlingRunId: z.string().uuid(),
  quantity: z.number().int().positive(),
  customerRef: z.string().optional(),
  notes: z.string().optional(),
})

