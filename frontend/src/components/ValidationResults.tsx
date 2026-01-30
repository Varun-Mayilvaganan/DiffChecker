import { useState } from 'react'
import { CheckCircle, AlertTriangle, XCircle, FileText, Table, BarChart3, List, ChevronLeft, ChevronRight, ChevronsLeft, ChevronsRight } from 'lucide-react'
import { ValidationResponse, ValidationResult } from '../types'

interface ValidationResultsProps {
  results: ValidationResponse
}

function StatusBadge({ status }: { status: string }) {
  const config = {
    pass: { bg: 'bg-success-500', text: 'PASS', icon: CheckCircle },
    warning: { bg: 'bg-warning-500', text: 'WARNING', icon: AlertTriangle },
    fail: { bg: 'bg-error-500', text: 'FAIL', icon: XCircle },
  }
  
  const { bg, text, icon: Icon } = config[status as keyof typeof config] || config.fail
  
  return (
    <span className={`${bg} text-white px-4 py-2 rounded-lg font-semibold inline-flex items-center gap-2`}>
      <Icon className="w-5 h-5" />
      {text}
    </span>
  )
}

function ResultCard({ result }: { result: ValidationResult }) {
  const icons: Record<string, typeof FileText> = {
    'File Validation': FileText,
    'Schema Validation': Table,
    'Column Statistics': BarChart3,
    'Row-Level Differences': List,
    'Row Level Differences': List,
  }
  
  const Icon = icons[result.name] || FileText
  
  const statusColors = {
    pass: 'border-l-success-500 bg-success-50',
    warning: 'border-l-warning-500 bg-warning-50',
    fail: 'border-l-error-500 bg-error-50',
  }
  
  return (
    <div className={`border-l-4 ${statusColors[result.status]} rounded-lg p-4 mb-4`}>
      <div className="flex items-start justify-between">
        <div className="flex items-center gap-3">
          <Icon className="w-5 h-5 text-gray-600" />
          <div>
            <h4 className="font-semibold text-gray-900">{result.name}</h4>
            <p className="text-sm text-gray-600">{result.summary}</p>
          </div>
        </div>
        <StatusBadge status={result.status} />
      </div>
      
      {/* Details rendering based on result type */}
      {result.name === 'File Validation' && (
        <FileValidationDetails details={result.details} />
      )}
      {result.name === 'Schema Validation' && (
        <SchemaValidationDetails details={result.details} />
      )}
      {result.name === 'Column Statistics' && (
        <StatsValidationDetails details={result.details} />
      )}
      {(result.name === 'Row-Level Differences' || result.name === 'Row Level Differences') && (
        <RowValidationDetails details={result.details} />
      )}
    </div>
  )
}

function FileValidationDetails({ details }: { details: Record<string, unknown> }) {
  if (!details) return null
  return (
    <div className="mt-4 grid grid-cols-2 md:grid-cols-4 gap-4">
      <MetricCard label="Cognos Rows" value={Number(details?.row_count_1 || 0)} />
      <MetricCard label="PowerBI Rows" value={Number(details?.row_count_2 || 0)} />
      <MetricCard label="Cognos Columns" value={Number(details?.column_count_1 || 0)} />
      <MetricCard label="PowerBI Columns" value={Number(details?.column_count_2 || 0)} />
    </div>
  )
}

interface TypeMismatch {
  column: string
  source_type: string
  target_type: string
}

