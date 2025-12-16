import { NextResponse } from 'next/server'
import { prisma } from '@/lib/prisma'

export async function GET() {
  try {
    const now = new Date()
    const startOfMonth = new Date(now.getFullYear(), now.getMonth(), 1)

    const [totalBarrels, agingBarrels, bottlingRuns, monthlyShipments] = await Promise.all([
      prisma.barrel.count(),
      prisma.barrel.count({
        where: { status: 'Aging' },
      }),
      prisma.bottlingRun.findMany({
        select: { remainingInventory: true },
      }),
      prisma.shipment.findMany({
        where: {
          date: {
            gte: startOfMonth,
          },
        },
        select: { cogs: true },
      }),
    ])

    const bottledInventory = bottlingRuns.reduce(
      (sum, run) => sum + run.remainingInventory,
      0
    )

    const monthlyCOGS = monthlyShipments.reduce(
      (sum, shipment) => sum + Number(shipment.cogs),
      0
    )

    return NextResponse.json({
      totalBarrels,
      agingBarrels,
      bottledInventory,
      monthlyCOGS,
    })
  } catch (error) {
    console.error('Error fetching dashboard stats:', error)
    return NextResponse.json(
      { error: 'Failed to fetch dashboard stats' },
      { status: 500 }
    )
  }
}

