import pygsheets



class Sheets():
    def __init__(self,sheet):
        self.sheet = sheet
        self.sheet_response = None
        self.worksheet=None

    def _sheetslogin(self):
        gc = pygsheets.authorize(service_account_file="./Sheets/.gdrive_private/query-maker-0c38986cec93.json")
        self.sheet_response = gc.open(self.sheet)
        print("Connected to %s" %self.sheet)
        return self

    def read(self, spreadsheet,start='A1',include_tailing_empty=True):
        if self.sheet_response is None:
            self._sheetslogin()
        self.worksheet = self.sheet_response.worksheet('title',value=spreadsheet)
        cells = self.worksheet.get_all_values(include_tailing_empty=include_tailing_empty, include_tailing_empty_rows=False, returnas='cell')
        bottom_right = cells[-1][-1]
        dataset=self.worksheet.get_as_df(start=start,end=(bottom_right.row,bottom_right.col))
        dataset
        return dataset

    def write(self, spreadsheet,dataset,start='A1'):
        if self.sheet_response is None:
            self._sheetslogin()
        self.worksheet = self.sheet_response.worksheet('title',value=spreadsheet)
        self.worksheet.set_dataframe(df=dataset,start=start,copy_head=True)
        print("%s cells updated" %self.worksheet.title)
        return self

