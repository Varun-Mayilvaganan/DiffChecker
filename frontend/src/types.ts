export interface ValidationResult {
  name: string
  status: 'pass' | 'warning' | 'fail'
  summary: string
  details: Record<string, unknown>
}

export interface ValidationResponse {
  success: boolean
  overall_status: 'pass' | 'warning' | 'fail'
  validation_date: string
  project_name: string
  report_name: string
  environment: string
  cognos_file: string
  powerbi_file: string
  cognos_shape: { rows: number; columns: number }
  powerbi_shape: { rows: number; columns: number }
  results: ValidationResult[]
}
