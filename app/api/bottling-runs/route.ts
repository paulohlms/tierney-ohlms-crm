import { NextResponse } from 'next/server'
import { prisma } from '@/lib/prisma'
import { bottlingRunSchema } from '@/lib/validations'

export async function GET() {
  try {
    const runs = await prisma.bottlingRun.findMany({
      orderBy: { date: 'desc' },
    })

    return NextResponse.json(runs)
  } catch (error) {
    console.error('Error fetching bottling runs:', error)
    return NextResponse.json(
      { error: 'Failed to fetch bottling runs' },
      { status: 500 }
    )
  }
}

export async function POST(request: Request) {
  try {
    const body = await request.json()
    const validated = bottlingRunSchema.parse({
      ...body,
      date: new Date(body.date),
    })

    // Get usage logs and calculate total cost
    const usageLogs = await prisma.usageLog.findMany({
      where: {
        id: { in: validated.usageLogIds },
      },
    })

    if (usageLogs.length !== validated.usageLogIds.length) {
      return NextResponse.json(
        { error: 'One or more usage logs not found' },
        { status: 404 }
      )
    }

    // Check if any usage log is already used
    const existingLinks = await prisma.bottlingRunUsage.findMany({
      where: {
        usageLogId: { in: validated.usageLogIds },
      },
    })

    if (existingLinks.length > 0) {
      return NextResponse.json(
        { error: 'One or more usage logs are already linked to a bottling run' },
        { status: 400 }
      )
    }

    const totalCost = usageLogs.reduce(
      (sum, log) => sum + Number(log.allocatedCost),
      0
    )

    const unitCost = totalCost / validated.totalBottlesProduced

    // Create bottling run
    const bottlingRun = await prisma.bottlingRun.create({
      data: {
        name: validated.name,
        date: validated.date,
        bottleType: validated.bottleType,
        totalBottlesProduced: validated.totalBottlesProduced,
        totalCost,
        unitCost,
        remainingInventory: validated.totalBottlesProduced,
        notes: validated.notes,
      },
    })

    // Link usage logs
    await prisma.bottlingRunUsage.createMany({
      data: validated.usageLogIds.map((usageLogId) => ({
        bottlingRunId: bottlingRun.id,
        usageLogId,
      })),
    })

    return NextResponse.json(bottlingRun, { status: 201 })
  } catch (error: any) {
    console.error('Error creating bottling run:', error)
    return NextResponse.json(
      { error: error.message || 'Failed to create bottling run' },
      { status: 500 }
    )
  }
}

