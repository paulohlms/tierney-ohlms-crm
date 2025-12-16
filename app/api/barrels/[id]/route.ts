import { NextResponse } from 'next/server'
import { prisma } from '@/lib/prisma'
import { z } from 'zod'

const updateSchema = z.object({
  groupLabel: z.string().optional().nullable(),
  currentFillPercent: z.number().min(0).max(100).optional(),
  status: z.string().optional(),
  notes: z.string().optional().nullable(),
})

export async function PATCH(
  request: Request,
  { params }: { params: { id: string } }
) {
  try {
    const body = await request.json()
    const validated = updateSchema.parse(body)

    const barrel = await prisma.barrel.update({
      where: { id: params.id },
      data: {
        groupLabel: validated.groupLabel,
        currentFillPercent: validated.currentFillPercent,
        status: validated.status,
        notes: validated.notes,
      },
    })

    return NextResponse.json(barrel)
  } catch (error: any) {
    console.error('Error updating barrel:', error)
    return NextResponse.json(
      { error: error.message || 'Failed to update barrel' },
      { status: 500 }
    )
  }
}

