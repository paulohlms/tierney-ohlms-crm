import { NextResponse } from 'next/server'
import { prisma } from '@/lib/prisma'

export async function GET(request: Request) {
  try {
    const { searchParams } = new URL(request.url)
    const includeBatch = searchParams.get('includeBatch') === 'true'

    const barrels = await prisma.barrel.findMany({
      include: {
        batch: includeBatch
          ? {
              select: {
                name: true,
                totalCost: true,
                numBarrels: true,
              },
            }
          : {
              select: {
                name: true,
              },
            },
      },
      orderBy: { barrelId: 'asc' },
    })

    return NextResponse.json(barrels)
  } catch (error) {
    console.error('Error fetching barrels:', error)
    return NextResponse.json(
      { error: 'Failed to fetch barrels' },
      { status: 500 }
    )
  }
}

