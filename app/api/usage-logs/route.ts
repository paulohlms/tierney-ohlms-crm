import { NextResponse } from 'next/server'
import { prisma } from '@/lib/prisma'
import { usageLogSchema } from '@/lib/validations'

export async function GET() {
  try {
    const logs = await prisma.usageLog.findMany({
      include: {
        barrel: {
          select: {
            barrelId: true,
          },
        },
        bottlingRunUsages: {
          select: {
            id: true,
          },
        },
      },
      orderBy: { date: 'desc' },
    })

    return NextResponse.json(logs)
  } catch (error) {
    console.error('Error fetching usage logs:', error)
    return NextResponse.json(
      { error: 'Failed to fetch usage logs' },
      { status: 500 }
    )
  }
}

export async function POST(request: Request) {
  try {
    const body = await request.json()
    const validated = usageLogSchema.parse({
      ...body,
      date: new Date(body.date),
    })

    // Get barrel to calculate cost
    const barrel = await prisma.barrel.findUnique({
      where: { id: validated.barrelId },
      include: {
        batch: true,
      },
    })

    if (!barrel) {
      return NextResponse.json(
        { error: 'Barrel not found' },
        { status: 404 }
      )
    }

    // Check if barrel has enough fill
    const currentFill = parseFloat(barrel.currentFillPercent.toString())
    if (validated.percentUsed > currentFill) {
      return NextResponse.json(
        { error: `Cannot use ${validated.percentUsed}% - only ${currentFill}% remaining` },
        { status: 400 }
      )
    }

    // Calculate allocated cost
    const batchCost = Number(barrel.batch.totalCost)
    const barrelsInBatch = barrel.batch.numBarrels
    const costPerBarrel = batchCost / barrelsInBatch
    const allocatedCost = (costPerBarrel * validated.percentUsed) / 100

    // Create usage log
    const usageLog = await prisma.usageLog.create({
      data: {
        date: validated.date,
        barrelId: validated.barrelId,
        percentUsed: validated.percentUsed,
        allocatedCost,
        notes: validated.notes,
      },
    })

    // Update barrel fill percentage
    const newFillPercent = currentFill - validated.percentUsed
    await prisma.barrel.update({
      where: { id: validated.barrelId },
      data: {
        currentFillPercent: newFillPercent,
        status: newFillPercent <= 0 ? 'Empty' : barrel.status,
      },
    })

    return NextResponse.json(usageLog, { status: 201 })
  } catch (error: any) {
    console.error('Error creating usage log:', error)
    return NextResponse.json(
      { error: error.message || 'Failed to create usage log' },
      { status: 500 }
    )
  }
}

