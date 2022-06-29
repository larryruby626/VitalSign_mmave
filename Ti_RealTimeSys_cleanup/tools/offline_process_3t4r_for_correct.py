import numpy as np
import mmwave as mm
from mmwave.dsp.utils import Window
from mmwave.dsp.doppler_processing import separate_tx

class DataProcessor_offline():
    def __init__(self):
        """
        :param name: str
                        Object name

        :param config: sequence of ints
                        Radar config in the order
                        [0]: samples number
                        [1]: chirps number
                        [3]: transmit antenna number
                        [4]: receive antenna number

        :param bin_queue: queue object
                        A queue for access data received by UdpListener

        :param rdi_queue: queue object
                        A queue for store RDI

        :param rai_queue: queue object
                        A queue for store RDI

        """
        self.weight_matrix = np.zeros([181, 8], dtype=complex)
        self.weight_matrix1 = np.zeros([181, 2], dtype=complex)
        self.out_matrix = np.zeros([1024, 181], dtype=complex)
        self.out_matrix1 = np.zeros([8192, 181], dtype=complex)
        self.frame_count = 0
        self.moving_list = []
        self.Y_last = 0
        Fc = 60
        count = 0
        lambda_start = 3e8 / Fc
        for theta in range(-90, 91):
            d = 0.5 * lambda_start * np.sin(theta * np.pi / 180)
            beamforming_factor = np.array([0, d, 2 * d, 3 * d, 4 * d, 5 * d, 6 * d, 7 * d]) / (3e8 / Fc)
            beamforming_factor1 = np.array([0, d, 2 * d, 3 * d]) / (3e8 / Fc)
            beamforming_factor1 = np.array([0, d]) / (3e8 / Fc)
            self.weight_matrix[count, :] = np.exp(-1j * 2 * np.pi * beamforming_factor)
            self.weight_matrix1[count, :] = np.exp(-1j * 2 * np.pi * beamforming_factor1)
            count += 1

    def larry_static_clutter_reomval(self, input_val, frame_count):
        axis = 0
        reordering = np.arange(len(input_val.shape))
        reordering[0] = axis
        reordering[axis] = 0
        input_val = input_val.transpose(reordering)

        # Apply static clutter removal
        tmp_mean = input_val.transpose(reordering).mean(0)

        if frame_count < 10:
            if frame_count == 0:
                print("first")
                self.mean = tmp_mean
            else:

                self.mean = (tmp_mean + self.mean) / 2
            return input_val
        else:
            self.mean = (tmp_mean + self.mean) / 2  # keeping update the data
            output_val = input_val - self.mean
            return output_val.transpose(reordering)

    def thumouse_clutter_removal(self, input_val, frame_count):
        # input_val = np.array([row - np.mean(row) for row in input_val])
        newout = np.zeros(np.shape(input_val))
        cc = 0
        for row in input_val:
            newout[cc] = row - np.mean(row)
            cc+=1
        return newout

    def sum_value(self,input ,reordering):
        tmp = None
        for i in range(len(input)):
            if i ==0 :
                tmp = input[i].transpose(reordering).mean(0)
            else:
                tmp +=input[i].transpose(reordering).mean(0)
        tmp = tmp /len(input)
        return tmp

    def moving_average_clutter_reomval(self, input_val, frame_count, moving_list):
        axis = 0

        reordering = np.arange(len(input_val.shape))
        reordering[0] = axis
        reordering[axis] = 0
        # input_val = input_val.transpose(reordering)

        # Apply static clutter removal
        # tmp_mean = input_val.transpose(reordering).mean(0)
        moving_list.append(input_val)

        if len(moving_list) <3 :
            return input_val
        else:
            self.mean = self.sum_value(moving_list,reordering)  #　keeping update the data
            output_val = moving_list[1] - self.mean
            moving_list.pop(0)
            return output_val.transpose(reordering)

    def delay_filter_src(self, X, pre_Y, a_weight):
        """
        :param X: new frame input
        :param pre_Y: last src_weight
        :param a_weight: the weight to mulitply pre_y
        :return: 1). after src process data
                 2). the current src_weight to feed next frame
        """
        axis = 0
        reordering = np.arange(len(X.shape))
        reordering[0] = axis
        reordering[axis] = 0
        tmp_mean = X.transpose(reordering).mean(0)
        Y = (1-a_weight)*tmp_mean + a_weight * pre_Y
        # Y = tmp_mean + a_weight * pre_Y  #the error method

        output_val = X - Y
        # ------ unit gain test
        # print(20*np.log10(np.sum(np.abs(Y))/np.sum(np.abs(tmp_mean))))
        # print((np.sum(np.abs(Y))/np.sum(np.abs(tmp_mean))))
        return output_val.transpose(reordering),Y

    def run_proecss(self,raw_data,RAI_mode,Sure_staic_RM,chirp):
        frame_count = 0
        while True:

            range_resolution, bandwidth = mm.dsp.range_resolution(64,2000,121.134)
            doppler_resolution = mm.dsp.doppler_resolution(bandwidth, 60, 33.02, 9.43, 16, 3)
            # print(range_resolution)
            raw_data = np.reshape(raw_data,[-1,4,64])
            radar_cube = mm.dsp.range_processing(raw_data, window_type_1d=Window.HAMMING)
            # radar_cube = mm.dsp.range_processing(raw_data)
            assert radar_cube.shape == (
                48, 4, 64), "[ERROR] Radar cube is not the correct shape!" #(numChirpsPerFrame, numRxAntennas, numADCSamples)


            fft2d_in = separate_tx(radar_cube, 3, vx_axis=1, axis=0)

            # fft2d_in = self.larry_static_clutter_reomval(fft2d_in, self.frame_count)
            # fft2d_in = self.thumouse_clutter_removal(fft2d_in, self.frame_count)
            # fft2d_in = self.moving_average_clutter_reomval(fft2d_in, self.frame_count ,self.moving_list)
            # fft2d_in,self.Y_last = self.delay_filter_src(fft2d_in,self.Y_last,a_weight=0)
            # 
            self.frame_count += 1

            # (3) Doppler Processing
            det_matrix, aoa_input = mm.dsp.doppler_processing(fft2d_in, num_tx_antennas=3,
                                                              clutter_removal_enabled=Sure_staic_RM,
                                                              window_type_2d=Window.BLACKMAN,
                                                               accumulate=True,interleaved=False)


            det_matrix_vis = np.fft.fftshift(det_matrix, axes=1)


            # (4) Angle Processing sample, channel, chirp        self.frame_count = 0
            azimuth_ant_1 = aoa_input[:, :2 * 4, :]
            azimuth_ant_2 = aoa_input[:, 2 * 4:, :]
            elevation_ant_1 = aoa_input[:, 2, :]
            elevation_ant_2 = aoa_input[:, 8, :]
            elevation_combine = np.array([elevation_ant_1, elevation_ant_2]).transpose([1, 0, 2])

            # (4-1) Range Angle change to chirps, samples, channels
            azimuth_ant_1 = azimuth_ant_1.transpose([2, 0, 1])
            elevation_combine = elevation_combine.transpose([2, 0, 1])

            def Range_Angle(data, padding_size):
                rai_abs = np.fft.fft(data, n=padding_size, axis=2)
                rai_abs = np.fft.fftshift(np.abs(rai_abs), axes=2)
                rai_abs = np.flip(rai_abs, axis=1 )
                return rai_abs

            RAI_mode = 0
            if RAI_mode == 0:
                azimuth_map = Range_Angle(azimuth_ant_1, 90)
                elevation_map = Range_Angle(elevation_combine, 90)

            elif RAI_mode == 1:
                print(np.shape(azimuth_ant_1))
                rdi_raw = azimuth_ant_1.reshape([-1, 8])
                for i in range(64*chirp):
                    self.out_matrix[i, :] = np.matmul(self.weight_matrix, rdi_raw[i, :])
                rai = self.out_matrix.reshape([chirp, 64, -1])
                rai = np.flip(np.abs(rai), axis=1)

                azimuth_map = np.abs(rai)

            elif RAI_mode == 2:
                # pass
                azimuth_map = Range_Angle(azimuth_ant_1, 90)
                azimuth_map = azimuth_map.astype(np.int64)
                ang_thresholdDoppler, ang_noiseFloorDoppler = np.apply_along_axis(func1d=mm.dsp.ca_,
                                                                          axis=0,
                                                                          arr=azimuth_map.T,
                                                                          l_bound=5,
                                                                          guard_len=2,
                                                                          noise_len=4)

                ang_thresholdRange, ang_noiseFloorRange = np.apply_along_axis(func1d=mm.dsp.ca_,
                                                                      axis=0,
                                                                      arr=azimuth_map,
                                                                      l_bound=5,
                                                                      guard_len=5,
                                                                      noise_len=4)

                ang_thresholdDoppler, ang_noiseFloorDoppler = ang_thresholdDoppler.T, ang_noiseFloorDoppler.T

                ang_det_doppler_mask = (azimuth_map > ang_thresholdDoppler)
                ang_det_range_mask = (azimuth_map > ang_thresholdRange)
                # print("ang_det_doppler_mask:{}".format(np.shape(ang_det_doppler_mask)))
                # print("ang_det_range_mask:{}".format(np.shape(ang_det_range_mask)))
                azimuth_map=ang_det_doppler_mask
                # Get indices of detected peaks
                azimuth_map = (ang_det_doppler_mask & ang_det_range_mask)
                # azimuth_map = np.argwhere(full_mask == True)
                # print("azimuth_map:{}".format(np.shape(azimuth_map)))

            # (5) Object Detection
            fft2d_sum = det_matrix.astype(np.int64)


            thresholdDoppler, noiseFloorDoppler = np.apply_along_axis(func1d=mm.dsp.ca_,
                                                                      axis=0,
                                                                      arr=fft2d_sum.T,
                                                                      l_bound=5,
                                                                      guard_len=2,
                                                                      noise_len=4)

            thresholdRange, noiseFloorRange = np.apply_along_axis(func1d=mm.dsp.ca_,
                                                                  axis=0,
                                                                  arr=fft2d_sum,
                                                                  l_bound=5,
                                                                  guard_len=5,
                                                                  noise_len=4)

            thresholdDoppler, noiseFloorDoppler = thresholdDoppler.T, noiseFloorDoppler.T

            det_doppler_mask = (det_matrix > thresholdDoppler)
            det_range_mask = (det_matrix > thresholdRange)


            # Get indices of detected peaks
            full_mask = (det_doppler_mask & det_range_mask)
            det_peaks_indices = np.argwhere(full_mask == True)

            # peakVals and SNR calculation
            peakVals = fft2d_sum[det_peaks_indices[:, 0], det_peaks_indices[:, 1]]
            snr = peakVals - noiseFloorRange[det_peaks_indices[:, 0], det_peaks_indices[:, 1]]

            dtype_location = '(' + str(3) + ',)<f4' # 3 == numTxAntennas
            dtype_detObj2D = np.dtype({'names': ['rangeIdx', 'dopplerIdx', 'peakVal', 'location', 'SNR'],
                                       'formats': ['<i4', '<i4', '<f4', dtype_location, '<f4']})

            detObj2DRaw = np.zeros((det_peaks_indices.shape[0],), dtype=dtype_detObj2D)
            detObj2DRaw['rangeIdx'] = det_peaks_indices[:, 0].squeeze()
            detObj2DRaw['dopplerIdx'] = det_peaks_indices[:, 1].squeeze()
            detObj2DRaw['peakVal'] = peakVals.flatten()
            detObj2DRaw['SNR'] = snr.flatten()
            # print(peakVals)
            detObj2DRaw = mm.dsp.prune_to_peaks(detObj2DRaw, det_matrix, chirp, reserve_neighbor=True) # 16 = numDopplerBins
            # --- Peak Grouping
            detObj2D = mm.dsp.peak_grouping_along_doppler(detObj2DRaw, det_matrix, 16) # 16 = numDopplerBins

            # SNRThresholds2 = np.array([[2, 23], [10, 11.5], [35, 16]])
            # peakValThresholds2 = np.array([[2, 275], [1, 400], [500, 0]])
            #
            SNRThresholds2 = np.array([[0, 0], [0, 0], [0, 0]])
            peakValThresholds2 = np.array([[0, 0], [0, 0], [0, 0]])
            # SNRThresholds2 = np.array([[0, 15], [10, 16], [0 , 20]])
            # SNRThresholds2 = np.array([[0, 20], [10, 0], [0 , 0]])

            # detObj2D = mm.dsp.range_based_pruning(detObj2D, SNRThresholds2, peakValThresholds2, 58, 53, # 64== numRangeBins
            # detObj2D = mm.dsp.range_based_pru ning(detObj2D, SNRThresholds2, peakValThresholds2, 64, 58, # 64== numRangeBins
            #                                       range_resolution)
            # detObj2D = mm.dsp.range_based_pruning(detObj2D, SNRThresholds2, peakValThresholds2, 58, 55, # 64== numRangeBins
            detObj2D = mm.dsp.range_based_pruning(detObj2D, SNRThresholds2, peakValThresholds2, 64, 55, # 64== numRangeBins
            # detObj2D = mm.dsp.range_based_pruning(detObj2D, SNRThresholds2, peakValThresholds2, 64, 0, # 64== numRangeBins
                                                  range_resolution)

            azimuthInput = aoa_input[detObj2D['rangeIdx'], :, detObj2D['dopplerIdx']]

            # print(np.shape(detObj2D['dopplerIdx']))
            Psi, Theta, Ranges, velocity, xyzVec = mm.dsp.beamforming_naive_mixed_xyz(azimuthInput,
                                                                                      # detObj2D['rangeIdx'],
                                                                                      63-detObj2D['rangeIdx'],
                                                                                      # detObj2D['dopplerIdx'],
                                                                                      63-detObj2D['dopplerIdx'],
                                                                                      range_resolution,
                                                                                      method='Bartlett')
            # print("psi = {}".format(Psi))
            # print("Theta = {}".format(Theta))
            # print(xyzVec)
            if RAI_mode==2:
                # det_matrix_vis  =np.fft.fftshift(full_mask, axes=1)
                # det_matrix_vis= det_matrix_vis&full_mask
                # print(full_mask)
                # print(np.shape(np.where(np.any(full_mask == False))))
                # det1 =  azimuth_ant_1
                det1 = np.zeros([32,64,8])
                mask_tupe = (np.where(full_mask==True))
                x =list(mask_tupe[0])
                y =list(mask_tupe[1])

                for i in range(len(x)):
                    det1[y[i],x[i],:]  = azimuth_ant_1[y[i],x[i],:]
                # det1 = np.fft.fftshift(det1, axes=1)
                azimuth_map = Range_Angle(det1, 90)
            # return  np.flip(det_matrix_vis),np.flip(azimuth_map),xyzVec
            # else:
            # return  det_matrix_vis,azimuth_map.sum(0),xyzVec


            # return  det_matrix_vis,azimuth_map.sum(0)[6:9,:],elevation_map.sum(0)[6:9,:].T,xyzVec
            # det_matrix_vis = np.fft.fftshift(det_matrix*full_mask,axes= 1)
            # return  det_matrix_vis,azimuth_map.sum(0),np.zeros([1,1]),xyzVec

            # azimuth_map = Range_Angle(azimuth_ant_1, 90)
            return  det_matrix_vis,azimuth_map.sum(0),np.zeros([1,1]),xyzVec

        output_a_angles.append((180 / np.pi) * np.arcsin(np.sin(a_angle) * np.cos(e_angle)))

