import { Download, FileSpreadsheet } from 'lucide-react'

interface ExportSectionProps {
  onExport: () => void
}

export default function ExportSection({ onExport }: ExportSectionProps) {
  return (
    <div className="mt-8 card bg-gradient-to-r from-primary-600 to-primary-700 text-white">
      <div className="flex flex-col md:flex-row items-center justify-between gap-4">
        <div className="flex items-center gap-4">
          <div className="bg-white/20 p-3 rounded-lg">
            <FileSpreadsheet className="w-8 h-8" />
          </div>
          <div>
            <h3 className="text-lg font-semibold">Export Validation Report</h3>
            <p className="text-primary-100 text-sm">
              Download a comprehensive Excel report with all validation details
            </p>
          </div>
        </div>
        <button
          onClick={onExport}
          className="bg-white text-primary-600 hover:bg-primary-50 font-semibold py-3 px-6 rounded-lg transition-all flex items-center gap-2 shadow-lg hover:shadow-xl"
        >
          <Download className="w-5 h-5" />
          Download Excel Report
        </button>
      </div>
    </div>
  )
}
