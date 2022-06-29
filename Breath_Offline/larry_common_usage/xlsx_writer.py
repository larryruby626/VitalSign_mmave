import numpy as np
import xlsxwriter


class XlsxWriter():
    def __init__(self, path):
        self.workbook = xlsxwriter.Workbook(path)
        self.worksheet = self.workbook.add_worksheet()

        self.data_format_white = self.workbook.add_format({'bg_color': '#FFFFFF'})
        self.data_format1 = self.workbook.add_format({'bg_color': '#FFC7CE'})

        self.row_c = 0

    def addline(self, datalist):
        current_data_len = len(datalist)
        for col_c in range(current_data_len):
            self.worksheet.write(self.row_c, col_c, datalist[col_c])
        self.row_c += 1

    def jump_row(self):
        self.row_c += 1

    def save(self):
        self.workbook.close()

    def high_light_row(self):
        self.worksheet.set_row(self.row_c, cell_format=self.data_format1)


if __name__ == "__main__":
    range_list = [20, 40, 60]
    save_path = "G:\\我的雲端硬碟\\開酷\\FoV_experiment\\SIC_phase_noise_110_11_16\\phase_buffer\\"
    xl_path = "G:\\我的雲端硬碟\\開酷\\FoV_experiment\\SIC_phase_noise_110_11_16\\phase_buffer\\xxx.xlsx"
    xl = XlsxWriter(xl_path)
    xl.addline(["time", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10"])

    for i in range_list:
        tmp_path = save_path + str(i) + "_meanlist.npy"
        tmp_data = np.load(tmp_path, allow_pickle=True)

        xl.addline(tmp_data)
    xl.save()