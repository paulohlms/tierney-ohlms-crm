'use client'

import * as React from "react"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table"
import { Download } from "lucide-react"

interface Column<T> {
  header: string
  accessor: keyof T | ((row: T) => React.ReactNode)
  cell?: (value: any, row: T) => React.ReactNode
}

interface DataTableProps<T> {
  data: T[]
  columns: Column<T>[]
  searchKey?: keyof T
  searchPlaceholder?: string
  exportFilename?: string
}

export function DataTable<T extends Record<string, any>>({
  data,
  columns,
  searchKey,
  searchPlaceholder = "Search...",
  exportFilename = "export",
}: DataTableProps<T>) {
  const [search, setSearch] = React.useState("")
  const [filteredData, setFilteredData] = React.useState(data)

  React.useEffect(() => {
    if (!searchKey || !search) {
      setFilteredData(data)
      return
    }

    const filtered = data.filter((row) => {
      const value = row[searchKey]
      return value?.toString().toLowerCase().includes(search.toLowerCase())
    })
    setFilteredData(filtered)
  }, [search, data, searchKey])

  const exportToCSV = () => {
    const headers = columns.map((col) => col.header)
    const rows = filteredData.map((row) =>
      columns.map((col) => {
        const value =
          typeof col.accessor === "function"
            ? col.accessor(row)
            : row[col.accessor]
        // Remove HTML tags and format for CSV
        if (typeof value === "object" && value !== null) {
          return JSON.stringify(value)
        }
        return String(value ?? "").replace(/,/g, ";")
      })
    )

    const csvContent = [
      headers.join(","),
      ...rows.map((row) => row.join(",")),
    ].join("\n")

    const blob = new Blob([csvContent], { type: "text/csv;charset=utf-8;" })
    const link = document.createElement("a")
    const url = URL.createObjectURL(blob)
    link.setAttribute("href", url)
    link.setAttribute("download", `${exportFilename}-${new Date().toISOString().split("T")[0]}.csv`)
    link.style.visibility = "hidden"
    document.body.appendChild(link)
    link.click()
    document.body.removeChild(link)
  }

  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between">
        {searchKey && (
          <Input
            placeholder={searchPlaceholder}
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            className="max-w-sm"
          />
        )}
        <Button onClick={exportToCSV} variant="outline" size="lg">
          <Download className="mr-2 h-4 w-4" />
          Export CSV
        </Button>
      </div>
      <div className="rounded-md border">
        <Table>
          <TableHeader>
            <TableRow>
              {columns.map((column, index) => (
                <TableHead key={index}>{column.header}</TableHead>
              ))}
            </TableRow>
          </TableHeader>
          <TableBody>
            {filteredData.length === 0 ? (
              <TableRow>
                <TableCell
                  colSpan={columns.length}
                  className="h-24 text-center text-muted-foreground"
                >
                  {data.length === 0 ? 'No data available. Get started by creating your first record.' : 'No results match your search. Try different keywords.'}
                </TableCell>
              </TableRow>
            ) : (
              filteredData.map((row, rowIndex) => (
                <TableRow key={rowIndex}>
                  {columns.map((column, colIndex) => {
                    const value =
                      typeof column.accessor === "function"
                        ? column.accessor(row)
                        : row[column.accessor]
                    return (
                      <TableCell key={colIndex}>
                        {column.cell ? column.cell(value, row) : String(value ?? "")}
                      </TableCell>
                    )
                  })}
                </TableRow>
              ))
            )}
          </TableBody>
        </Table>
      </div>
    </div>
  )
}