function SchemaValidationDetails({ details }: { details: Record<string, unknown> }) {
  if (!details) return null
  
  const missing = (details?.missing_columns as string[]) || []
  const extra = (details?.extra_columns as string[]) || []
  const typeMismatches = (details?.type_mismatches as TypeMismatch[]) || []
  
  if (missing.length === 0 && extra.length === 0 && typeMismatches.length === 0) {
    return (
      <div className="mt-4 text-sm text-success-600 bg-success-100 px-3 py-2 rounded">
        All columns and data types match perfectly
      </div>
    )
  }
  
  return (
    <div className="mt-4 space-y-3">
      {missing.length > 0 && (
        <div className="text-sm">
          <span className="font-medium text-error-600">Missing Columns: </span>
          {missing.map((col, i) => (
            <span key={i} className="inline-block bg-error-100 text-error-700 px-2 py-0.5 rounded mr-1 mb-1">
              {col}
            </span>
          ))}
        </div>
      )}
      {extra.length > 0 && (
        <div className="text-sm">
          <span className="font-medium text-warning-600">Extra Columns: </span>
          {extra.map((col, i) => (
            <span key={i} className="inline-block bg-warning-100 text-warning-700 px-2 py-0.5 rounded mr-1 mb-1">
              {col}
            </span>
          ))}
        </div>
      )}
      {typeMismatches.length > 0 && (
        <div className="text-sm">
          <span className="font-medium text-error-600">Type Mismatches: </span>
          <div className="mt-2 overflow-x-auto">
            <table className="min-w-full text-xs">
              <thead>
                <tr className="bg-gray-100">
                  <th className="px-3 py-2 text-left">Column</th>
                  <th className="px-3 py-2 text-left">Cognos Type</th>
                  <th className="px-3 py-2 text-left">PowerBI Type</th>
                </tr>
              </thead>
              <tbody>
                {typeMismatches.map((mismatch, i) => (
                  <tr key={i} className="border-b">
                    <td className="px-3 py-2">{mismatch?.column || ''}</td>
                    <td className="px-3 py-2">{mismatch?.source_type || ''}</td>
                    <td className="px-3 py-2">{mismatch?.target_type || ''}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}
    </div>
  )
}

function StatsValidationDetails({ details }: { details: Record<string, unknown> }) {
  const stats = (details?.stats as Array<Record<string, unknown>>) || []
  const [currentPage, setCurrentPage] = useState(1)
  const [rowsPerPage, setRowsPerPage] = useState(10)
  
  if (!stats || stats.length === 0) return null
  
  const totalPages = Math.ceil(stats.length / rowsPerPage)
  const startIndex = (currentPage - 1) * rowsPerPage
  const endIndex = startIndex + rowsPerPage
  const currentStats = stats.slice(startIndex, endIndex)
  
  const goToPage = (page: number) => {
    setCurrentPage(Math.max(1, Math.min(page, totalPages)))
  }
  
  return (
    <div className="mt-4">
      {/* Rows per page selector */}
      <div className="flex justify-between items-center mb-3">
        <div className="flex items-center gap-2 text-sm">
          <span className="text-gray-600">Show</span>
          <select 
            value={rowsPerPage}
            onChange={(e) => {
              setRowsPerPage(Number(e.target.value))
              setCurrentPage(1)
            }}
            className="border border-gray-300 rounded px-2 py-1 text-sm bg-white"
          >
            <option value={10}>10</option>
            <option value={25}>25</option>
            <option value={50}>50</option>
            <option value={stats.length}>All ({stats.length})</option>
          </select>
          <span className="text-gray-600">rows</span>
        </div>
        <span className="text-sm text-gray-500">
          Total: {stats.length} columns
        </span>
      </div>
      
      <div className="overflow-x-auto">
        <table className="min-w-full text-sm">
          <thead>
            <tr className="bg-gray-100">
              <th className="px-3 py-2 text-left">Column</th>
              <th className="px-3 py-2 text-center">Metric</th>
              <th className="px-3 py-2 text-center">Cognos</th>
              <th className="px-3 py-2 text-center">PowerBI</th>
              <th className="px-3 py-2 text-center">Match</th>
            </tr>
          </thead>
          <tbody>
            {currentStats.map((stat, i) => (
              <tr key={startIndex + i} className="border-b hover:bg-gray-50">
                <td className="px-3 py-2 font-medium">{String(stat?.column || '')}</td>
                <td className="px-3 py-2 text-center">{stat?.type === 'numeric' ? 'Sum' : 'Unique'}</td>
                <td className="px-3 py-2 text-center">
                  {stat?.type === 'numeric' 
                    ? (stat?.source_sum != null ? Number(stat.source_sum).toLocaleString() : 'N/A')
                    : (stat?.source_unique ?? 'N/A')}
                </td>
                <td className="px-3 py-2 text-center">
                  {stat?.type === 'numeric' 
                    ? (stat?.target_sum != null ? Number(stat.target_sum).toLocaleString() : 'N/A')
                    : (stat?.target_unique ?? 'N/A')}
                </td>
                <td className="px-3 py-2 text-center">
                  {stat?.match !== false ? (
                    <CheckCircle className="w-4 h-4 text-success-500 mx-auto" />
                  ) : (
                    <XCircle className="w-4 h-4 text-error-500 mx-auto" />
                  )}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
      
      {/* Pagination controls */}
      {totalPages > 1 && (
        <div className="flex items-center justify-between mt-4 pt-3 border-t">
          <span className="text-sm text-gray-600">
            Showing {startIndex + 1} to {Math.min(endIndex, stats.length)} of {stats.length} columns
          </span>
          <div className="flex items-center gap-1">
            <button
              onClick={() => goToPage(1)}
              disabled={currentPage === 1}
              className="p-1.5 rounded hover:bg-gray-100 disabled:opacity-40 disabled:cursor-not-allowed"
              title="First page"
            >
              <ChevronsLeft className="w-4 h-4" />
            </button>
            <button
              onClick={() => goToPage(currentPage - 1)}
              disabled={currentPage === 1}
              className="p-1.5 rounded hover:bg-gray-100 disabled:opacity-40 disabled:cursor-not-allowed"
              title="Previous page"
            >
              <ChevronLeft className="w-4 h-4" />
            </button>
            
            <div className="flex items-center gap-1 mx-2">
              {/* Page numbers */}
              {Array.from({ length: totalPages }, (_, i) => i + 1)
                .filter(page => {
                  // Show first, last, current, and adjacent pages
                  return page === 1 || 
                         page === totalPages || 
                         Math.abs(page - currentPage) <= 1
                })
                .map((page, idx, arr) => {
                  // Add ellipsis where there are gaps
                  const prevPage = arr[idx - 1]
                  const showEllipsis = prevPage && page - prevPage > 1
                  
                  return (
                    <span key={page} className="flex items-center">
                      {showEllipsis && <span className="px-1 text-gray-400">...</span>}
                      <button
                        onClick={() => goToPage(page)}
                        className={`w-8 h-8 rounded text-sm font-medium transition-colors ${
                          currentPage === page
                            ? 'bg-primary-600 text-white'
                            : 'hover:bg-gray-100 text-gray-700'
                        }`}
                      >
                        {page}
                      </button>
                    </span>
                  )
                })}
            </div>
            
            <button
              onClick={() => goToPage(currentPage + 1)}
              disabled={currentPage === totalPages}
              className="p-1.5 rounded hover:bg-gray-100 disabled:opacity-40 disabled:cursor-not-allowed"
              title="Next page"
            >
              <ChevronRight className="w-4 h-4" />
            </button>
            <button
              onClick={() => goToPage(totalPages)}
              disabled={currentPage === totalPages}
              className="p-1.5 rounded hover:bg-gray-100 disabled:opacity-40 disabled:cursor-not-allowed"
              title="Last page"
            >
              <ChevronsRight className="w-4 h-4" />
            </button>
          </div>
        </div>
      )}
    </div>
  )
}

function RowValidationDetails({ details }: { details: Record<string, unknown> }) {
  if (!details) return null
  
  const differences = (details?.differences as Array<unknown>) || []
  const total = Number(details?.total_differences || differences.length || 0)
  
  // Check if row comparison was skipped (no differences array or empty with warning status)
  if (details?.skipped || (differences.length === 0 && total === 0)) {
    return (
      <div className="mt-4 text-sm text-gray-600 bg-gray-100 px-3 py-2 rounded">
        Row-level comparison completed - no differences or comparison was skipped
      </div>
    )
  }
  
  if (differences.length === 0) {
    return (
      <div className="mt-4 text-sm text-success-600 bg-success-100 px-3 py-2 rounded">
        Perfect match - all row values are identical
      </div>
    )
  }
  
  return (
    <div className="mt-4">
      <p className="text-sm text-error-600 mb-2 font-medium">
        Found {total.toLocaleString()} cell-level mismatches
      </p>
      <div className="overflow-x-auto">
        <table className="min-w-full text-sm">
          <thead>
            <tr className="bg-gray-100">
              <th className="px-3 py-2 text-left">Row</th>
              <th className="px-3 py-2 text-left">Column</th>
              <th className="px-3 py-2 text-left">Cognos Value</th>
              <th className="px-3 py-2 text-left">PowerBI Value</th>
            </tr>
          </thead>
          <tbody>
            {differences.slice(0, 10).map((diff, i) => {
              // Handle both array format [row, col, val1, val2] and object format
              let row = 0, col = '', val1 = '', val2 = ''
              if (Array.isArray(diff)) {
                [row, col, val1, val2] = diff as [number, string, unknown, unknown]
              } else if (typeof diff === 'object' && diff !== null) {
                const d = diff as Record<string, unknown>
                row = Number(d.row || d.row_number || 0)
                col = String(d.column || d.col || '')
                val1 = d.cognos_value ?? d.source_value ?? d.val1 ?? ''
                val2 = d.powerbi_value ?? d.target_value ?? d.val2 ?? ''
              }
              return (
                <tr key={i} className="border-b">
                  <td className="px-3 py-2">{row}</td>
                  <td className="px-3 py-2">{col}</td>
                  <td className="px-3 py-2 text-success-600">{String(val1 ?? '')}</td>
                  <td className="px-3 py-2 text-error-600">{String(val2 ?? '')}</td>
                </tr>
              )
            })}
          </tbody>
        </table>
        {differences.length > 10 && (
          <p className="text-xs text-gray-500 mt-2">Showing first 10 of {total.toLocaleString()} differences</p>
        )}
      </div>
    </div>
  )
}

function MetricCard({ label, value }: { label: string; value: number }) {
  return (
    <div className="bg-white rounded-lg p-3 border border-gray-200">
      <p className="text-xs text-gray-500 uppercase tracking-wide">{label}</p>
      <p className="text-xl font-bold text-gray-900">{value?.toLocaleString()}</p>
    </div>
  )
}

export default function ValidationResults({ results }: ValidationResultsProps) {
  if (!results) {
    return <div className="mt-8 card text-center text-gray-500">No results to display</div>
  }

  return (
    <div className="mt-8">
      {/* Overall Status */}
      <div className="card mb-6 text-center">
        <h3 className="text-lg font-semibold text-gray-700 mb-3">Overall Validation Status</h3>
        <StatusBadge status={results.overall_status || 'fail'} />
        <div className="mt-4 grid grid-cols-2 md:grid-cols-4 gap-4 text-sm">
          <div>
            <p className="text-gray-500">Project</p>
            <p className="font-medium">{results.project_name || 'N/A'}</p>
          </div>
          <div>
            <p className="text-gray-500">Environment</p>
            <p className="font-medium">{results.environment || 'N/A'}</p>
          </div>
          <div>
            <p className="text-gray-500">Cognos File</p>
            <p className="font-medium truncate">{results.cognos_file || 'N/A'}</p>
          </div>
          <div>
            <p className="text-gray-500">PowerBI File</p>
            <p className="font-medium truncate">{results.powerbi_file || 'N/A'}</p>
          </div>
        </div>
      </div>

      {/* Individual Results */}
      <div className="card">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">Detailed Analysis</h3>
        {results.results && results.results.length > 0 ? (
          results.results.map((result, index) => (
            <ResultCard key={index} result={result} />
          ))
        ) : (
          <p className="text-gray-500">No detailed results available</p>
        )}
      </div>
    </div>
  )
}
