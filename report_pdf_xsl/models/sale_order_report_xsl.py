from odoo.addons.report_xlsx.report.report_xlsx import ReportXlsxAbstract
from datetime import date, datetime, time, timedelta
from pytz import timezone
class BranchReasonProfitDataXls(ReportXlsxAbstract):
    _name = 'report.report_pdf_xsl.sale_order_report_xls'
    _inherit = 'report.report_xlsx.abstract'

    def current_datetime(self):
        south_africa = timezone('Africa/Cairo')
        sa_time = datetime.now(south_africa)
        current_zoned_time = sa_time.strftime('%Y-%m-%d %H:%M:%S')
        return current_zoned_time

    #################


    def generate_xlsx_report(self, workbook, data, lines):
        for lin in lines:

            header_format = workbook.add_format({
                'border': 0,
                'align': 'center',
                'font_color': 'white',
                'bold': True,
                'valign': 'vcenter',
                'fg_color': '#C0C0C0'})
            header_format.set_text_wrap()
            header1_format = workbook.add_format({
                'border': 0,
                'border_color': 'black',
                'align': 'center',
                'font_color': 'black',
                'bold': True,
                'valign': 'vcenter',
                'fg_color': '#366092'})
            header_title_format = workbook.add_format({
                'border': 2,
                'border_color': 'black',
                'align': 'center',
                'font_color': '#000000',
                'bold': True,
                'valign': 'vcenter',
                'fg_color': '#C0C0C0'})
            header_title_format.set_text_wrap()
            header_title_format.set_font_size(14)

            header2_format = workbook.add_format({
                'border': 10,
                'border_color': 'black',
                'align': 'center',
                'font_color': 'black',
                'bold': True,
                'valign': 'vcenter',
                'fg_color': '#C0C0C0'})
            header2_format.set_text_wrap()
            header2_format.set_font_size(12)

            header3_format = workbook.add_format({
                'border': 10,
                'border_color': 'black',
                'align': 'center',
                'font_color': 'black',
                'bold': False,
                'valign': 'vcenter',
                'fg_color': '#FFFFFF'})
            header3_format.set_text_wrap()
            header3_format.set_font_size(12)

            t2 = workbook.add_format({
                'border': 1,
                'align': 'center',
                'font_color': 'black',
                'valign': 'vcenter',
                'fg_color': '#D8D8D8'})
            t2.set_text_wrap()
            t3 = workbook.add_format({
                'border': 2,
                'align': 'center',
                'font_color': 'black',
                'valign': 'vcenter'})
            t3.set_text_wrap()

            worksheet = workbook.add_worksheet()

            worksheet.right_to_left()
            worksheet.set_column('A:A',27)
            worksheet.set_column('B:B', 27)
            worksheet.set_column('C:C',27)
            worksheet.set_column('D:D', 27)
            worksheet.set_column('E:E', 27)
            worksheet.set_column('G:G', 27)
            worksheet.set_column('F:F', 27)
            worksheet.set_row(0, 40)



            worksheet.merge_range('A1:F1','Quotation # '+str(lin.name), header_title_format)

            worksheet.write('E3', 'Quotation Date', header2_format)
            worksheet.write('E4', lin.date_order, header3_format)
            worksheet.write('D3', 'Salesperson', header2_format)
            worksheet.write('D4', lin.create_uid.name, header3_format)
            worksheet.write('C3', 'Customer', header2_format)
            worksheet.write('C4',lin.partner_id.name, header3_format)
            worksheet.write('A7', 'Amount', header2_format)
            worksheet.write('B7', 'Taxes', header2_format)
            worksheet.write('C7', 'Unit Price', header2_format)
            worksheet.write('D7', 'Quantity', header2_format)
            worksheet.write('E7', 'Delivery Note', header2_format)
            worksheet.write('F7', 'Description', header2_format)



            number = 1
            row = 7
            col = 0
            for line in lin.order_line:
                worksheet.write(row, col, line.price_subtotal, header3_format)
                worksheet.write(row, col + 1, line.tax_id.name, header3_format)
                worksheet.write(row, col + 2, line.price_unit, header3_format)
                worksheet.write(row, col + 3,line.product_uom_qty , header3_format)
                worksheet.write(row, col + 4, line.delivery_note, header3_format)
                worksheet.write(row, col + 5,line.name , header3_format)

                number += 1
                row += 1
                print(row,col)
            worksheet.write(row+2,col,lin.amount_untaxed, header3_format)
            worksheet.write(row+2, col+1, 'Subtotal', header2_format)
            worksheet.write(row + 3, col, lin.amount_total, header3_format)
            worksheet.write(row + 3, col+1, 'Total', header2_format)
            row+=4


        return

