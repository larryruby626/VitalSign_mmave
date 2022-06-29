import sys
import numpy as np
import xlsxwriter
import pickle

def save_obj(obj, name ):
    with open('./out_result/'+ name + '.pkl', 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)

def load_obj(name ):
    with open('./' + name + '.pkl', 'rb') as f:
        return pickle.load(f)

if __name__ == "__main__":
    channel =1
    sure_xlsx = True
    process_type = "chest"

    if process_type == "chest":
        noise_floor = np.load("./noise_floor/sumof_noise_floor_freeze.npy", allow_pickle=True)

        if channel == 1:
            # path = "C:\\Fov_chest\\processed_data\\channel1\\"
            path = "./dataset_7G_SIC_Freeze/processed_data/channel1/"
        elif channel == 2:
            # path = "C:\\Fov_chest\\processed_data\\channel2\\"
            path = "./dataset_7G_SIC_Freeze/processed_data/channel2/"

    noise_index = list(noise_floor[0,:])
    #  ---- for corner reflector usage ----
    angle_list = ["-30", "-20", "-10", "0", "+10", "+20", "+30"] # SIC_freeze
    range_list = ["10", "15", "20", "25", "30", "35", "40", "45", "50", "55", "60"]

    SNR_dic ={}
    for method in range(1,3):
        for time in range(1,2):
            for angle in angle_list:
                for rangeX in range_list:
                    file_name = "m" + str(method) + "_range" + rangeX + "_angle" + angle + "_time_" + str(time) + ".npy"
                    if angle == "-40" or angle == "+40":
                        if rangeX != "10" and rangeX != "15" and rangeX != "60":
                            signal = np.load(path + file_name, allow_pickle=True)
                            average = np.round(np.average(signal[:, 0]))
                            if average > 124:
                                nosie_dB = noise_floor[1, noise_index.index(124)]
                            else:
                                nosie_dB = noise_floor[1, noise_index.index(average)]
                            snr = signal[:, 1] - nosie_dB
                            sum_of_snr = np.average(snr)
                            name = "m" + str(method) + "_r" + rangeX + "_a" + angle + "_t" + str(time)
                    else:
                        signal = np.load(path + file_name, allow_pickle=True)
                        average = np.round(np.average(signal[:, 0]))
                        if average > 124:
                            nosie_dB = noise_floor[1, noise_index.index(124)]
                        else:
                            nosie_dB = noise_floor[1, noise_index.index(average)]
                        snr = signal[:, 1] - nosie_dB
                        sum_of_snr = np.average(snr)
                    name = "m" + str(method) + "_r" + rangeX + "_a" + angle + "_t" + str(time)


                    if angle == "-40" or angle == "+40":
                        if rangeX == "10" or rangeX == "15":
                            SNR_dic[name] = 0
                        else:
                            SNR_dic[name] = sum_of_snr
                    else:
                        SNR_dic[name] = sum_of_snr


    if sure_xlsx:
        # method = 1
        # method = 2
        # time = 1
        # time = 2
        if channel ==1 :
            workbook = xlsxwriter.Workbook("./out_result/SNR_Freeze_CH1.xlsx")
        elif channel ==2:
            workbook = xlsxwriter.Workbook("./out_result/SNR_Freeze_CH2.xlsx")
        worksheet = workbook.add_worksheet()
        row = 0


        for method in range(1,3):
            for time in range(1,2):
                worksheet.write(row, 0, "method_{}time_{}".format(method, time))  # Writes an int
                row+=1
                worksheet.write(row, 0, "angle/range")  # Writes an int
                worksheet.write(row, 1, "angle-30")  # Writes a float
                worksheet.write(row, 2, "angle-20")  # Writes a float
                worksheet.write(row, 3, "angle-10")  # Writes a float
                worksheet.write(row, 4, "angle0")  # Writes a float
                worksheet.write(row, 5, "angle+10")  # Writes a float
                worksheet.write(row, 6, "angle+20")  # Writes a float
                worksheet.write(row, 7, "angle+30")  # Writes a float
                row +=1
                for rangeX in range_list:
                    col = 0
                    worksheet.write(row, col, rangeX + "cm")  # Writes an int
                    for angle in angle_list:
                        name = "m" + str(method) + "_r" + rangeX + "_a" + angle + "_t" + str(time)
                        col += 1
                        worksheet.write(row, col, str(SNR_dic[name]))
                    row += 1
                row+=2

        workbook.close()
        # np.save("SNR_DIC.npy", SNR_dic)

    if channel ==1 :
        save_obj(SNR_dic, "SNR_Freeze_DIC_ch1")
    elif channel ==2:
        save_obj(SNR_dic, "SNR_Freeze_DIC_ch2")

    print("Calculate SNR Process End")
    sys.exit()