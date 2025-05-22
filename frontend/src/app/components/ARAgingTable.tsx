'use client'

type ARAgingRow = {
  customer: string
  current: number
  "30_days": number
  "60_days": number
  "90_days": number
  over_90_days: number
  total: number
}

export default function ARAgingTable({ rows }: { rows: ARAgingRow[] }) {
  return (
    <table className="min-w-full table-auto border-collapse border border-gray-300 text-sm">
      <thead className="bg-gray-800 text-white">
        <tr>
          <th className="border px-4 py-2 text-left">Customer</th>
          <th className="border px-4 py-2 text-right">Current</th>
          <th className="border px-4 py-2 text-right">30 Days</th>
          <th className="border px-4 py-2 text-right">60 Days</th>
          <th className="border px-4 py-2 text-right">90 Days</th>
          <th className="border px-4 py-2 text-right">Over 90 Days</th>
          <th className="border px-4 py-2 text-right font-bold">Total</th>
        </tr>
      </thead>
      <tbody>
        {rows.map((row, i) => (
          <tr key={i} className="hover:bg-gray-100 dark:hover:bg-gray-700">
            <td className="border px-4 py-2">{row.customer}</td>
            <td className="border px-4 py-2 text-right">${row.current.toFixed(2)}</td>
            <td className="border px-4 py-2 text-right">${row["30_days"].toFixed(2)}</td>
            <td className="border px-4 py-2 text-right">${row["60_days"].toFixed(2)}</td>
            <td className="border px-4 py-2 text-right">${row["90_days"].toFixed(2)}</td>
            <td className="border px-4 py-2 text-right">${row.over_90_days.toFixed(2)}</td>
            <td className="border px-4 py-2 text-right font-bold">${row.total.toFixed(2)}</td>
          </tr>
        ))}
      </tbody>
    </table>
  )
}