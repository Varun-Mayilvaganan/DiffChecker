import { useState } from 'react'
import Header from './components/Header'
import ConfigSection from './components/ConfigSection'
import FileUpload from './components/FileUpload'
import ValidationResults from './components/ValidationResults'
import ExportSection from './components/ExportSection'
import { ValidationResponse } from './types'

function App() {
  const [projectName, setProjectName] = useState('')
  const [reportName, setReportName] = useState('')
  const [environment, setEnvironment] = useState('UAT')
  const [cognosFile, setCognosFile] = useState<File | null>(null)
  const [powerbiFile, setPowerbiFile] = useState<File | null>(null)
  const [isLoading, setIsLoading] = useState(false)
  const [results, setResults] = useState<ValidationResponse | null>(null)
  const [error, setError] = useState<string | null>(null)

  const handleValidate = async () => {
    if (!cognosFile || !powerbiFile) {
      setError('Please upload both CSV files')
      return
    }

    setIsLoading(true)
    setError(null)
    setResults(null)

    const formData = new FormData()
    formData.append('cognos_file', cognosFile)
    formData.append('powerbi_file', powerbiFile)
    formData.append('project_name', projectName)
    formData.append('report_name', reportName)
    formData.append('environment', environment)

    try {
      const response = await fetch('http://localhost:8000/api/validate', {
        method: 'POST',
        body: formData,
      })

      if (!response.ok) {
        const errorData = await response.json()
        throw new Error(errorData.detail || 'Validation failed')
      }

      const data = await response.json()
      console.log('Validation results:', data)
      setResults(data)
    } catch (err) {
      console.error('Validation error:', err)
      setError(err instanceof Error ? err.message : 'An error occurred')
    } finally {
      setIsLoading(false)
    }
  }

  const handleExport = async () => {
    if (!cognosFile || !powerbiFile) return

    const formData = new FormData()
    formData.append('cognos_file', cognosFile)
    formData.append('powerbi_file', powerbiFile)
    formData.append('project_name', projectName)
    formData.append('report_name', reportName)
    formData.append('environment', environment)

    try {
      const response = await fetch('http://localhost:8000/api/export-excel', {
        method: 'POST',
        body: formData,
      })

      if (!response.ok) {
        throw new Error('Export failed')
      }

      const blob = await response.blob()
      const url = window.URL.createObjectURL(blob)
      const a = document.createElement('a')
      a.href = url
      a.download = `DataSure_Validation_Report_${new Date().toISOString().slice(0, 10)}.xlsx`
      document.body.appendChild(a)
      a.click()
      window.URL.revokeObjectURL(url)
      document.body.removeChild(a)
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Export failed')
    }
  }

  const handleReset = () => {
    setCognosFile(null)
    setPowerbiFile(null)
    setResults(null)
    setError(null)
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-50 to-gray-100">
      <Header />
      
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Configuration Section */}
        <ConfigSection
          projectName={projectName}
          setProjectName={setProjectName}
          reportName={reportName}
          setReportName={setReportName}
          environment={environment}
          setEnvironment={setEnvironment}
        />

        {/* File Upload Section */}
        <FileUpload
          cognosFile={cognosFile}
          setCognosFile={setCognosFile}
          powerbiFile={powerbiFile}
          setPowerbiFile={setPowerbiFile}
        />

        {/* Error Display */}
        {error && (
          <div className="mt-6 bg-error-50 border border-error-500 text-error-600 px-4 py-3 rounded-lg">
            <p className="font-medium">Error: {error}</p>
          </div>
        )}

        {/* Action Buttons */}
        <div className="mt-8 flex justify-center gap-4">
          <button
            onClick={handleValidate}
            disabled={!cognosFile || !powerbiFile || isLoading}
            className="btn-primary disabled:opacity-50 disabled:cursor-not-allowed flex items-center gap-2"
          >
            {isLoading ? (
              <>
                <svg className="animate-spin h-5 w-5" viewBox="0 0 24 24">
                  <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" fill="none" />
                  <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
                </svg>
                Validating...
              </>
            ) : (
              <>
                <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
                Run Validation
              </>
            )}
          </button>
          
          {results && (
            <button onClick={handleReset} className="btn-secondary">
              Reset
            </button>
          )}
        </div>

        {/* Validation Results */}
        {results && (
          <>
            <ValidationResults results={results} />
            <ExportSection onExport={handleExport} />
          </>
        )}
      </main>

      {/* Footer */}
      <footer className="bg-white border-t border-gray-200 mt-12">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <p className="text-center text-gray-500 text-sm">
            DataSure - IBM Cognos to PowerBI Migration Validation Platform
          </p>
        </div>
      </footer>
    </div>
  )
}

export default App
