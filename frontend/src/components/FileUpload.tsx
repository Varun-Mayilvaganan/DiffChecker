import { useCallback } from 'react'
import { useDropzone } from 'react-dropzone'
import { Upload, FileSpreadsheet, X } from 'lucide-react'

interface FileUploadProps {
  cognosFile: File | null
  setCognosFile: (file: File | null) => void
  powerbiFile: File | null
  setPowerbiFile: (file: File | null) => void
}

interface DropZoneProps {
  file: File | null
  setFile: (file: File | null) => void
  label: string
  color: 'green' | 'blue'
}

function DropZone({ file, setFile, label, color }: DropZoneProps) {
  const onDrop = useCallback((acceptedFiles: File[]) => {
    if (acceptedFiles.length > 0) {
      setFile(acceptedFiles[0])
    }
  }, [setFile])

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: { 'text/csv': ['.csv'] },
    multiple: false,
  })

  const colorClasses = {
    green: {
      border: isDragActive ? 'border-success-500 bg-success-50' : 'border-gray-300 hover:border-success-400',
      icon: 'text-success-500',
      badge: 'bg-success-100 text-success-700',
    },
    blue: {
      border: isDragActive ? 'border-primary-500 bg-primary-50' : 'border-gray-300 hover:border-primary-400',
      icon: 'text-primary-500',
      badge: 'bg-primary-100 text-primary-700',
    },
  }

  const colors = colorClasses[color]

  return (
    <div className="flex-1">
      <label className="block text-sm font-medium text-gray-700 mb-2">
        <span className={`inline-flex items-center gap-1 px-2 py-1 rounded-full text-xs font-semibold ${colors.badge}`}>
          {label}
        </span>
      </label>
      
      {file ? (
        <div className={`border-2 border-dashed rounded-xl p-6 ${colors.border} transition-all`}>
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <FileSpreadsheet className={`w-10 h-10 ${colors.icon}`} />
              <div>
                <p className="font-medium text-gray-900">{file.name}</p>
                <p className="text-sm text-gray-500">
                  {(file.size / 1024).toFixed(1)} KB
                </p>
              </div>
            </div>
            <button
              onClick={() => setFile(null)}
              className="p-2 hover:bg-gray-100 rounded-full transition-colors"
            >
              <X className="w-5 h-5 text-gray-500" />
            </button>
          </div>
        </div>
      ) : (
        <div
          {...getRootProps()}
          className={`border-2 border-dashed rounded-xl p-8 cursor-pointer transition-all ${colors.border}`}
        >
          <input {...getInputProps()} />
          <div className="text-center">
            <Upload className={`w-12 h-12 mx-auto mb-3 ${colors.icon}`} />
            <p className="text-gray-600 font-medium">
              {isDragActive ? 'Drop the file here' : 'Drag & drop CSV file here'}
            </p>
            <p className="text-sm text-gray-400 mt-1">or click to browse</p>
          </div>
        </div>
      )}
    </div>
  )
}

export default function FileUpload({
  cognosFile,
  setCognosFile,
  powerbiFile,
  setPowerbiFile,
}: FileUploadProps) {
  return (
    <div className="card">
      <div className="flex items-center gap-2 mb-4">
        <Upload className="w-5 h-5 text-primary-600" />
        <h2 className="text-lg font-semibold text-gray-900">File Upload</h2>
      </div>
      
      <div className="flex flex-col md:flex-row gap-6">
        <DropZone
          file={cognosFile}
          setFile={setCognosFile}
          label="Cognos (Source)"
          color="green"
        />
        <DropZone
          file={powerbiFile}
          setFile={setPowerbiFile}
          label="Power BI (Target)"
          color="blue"
        />
      </div>
    </div>
  )
}
