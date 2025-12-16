import { NextResponse } from 'next/server'
import { prisma } from '@/lib/prisma'
import { barrelBatchSchema } from '@/lib/validations'

export async function GET() {
  try {
    const batches = await prisma.barrelBatch.findMany({
      orderBy: { purchaseDate: 'desc' },
      include: {
        _count: {
          select: { barrels: true },
        },
      },
    })

    const batchesWithCostPerBarrel = batches.map((batch) => ({
      id: batch.id,
      name: batch.name,
      purchaseDate: batch.purchaseDate.toISOString(),
      numBarrels: batch.numBarrels,
      totalCost: batch.totalCost.toString(),
      supplier: batch.supplier,
      costPerBarrel: (Number(batch.totalCost) / batch.numBarrels).toFixed(2),
    }))

    return NextResponse.json(batchesWithCostPerBarrel)
  } catch (error) {
    console.error('Error fetching barrel batches:', error)
    return NextResponse.json(
      { error: 'Failed to fetch barrel batches' },
      { status: 500 }
    )
  }
}

export async function POST(request: Request) {
  try {
    const body = await request.json()
    const validated = barrelBatchSchema.parse({
      ...body,
      purchaseDate: new Date(body.purchaseDate),
    })

    const batch = await prisma.barrelBatch.create({
      data: {
        name: validated.name,
        purchaseDate: validated.purchaseDate,
        numBarrels: validated.numBarrels,
        totalCost: validated.totalCost,
        supplier: validated.supplier,
        notes: validated.notes,
      },
    })

    // Auto-create individual barrel records
    // Find the highest existing barrel number to ensure uniqueness
    const existingBarrels = await prisma.barrel.findMany({
      orderBy: { barrelId: 'desc' },
      take: 1,
    })

    let startNumber = 1
    if (existingBarrels.length > 0) {
      const lastBarrelId = existingBarrels[0].barrelId
      const lastNumber = parseInt(lastBarrelId.replace('BAR-', ''))
      startNumber = lastNumber + 1
    }

    const barrels = []
    for (let i = 0; i < validated.numBarrels; i++) {
      const barrelNumber = startNumber + i
      const barrelId = `BAR-${String(barrelNumber).padStart(3, '0')}`
      barrels.push({
        barrelId,
        batchId: batch.id,
        currentFillPercent: 100,
        status: 'Aging',
      })
    }

    await prisma.barrel.createMany({
      data: barrels,
    })

    return NextResponse.json(batch, { status: 201 })
  } catch (error: any) {
    console.error('Error creating barrel batch:', error)
    return NextResponse.json(
      { error: error.message || 'Failed to create barrel batch' },
      { status: 500 }
    )
  }
}

