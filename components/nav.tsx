'use client'

import Link from 'next/link'
import { usePathname } from 'next/navigation'
import { useAuth } from '@/app/providers'
import { Button } from '@/components/ui/button'
import { cn } from '@/lib/utils'
import {
  LayoutDashboard,
  Package,
  Barrel,
  FileText,
  Truck,
  BarChart3,
  LogOut,
} from 'lucide-react'

const navItems = [
  { href: '/', label: 'Dashboard', icon: LayoutDashboard },
  { href: '/barrel-batches', label: 'Barrel Batches', icon: Package },
  { href: '/barrels', label: 'Barrels', icon: Barrel },
  { href: '/usage-logs', label: 'Usage Logs', icon: FileText },
  { href: '/bottling-runs', label: 'Bottling Runs', icon: Package },
  { href: '/shipments', label: 'Shipments', icon: Truck },
  { href: '/reports', label: 'Reports', icon: BarChart3 },
]

export function Nav() {
  const pathname = usePathname()
  const { user, signOut } = useAuth()

  if (!user) return null

  return (
    <nav className="border-b bg-background sticky top-0 z-50">
      <div className="container mx-auto flex h-16 items-center justify-between px-4">
        <div className="flex items-center space-x-4 md:space-x-8">
          <Link href="/" className="text-lg md:text-xl font-bold whitespace-nowrap">
            Whiskey Inventory
          </Link>
          <div className="hidden md:flex space-x-1">
            {navItems.map((item) => {
              const Icon = item.icon
              const isActive = pathname === item.href
              return (
                <Link
                  key={item.href}
                  href={item.href}
                  className={cn(
                    'flex items-center space-x-2 rounded-md px-3 py-2 text-sm font-medium transition-colors',
                    isActive
                      ? 'bg-primary text-primary-foreground'
                      : 'hover:bg-accent hover:text-accent-foreground'
                  )}
                >
                  <Icon className="h-4 w-4" />
                  <span className="hidden lg:inline">{item.label}</span>
                </Link>
              )
            })}
          </div>
        </div>
        <div className="flex items-center space-x-2 md:space-x-4">
          <span className="hidden sm:inline text-sm text-muted-foreground truncate max-w-[150px]">{user.email}</span>
          <Button onClick={signOut} variant="outline" size="sm" className="h-9">
            <LogOut className="h-4 w-4 md:mr-2" />
            <span className="hidden md:inline">Sign Out</span>
          </Button>
        </div>
      </div>
      {/* Mobile menu */}
      <div className="md:hidden border-t bg-background">
        <div className="container mx-auto px-4 py-2 overflow-x-auto">
          <div className="flex space-x-1 min-w-max">
            {navItems.map((item) => {
              const Icon = item.icon
              const isActive = pathname === item.href
              return (
                <Link
                  key={item.href}
                  href={item.href}
                  className={cn(
                    'flex flex-col items-center space-y-1 rounded-md px-3 py-2 text-xs font-medium transition-colors min-w-[70px]',
                    isActive
                      ? 'bg-primary text-primary-foreground'
                      : 'hover:bg-accent hover:text-accent-foreground'
                  )}
                >
                  <Icon className="h-4 w-4" />
                  <span className="text-[10px]">{item.label}</span>
                </Link>
              )
            })}
          </div>
        </div>
      </div>
    </nav>
  )
}

