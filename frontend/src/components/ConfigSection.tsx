import { Settings } from 'lucide-react'

interface ConfigSectionProps {
  projectName: string
  setProjectName: (value: string) => void
  reportName: string
  setReportName: (value: string) => void
  environment: string
  setEnvironment: (value: string) => void
}

const environments = ['UAT', 'DEV', 'SIT', 'PROD', 'QA']

export default function ConfigSection({
  projectName,
  setProjectName,
  reportName,
  setReportName,
  environment,
  setEnvironment,
}: ConfigSectionProps) {
  return (
    <div className="card mb-6">
      <div className="flex items-center gap-2 mb-4">
        <Settings className="w-5 h-5 text-primary-600" />
        <h2 className="text-lg font-semibold text-gray-900">Report Configuration</h2>
      </div>
      
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">
            Project Name
          </label>
          <input
            type="text"
            value={projectName}
            onChange={(e) => setProjectName(e.target.value)}
            placeholder="e.g., CPS Performance Metrics"
            className="input-field"
          />
        </div>
        
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">
            Environment
          </label>
          <select
            value={environment}
            onChange={(e) => setEnvironment(e.target.value)}
            className="input-field bg-white"
          >
            {environments.map((env) => (
              <option key={env} value={env}>
                {env}
              </option>
            ))}
          </select>
        </div>
        
        <div className="md:col-span-2">
          <label className="block text-sm font-medium text-gray-700 mb-1">
            Report Name
          </label>
          <input
            type="text"
            value={reportName}
            onChange={(e) => setReportName(e.target.value)}
            placeholder="e.g., Sales Report Q1 2024"
            className="input-field"
          />
        </div>
      </div>
    </div>
  )
}
