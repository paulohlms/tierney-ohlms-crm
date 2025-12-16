import { NextResponse } from 'next/server'
import { prisma } from '@/lib/prisma'

export async function GET(request: Request) {
  try {
    const { searchParams } = new URL(request.url)
    const month = searchParams.get('month')

    if (!month) {
      return NextResponse.json(
        { error: 'Month parameter is required (YYYY-MM)' },
        { status: 400 }
      )
    }

    const [year, monthNum] = month.split('-').map(Number)
    const startDate = new Date(year, monthNum - 1, 1)
    const endDate = new Date(year, monthNum, 0, 23, 59, 59)

    // Get all shipments for the month
    const shipments = await prisma.shipment.findMany({
      where: {
        date: {
          gte: startDate,
          lte: endDate,
        },
      },
      include: {
        bottlingRun: {
          select: {
            bottleType: true,
          },
        },
      },
    })

    // Group by bottle type
    const grouped = shipments.reduce((acc, shipment) => {
      const bottleType = shipment.bottlingRun.bottleType
      if (!acc[bottleType]) {
        acc[bottleType] = {
          bottleType,
          totalUnits: 0,
          totalCOGS: 0,
        }
      }
      acc[bottleType].totalUnits += shipment.quantity
      acc[bottleType].totalCOGS += Number(shipment.cogs)
      return acc
    }, {} as Record<string, { bottleType: string; totalUnits: number; totalCOGS: number }>)

    const shipmentsByType = Object.values(grouped)
    const totalCOGS = shipmentsByType.reduce((sum, item) => sum + item.totalCOGS, 0)

    return NextResponse.json({
      month,
      shipments: shipmentsByType,
      totalCOGS,
    })
  } catch (error) {
    console.error('Error generating monthly report:', error)
    return NextResponse.json(
      { error: 'Failed to generate report' },
      { status: 500 }
    )
  }
}

