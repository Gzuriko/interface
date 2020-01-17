import win32com.client 

def save(wb,name): 
        wb.SaveAs(name) 

def create(): 
        Excel = win32com.client.Dispatch("Excel.Application") 
        wb = Excel.Workbooks.Open('C:\\laba\\1.xlsx') 
        c='' 
        sheet = wb.ActiveSheet
        x=0
        row = 2
        j = 2
        i = 1
        checkdata = sheet.Cells(row, 1).value
        while checkdata:
                row += 1
                x +=1
                print(checkdata)
                checkdata = sheet.Cells(row, 1).value
        print()
        while i <= x:
                b=input('Введите оценку: ') 
                sheet.Cells(j,2).value = b
                i += 1
                j += 1
        print()
        c = input('Введите имя файла: ')
        c='C:\\laba\\'+c 
        save(wb,c) 
        wb.Close() 
        Excel.Quit()
create()
