import { FileDown } from 'lucide-react'
import jsPDF from 'jspdf'

export default function Header() {
  const downloadDocumentation = () => {
    const doc = new jsPDF()
    const pageWidth = doc.internal.pageSize.getWidth()
    const pageHeight = doc.internal.pageSize.getHeight()
    const margin = 20
    const lineHeight = 6
    let y = margin

    const addPage = () => {
      doc.addPage()
      y = margin
    }

    const checkPageBreak = (requiredSpace: number) => {
      if (y + requiredSpace > pageHeight - margin) {
        addPage()
      }
    }

    const addTitle = (text: string, size: number = 18) => {
      checkPageBreak(20)
      doc.setFontSize(size)
      doc.setFont('helvetica', 'bold')
      doc.setTextColor(30, 64, 175) // Blue color
      doc.text(text, pageWidth / 2, y, { align: 'center' })
      y += lineHeight * 2
    }

    const addSubtitle = (text: string) => {
      checkPageBreak(15)
      doc.setFontSize(10)
      doc.setFont('helvetica', 'normal')
      doc.setTextColor(100, 100, 100)
      doc.text(text, pageWidth / 2, y, { align: 'center' })
      y += lineHeight * 1.5
    }

    const addSectionHeader = (text: string) => {
      checkPageBreak(20)
      y += lineHeight
      doc.setFontSize(14)
      doc.setFont('helvetica', 'bold')
      doc.setTextColor(30, 64, 175)
      doc.text(text, margin, y)
      y += lineHeight
      // Add underline
      doc.setDrawColor(30, 64, 175)
      doc.setLineWidth(0.5)
      doc.line(margin, y, pageWidth - margin, y)
      y += lineHeight * 1.5
    }

    const addParagraph = (text: string) => {
      checkPageBreak(lineHeight * 2)
      doc.setFontSize(10)
      doc.setFont('helvetica', 'normal')
      doc.setTextColor(50, 50, 50)
      const lines = doc.splitTextToSize(text, pageWidth - margin * 2)
      lines.forEach((line: string) => {
        checkPageBreak(lineHeight)
        doc.text(line, margin, y)
        y += lineHeight
      })
      y += lineHeight * 0.5
    }

    const addBullet = (text: string, indent: number = 0) => {
      checkPageBreak(lineHeight)
      doc.setFontSize(10)
      doc.setFont('helvetica', 'normal')
      doc.setTextColor(50, 50, 50)
      const bulletX = margin + indent
      doc.text('•', bulletX, y)
      const lines = doc.splitTextToSize(text, pageWidth - margin * 2 - indent - 5)
      lines.forEach((line: string, idx: number) => {
        checkPageBreak(lineHeight)
        doc.text(line, bulletX + 5, y)
        if (idx < lines.length - 1) y += lineHeight
      })
      y += lineHeight
    }

    const addTable = (headers: string[], rows: string[][], colWidths: number[]) => {
      const tableWidth = colWidths.reduce((a, b) => a + b, 0)
      const startX = margin
      
      checkPageBreak(lineHeight * (rows.length + 2))
      
      // Header
      doc.setFillColor(240, 240, 240)
      doc.rect(startX, y - 4, tableWidth, lineHeight + 2, 'F')
      doc.setFontSize(9)
      doc.setFont('helvetica', 'bold')
      doc.setTextColor(50, 50, 50)
      
      let x = startX
      headers.forEach((header, i) => {
        doc.text(header, x + 2, y)
        x += colWidths[i]
      })
      y += lineHeight + 2
      
      // Rows
      doc.setFont('helvetica', 'normal')
      doc.setFontSize(9)
      rows.forEach((row) => {
        checkPageBreak(lineHeight)
        x = startX
        row.forEach((cell, i) => {
          const lines = doc.splitTextToSize(cell, colWidths[i] - 4)
          doc.text(lines[0] || '', x + 2, y)
          x += colWidths[i]
        })
        y += lineHeight
      })
      y += lineHeight * 0.5
    }

    const addStatusBox = (status: string, color: number[], description: string) => {
      checkPageBreak(lineHeight * 2)
      const boxWidth = 60
      doc.setFillColor(color[0], color[1], color[2])
      doc.roundedRect(margin, y - 4, boxWidth, lineHeight + 2, 2, 2, 'F')
      doc.setFontSize(9)
      doc.setFont('helvetica', 'bold')
      doc.setTextColor(255, 255, 255)
      doc.text(status, margin + boxWidth / 2, y, { align: 'center' })
      doc.setTextColor(50, 50, 50)
      doc.setFont('helvetica', 'normal')
      doc.text(description, margin + boxWidth + 5, y)
      y += lineHeight * 1.5
    }

    // === PAGE 1: Title & Overview ===
    y = 40
    addTitle('DATASURE', 24)
    addTitle('Validation Checks Documentation', 16)
    y += 5
    addSubtitle('IBM Cognos to PowerBI Migration Validation Platform')
    y += 10
    addSubtitle('Document Version: 1.0  |  January 2026')
    
    y += 20
    doc.setDrawColor(200, 200, 200)
    doc.line(margin, y, pageWidth - margin, y)
    y += 15

    // Table of Contents
    doc.setFontSize(12)
    doc.setFont('helvetica', 'bold')
    doc.setTextColor(50, 50, 50)
    doc.text('TABLE OF CONTENTS', margin, y)
    y += lineHeight * 2

    const tocItems = [
      '1. Overview',
      '2. File Validation Checks',
      '3. Schema Validation Checks',
      '4. Column Statistics Validation',
      '5. Row-Level Difference Analysis',
      '6. Validation Status Definitions',
      '7. Best Practices'
    ]
    
    doc.setFontSize(10)
    doc.setFont('helvetica', 'normal')
    tocItems.forEach(item => {
      doc.text(item, margin + 10, y)
      y += lineHeight * 1.2
    })

    // === Section 1: Overview ===
    addPage()
    addSectionHeader('1. OVERVIEW')
    addParagraph('DataSure performs comprehensive data validation between IBM Cognos reports and PowerBI reports to ensure data integrity during migration. The validation process consists of four main check categories:')
    y += lineHeight * 0.5
    addBullet('File Validation - Structural comparison of files')
    addBullet('Schema Validation - Column names and data types verification')
    addBullet('Column Statistics - Aggregate data comparison')
    addBullet('Row-Level Analysis - Cell-by-cell value comparison')

    // === Section 2: File Validation ===
    addSectionHeader('2. FILE VALIDATION CHECKS')
    addParagraph('Purpose: Verify that both files have compatible structures for comparison.')
    y += lineHeight
    doc.setFont('helvetica', 'bold')
    doc.setFontSize(11)
    doc.text('Checks Performed:', margin, y)
    y += lineHeight * 1.5
    
    addTable(
      ['Check Name', 'Description'],
      [
        ['Row Count Match', 'Compares total number of rows between Cognos and PowerBI files'],
        ['Column Count Match', 'Verifies both files have the same number of columns']
      ],
      [50, pageWidth - margin * 2 - 50]
    )

    y += lineHeight
    doc.setFont('helvetica', 'bold')
    doc.setFontSize(10)
    doc.text('Pass Criteria:', margin, y)
    y += lineHeight
    doc.setFont('helvetica', 'normal')
    addBullet('Row counts must match exactly')
    addBullet('Column counts must match exactly')

    // === Section 3: Schema Validation ===
    addSectionHeader('3. SCHEMA VALIDATION CHECKS')
    addParagraph('Purpose: Ensure column names and data types are consistent between sources.')
    y += lineHeight
    
    addTable(
      ['Check Name', 'Description'],
      [
        ['Missing Columns', 'Columns present in Cognos but missing in PowerBI'],
        ['Extra Columns', 'Columns present in PowerBI but not in Cognos'],
        ['Column Name Match', 'Detects trailing spaces, case sensitivity, or typos'],
        ['Data Type Match', 'Compares inferred data types between columns']
      ],
      [50, pageWidth - margin * 2 - 50]
    )

    y += lineHeight
    doc.setFont('helvetica', 'bold')
    doc.setFontSize(10)
    doc.text('Common Issues Detected:', margin, y)
    y += lineHeight
    doc.setFont('helvetica', 'normal')
    addBullet('Trailing spaces in column names (e.g., "Employee Name " vs "Employee Name")')
    addBullet('Case sensitivity differences')
    addBullet('Type conversions (string to number, date format changes)')

    // === Section 4: Column Statistics ===
    addSectionHeader('4. COLUMN STATISTICS VALIDATION')
    addParagraph('Purpose: Verify data integrity through aggregate statistical comparison.')
    y += lineHeight
    
    addTable(
      ['Metric', 'Numeric Columns', 'Non-Numeric Columns'],
      [
        ['Sum/Count', 'Total sum of all values', 'Count of unique values'],
        ['Min Value', 'Minimum value in column', 'N/A'],
        ['Max Value', 'Maximum value in column', 'N/A'],
        ['Null Count', 'Count of NULL/empty values', 'Count of NULL/empty values'],
        ['Unique Count', 'Count of distinct values', 'Count of distinct values']
      ],
      [40, 55, 55]
    )

    y += lineHeight
    doc.setFont('helvetica', 'bold')
    doc.setFontSize(10)
    doc.text('Failure Implications:', margin, y)
    y += lineHeight
    doc.setFont('helvetica', 'normal')
    addBullet('Sum mismatch: Calculation errors, data truncation, or missing records')
    addBullet('Null count difference: Different NULL handling or data quality issues')
    addBullet('Unique count difference: Data deduplication or consolidation issues')

    // === Section 5: Row-Level Analysis ===
    addSectionHeader('5. ROW-LEVEL DIFFERENCE ANALYSIS')
    addParagraph('Purpose: Identify specific cell-level differences between datasets.')
    y += lineHeight
    
    doc.setFont('helvetica', 'bold')
    doc.setFontSize(10)
    doc.text('Output Information:', margin, y)
    y += lineHeight
    doc.setFont('helvetica', 'normal')
    addBullet('Row Number: The row where difference was found')
    addBullet('Column Name: The column containing the mismatch')
    addBullet('Cognos Value: The value from the source (Cognos) file')
    addBullet('PowerBI Value: The value from the target (PowerBI) file')

    y += lineHeight
    doc.setFont('helvetica', 'bold')
    doc.setFontSize(10)
    doc.text('Limitations:', margin, y)
    y += lineHeight
    doc.setFont('helvetica', 'normal')
    addBullet('Comparison is skipped if column names don\'t match')
    addBullet('Large datasets may show only first N differences for performance')
    addBullet('Floating-point comparisons include tolerance for precision')

    // === Section 6: Status Definitions ===
    addSectionHeader('6. VALIDATION STATUS DEFINITIONS')
    addParagraph('Each validation check returns one of three statuses:')
    y += lineHeight

    addStatusBox('PASS', [34, 197, 94], 'All checks passed. Data is consistent between sources.')
    addStatusBox('WARNING', [234, 179, 8], 'Some checks have concerns but may be acceptable.')
    addStatusBox('FAIL', [239, 68, 68], 'Critical differences found. Investigation required.')

    y += lineHeight
    doc.setFont('helvetica', 'bold')
    doc.setFontSize(10)
    doc.text('Overall Status Determination:', margin, y)
    y += lineHeight
    doc.setFont('helvetica', 'normal')
    addBullet('PASS: All individual checks pass')
    addBullet('WARNING: No failures, but some checks have warnings')
    addBullet('FAIL: One or more checks failed')

    // === Section 7: Best Practices ===
    addSectionHeader('7. BEST PRACTICES')
    
    doc.setFont('helvetica', 'bold')
    doc.setFontSize(10)
    doc.text('Before Running Validation:', margin, y)
    y += lineHeight
    doc.setFont('helvetica', 'normal')
    addBullet('Ensure files are exported with consistent settings')
    addBullet('Use the same date range filters in both reports')
    addBullet('Export to CSV/Excel with consistent formatting')
    addBullet('Verify file encoding is UTF-8 for both files')

    y += lineHeight
    doc.setFont('helvetica', 'bold')
    doc.setFontSize(10)
    doc.text('Interpreting Results:', margin, y)
    y += lineHeight
    doc.setFont('helvetica', 'normal')
    addBullet('Start with File Validation - structural issues block other checks')
    addBullet('Review Schema Validation - column name issues cause row comparison to skip')
    addBullet('Check Column Statistics - aggregate mismatches indicate data issues')
    addBullet('Use Row-Level Analysis - for identifying specific problematic records')

    y += lineHeight * 2
    addTable(
      ['Issue', 'Likely Cause', 'Solution'],
      [
        ['Column name mismatch', 'Trailing spaces, case sensitivity', 'Standardize column names'],
        ['Sum mismatch (small)', 'Floating-point precision', 'Usually acceptable'],
        ['Null count difference', 'Different NULL handling', 'Align NULL/empty treatment'],
        ['Row count mismatch', 'Filter differences', 'Verify export filters']
      ],
      [50, 50, 50]
    )

    // Footer on all pages
    const totalPages = doc.getNumberOfPages()
    for (let i = 1; i <= totalPages; i++) {
      doc.setPage(i)
      doc.setFontSize(8)
      doc.setTextColor(150, 150, 150)
      doc.text(`Page ${i} of ${totalPages}`, pageWidth / 2, pageHeight - 10, { align: 'center' })
      doc.text('© 2026 DataSure - Data Validation Platform', margin, pageHeight - 10)
    }

    // Save
    doc.save('DataSure_Validation_Checks_Documentation.pdf')
  }

  return (
    <header className="bg-white shadow-sm border-b border-gray-200">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-4">
            <img 
              src="/logo.png" 
              alt="DataSure Logo" 
              className="w-16 h-16 object-contain"
            />
            <div>
              <h1 className="text-3xl font-bold text-gray-900">DataSure</h1>
              <p className="text-sm text-gray-500">IBM Cognos to PowerBI Migration Validation Platform</p>
            </div>
          </div>
          <button
            onClick={downloadDocumentation}
            className="flex items-center gap-2 px-4 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700 transition-colors text-sm font-medium shadow-sm"
          >
            <FileDown className="w-4 h-4" />
            Checks Documentation
          </button>
        </div>
      </div>
    </header>
  )
}
