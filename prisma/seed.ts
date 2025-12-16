import { PrismaClient } from '@prisma/client'

const prisma = new PrismaClient()

async function main() {
  console.log('Seeding database...')

  // Create a sample barrel batch
  const batch = await prisma.barrelBatch.create({
    data: {
      name: 'Q1 2025 Purchase',
      purchaseDate: new Date('2025-01-15'),
      numBarrels: 100,
      totalCost: 100000,
      supplier: 'Kentucky Barrel Co.',
      notes: 'Initial purchase for 2025 production',
    },
  })

  console.log(`Created batch: ${batch.id}`)

  // Create sample barrels (first 10 for demo)
  const barrels = []
  for (let i = 1; i <= 10; i++) {
    const barrelId = `BAR-${String(i).padStart(3, '0')}`
    barrels.push({
      barrelId,
      batchId: batch.id,
      groupLabel: i <= 5 ? '2025 Rye Private Selection - Group A' : '2025 Rye Private Selection - Group B',
      currentFillPercent: 100,
      status: 'Aging',
    })
  }

  await prisma.barrel.createMany({
    data: barrels,
  })

  console.log(`Created ${barrels.length} barrels`)

  // Create sample usage logs
  const barrel1 = await prisma.barrel.findFirst({ where: { barrelId: 'BAR-001' } })
  const barrel2 = await prisma.barrel.findFirst({ where: { barrelId: 'BAR-002' } })

  if (barrel1) {
    const costPerBarrel = Number(batch.totalCost) / batch.numBarrels
    const usage1 = await prisma.usageLog.create({
      data: {
        date: new Date('2025-02-01'),
        barrelId: barrel1.id,
        percentUsed: 5,
        allocatedCost: (costPerBarrel * 5) / 100,
        notes: 'Initial tasting sample',
      },
    })

    await prisma.barrel.update({
      where: { id: barrel1.id },
      data: { currentFillPercent: 95 },
    })

    console.log(`Created usage log: ${usage1.id}`)

    // Create a bottling run
    const bottlingRun = await prisma.bottlingRun.create({
      data: {
        name: '2025 Rye Batch 1',
        date: new Date('2025-02-15'),
        bottleType: 'RYE-750ML-001',
        totalBottlesProduced: 500,
        totalCost: Number(usage1.allocatedCost),
        unitCost: Number(usage1.allocatedCost) / 500,
        remainingInventory: 500,
        notes: 'First production run',
      },
    })

    await prisma.bottlingRunUsage.create({
      data: {
        bottlingRunId: bottlingRun.id,
        usageLogId: usage1.id,
      },
    })

    console.log(`Created bottling run: ${bottlingRun.id}`)

    // Create a sample shipment
    if (barrel2) {
      const usage2 = await prisma.usageLog.create({
        data: {
          date: new Date('2025-02-10'),
          barrelId: barrel2.id,
          percentUsed: 10,
          allocatedCost: (costPerBarrel * 10) / 100,
          notes: 'Production usage',
        },
      })

      await prisma.barrel.update({
        where: { id: barrel2.id },
        data: { currentFillPercent: 90 },
      })

      const bottlingRun2 = await prisma.bottlingRun.create({
        data: {
          name: '2025 Rye Batch 2',
          date: new Date('2025-02-20'),
          bottleType: 'RYE-750ML-001',
          totalBottlesProduced: 1000,
          totalCost: Number(usage2.allocatedCost),
          unitCost: Number(usage2.allocatedCost) / 1000,
          remainingInventory: 1000,
        },
      })

      await prisma.bottlingRunUsage.create({
        data: {
          bottlingRunId: bottlingRun2.id,
          usageLogId: usage2.id,
        },
      })

      const shipment = await prisma.shipment.create({
        data: {
          date: new Date('2025-03-01'),
          bottlingRunId: bottlingRun.id,
          quantity: 100,
          customerRef: 'SUB-001',
          cogs: Number(bottlingRun.unitCost) * 100,
          notes: 'Monthly subscription shipment',
        },
      })

      await prisma.bottlingRun.update({
        where: { id: bottlingRun.id },
        data: { remainingInventory: 400 },
      })

      console.log(`Created shipment: ${shipment.id}`)
    }
  }

  console.log('Seeding completed!')
}

main()
  .catch((e) => {
    console.error(e)
    process.exit(1)
  })
  .finally(async () => {
    await prisma.$disconnect()
  })

