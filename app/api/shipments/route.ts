import { NextResponse } from 'next/server'
import { prisma } from '@/lib/prisma'
import { shipmentSchema } from '@/lib/validations'

export async function GET() {
  try {
    const shipments = await prisma.shipment.findMany({
      include: {
        bottlingRun: {
          select: {
            name: true,
            bottleType: true,
          },
        },
      },
      orderBy: { date: 'desc' },
    })

    return NextResponse.json(shipments)
  } catch (error) {
    console.error('Error fetching shipments:', error)
    return NextResponse.json(
      { error: 'Failed to fetch shipments' },
      { status: 500 }
    )
  }
}

export async function POST(request: Request) {
  try {
    const body = await request.json()
    const validated = shipmentSchema.parse({
      ...body,
      date: new Date(body.date),
    })

    // Get bottling run
    const bottlingRun = await prisma.bottlingRun.findUnique({
      where: { id: validated.bottlingRunId },
    })

    if (!bottlingRun) {
      return NextResponse.json(
        { error: 'Bottling run not found' },
        { status: 404 }
      )
    }

    // Check inventory
    if (validated.quantity > bottlingRun.remainingInventory) {
      return NextResponse.json(
        { error: `Cannot ship ${validated.quantity} bottles - only ${bottlingRun.remainingInventory} remaining` },
        { status: 400 }
      )
    }

    // Calculate COGS
    const cogs = Number(bottlingRun.unitCost) * validated.quantity

    // Create shipment
    const shipment = await prisma.shipment.create({
      data: {
        date: validated.date,
        bottlingRunId: validated.bottlingRunId,
        quantity: validated.quantity,
        customerRef: validated.customerRef,
        cogs,
        notes: validated.notes,
      },
    })

    // Update remaining inventory
    await prisma.bottlingRun.update({
      where: { id: validated.bottlingRunId },
      data: {
        remainingInventory: bottlingRun.remainingInventory - validated.quantity,
      },
    })

    return NextResponse.json(shipment, { status: 201 })
  } catch (error: any) {
    console.error('Error creating shipment:', error)
    return NextResponse.json(
      { error: error.message || 'Failed to create shipment' },
      { status: 500 }
    )
  }
}

