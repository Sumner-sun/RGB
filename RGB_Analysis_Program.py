import sys
import cv2
import numpy as np
import json
from datetime import datetime
import os
import shutil
import threading
import time
import ctypes

class RGB_Analysis_Program:
    def __init__(self):
        self.configPath = './config.json'
        self.total_analysis_log = './result/Total_analysis.log'
        self.total_result_log = './result/Total_result.log'
        self.red_result_save_dir = './result/red'
        self.blue_result_save_dir = './result/blue'
        self.green_result_save_dir = './result/green'
        self.white_result_save_dir = './result/white'
        self.black_result_save_dir = './result/black'
        # if os.path.isdir('./result'):
        #     shutil.rmtree('./result', ignore_errors=True)
        # for path in [self.red_result_save_dir, self.blue_result_save_dir, self.green_result_save_dir,
        #              self.white_result_save_dir, self.black_result_save_dir]:
        #     if os.path.isdir(path):
        #         shutil.rmtree(path, ignore_errors=True)
        #     if not os.path.isdir(path):
        #         os.makedirs(path)
        # self.SaveLogs(self.total_analysis_log,'Tool Version: 20241129-V21')
        # if len(sys.argv) >1:
        #     self.sn = sys.argv[1].strip()
        # else:
        #     self.sn = 'NA'
        # if len(sys.argv) >2:
        #     self.lcd = sys.argv[2].strip()
        # else:
        #     self.lcd = 'NA'
        # if len(sys.argv) >3:
        #     self.line_face = sys.argv[3].strip()
        # else:
        #     self.line_face = 'NA'
        if len(sys.argv) >1:
            self.path_analysis_color = sys.argv[1]
        else:
            self.analysis_color = ''

        color = os.path.splitext(os.path.basename(self.path_analysis_color))[0]
        if color == 'red':
            if os.path.isdir(self.red_result_save_dir):
                shutil.rmtree(self.red_result_save_dir, ignore_errors=True)
            if not os.path.isdir(self.red_result_save_dir):
                os.makedirs(self.red_result_save_dir)
        elif color == 'blue':
            if os.path.isdir(self.blue_result_save_dir):
                shutil.rmtree(self.blue_result_save_dir, ignore_errors=True)
            if not os.path.isdir(self.blue_result_save_dir):
                os.makedirs(self.blue_result_save_dir)
        elif color == 'green':
            if os.path.isdir(self.green_result_save_dir):
                shutil.rmtree(self.green_result_save_dir, ignore_errors=True)
            if not os.path.isdir(self.green_result_save_dir):
                os.makedirs(self.green_result_save_dir)
        elif color == 'white':
            if os.path.isdir(self.white_result_save_dir):
                shutil.rmtree(self.white_result_save_dir, ignore_errors=True)
            if not os.path.isdir(self.white_result_save_dir):
                os.makedirs(self.white_result_save_dir)
        elif color == 'black':
            if os.path.isdir(self.black_result_save_dir):
                shutil.rmtree(self.black_result_save_dir, ignore_errors=True)
            if not os.path.isdir(self.black_result_save_dir):
                os.makedirs(self.black_result_save_dir)

        # self.SaveLogs(self.total_analysis_log,f"USN: {self.sn}")
        # self.SaveLogs(self.total_analysis_log,f"LCD: {self.lcd}")
        # self.SaveLogs(self.total_analysis_log,f"LINE FACE: {self.line_face}")
        self.LoadCFG()

    def SaveLogs(self, logPath, msg):
        currentTime = datetime.now().strftime('%Y-%m-%d %H-%M-%S')
        with open(logPath, 'a') as f:
            f.write('%s: %s\n' % (currentTime, str(msg)))

    def LoadCFG(self):
        try:
            with open(self.configPath) as cfgFile:
                cfgData = json.load(cfgFile)
                # self.SaveLogs(self.total_analysis_log,'LoadCFG: %s' % str(cfgData))
                # self.SaveLogs(self.total_analysis_log,'LoadCFG: %s' % str(json.dumps(cfgData, indent=4)))
                self.CFG_TIMEOUT = cfgData['TIMEOUT']
                self.DISTANCE_CENTER = cfgData['DISTANCE']['CENTER']
                self.DISTANCE_EDGE = cfgData['DISTANCE']['EDGE']

                self.CFG_AREA = cfgData['DETECT_ANALYSIS_REGION']['AREA']

                self.SEPARATE_POINT = cfgData['SEPARATE_POINT_LINE_REGION']['POINT']
                self.SEPARATE_LINE = cfgData['SEPARATE_POINT_LINE_REGION']['LINE']
                self.SEPARATE_REGION = cfgData['SEPARATE_POINT_LINE_REGION']['REGION']
                # self.EXPECTED_COLOR = cfgData['EXPECTED']['COLOR']
                # self.EXPECTED_REGION = cfgData['EXPECTED']['REGION']


                self.EXPECTED_WHITE = cfgData['EXPECTED']['WHITE']
                self.EXPECTED_BLACK = cfgData['EXPECTED']['BLACK']
                self.EXPECTED_RED = cfgData['EXPECTED']['RED']
                self.EXPECTED_BLUE = cfgData['EXPECTED']['BLUE']
                self.EXPECTED_GREEN = cfgData['EXPECTED']['GREEN']

                self.SEPARATION_ENV_RED = cfgData['SEPARATION_ENV']['RED']
                self.SEPARATION_ENV_BLUE = cfgData['SEPARATION_ENV']['BLUE']
                self.SEPARATION_ENV_GREEN = cfgData['SEPARATION_ENV']['GREEN']
                self.SEPARATION_ENV_WHITE = cfgData['SEPARATION_ENV']['WHITE']
                self.SEPARATION_ENV_BLACK = cfgData['SEPARATION_ENV']['BLACK']

                self.DETECT_BLACK_POINT_RED = cfgData['DETECT_BLACK_POINT']['RED']
                self.DETECT_BLACK_POINT_BLUE = cfgData['DETECT_BLACK_POINT']['BLUE']
                self.DETECT_BLACK_POINT_GREEN = cfgData['DETECT_BLACK_POINT']['GREEN']
                self.DETECT_BLACK_POINT_WHITE = cfgData['DETECT_BLACK_POINT']['WHITE']
                self.DETECT_BLACK_POINT_BLACK = cfgData['DETECT_BLACK_POINT']['BLACK']

                self.DETECT_WHITE_POINT_RED = cfgData['DETECT_WHITE_POINT']['RED']
                self.DETECT_WHITE_POINT_BLUE = cfgData['DETECT_WHITE_POINT']['BLUE']
                self.DETECT_WHITE_POINT_GREEN = cfgData['DETECT_WHITE_POINT']['GREEN']
                self.DETECT_WHITE_POINT_WHITE = cfgData['DETECT_WHITE_POINT']['WHITE']
                self.DETECT_WHITE_POINT_BLACK = cfgData['DETECT_WHITE_POINT']['BLACK']

                self.DETECT_LEAKAGE_MURA_RED = cfgData['DETECT_LEAKAGE_MURA']['RED']
                self.DETECT_LEAKAGE_MURA_BLUE = cfgData['DETECT_LEAKAGE_MURA']['BLUE']
                self.DETECT_LEAKAGE_MURA_GREEN = cfgData['DETECT_LEAKAGE_MURA']['GREEN']
                self.DETECT_LEAKAGE_MURA_WHITE = cfgData['DETECT_LEAKAGE_MURA']['WHITE']
                self.DETECT_LEAKAGE_MURA_BLACK = cfgData['DETECT_LEAKAGE_MURA']['BLACK']
        except Exception as e:
            # self.SaveLogs(self.total_analysis_log, 'LoadCFG: %s' % str(e))
            # with open(self.total_result_log, 'w') as resultFile:
            #     resultFile.writelines('FAIL')
            quit(1)

    def Separation_Env(self, color, image, hsvcolor1, contrast1, clahe1, blur1, threshold1, hsvcolor2, threshold2,
                       addweight):
        msg = ''
        result = True
        try:
            # I: tách các vật thể dư thừa
            # Giới hạn hsv cho màu cần phân tích
            lower_filter1 = np.array(hsvcolor1[0])
            upper_filter1 = np.array(hsvcolor1[1])
            # Chuyển hình ảnh BGR thành HSV
            hsv_1 = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
            # Tạo mặt nạ HSV với vùng màu trong giới hạn
            maskhsv_filter1 = cv2.inRange(hsv_1, lower_filter1, upper_filter1)
            # Tách những vật thể khác màu trong ảnh gốc
            hsv_filter1 = cv2.bitwise_and(image, image, mask=maskhsv_filter1)
            # Chuyển hình ảnh BGR thành GRAY
            gray_filter1 = cv2.cvtColor(hsv_filter1, cv2.COLOR_RGB2GRAY)
            # Điều chỉnh độ tương phản của ảnh GRAY
            change_contrast_filter1 = cv2.convertScaleAbs(gray_filter1, alpha=contrast1, beta=0)
            # Cân bằng độ sáng (độ sáng: 5, vùng điều chỉnh pixel 20x20)
            clahe_filter1 = cv2.createCLAHE(clipLimit=clahe1[0], tileGridSize=clahe1[1])
            equalized_filter1 = clahe_filter1.apply(change_contrast_filter1)
            # Lọc nhiễu với bộ lọc pixel 5x5)
            blurred_filter1 = cv2.GaussianBlur(equalized_filter1, blur1, 0)
            # Áp dụng ngưỡng vào ảnh để tìm ra các vật thể
            if color != 'Black':
                threshold_filter1 = cv2.adaptiveThreshold(blurred_filter1, 255, cv2.ADAPTIVE_THRESH_MEAN_C,
                                                          cv2.THRESH_BINARY_INV,
                                                          threshold1[0], threshold1[1])
            else:
                _, threshold_filter1 = cv2.threshold(blurred_filter1, threshold1[0], threshold1[1], cv2.THRESH_BINARY)
            # Tìm ra các vật thể
            conts_filter1, _ = cv2.findContours(threshold_filter1, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
            # Sắp xếp vật thể theo số lượng pixel từ lớn đến bé
            contours_filter1 = sorted(conts_filter1, key=cv2.contourArea, reverse=True)
            # Chọn vật thể có số pixel lớn nhất
            cnt_filter1 = contours_filter1[0]
            # Tạo một mặt nạ tất cả đen với cùng kích thước với hình ảnh ban đầu
            mask_filter1 = np.zeros_like(image)
            # Tìm ra các đỉnh da giác phẳng của vật thể
            approx_filter1 = cv2.approxPolyDP(cnt_filter1,
                                              0.000000000000000000000000000000001 * cv2.arcLength(cnt_filter1, True),
                                              True)
            # Vẽ đa giác phẳng, ảnh sẽ bao gồm 2 màu đen và trắng
            cv2.drawContours(mask_filter1, [approx_filter1], -1, (0, 0, 255), thickness=cv2.FILLED)
            # Vẽ viền trắng xung quanh vật thể sau khi cắt
            # cv2.drawContours(mask_filter1, [approx_filter1], -1, (255, 255, 255), 20, cv2.LINE_AA)
            if color != 'Black':
                cv2.drawContours(mask_filter1, [approx_filter1], -1, (255, 255, 255), 40, cv2.LINE_AA)
            else:
                cv2.drawContours(mask_filter1, [approx_filter1], -1, (255, 255, 255), 10, cv2.LINE_AA)

            # II: tách nhiễu cạnh của vật thể cần phân tích
            # Giới hạn HSV của màu trắng
            lower_filter2 = np.array(hsvcolor2[0])
            upper_filter2 = np.array(hsvcolor2[1])
            # Chuyển hình ảnh BGR thành HSV
            hsv_2 = cv2.cvtColor(mask_filter1, cv2.COLOR_BGR2HSV)
            # Tạo mặt nạ HSV với vùng màu trong giới hạn
            maskhsv_filter2 = cv2.inRange(hsv_2, lower_filter2, upper_filter2)
            # Tách những vật thể khác màu trong ảnh gốc
            hsv_filter2 = cv2.bitwise_and(mask_filter1, mask_filter1, mask=maskhsv_filter2)
            # Chuyển hình ảnh BGR thành GRAY
            gray_filter2 = cv2.cvtColor(hsv_filter2, cv2.COLOR_BGR2GRAY)
            # Áp dụng ngưỡng vào ảnh để tìm ra các vật thể
            threshold_filter2 = cv2.adaptiveThreshold(gray_filter2, 255, cv2.ADAPTIVE_THRESH_MEAN_C,
                                                      cv2.THRESH_BINARY_INV,
                                                      threshold2[0], threshold2[1])
            # Tìm ra các vật thể
            conts_filter2, _ = cv2.findContours(threshold_filter2, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
            # Sắp xếp vật thể theo số lượng pixel từ lớn đến bé
            contours_filter2 = sorted(conts_filter2, key=cv2.contourArea, reverse=True)
            # Chọn vật thể có số pixel lớn nhất
            cnt_filter2 = contours_filter2[0]
            # Tạo một mặt nạ tất cả đen với cùng kích thước với hình ảnh ban đầu
            mask_filter2 = np.zeros_like(image)
            # Tìm ra các đỉnh da giác phẳng của vật thể
            approx_filter2 = cv2.approxPolyDP(cnt_filter2,
                                              0.000000000000000000000000000000001 * cv2.arcLength(cnt_filter2, True),
                                              True)
            cv2.drawContours(mask_filter2, [approx_filter2], -1, (255, 255, 255), thickness=cv2.FILLED)
            image_filter2 = cv2.bitwise_and(image, mask_filter2)
            # Chuyển đổi mặt nạ từ BGR sang GRAY
            maskgray = cv2.cvtColor(mask_filter2, cv2.COLOR_BGR2GRAY)
            # Lấy giá trị màu BGR trung bình của mặt nạ
            mean_bgr = cv2.mean(image, mask=maskgray)[:3]
            # Tạo một mặt nạ tất cả đen với cùng kích thước với hình ảnh ban đầu
            new_image = np.zeros_like(image)
            # Vẽ đa giác phẳng
            cv2.drawContours(new_image, [approx_filter2], -1, (mean_bgr[0] / 3.0, mean_bgr[1] / 3.0, mean_bgr[2] / 3.0),
                             thickness=cv2.FILLED)
            image_filter3 = cv2.addWeighted(image_filter2, addweight[0], new_image, addweight[1], 0)

            height, width, channels = image.shape
            avg_color_image = np.zeros((height, width, channels), dtype=np.uint8)
            avg_color_image[:] = [mean_bgr[0]/1.5, mean_bgr[1]/1.5, mean_bgr[2]/1.5]  # Tất cả trong màu đỏ
            # new_image1[:] = [255,255,255]  # Tất cả trong màu đỏ

            cv2.drawContours(avg_color_image, [approx_filter2], -1, (0, 0, 0),
                             thickness=cv2.FILLED)

            image_filter4 = cv2.bitwise_xor(image_filter3, avg_color_image)

            path = r'%s/separation_env' % getattr(self, '%s_result_save_dir' % color.lower())
            if os.path.isdir(path):
                shutil.rmtree(path, ignore_errors=True)
            if not os.path.isdir(path):
                os.makedirs(path)
            # cv2.imwrite(os.path.join(path, 'new_image.png'), new_image)
            # cv2.imwrite(os.path.join(path, 'maskhsv_filter1.png'), maskhsv_filter1)
            # cv2.imwrite(os.path.join(path, 'hsv_filter1.png'), hsv_filter1)
            # cv2.imwrite(os.path.join(path, 'mask_filter1.png'), mask_filter1)
            # cv2.imwrite(os.path.join(path, 'threshold_filter1.png'), threshold_filter1)
            # cv2.imwrite(os.path.join(path, 'image_filter2.png'), image_filter2)
            # cv2.imwrite(os.path.join(path, 'hsv_filter2.png'), hsv_filter2)
            # cv2.imwrite(os.path.join(path, 'threshold_filter2.png'), threshold_filter2)
            # cv2.imwrite(os.path.join(path, 'mask_filter2.png'), mask_filter2)
            # cv2.imwrite(os.path.join(path, 'image_filter3.png'), image_filter3)
            # cv2.imwrite(os.path.join(path, 'image_filter4.png'), image_filter4)
        except Exception as e:
            result = False
            msg = str(e)
            image_filter3 = np.array([0,0,0])
        return result, image_filter2, image_filter3, image_filter4, approx_filter2, msg

    def single_scale_retinex(self, img, sigma):
        retinex = np.log10(img + 0.02) - np.log10(cv2.GaussianBlur(img, (0, 0), sigma) + 0.01)
        return retinex

    def Detect_black_point(self, color, image, image_drawcontours, approx_filter, vsigma, rtn, clahe, median_blur, gaussian_blur,
                           border_thickness, threshold, dilate_kernel, erode_kernel, canny):
        list_detect_black_point = []
        dict_black_conts = {}
        result = True
        msg = ''
        try:

            lab = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
            # hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

            # Chia ảnh thành các kênh màu
            l, a, b = cv2.split(lab)
            # h, s, v = cv2.split(hsv)

            retinex = self.single_scale_retinex(np.float32(l), sigma=vsigma)
            # retinex = self.single_scale_retinex(np.float32(v), sigma=vsigma)

            retinex_image = np.uint8(rtn * (retinex - np.min(retinex)) / (np.max(retinex) - np.min(retinex)))


            clahe_image = cv2.createCLAHE(clipLimit=clahe[0], tileGridSize=clahe[1])

            # Áp dụng cân bằng sáng histogram
            equalized_image = clahe_image.apply(retinex_image)


            kernel2 = np.ones((dilate_kernel[0], dilate_kernel[1]), np.uint8)
            dilate_image = cv2.dilate(equalized_image, kernel2, iterations=1)  # mask1
            kernel1 = np.ones((erode_kernel[0], erode_kernel[1]), np.uint8)
            erode_image = cv2.erode(dilate_image, kernel1, iterations=1)  # mask1

            median_blurred_image = cv2.medianBlur(erode_image, median_blur)

            gaussian_blurred_image = cv2.GaussianBlur(median_blurred_image, (gaussian_blur[0], gaussian_blur[1]), 0)

            if color == 'Black':
                cv2.drawContours(gaussian_blurred_image, [approx_filter], -1, (255, 255, 255), border_thickness, cv2.LINE_AA)
            else:
                cv2.drawContours(gaussian_blurred_image, [approx_filter], -1, (0, 0, 0), border_thickness, cv2.LINE_AA)

            # print(blurred_image.shape)
            threshold_image = cv2.adaptiveThreshold(gaussian_blurred_image, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                           cv2.THRESH_BINARY_INV, threshold[0], threshold[1])

            sx = cv2.Sobel(gaussian_blurred_image, cv2.CV_16SC1, 1, 0, ksize=3)
            sy = cv2.Sobel(gaussian_blurred_image, cv2.CV_16SC1, 0, 1, ksize=3)
            canny_image = cv2.Canny(sx, sy, canny[0], canny[1], L2gradient=True)
            conts_canny, _ = cv2.findContours(canny_image, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)


            sx_binary = cv2.Sobel(threshold_image, cv2.CV_16SC1, 1, 0, ksize=3)
            sy_binary = cv2.Sobel(threshold_image, cv2.CV_16SC1, 0, 1, ksize=3)
            canny_image_binary = cv2.Canny(sx_binary, sy_binary, canny[0], canny[1], L2gradient=True)

            conts_canny_binary, _ = cv2.findContours(canny_image_binary, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

            n=0
            for cont in conts_canny:
                area = cv2.contourArea(cont)
                if self.CFG_AREA[0] > area > self.CFG_AREA[1]:
                    n+=1
                    m = cv2.moments(cont)
                    x = int(m['m10'] / m['m00'])  # x坐标
                    y = int(m['m01'] / m['m00'])  # y坐标
                    l = cv2.minEnclosingCircle(cont)[1] * 2
                    list_detect_black_point.append((x, y, area, n, l, cont))
                    dict_black_conts[str(n)] = cont
                    cv2.drawContours(image_drawcontours, [cont], -1, (0, 255, 255), cv2.FILLED)


            for cont in conts_canny_binary:
                area = cv2.contourArea(cont)
                if self.CFG_AREA[0] > area > self.CFG_AREA[1]:
                    n+=1
                    m = cv2.moments(cont)
                    x = int(m['m10'] / m['m00'])  # x坐标
                    y = int(m['m01'] / m['m00'])  # y坐标
                    l = cv2.minEnclosingCircle(cont)[1] * 2
                    list_detect_black_point.append((x, y, area, n, l, cont))
                    dict_black_conts[str(n)] = cont
                    cv2.drawContours(image_drawcontours, [cont], -1, (0, 255, 255), cv2.FILLED)

            path = r'%s/detect_black_point' % getattr(self, '%s_result_save_dir' % color.lower())
            if os.path.isdir(path):
                shutil.rmtree(path, ignore_errors=True)
            if not os.path.isdir(path):
                os.makedirs(path)
            # cv2.imwrite(os.path.join(path, 'retinex_image.png'), retinex_image)
            # cv2.imwrite(os.path.join(path, 'equalized_image.png'), equalized_image)
            # cv2.imwrite(os.path.join(path, 'median_blurred_image.png'), median_blurred_image)
            # cv2.imwrite(os.path.join(path, 'gaussian_blurred_image.png'), gaussian_blurred_image)
            # cv2.imwrite(os.path.join(path, 'threshold_image.png'), threshold_image)
            # cv2.imwrite(os.path.join(path, 'canny_image.png'), canny_image)
            # cv2.imwrite(os.path.join(path, 'image_drawcontours.png'), image_drawcontours)
        except Exception as e:
            msg = str(e)
            result = False
        return result, msg,  list_detect_black_point, dict_black_conts, image_drawcontours

    def Detect_white_point(self, color, image, image_drawcontours, border_thickness, threshold, dilate_kernel, erode_kernel, blur, canny):
        list_detect_white_point = []
        dict_white_conts = {}
        result = True
        msg = ''
        try:
            # Tạo kernel để làm sắc nét
            sharpening_kernel = np.array([[-5, -1, 3],
                                          [-1, 5, -1],
                                          [1, -1, 1]])

            # Áp dụng kernel lên ảnh
            sharpened_image = cv2.filter2D(image, -1, sharpening_kernel)


            # Chuyển ảnh thành GRAY
            gray_detect_roi = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            # Áp dụng ngưỡng để tìm ra vùng cần phân tích
            threshold_detect_roi = cv2.adaptiveThreshold(gray_detect_roi, 255, cv2.ADAPTIVE_THRESH_MEAN_C,
                                                         cv2.THRESH_BINARY_INV, threshold[0], threshold[1])
            # Tìm các vùng sau khi áp dụng ngưỡng
            conts_detect_roi, _ = cv2.findContours(threshold_detect_roi, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
            # Sắp xếp các vùng từ lớn đến nhỏ
            contours_detect_roi = sorted(conts_detect_roi, key=cv2.contourArea, reverse=True)
            # Chọn vùng lớn nhất là vùng cần phân tích
            cnt_detect_roi = contours_detect_roi[0]
            # Tạo một mặt nạ tất cả đen với cùng kích thước với hình ảnh ban đầu
            mask_detect_roi = np.zeros_like(gray_detect_roi)
            # Tìm ra các cạnh của đa giác phẳng
            approx_detect_roi = cv2.approxPolyDP(cnt_detect_roi, 0.000000000000000000000000000000001 * cv2.arcLength(cnt_detect_roi, True), True)
            # Vẽ đa giác phẳng
            cv2.drawContours(mask_detect_roi, [approx_detect_roi], -1, (255, 255, 255), thickness=cv2.FILLED)
            # Tạo 1 kernel
            kernel_dilate = np.ones(dilate_kernel, np.uint8)
            # Phóng to các pixel dựa theo kernel trên
            dilate_image = cv2.dilate(sharpened_image, kernel_dilate, iterations=1)
            # Tạo 1 kernel
            kernel_erode = np.ones(erode_kernel, np.uint8)
            # thu nhỏ các pixel dựa theo kernel trên
            erode_image = cv2.erode(dilate_image, kernel_erode, iterations=1)
            # Chuyển đổi thành ảnh GRAY
            gray_image = cv2.cvtColor(erode_image, cv2.COLOR_BGR2GRAY)
            # Lọc nhiễu trong hình ảnh
            blurred_image = cv2.GaussianBlur(gray_image, blur, 0)
            # Dùng thuật toán and để tìm ra vùng cần phân tích
            analysis_image = cv2.bitwise_and(blurred_image, mask_detect_roi)
            # Vẽ viền trắng bao quanh vùng phân tích để làm mượt các cạnh
            if color != 'Black':
                cv2.drawContours(analysis_image, [approx_detect_roi], -1, (255, 255, 255), border_thickness, cv2.LINE_AA)
            else:
                cv2.drawContours(analysis_image, [approx_detect_roi], -1, (255, 255, 255), border_thickness, cv2.LINE_AA)

            # Áp dụng thuật toán Canny để tìm ra các điểm NG
            sx = cv2.Sobel(analysis_image, cv2.CV_16SC1, 1, 0, ksize=3)
            sy = cv2.Sobel(analysis_image, cv2.CV_16SC1, 0, 1, ksize=3)
            canny_image = cv2.Canny(sx, sy, canny[0], canny[1], L2gradient=True)
            # Lưu các điểm NG
            conts, _ = cv2.findContours(canny_image, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
            n=0
            for cont in conts:
                area = cv2.contourArea(cont)
                if self.CFG_AREA[0] > area > self.CFG_AREA[1]:
                    n+=1
                    m = cv2.moments(cont)
                    x = int(m['m10'] / m['m00'])  # x坐标
                    y = int(m['m01'] / m['m00'])  # y坐标
                    l = cv2.minEnclosingCircle(cont)[1] * 2
                    # area = round(area/3.5,2)
                    list_detect_white_point.append((x, y, area, n, l, cont))
                    dict_white_conts[str(n)] = cont
                    cv2.drawContours(image_drawcontours, [cont], -1, (0, 255, 255), cv2.FILLED)
            path = r'%s/detect_white_point' % getattr(self, '%s_result_save_dir' % color.lower())
            if os.path.isdir(path):
                shutil.rmtree(path, ignore_errors=True)
            if not os.path.isdir(path):
                os.makedirs(path)
            # cv2.imwrite(os.path.join(path, 'sharpened_image.png'), sharpened_image)
            # cv2.imwrite(os.path.join(path, 'gray_detect_roi.png'), gray_detect_roi)
            # cv2.imwrite(os.path.join(path, 'threshold_detect_roi.png'), threshold_detect_roi)
            # cv2.imwrite(os.path.join(path, 'dilate_image.png'), dilate_image)
            # cv2.imwrite(os.path.join(path, 'erode_image.png'), erode_image)
            # cv2.imwrite(os.path.join(path, 'gray_image.png'), gray_image)
            # cv2.imwrite(os.path.join(path, 'blurred_image.png'), blurred_image)
            # cv2.imwrite(os.path.join(path, 'analysis_image.png'), analysis_image)
            # cv2.imwrite(os.path.join(path, 'canny_image.png'), canny_image)
        except Exception as e:
            msg = str(e)
            result = False
        return result, msg, list_detect_white_point, dict_white_conts, image_drawcontours

    def Detect_leakage_mura_color(self, color, image, image_drawcontours, approx_filter, clahe, blur, border_thickness, threshold):
        list_detect_leakage_mura = []
        dict_leakage_mura_conts = {}
        result = True
        msg = ''
        try:
            lab = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
            l, a, b = cv2.split(lab)
            clahe_image = cv2.createCLAHE(clipLimit=clahe[0], tileGridSize=clahe[1])

            # Áp dụng cân bằng sáng histogram
            equalized_image = clahe_image.apply(l)

            gaussian_blurred_image = cv2.GaussianBlur(equalized_image, (blur[0], blur[1]), 0)

            cv2.drawContours(gaussian_blurred_image, [approx_filter], -1, (255, 255, 255), border_thickness, cv2.LINE_AA)

            _, threshold_image = cv2.threshold(gaussian_blurred_image, threshold[0], threshold[1], cv2.THRESH_BINARY)

            conts, _ = cv2.findContours(threshold_image, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
            n=0
            for cont in conts:
                area = cv2.contourArea(cont)
                if self.CFG_AREA[0] > area > self.CFG_AREA[1]:
                    n+=1
                    m = cv2.moments(cont)
                    x = int(m['m10'] / m['m00'])  # x坐标
                    y = int(m['m01'] / m['m00'])  # y坐标
                    x1, y1, w1, h1 = cv2.boundingRect(cont)
                    length = cv2.minEnclosingCircle(cont)[1] * 2
                    list_detect_leakage_mura.append((x, y, area, n, length, cont))
                    dict_leakage_mura_conts[str(n)] = cont
                    cv2.drawContours(image_drawcontours, [cont], -1, (0, 255, 255), cv2.FILLED)
                    cv2.putText(image_drawcontours, str(n), (x1 + w1 + 30, y1), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 125, 255), 2,
                                cv2.LINE_AA)
            path = r'%s/detect_leakage_mura' % getattr(self, '%s_result_save_dir' % color.lower())
            if os.path.isdir(path):
                shutil.rmtree(path, ignore_errors=True)
            if not os.path.isdir(path):
                os.makedirs(path)
            # cv2.imwrite(os.path.join(path, 'l.png'), l)
            # cv2.imwrite(os.path.join(path, 'equalized_image.png'), equalized_image)
            # cv2.imwrite(os.path.join(path, 'gaussian_blurred_image.png'), gaussian_blurred_image)
            # cv2.imwrite(os.path.join(path, 'threshold_image.png'), threshold_image)
        except Exception as e:
            msg = str(e)
            result = False
        return result, msg, list_detect_leakage_mura, dict_leakage_mura_conts, image_drawcontours

    def Detect_leakage_mura_black(self, color, image, image_drawcontours, threshold, dilate_kernel, erode_kernel, blur,
                                  border_thickness, th_leakage_mura, canny):
        list_detect_leakage_mura = []
        dict_leakage_mura_conts = {}
        result = True
        msg = ''
        try:
            # Tạo kernel để làm sắc nét
            sharpening_kernel = np.array([[1, 1, 1],
                                          [1, 2, 1],
                                          [1, 1, 1]])

            # Áp dụng kernel lên ảnh
            sharpened_image = cv2.filter2D(image, -1, sharpening_kernel)


            # Chuyển ảnh thành GRAY
            gray_detect_roi = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            # Áp dụng ngưỡng để tìm ra vùng cần phân tích
            threshold_detect_roi = cv2.adaptiveThreshold(gray_detect_roi, 255, cv2.ADAPTIVE_THRESH_MEAN_C,
                                                         cv2.THRESH_BINARY_INV, threshold[0], threshold[1])
            # Tìm các vùng sau khi áp dụng ngưỡng
            conts_detect_roi, _ = cv2.findContours(threshold_detect_roi, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
            # Sắp xếp các vùng từ lớn đến nhỏ
            contours_detect_roi = sorted(conts_detect_roi, key=cv2.contourArea, reverse=True)
            # Chọn vùng lớn nhất là vùng cần phân tích
            cnt_detect_roi = contours_detect_roi[0]
            # Tạo một mặt nạ tất cả đen với cùng kích thước với hình ảnh ban đầu
            mask_detect_roi = np.zeros_like(gray_detect_roi)
            # Tìm ra các cạnh của đa giác phẳng
            approx_detect_roi = cv2.approxPolyDP(cnt_detect_roi, 0.000000000000000000000000000000001 * cv2.arcLength(cnt_detect_roi, True), True)
            # Vẽ đa giác phẳng
            cv2.drawContours(mask_detect_roi, [approx_detect_roi], -1, (255, 255, 255), thickness=cv2.FILLED)
            # Tạo 1 kernel
            kernel_dilate = np.ones(dilate_kernel, np.uint8)
            # Phóng to các pixel dựa theo kernel trên
            dilate_image = cv2.dilate(sharpened_image, kernel_dilate, iterations=1)
            # Tạo 1 kernel
            kernel_erode = np.ones(erode_kernel, np.uint8)
            # thu nhỏ các pixel dựa theo kernel trên
            erode_image = cv2.erode(dilate_image, kernel_erode, iterations=1)
            # Chuyển đổi thành ảnh GRAY
            gray_image = cv2.cvtColor(erode_image, cv2.COLOR_BGR2GRAY)
            # Lọc nhiễu trong hình ảnh
            blurred_image = cv2.GaussianBlur(gray_image, blur, 0)
            # Dùng thuật toán and để tìm ra vùng cần phân tích
            analysis_image = cv2.bitwise_and(blurred_image, mask_detect_roi)
            # Vẽ viền trắng bao quanh vùng phân tích để làm mượt các cạnh
            cv2.drawContours(analysis_image, [approx_detect_roi], -1, (0, 0, 0), border_thickness, cv2.LINE_AA)
            #áp dụng ngưỡng nhị phân để tìm ra vùng leakage hoặc mura
            _, binary_image = cv2.threshold(analysis_image, th_leakage_mura[0], th_leakage_mura[1], cv2.THRESH_BINARY)

            sx = cv2.Sobel(binary_image, cv2.CV_16SC1, 1, 0, ksize=3)
            sy = cv2.Sobel(binary_image, cv2.CV_16SC1, 0, 1, ksize=3)
            canny_image = cv2.Canny(sx, sy, canny[0], canny[1], L2gradient=True)

            # Lưu các điểm NG
            conts, _ = cv2.findContours(canny_image, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
            n=0
            for cont in conts:
                area = cv2.contourArea(cont)
                if self.CFG_AREA[0] > area > self.CFG_AREA[1]:
                    n+=1
                    m = cv2.moments(cont)
                    x = int(m['m10'] / m['m00'])  # x坐标
                    y = int(m['m01'] / m['m00'])  # y坐标
                    l = cv2.minEnclosingCircle(cont)[1] * 2
                    # area = round(area/3.5,2)
                    list_detect_leakage_mura.append((x, y, area, n, l, cont))
                    dict_leakage_mura_conts[str(n)] = cont
                    cv2.drawContours(image_drawcontours, [cont], -1, (0, 255, 255), cv2.FILLED)
            path = r'%s/detect_leakage_mura' % getattr(self, '%s_result_save_dir' % color.lower())
            if os.path.isdir(path):
                shutil.rmtree(path, ignore_errors=True)
            if not os.path.isdir(path):
                os.makedirs(path)
            # cv2.imwrite(os.path.join(path, 'sharpened_image.png'), sharpened_image)
            # cv2.imwrite(os.path.join(path, 'gray_detect_roi.png'), gray_detect_roi)
            # cv2.imwrite(os.path.join(path, 'threshold_detect_roi.png'), threshold_detect_roi)
            # cv2.imwrite(os.path.join(path, 'dilate_image.png'), dilate_image)
            # cv2.imwrite(os.path.join(path, 'erode_image.png'), erode_image)
            # cv2.imwrite(os.path.join(path, 'gray_image.png'), gray_image)
            # cv2.imwrite(os.path.join(path, 'blurred_image.png'), blurred_image)
            # cv2.imwrite(os.path.join(path, 'analysis_image.png'), analysis_image)
            # cv2.imwrite(os.path.join(path, 'binary_image.png'), binary_image)
            # cv2.imwrite(os.path.join(path, 'canny_image.png'), canny_image)
        except Exception as e:
            msg = str(e)
            result = False
        return result, msg, list_detect_leakage_mura, dict_leakage_mura_conts, image_drawcontours

    def merge_bad_points(self, input_list):
        listAllBPNearly = []
        for n in range(len(input_list)):
            # print('-----------------------------------------------------')
            #(x, y, area, n, l, cont)
            listBPNearly = []
            mainBD = input_list[n]
            mainBP_X, mainBP_Y, mainBP_W, mainBP_H = cv2.boundingRect(mainBD[5])
            mainBP_X_Start = mainBP_X - self.DISTANCE_EDGE
            mainBP_Y_Start = mainBP_Y - self.DISTANCE_EDGE
            mainBP_X_End = mainBP_X + mainBP_W + self.DISTANCE_EDGE
            mainBP_Y_End = mainBP_Y + mainBP_H + self.DISTANCE_EDGE
            listBPNearly.append(mainBD[:5])
            listBPFilter = input_list.copy()
            listBPFilter.pop(n)
            for bp in listBPFilter:
                # print(bp[:2])
                distance = abs(np.sqrt((bp[0] - mainBD[0])**2 + (bp[1] - mainBD[1])**2))
                # print(distance)
                bp_X, bp_Y, bp_W, bp_H = cv2.boundingRect(bp[5])
                bp_X_Start = bp_X - self.DISTANCE_EDGE
                bp_Y_Start = bp_Y - self.DISTANCE_EDGE
                bp_X_End = bp_X + bp_W + self.DISTANCE_EDGE
                bp_Y_End = bp_Y + bp_H + self.DISTANCE_EDGE
                # if (-10, -10) < (x, y) < (10, 10):
                if distance < self.DISTANCE_CENTER or ((mainBP_X_Start<bp_X_Start<mainBP_X_End and mainBP_Y_Start<bp_Y_Start<mainBP_Y_End) or
                                     (mainBP_X_Start<bp_X_End<mainBP_X_End and mainBP_Y_Start<bp_Y_End<mainBP_Y_End)):
                # if (mainBP_X_Start<bp_X_Start<mainBP_X_End and mainBP_Y_Start<bp_Y_Start<mainBP_Y_End) or (mainBP_X_Start<bp_X_End<mainBP_X_End and mainBP_Y_Start<bp_Y_End<mainBP_Y_End):
                    # print(x, y)
                    listBPNearly.append(bp[:5])
                    # listBPNearly.append(bp)
            listBPNearly.sort(key=lambda x: (x[0], x[1]))
            listAllBPNearly.append(listBPNearly)
        return listAllBPNearly

    def remove_duplicates(self, input_list):
        output_list = []
        for item in input_list:
            if item not in output_list:
                output_list.append(item)
        return output_list

    def make_list_same_element(self, input_list):
        flag = True
        self.new_list = []
        unique_bp_list = self.remove_duplicates(input_list)
        for unique_bp in unique_bp_list:
            list_same_element = []
            list_same_element = list_same_element + unique_bp
            unique_bp_list1 = unique_bp_list.copy()
            unique_bp_list1.remove(unique_bp)
            for bp in unique_bp:
                for unique_bp1 in unique_bp_list1:
                    if bp in unique_bp1:
                        list_same_element = list_same_element + unique_bp1
                        flag = False
            list_same_element1 = self.remove_duplicates(list_same_element)
            list_same_element1.sort()
            self.new_list.append(list_same_element1)
        if not flag:
            self.make_list_same_element(self.new_list)

    def add_element_in_list(self, dict_conts):
        final_list = []
        for elements in self.new_list:
            sum_x = 0
            sum_y = 0
            sum_area = 0
            sum_length = 0
            list_cont = []
            for ele in elements:
                sum_x += ele[0]
                sum_y += ele[1]
                sum_area += ele[2]
                sum_length += ele[4]
                list_cont.append(dict_conts[str(ele[3])])
            x = int(sum_x/len(elements))
            y = int(sum_y/len(elements))
            area = sum_area
            length = sum_length
            cont = np.concatenate(tuple(list_cont), axis=0)
            final_list.append([x, y, area, length, cont])
        return final_list

    def Analysis_Result(self, color, category, n, n1, n_p, n_l, n_r, list_detect, dict_conts, msg, Analysis_path_log, debug_path_log, Analysis_point_path_log, Analysis_line_path_log, Analysis_region_path_log, image, image2):
        detect_flag = False
        self.SaveLogs(Analysis_path_log,
                      '------------------------------%s-----------------------------' %category)
        self.SaveLogs(debug_path_log,
                      '------------------------------%s-----------------------------' %category)
        self.SaveLogs(Analysis_point_path_log,
                      '------------------------------%s-----------------------------' %category)
        self.SaveLogs(Analysis_line_path_log,
                      '------------------------------%s-----------------------------' %category)
        self.SaveLogs(Analysis_region_path_log,
                      '------------------------------%s-----------------------------' %category)
        self.SaveLogs(Analysis_path_log,
                      'Exception: %s' % msg)
        if list_detect:

            if category == 'Detect Black Point':
                SEPARATE_POINT_W_L = self.SEPARATE_POINT['LOWER'][0] - 4
                SEPARATE_POINT_H_L = self.SEPARATE_POINT['LOWER'][1] - 4
                SEPARATE_POINT_W_U = self.SEPARATE_POINT['UPPER'][0] - 4
                SEPARATE_POINT_H_U = self.SEPARATE_POINT['UPPER'][1] - 4

                SEPARATE_LINE_W_L = self.SEPARATE_LINE['LOWER'][0] - 4
                SEPARATE_LINE_H_L = self.SEPARATE_LINE['LOWER'][1] - 4
                SEPARATE_LINE_W_U = self.SEPARATE_LINE['UPPER'][0] - 4
                SEPARATE_LINE_H_U = self.SEPARATE_LINE['UPPER'][1] - 4

                SEPARATE_REGION_W_L = self.SEPARATE_REGION['LOWER'][0] - 4
                SEPARATE_REGION_H_L = self.SEPARATE_REGION['LOWER'][1] - 4
                SEPARATE_REGION_W_U = self.SEPARATE_REGION['UPPER'][0] - 4
                SEPARATE_REGION_H_U = self.SEPARATE_REGION['UPPER'][1] - 4
            else:
                SEPARATE_POINT_W_L = self.SEPARATE_POINT['LOWER'][0]
                SEPARATE_POINT_H_L = self.SEPARATE_POINT['LOWER'][1]
                SEPARATE_POINT_W_U = self.SEPARATE_POINT['UPPER'][0]
                SEPARATE_POINT_H_U = self.SEPARATE_POINT['UPPER'][1]

                SEPARATE_LINE_W_L = self.SEPARATE_LINE['LOWER'][0]
                SEPARATE_LINE_H_L = self.SEPARATE_LINE['LOWER'][1]
                SEPARATE_LINE_W_U = self.SEPARATE_LINE['UPPER'][0]
                SEPARATE_LINE_H_U = self.SEPARATE_LINE['UPPER'][1]

                SEPARATE_REGION_W_L = self.SEPARATE_REGION['LOWER'][0]
                SEPARATE_REGION_H_L = self.SEPARATE_REGION['LOWER'][1]
                SEPARATE_REGION_W_U = self.SEPARATE_REGION['UPPER'][0]
                SEPARATE_REGION_H_U = self.SEPARATE_REGION['UPPER'][1]

            if color == 'white':
                EXPECTED_REGION = self.EXPECTED_WHITE
            elif color == 'black':
                EXPECTED_REGION = self.EXPECTED_BLACK
            elif color == 'red':
                EXPECTED_REGION = self.EXPECTED_RED
            elif color == 'blue':
                EXPECTED_REGION = self.EXPECTED_BLUE
            else: #green
                EXPECTED_REGION = self.EXPECTED_GREEN

            listAllBlackBPNearly = self.merge_bad_points(list_detect)
            self.make_list_same_element(listAllBlackBPNearly)
            final_list = self.add_element_in_list(dict_conts)
            for element in final_list:
                n1 += 1
                x, y, w, h = cv2.boundingRect(element[4])

                self.SaveLogs(debug_path_log,
                              '%s, %s, %s, %s, %s, %s, %s' % (
                              str(n1), str(x), str(y), str(w), str(h), str(element[3]), str(element[2])))
                cv2.rectangle(image2, (x - 20, y - 20), (x + w + 20, y + h + 20), (255, 255, 0), 4)
                cv2.putText(image2, str(n1), (x + w + 30, y), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 125, 255), 2,
                            cv2.LINE_AA)
                self.SaveLogs(debug_path_log,
                              '-----------------------------------------------------------')

                if w >= SEPARATE_POINT_W_L and h >= SEPARATE_POINT_H_L:
                    flagExpected = False
                    for region in EXPECTED_REGION:
                        if (element[0] in range(region[0][0]-region[1][0], region[0][0]+region[1][0]) and
                                element[1] in range(region[0][1] - region[1][1], region[0][1] + region[1][1])):
                            if w <= region[1][0]*2 and h <= region[1][1]*2:
                                flagExpected = True
                                break
                    if flagExpected:
                        continue
                    else:
                        pass
                    detect_flag = True
                    n += 1
                    self.SaveLogs(Analysis_path_log, '%s, %s, %s, %s, %s, %s, %s' % (
                    str(n), str(x), str(y), str(w), str(h), str(element[3]), str(element[2])))
                    cv2.rectangle(image, (x - 20, y - 20), (x + w + 20, y + h + 20), (255, 255, 0), 4)
                    cv2.putText(image, str(n), (x + w + 30, y), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 125, 255), 2,
                                cv2.LINE_AA)
                    self.SaveLogs(Analysis_path_log,
                                  '-----------------------------------------------------------')


                    w1 = min(w,h)
                    h1 = max(w,h)

                    if SEPARATE_POINT_W_L<=w1<=SEPARATE_POINT_W_U and SEPARATE_POINT_H_L<=h1<=SEPARATE_POINT_H_U:
                        n_p += 1
                        self.SaveLogs(Analysis_point_path_log, '%s, %s, %s, %s, %s, %s, %s' % (
                            str(n), str(x), str(y), str(w), str(h), str(element[3]), str(element[2])))
                        self.SaveLogs(Analysis_point_path_log,
                                      '-----------------------------------------------------------')
                    elif SEPARATE_LINE_W_L<w1<=SEPARATE_LINE_W_U and SEPARATE_LINE_H_L<h1<=SEPARATE_LINE_H_U:
                        n_l += 1
                        self.SaveLogs(Analysis_line_path_log, '%s, %s, %s, %s, %s, %s, %s' % (
                            str(n), str(x), str(y), str(w), str(h), str(element[3]), str(element[2])))
                        self.SaveLogs(Analysis_line_path_log,
                                      '-----------------------------------------------------------')
                    elif SEPARATE_REGION_W_L < w1 <= SEPARATE_REGION_W_U and SEPARATE_REGION_H_L < h1 <= SEPARATE_REGION_H_U:
                        n_r += 1
                        self.SaveLogs(Analysis_region_path_log, '%s, %s, %s, %s, %s, %s, %s' % (
                            str(n), str(x), str(y), str(w), str(h), str(element[3]), str(element[2])))
                        self.SaveLogs(Analysis_region_path_log,
                                      '-----------------------------------------------------------')
        return detect_flag, n, n1, n_p, n_l, n_r, image, image2

    def Red_Analysis(self, pathImage):
        result = True
        Analysis_path_log = '%s/Analysis.log' %self.red_result_save_dir
        debug_path_log = '%s/debug.log' %self.red_result_save_dir
        Result_path_log = '%s/Result.log' %self.red_result_save_dir


        Point_path_folder = '%s/Point' %self.red_result_save_dir
        Line_path_folder = '%s/Line' %self.red_result_save_dir
        Region_path_folder = '%s/Region' %self.red_result_save_dir

        Point_path_log = '%s/Analysis.log' % Point_path_folder
        Line_path_log = '%s/Analysis.log' % Line_path_folder
        Region_path_log = '%s/Analysis.log' % Region_path_folder

        if not os.path.isdir(Point_path_folder):
            os.makedirs(Point_path_folder)
        if not os.path.isdir(Line_path_folder):
            os.makedirs(Line_path_folder)
        if not os.path.isdir(Region_path_folder):
            os.makedirs(Region_path_folder)

        try:
            self.SaveLogs(Analysis_path_log,pathImage)
            image = cv2.imread(pathImage)
            image1 = image.copy()
            image2 = image.copy()
            self.SaveLogs(Analysis_path_log,'------------------------------Separation Enviroment-----------------------------')
            result_separation_env_image, image_filter, separation_env_image, separation_env_image_full, approx_filter, msg_1 = self.Separation_Env('Red', image, self.SEPARATION_ENV_RED['HSV_RANGE_1'],
                                                       self.SEPARATION_ENV_RED['CONTRAST'],
                                                       self.SEPARATION_ENV_RED['CLAHE'],
                                                       self.SEPARATION_ENV_RED['GAUSSIAN_BLUR'],
                                                       self.SEPARATION_ENV_RED['THRESHOLD_1'],
                                                       self.SEPARATION_ENV_RED['HSV_RANGE_2'],
                                                       self.SEPARATION_ENV_RED['THRESHOLD_2'],
                                                       self.SEPARATION_ENV_RED['ADDWEIGHT'])
            self.SaveLogs(Analysis_path_log,'Exception: %s' %msg_1)
            if result_separation_env_image:
                result_detect_black_point, msg_2, list_detect_black_point, dict_black_conts, image_drawcontours = self.Detect_black_point('Red', separation_env_image_full, image1, approx_filter,
                                                                          self.DETECT_BLACK_POINT_RED['SIGMA'],
                                                                          self.DETECT_BLACK_POINT_RED['RTN'],
                                                                          self.DETECT_BLACK_POINT_RED['CLAHE'],
                                                                          self.DETECT_BLACK_POINT_RED['MEDIAN_BLUR'],
                                                                          self.DETECT_BLACK_POINT_RED['GAUSSIAN_BLUR'],
                                                                          self.DETECT_BLACK_POINT_RED['BORDER_THICKNESS'],
                                                                          self.DETECT_BLACK_POINT_RED['THRESHOLD'],
                                                                          self.DETECT_BLACK_POINT_RED['DILATE_KERNEL'],
                                                                          self.DETECT_BLACK_POINT_RED['ERODE_KERNEL'],
                                                                          self.DETECT_BLACK_POINT_RED['CANNY'])
                result_detect_white_point, msg_3, list_detect_white_point, dict_white_conts, image_drawcontours = self.Detect_white_point('Red', separation_env_image, image_drawcontours,
                                                                          self.DETECT_WHITE_POINT_RED['BORDER_THICKNESS'],
                                                                          self.DETECT_WHITE_POINT_RED['THRESHOLD'],
                                                                          self.DETECT_WHITE_POINT_RED['DILATE_KERNEL'],
                                                                          self.DETECT_WHITE_POINT_RED['ERODE_KERNEL'],
                                                                          self.DETECT_WHITE_POINT_RED['GAUSSIAN_BLUR'],
                                                                          self.DETECT_WHITE_POINT_RED['CANNY'])
                result_detect_leakage_mura, msg_4, list_detect_leakage_mura, dict_leakage_mura_conts, image_drawcontours = self.Detect_leakage_mura_color('Red', image_filter, image_drawcontours, approx_filter,
                                                                            self.DETECT_LEAKAGE_MURA_RED['CLAHE'],
                                                                            self.DETECT_LEAKAGE_MURA_RED['GAUSSIAN_BLUR'],
                                                                            self.DETECT_LEAKAGE_MURA_RED['BORDER_THICKNESS'],
                                                                            self.DETECT_LEAKAGE_MURA_RED['THRESHOLD_LEAKAGE_MURA'])
                n = 0
                n1 = 0
                n_p = 0
                n_l = 0
                n_r = 0
                detect_black_flag, n, n1, n_p, n_l, n_r, image, image2 = self.Analysis_Result('red', 'Detect Black Point', n, n1, n_p,
                n_l, n_r, list_detect_black_point, dict_black_conts, msg_2, Analysis_path_log, debug_path_log, Point_path_log,
                Line_path_log, Region_path_log, image, image2)

                detect_white_flag, n, n1, n_p, n_l, n_r, image, image2 = self.Analysis_Result('red',
                    'Detect White Point', n, n1, n_p,
                    n_l, n_r, list_detect_white_point, dict_white_conts, msg_3, Analysis_path_log, debug_path_log,
                    Point_path_log,
                    Line_path_log, Region_path_log, image, image2)

                detect_leakage_mura_flag, n, n1, n_p, n_l, n_r, image, image2 = self.Analysis_Result('red',
                                                                                                     'Detect Leakage Mura',
                                                                                                     n, n1, n_p,
                                                                                                     n_l, n_r,
                                                                                                     list_detect_leakage_mura,
                                                                                                     dict_leakage_mura_conts,
                                                                                                     msg_4,
                                                                                                     Analysis_path_log,
                                                                                                     debug_path_log,
                                                                                                     Point_path_log,
                                                                                                     Line_path_log,
                                                                                                     Region_path_log,
                                                                                                     image,
                                                                                                     image2)

                with open(os.path.join(Point_path_folder, 'Count.log'), 'w') as c_p_f:
                    c_p_f.writelines(str(n_p))
                with open(os.path.join(Line_path_folder, 'Count.log'), 'w') as c_l_f:
                    c_l_f.writelines(str(n_l))
                with open(os.path.join(Region_path_folder, 'Count.log'), 'w') as c_r_f:
                    c_r_f.writelines(str(n_r))
                cv2.imwrite(os.path.join(self.red_result_save_dir, 'analysis_image.png'), image)
                cv2.imwrite(os.path.join(self.red_result_save_dir, 'debug.png'), image2)
                cv2.imwrite(os.path.join(self.red_result_save_dir, 'analysis_image_drawContours.png'), image_drawcontours)
            else:
                result = False
                self.SaveLogs(Analysis_path_log,
                              'Image environment separator appears exception')
            if not result_detect_black_point:
                result = False
                self.SaveLogs(Analysis_path_log,
                              'Image detect black point appears exception')
            if not result_detect_white_point:
                result = False
                self.SaveLogs(Analysis_path_log,
                              'Image detect white point appears exception')
            if not result_detect_leakage_mura:
                result = False
                self.SaveLogs(Analysis_path_log,
                              'Image detect leakage mura appears exception')
            if detect_black_flag:
                result = False
                self.SaveLogs(Analysis_path_log,
                              'Image detect black point appears NG points')
            if detect_white_flag:
                result = False
                self.SaveLogs(Analysis_path_log,
                              'Image detect white point appears NG points')
            if detect_leakage_mura_flag:
                result = False
                self.SaveLogs(Analysis_path_log,
                              'Image detect leakage mura appears NG points')
        except Exception as e:
            self.SaveLogs(Analysis_path_log,
                          'Exception: %s' %str(e))
            result = False
        if result:
            self.SaveLogs(Analysis_path_log,
                          'Red image analysis PASS')
        else:
            self.SaveLogs(Analysis_path_log,
                          'Red image analysis FAIL')
        with open(Result_path_log, 'w') as resultFile:
            if result:
                resultFile.writelines('PASS')
            else:
                resultFile.writelines('FAIL')

    def Blue_Analysis(self, pathImage):
        result = True
        Analysis_path_log = '%s/Analysis.log' %self.blue_result_save_dir
        debug_path_log = '%s/debug.log' %self.blue_result_save_dir
        Result_path_log = '%s/Result.log' %self.blue_result_save_dir

        Point_path_folder = '%s/Point' %self.blue_result_save_dir
        Line_path_folder = '%s/Line' %self.blue_result_save_dir
        Region_path_folder = '%s/Region' %self.blue_result_save_dir

        Point_path_log = '%s/Analysis.log' % Point_path_folder
        Line_path_log = '%s/Analysis.log' % Line_path_folder
        Region_path_log = '%s/Analysis.log' % Region_path_folder

        if not os.path.isdir(Point_path_folder):
            os.makedirs(Point_path_folder)
        if not os.path.isdir(Line_path_folder):
            os.makedirs(Line_path_folder)
        if not os.path.isdir(Region_path_folder):
            os.makedirs(Region_path_folder)
        try:
            self.SaveLogs(Analysis_path_log,pathImage)
            image = cv2.imread(pathImage)
            image1 = image.copy()
            image2 = image.copy()
            self.SaveLogs(Analysis_path_log,'------------------------------Separation Enviroment-----------------------------')
            result_separation_env_image, image_filter, separation_env_image, separation_env_image_full, approx_filter, msg_1 = self.Separation_Env('Blue', image, self.SEPARATION_ENV_BLUE['HSV_RANGE_1'],
                                                       self.SEPARATION_ENV_BLUE['CONTRAST'],
                                                       self.SEPARATION_ENV_BLUE['CLAHE'],
                                                       self.SEPARATION_ENV_BLUE['GAUSSIAN_BLUR'],
                                                       self.SEPARATION_ENV_BLUE['THRESHOLD_1'],
                                                       self.SEPARATION_ENV_BLUE['HSV_RANGE_2'],
                                                       self.SEPARATION_ENV_BLUE['THRESHOLD_2'],
                                                       self.SEPARATION_ENV_BLUE['ADDWEIGHT'])
            self.SaveLogs(Analysis_path_log,'Exception: %s' %msg_1)
            if result_separation_env_image:
                result_detect_black_point, msg_2, list_detect_black_point, dict_black_conts, image_drawcontours = self.Detect_black_point('Blue', separation_env_image_full, image1, approx_filter,
                                                                          self.DETECT_BLACK_POINT_BLUE['SIGMA'],
                                                                          self.DETECT_BLACK_POINT_BLUE['RTN'],
                                                                          self.DETECT_BLACK_POINT_BLUE['CLAHE'],
                                                                          self.DETECT_BLACK_POINT_BLUE['MEDIAN_BLUR'],
                                                                          self.DETECT_BLACK_POINT_BLUE['GAUSSIAN_BLUR'],
                                                                          self.DETECT_BLACK_POINT_BLUE['BORDER_THICKNESS'],
                                                                          self.DETECT_BLACK_POINT_BLUE['THRESHOLD'],
                                                                          self.DETECT_BLACK_POINT_BLUE['DILATE_KERNEL'],
                                                                          self.DETECT_BLACK_POINT_BLUE['ERODE_KERNEL'],
                                                                          self.DETECT_BLACK_POINT_BLUE['CANNY'])
                result_detect_white_point, msg_3, list_detect_white_point, dict_white_conts, image_drawcontours = self.Detect_white_point('Blue', separation_env_image, image_drawcontours,
                                                                          self.DETECT_WHITE_POINT_BLUE['BORDER_THICKNESS'],
                                                                          self.DETECT_WHITE_POINT_BLUE['THRESHOLD'],
                                                                          self.DETECT_WHITE_POINT_BLUE['DILATE_KERNEL'],
                                                                          self.DETECT_WHITE_POINT_BLUE['ERODE_KERNEL'],
                                                                          self.DETECT_WHITE_POINT_BLUE['GAUSSIAN_BLUR'],
                                                                          self.DETECT_WHITE_POINT_BLUE['CANNY'])
                result_detect_leakage_mura, msg_4, list_detect_leakage_mura, dict_leakage_mura_conts, image_drawcontours = self.Detect_leakage_mura_color('Blue', image_filter, image_drawcontours,approx_filter,
                                                                            self.DETECT_LEAKAGE_MURA_BLUE['CLAHE'],
                                                                            self.DETECT_LEAKAGE_MURA_BLUE['GAUSSIAN_BLUR'],
                                                                            self.DETECT_LEAKAGE_MURA_BLUE['BORDER_THICKNESS'],
                                                                            self.DETECT_LEAKAGE_MURA_BLUE['THRESHOLD_LEAKAGE_MURA'])
                n = 0
                n1 = 0
                n_p = 0
                n_l = 0
                n_r = 0
                detect_black_flag, n, n1, n_p, n_l, n_r, image, image2 = self.Analysis_Result('blue',
                    'Detect Black Point', n, n1, n_p,
                    n_l, n_r, list_detect_black_point, dict_black_conts, msg_2, Analysis_path_log, debug_path_log,
                    Point_path_log,
                    Line_path_log, Region_path_log, image, image2)

                detect_white_flag, n, n1, n_p, n_l, n_r, image, image2 = self.Analysis_Result('blue',
                    'Detect White Point', n, n1, n_p,
                    n_l, n_r, list_detect_white_point, dict_white_conts, msg_3, Analysis_path_log, debug_path_log,
                    Point_path_log,
                    Line_path_log, Region_path_log, image, image2)

                detect_leakage_mura_flag, n, n1, n_p, n_l, n_r, image, image2 = self.Analysis_Result('blue',
                                                                                                     'Detect Leakage Mura',
                                                                                                     n, n1, n_p,
                                                                                                     n_l, n_r,
                                                                                                     list_detect_leakage_mura,
                                                                                                     dict_leakage_mura_conts,
                                                                                                     msg_4,
                                                                                                     Analysis_path_log,
                                                                                                     debug_path_log,
                                                                                                     Point_path_log,
                                                                                                     Line_path_log,
                                                                                                     Region_path_log,
                                                                                                     image,
                                                                                                     image2)

                with open(os.path.join(Point_path_folder, 'Count.log'), 'w') as c_p_f:
                    c_p_f.writelines(str(n_p))
                with open(os.path.join(Line_path_folder, 'Count.log'), 'w') as c_l_f:
                    c_l_f.writelines(str(n_l))
                with open(os.path.join(Region_path_folder, 'Count.log'), 'w') as c_r_f:
                    c_r_f.writelines(str(n_r))
                cv2.imwrite(os.path.join(self.blue_result_save_dir, 'analysis_image.png'), image)
                cv2.imwrite(os.path.join(self.blue_result_save_dir, 'debug.png'), image2)
                cv2.imwrite(os.path.join(self.blue_result_save_dir, 'analysis_image_drawContours.png'), image_drawcontours)
            else:
                result = False
                self.SaveLogs(Analysis_path_log,
                              'Image environment separator appears exception')
            if not result_detect_black_point:
                result = False
                self.SaveLogs(Analysis_path_log,
                              'Image detect black point appears exception')
            if not result_detect_white_point:
                result = False
                self.SaveLogs(Analysis_path_log,
                              'Image detect white point appears exception')
            if not result_detect_leakage_mura:
                result = False
                self.SaveLogs(Analysis_path_log,
                              'Image detect leakage mura appears exception')
            if detect_black_flag:
                result = False
                self.SaveLogs(Analysis_path_log,
                              'Image detect black point appears NG points')
            if detect_white_flag:
                result = False
                self.SaveLogs(Analysis_path_log,
                              'Image detect white point appears NG points')
            if detect_leakage_mura_flag:
                result = False
                self.SaveLogs(Analysis_path_log,
                              'Image detect leakage mura appears NG points')
        except Exception as e:
            self.SaveLogs(Analysis_path_log,
                          'Exception: %s' %str(e))
            result = False
        if result:
            self.SaveLogs(Analysis_path_log,
                          'Blue image analysis PASS')
        else:
            self.SaveLogs(Analysis_path_log,
                          'Blue image analysis FAIL')
        with open(Result_path_log, 'w') as resultFile:
            if result:
                resultFile.writelines('PASS')
            else:
                resultFile.writelines('FAIL')

    def Green_Analysis(self, pathImage):
        result = True
        Analysis_path_log = '%s/Analysis.log' %self.green_result_save_dir
        debug_path_log = '%s/debug.log' %self.green_result_save_dir
        Result_path_log = '%s/Result.log' %self.green_result_save_dir

        Point_path_folder = '%s/Point' %self.green_result_save_dir
        Line_path_folder = '%s/Line' %self.green_result_save_dir
        Region_path_folder = '%s/Region' %self.green_result_save_dir

        Point_path_log = '%s/Analysis.log' % Point_path_folder
        Line_path_log = '%s/Analysis.log' % Line_path_folder
        Region_path_log = '%s/Analysis.log' % Region_path_folder

        if not os.path.isdir(Point_path_folder):
            os.makedirs(Point_path_folder)
        if not os.path.isdir(Line_path_folder):
            os.makedirs(Line_path_folder)
        if not os.path.isdir(Region_path_folder):
            os.makedirs(Region_path_folder)
        try:
            self.SaveLogs(Analysis_path_log,pathImage)
            image = cv2.imread(pathImage)
            image1 = image.copy()
            image2 = image.copy()
            self.SaveLogs(Analysis_path_log,'------------------------------Separation Enviroment-----------------------------')
            result_separation_env_image, image_filter, separation_env_image, separation_env_image_full, approx_filter, msg_1 = self.Separation_Env('Green', image, self.SEPARATION_ENV_GREEN['HSV_RANGE_1'],
                                                       self.SEPARATION_ENV_GREEN['CONTRAST'],
                                                       self.SEPARATION_ENV_GREEN['CLAHE'],
                                                       self.SEPARATION_ENV_GREEN['GAUSSIAN_BLUR'],
                                                       self.SEPARATION_ENV_GREEN['THRESHOLD_1'],
                                                       self.SEPARATION_ENV_GREEN['HSV_RANGE_2'],
                                                       self.SEPARATION_ENV_GREEN['THRESHOLD_2'],
                                                       self.SEPARATION_ENV_GREEN['ADDWEIGHT'])
            self.SaveLogs(Analysis_path_log,'Exception: %s' %msg_1)
            if result_separation_env_image:
                result_detect_black_point, msg_2, list_detect_black_point, dict_black_conts, image_drawcontours = self.Detect_black_point('Green', separation_env_image_full, image1, approx_filter,
                                                                          self.DETECT_BLACK_POINT_GREEN['SIGMA'],
                                                                          self.DETECT_BLACK_POINT_GREEN['RTN'],
                                                                          self.DETECT_BLACK_POINT_GREEN['CLAHE'],
                                                                          self.DETECT_BLACK_POINT_GREEN['MEDIAN_BLUR'],
                                                                          self.DETECT_BLACK_POINT_GREEN['GAUSSIAN_BLUR'],
                                                                          self.DETECT_BLACK_POINT_GREEN['BORDER_THICKNESS'],
                                                                          self.DETECT_BLACK_POINT_GREEN['THRESHOLD'],
                                                                          self.DETECT_BLACK_POINT_GREEN['DILATE_KERNEL'],
                                                                          self.DETECT_BLACK_POINT_GREEN['ERODE_KERNEL'],
                                                                          self.DETECT_BLACK_POINT_GREEN['CANNY'])
                result_detect_white_point, msg_3, list_detect_white_point, dict_white_conts, image_drawcontours = self.Detect_white_point('Green', separation_env_image, image_drawcontours,
                                                                          self.DETECT_WHITE_POINT_GREEN['BORDER_THICKNESS'],
                                                                          self.DETECT_WHITE_POINT_GREEN['THRESHOLD'],
                                                                          self.DETECT_WHITE_POINT_GREEN['DILATE_KERNEL'],
                                                                          self.DETECT_WHITE_POINT_GREEN['ERODE_KERNEL'],
                                                                          self.DETECT_WHITE_POINT_GREEN['GAUSSIAN_BLUR'],
                                                                          self.DETECT_WHITE_POINT_GREEN['CANNY'])
                result_detect_leakage_mura, msg_4, list_detect_leakage_mura, dict_leakage_mura_conts, image_drawcontours = self.Detect_leakage_mura_color('Green', image_filter, image_drawcontours, approx_filter,
                                                                            self.DETECT_LEAKAGE_MURA_GREEN['CLAHE'],
                                                                            self.DETECT_LEAKAGE_MURA_GREEN['GAUSSIAN_BLUR'],
                                                                            self.DETECT_LEAKAGE_MURA_GREEN['BORDER_THICKNESS'],
                                                                            self.DETECT_LEAKAGE_MURA_GREEN['THRESHOLD_LEAKAGE_MURA'])
                n = 0
                n1 = 0
                n_p = 0
                n_l = 0
                n_r = 0
                detect_black_flag, n, n1, n_p, n_l, n_r, image, image2 = self.Analysis_Result('green',
                    'Detect Black Point', n, n1, n_p,
                    n_l, n_r, list_detect_black_point, dict_black_conts, msg_2, Analysis_path_log, debug_path_log,
                    Point_path_log,
                    Line_path_log, Region_path_log, image, image2)

                detect_white_flag, n, n1, n_p, n_l, n_r, image, image2 = self.Analysis_Result('green',
                    'Detect White Point', n, n1, n_p,
                    n_l, n_r, list_detect_white_point, dict_white_conts, msg_3, Analysis_path_log, debug_path_log,
                    Point_path_log,
                    Line_path_log, Region_path_log, image, image2)

                detect_leakage_mura_flag, n, n1, n_p, n_l, n_r, image, image2 = self.Analysis_Result('green',
                                                                                                     'Detect Leakage Mura',
                                                                                                     n, n1, n_p,
                                                                                                     n_l, n_r,
                                                                                                     list_detect_leakage_mura,
                                                                                                     dict_leakage_mura_conts,
                                                                                                     msg_4,
                                                                                                     Analysis_path_log,
                                                                                                     debug_path_log,
                                                                                                     Point_path_log,
                                                                                                     Line_path_log,
                                                                                                     Region_path_log,
                                                                                                     image,
                                                                                                     image2)

                with open(os.path.join(Point_path_folder, 'Count.log'), 'w') as c_p_f:
                    c_p_f.writelines(str(n_p))
                with open(os.path.join(Line_path_folder, 'Count.log'), 'w') as c_l_f:
                    c_l_f.writelines(str(n_l))
                with open(os.path.join(Region_path_folder, 'Count.log'), 'w') as c_r_f:
                    c_r_f.writelines(str(n_r))
                cv2.imwrite(os.path.join(self.green_result_save_dir, 'analysis_image.png'), image)
                cv2.imwrite(os.path.join(self.green_result_save_dir, 'debug.png'), image2)
                cv2.imwrite(os.path.join(self.green_result_save_dir, 'analysis_image_drawContours.png'), image_drawcontours)
            else:
                result = False
                self.SaveLogs(Analysis_path_log,
                              'Image environment separator appears exception')
            if not result_detect_black_point:
                result = False
                self.SaveLogs(Analysis_path_log,
                              'Image detect black point appears exception')
            if not result_detect_white_point:
                result = False
                self.SaveLogs(Analysis_path_log,
                              'Image detect white point appears exception')
            if not result_detect_leakage_mura:
                result = False
                self.SaveLogs(Analysis_path_log,
                              'Image detect leakage mura appears exception')
            if detect_black_flag:
                result = False
                self.SaveLogs(Analysis_path_log,
                              'Image detect black point appears NG points')
            if detect_white_flag:
                result = False
                self.SaveLogs(Analysis_path_log,
                              'Image detect white point appears NG points')
            if detect_leakage_mura_flag:
                result = False
                self.SaveLogs(Analysis_path_log,
                              'Image detect leakage mura appears NG points')
        except Exception as e:
            self.SaveLogs(Analysis_path_log,
                          'Exception: %s' %str(e))
            result = False
        if result:
            self.SaveLogs(Analysis_path_log,
                          'Green image analysis PASS')
        else:
            self.SaveLogs(Analysis_path_log,
                          'Green image analysis FAIL')
        with open(Result_path_log, 'w') as resultFile:
            if result:
                resultFile.writelines('PASS')
            else:
                resultFile.writelines('FAIL')

    def White_Analysis(self, pathImage):
        result = True
        Analysis_path_log = '%s/Analysis.log' %self.white_result_save_dir
        debug_path_log = '%s/debug.log' %self.white_result_save_dir
        Result_path_log = '%s/Result.log' %self.white_result_save_dir

        Point_path_folder = '%s/Point' %self.white_result_save_dir
        Line_path_folder = '%s/Line' %self.white_result_save_dir
        Region_path_folder = '%s/Region' %self.white_result_save_dir

        Point_path_log = '%s/Analysis.log' % Point_path_folder
        Line_path_log = '%s/Analysis.log' % Line_path_folder
        Region_path_log = '%s/Analysis.log' % Region_path_folder

        if not os.path.isdir(Point_path_folder):
            os.makedirs(Point_path_folder)
        if not os.path.isdir(Line_path_folder):
            os.makedirs(Line_path_folder)
        if not os.path.isdir(Region_path_folder):
            os.makedirs(Region_path_folder)
        try:
            self.SaveLogs(Analysis_path_log,pathImage)
            image = cv2.imread(pathImage)
            image1 = image.copy()
            image2 = image.copy()
            self.SaveLogs(Analysis_path_log,'------------------------------Separation Enviroment-----------------------------')
            result_separation_env_image, image_filter, separation_env_image, separation_env_image_full, approx_filter, msg_1 = self.Separation_Env('White', image, self.SEPARATION_ENV_WHITE['HSV_RANGE_1'],
                                                       self.SEPARATION_ENV_WHITE['CONTRAST'],
                                                       self.SEPARATION_ENV_WHITE['CLAHE'],
                                                       self.SEPARATION_ENV_WHITE['GAUSSIAN_BLUR'],
                                                       self.SEPARATION_ENV_WHITE['THRESHOLD_1'],
                                                       self.SEPARATION_ENV_WHITE['HSV_RANGE_2'],
                                                       self.SEPARATION_ENV_WHITE['THRESHOLD_2'],
                                                       self.SEPARATION_ENV_WHITE['ADDWEIGHT'])
            self.SaveLogs(Analysis_path_log,'Exception: %s' %msg_1)
            if result_separation_env_image:
                result_detect_black_point, msg_2, list_detect_black_point, dict_black_conts, image_drawcontours = self.Detect_black_point('White', separation_env_image_full, image1, approx_filter,
                                                                          self.DETECT_BLACK_POINT_WHITE['SIGMA'],
                                                                          self.DETECT_BLACK_POINT_WHITE['RTN'],
                                                                          self.DETECT_BLACK_POINT_WHITE['CLAHE'],
                                                                          self.DETECT_BLACK_POINT_WHITE['MEDIAN_BLUR'],
                                                                          self.DETECT_BLACK_POINT_WHITE['GAUSSIAN_BLUR'],
                                                                          self.DETECT_BLACK_POINT_WHITE['BORDER_THICKNESS'],
                                                                          self.DETECT_BLACK_POINT_WHITE['THRESHOLD'],
                                                                          self.DETECT_BLACK_POINT_WHITE['DILATE_KERNEL'],
                                                                          self.DETECT_BLACK_POINT_WHITE['ERODE_KERNEL'],
                                                                          self.DETECT_BLACK_POINT_WHITE['CANNY'])
                result_detect_white_point, msg_3, list_detect_white_point, dict_white_conts, image_drawcontours = self.Detect_white_point('White', separation_env_image, image_drawcontours,
                                                                          self.DETECT_WHITE_POINT_WHITE['BORDER_THICKNESS'],
                                                                          self.DETECT_WHITE_POINT_WHITE['THRESHOLD'],
                                                                          self.DETECT_WHITE_POINT_WHITE['DILATE_KERNEL'],
                                                                          self.DETECT_WHITE_POINT_WHITE['ERODE_KERNEL'],
                                                                          self.DETECT_WHITE_POINT_WHITE['GAUSSIAN_BLUR'],
                                                                          self.DETECT_WHITE_POINT_WHITE['CANNY'])
                result_detect_leakage_mura, msg_4, list_detect_leakage_mura, dict_leakage_mura_conts, image_drawcontours = self.Detect_leakage_mura_color('White', image_filter, image_drawcontours, approx_filter,
                                                                            self.DETECT_LEAKAGE_MURA_WHITE['CLAHE'],
                                                                            self.DETECT_LEAKAGE_MURA_WHITE['GAUSSIAN_BLUR'],
                                                                            self.DETECT_LEAKAGE_MURA_WHITE['BORDER_THICKNESS'],
                                                                            self.DETECT_LEAKAGE_MURA_WHITE['THRESHOLD_LEAKAGE_MURA'])
                n = 0
                n1 = 0
                n_p = 0
                n_l = 0
                n_r = 0
                detect_black_flag, n, n1, n_p, n_l, n_r, image, image2 = self.Analysis_Result('white',
                    'Detect Black Point', n, n1, n_p,
                    n_l, n_r, list_detect_black_point, dict_black_conts, msg_2, Analysis_path_log, debug_path_log,
                    Point_path_log,
                    Line_path_log, Region_path_log, image, image2)

                detect_white_flag, n, n1, n_p, n_l, n_r, image, image2 = self.Analysis_Result('white',
                    'Detect White Point', n, n1, n_p,
                    n_l, n_r, list_detect_white_point, dict_white_conts, msg_3, Analysis_path_log, debug_path_log,
                    Point_path_log,
                    Line_path_log, Region_path_log, image, image2)

                detect_leakage_mura_flag, n, n1, n_p, n_l, n_r, image, image2 = self.Analysis_Result('white',
                                                                                                     'Detect Leakage Mura',
                                                                                                     n, n1, n_p,
                                                                                                     n_l, n_r,
                                                                                                     list_detect_leakage_mura,
                                                                                                     dict_leakage_mura_conts,
                                                                                                     msg_4,
                                                                                                     Analysis_path_log,
                                                                                                     debug_path_log,
                                                                                                     Point_path_log,
                                                                                                     Line_path_log,
                                                                                                     Region_path_log,
                                                                                                     image,
                                                                                                     image2)

                with open(os.path.join(Point_path_folder, 'Count.log'), 'w') as c_p_f:
                    c_p_f.writelines(str(n_p))
                with open(os.path.join(Line_path_folder, 'Count.log'), 'w') as c_l_f:
                    c_l_f.writelines(str(n_l))
                with open(os.path.join(Region_path_folder, 'Count.log'), 'w') as c_r_f:
                    c_r_f.writelines(str(n_r))
                cv2.imwrite(os.path.join(self.white_result_save_dir, 'analysis_image.png'), image)
                cv2.imwrite(os.path.join(self.white_result_save_dir, 'debug.png'), image2)
                cv2.imwrite(os.path.join(self.white_result_save_dir, 'analysis_image_drawContours.png'), image_drawcontours)
            else:
                result = False
                self.SaveLogs(Analysis_path_log,
                              'Image environment separator appears exception')
            if not result_detect_black_point:
                result = False
                self.SaveLogs(Analysis_path_log,
                              'Image detect black point appears exception')
            if not result_detect_white_point:
                result = False
                self.SaveLogs(Analysis_path_log,
                              'Image detect white point appears exception')
            if not result_detect_leakage_mura:
                result = False
                self.SaveLogs(Analysis_path_log,
                              'Image detect leakage mura appears exception')
            if detect_black_flag:
                result = False
                self.SaveLogs(Analysis_path_log,
                              'Image detect black point appears NG points')
            if detect_white_flag:
                result = False
                self.SaveLogs(Analysis_path_log,
                              'Image detect white point appears NG points')
            if detect_leakage_mura_flag:
                result = False
                self.SaveLogs(Analysis_path_log,
                              'Image detect leakage mura appears NG points')
        except Exception as e:
            self.SaveLogs(Analysis_path_log,
                          'Exception: %s' %str(e))
            result = False
        if result:
            self.SaveLogs(Analysis_path_log,
                          'White image analysis PASS')
        else:
            self.SaveLogs(Analysis_path_log,
                          'White image analysis FAIL')
        with open(Result_path_log, 'w') as resultFile:
            if result:
                resultFile.writelines('PASS')
            else:
                resultFile.writelines('FAIL')

    def Black_Analysis(self, pathImage):
        result = True
        Analysis_path_log = '%s/Analysis.log' %self.black_result_save_dir
        debug_path_log = '%s/debug.log' %self.black_result_save_dir
        Result_path_log = '%s/Result.log' %self.black_result_save_dir
        Point_path_folder = '%s/Point' %self.black_result_save_dir
        Line_path_folder = '%s/Line' %self.black_result_save_dir
        Region_path_folder = '%s/Region' %self.black_result_save_dir

        Point_path_log = '%s/Analysis.log' % Point_path_folder
        Line_path_log = '%s/Analysis.log' % Line_path_folder
        Region_path_log = '%s/Analysis.log' % Region_path_folder

        if not os.path.isdir(Point_path_folder):
            os.makedirs(Point_path_folder)
        if not os.path.isdir(Line_path_folder):
            os.makedirs(Line_path_folder)
        if not os.path.isdir(Region_path_folder):
            os.makedirs(Region_path_folder)
        try:
            self.SaveLogs(Analysis_path_log,pathImage)
            image = cv2.imread(pathImage)
            image1 = image.copy()
            image2 = image.copy()
            self.SaveLogs(Analysis_path_log,'------------------------------Separation Enviroment-----------------------------')
            result_separation_env_image, image_filter, separation_env_image, separation_env_image_full, approx_filter, msg_1 = self.Separation_Env('Black', image, self.SEPARATION_ENV_BLACK['HSV_RANGE_1'],
                                                       self.SEPARATION_ENV_BLACK['CONTRAST'],
                                                       self.SEPARATION_ENV_BLACK['CLAHE'],
                                                       self.SEPARATION_ENV_BLACK['GAUSSIAN_BLUR'],
                                                       self.SEPARATION_ENV_BLACK['THRESHOLD_1'],
                                                       self.SEPARATION_ENV_BLACK['HSV_RANGE_2'],
                                                       self.SEPARATION_ENV_BLACK['THRESHOLD_2'],
                                                       self.SEPARATION_ENV_BLACK['ADDWEIGHT'])
            self.SaveLogs(Analysis_path_log,'Exception: %s' %msg_1)
            if result_separation_env_image:
                result_detect_black_point, msg_2, list_detect_black_point, dict_black_conts, image_drawcontours = self.Detect_black_point('Black', separation_env_image_full, image1, approx_filter,
                                                                          self.DETECT_BLACK_POINT_BLACK['SIGMA'],
                                                                          self.DETECT_BLACK_POINT_BLACK['RTN'],
                                                                          self.DETECT_BLACK_POINT_BLACK['CLAHE'],
                                                                          self.DETECT_BLACK_POINT_BLACK['MEDIAN_BLUR'],
                                                                          self.DETECT_BLACK_POINT_BLACK['GAUSSIAN_BLUR'],
                                                                          self.DETECT_BLACK_POINT_BLACK['BORDER_THICKNESS'],
                                                                          self.DETECT_BLACK_POINT_BLACK['THRESHOLD'],
                                                                          self.DETECT_BLACK_POINT_BLACK['DILATE_KERNEL'],
                                                                          self.DETECT_BLACK_POINT_BLACK['ERODE_KERNEL'],
                                                                          self.DETECT_BLACK_POINT_BLACK['CANNY'])
                result_detect_white_point, msg_3, list_detect_white_point, dict_white_conts, image_drawcontours = self.Detect_white_point('Black', separation_env_image, image_drawcontours,
                                                                          self.DETECT_WHITE_POINT_BLACK['BORDER_THICKNESS'],
                                                                          self.DETECT_WHITE_POINT_BLACK['THRESHOLD'],
                                                                          self.DETECT_WHITE_POINT_BLACK['DILATE_KERNEL'],
                                                                          self.DETECT_WHITE_POINT_BLACK['ERODE_KERNEL'],
                                                                          self.DETECT_WHITE_POINT_BLACK['GAUSSIAN_BLUR'],
                                                                          self.DETECT_WHITE_POINT_BLACK['CANNY'])
                result_detect_leakage_mura, msg_4, list_detect_leakage_mura, dict_leakage_mura_conts, image_drawcontours = self.Detect_leakage_mura_black('Black', separation_env_image, image_drawcontours,
                                                                          self.DETECT_LEAKAGE_MURA_BLACK['THRESHOLD'],
                                                                          self.DETECT_LEAKAGE_MURA_BLACK['DILATE_KERNEL'],
                                                                          self.DETECT_LEAKAGE_MURA_BLACK['ERODE_KERNEL'],
                                                                          self.DETECT_LEAKAGE_MURA_BLACK['GAUSSIAN_BLUR'],
                                                                          self.DETECT_LEAKAGE_MURA_BLACK['BORDER_THICKNESS'],
                                                                          self.DETECT_LEAKAGE_MURA_BLACK['THRESHOLD_LEAKAGE_MURA'],
                                                                          self.DETECT_LEAKAGE_MURA_BLACK['CANNY'])

                n = 0
                n1 = 0
                n_p = 0
                n_l = 0
                n_r = 0
                detect_black_flag, n, n1, n_p, n_l, n_r, image, image2 = self.Analysis_Result('black',
                    'Detect Black Point', n, n1, n_p,
                    n_l, n_r, list_detect_black_point, dict_black_conts, msg_2, Analysis_path_log, debug_path_log,
                    Point_path_log,
                    Line_path_log, Region_path_log, image, image2)

                detect_white_flag, n, n1, n_p, n_l, n_r, image, image2 = self.Analysis_Result('black',
                    'Detect White Point', n, n1, n_p,
                    n_l, n_r, list_detect_white_point, dict_white_conts, msg_3, Analysis_path_log, debug_path_log,
                    Point_path_log,
                    Line_path_log, Region_path_log, image, image2)
                detect_leakage_mura_flag, n, n1, n_p, n_l, n_r, image, image2 = self.Analysis_Result('black',
                    'Detect Leakage Mura', n, n1, n_p,
                    n_l, n_r, list_detect_leakage_mura, dict_leakage_mura_conts, msg_4, Analysis_path_log, debug_path_log,
                    Point_path_log,
                    Line_path_log, Region_path_log, image, image2)

                with open(os.path.join(Point_path_folder, 'Count.log'), 'w') as c_p_f:
                    c_p_f.writelines(str(n_p))
                with open(os.path.join(Line_path_folder, 'Count.log'), 'w') as c_l_f:
                    c_l_f.writelines(str(n_l))
                with open(os.path.join(Region_path_folder, 'Count.log'), 'w') as c_r_f:
                    c_r_f.writelines(str(n_r))
                cv2.imwrite(os.path.join(self.black_result_save_dir, 'analysis_image.png'), image)
                cv2.imwrite(os.path.join(self.black_result_save_dir, 'debug.png'), image2)
                cv2.imwrite(os.path.join(self.black_result_save_dir, 'analysis_image_drawContours.png'), image_drawcontours)
            else:
                result = False
                self.SaveLogs(Analysis_path_log,
                              'Image environment separator appears exception')
            if not result_detect_black_point:
                result = False
                self.SaveLogs(Analysis_path_log,
                              'Image detect black point appears exception')
            if not result_detect_white_point:
                result = False
                self.SaveLogs(Analysis_path_log,
                              'Image detect white point appears exception')
            if not result_detect_leakage_mura:
                result = False
                self.SaveLogs(Analysis_path_log,
                              'Image detect leakage mura appears exception')
            if detect_black_flag:
                result = False
                self.SaveLogs(Analysis_path_log,
                              'Image detect black point appears NG points')
            if detect_white_flag:
                result = False
                self.SaveLogs(Analysis_path_log,
                              'Image detect white point appears NG points')
            if detect_leakage_mura_flag:
                result = False
                self.SaveLogs(Analysis_path_log,
                              'Image detect leakage mura appears NG points')
        except Exception as e:
            self.SaveLogs(Analysis_path_log,
                          'Exception: %s' %str(e))
            result = False
        if result:
            self.SaveLogs(Analysis_path_log,
                          'Black image analysis PASS')
        else:
            self.SaveLogs(Analysis_path_log,
                          'Black image analysis FAIL')
        with open(Result_path_log, 'w') as resultFile:
            if result:
                resultFile.writelines('PASS')
            else:
                resultFile.writelines('FAIL')

    def TimeOut(self):
        while time.time()-self.start_time < self.CFG_TIMEOUT:
            if self.runFlag:
                break
            time.sleep(0.2)
        else:
            listThread = ['thread_red', 'thread_blue', 'thread_green', 'thread_white', 'thread_black']
            for thread in listThread:
                if hasattr(self, thread):
                    ctypes.pythonapi.PyThreadState_SetAsyncExc(getattr(self, thread).ident,
                                                               ctypes.py_object(SystemExit))
                    delattr(self, thread)
            self.timeoutFlag = True
    def Main(self):
        if self.path_analysis_color:
            color = os.path.splitext(os.path.basename(self.path_analysis_color))[0]
            self.start_time = time.time()
            self.runFlag = False
            self.timeoutFlag = False
            # result = True
            if color == 'red':
                self.thread_red = threading.Thread(target=self.Red_Analysis, args=(self.path_analysis_color,), daemon=True)
                self.thread_red.start()
            if color == 'blue':
                self.thread_blue = threading.Thread(target=self.Blue_Analysis, args=(self.path_analysis_color,), daemon=True)
                self.thread_blue.start()
            if color == 'green':
                self.thread_green = threading.Thread(target=self.Green_Analysis, args=(self.path_analysis_color,), daemon=True)
                self.thread_green.start()
            if color == 'white':
                self.thread_white = threading.Thread(target=self.White_Analysis, args=(self.path_analysis_color,), daemon=True)
                self.thread_white.start()
            if color == 'black':
                self.thread_black = threading.Thread(target=self.Black_Analysis, args=(self.path_analysis_color,), daemon=True)
                self.thread_black.start()
            threading.Thread(target=self.TimeOut, daemon=True).start()
            while 1:
                if color == 'red':
                    if os.path.isfile(os.path.join(self.red_result_save_dir, 'Result.log')) or self.timeoutFlag:
                        self.runFlag = True
                        break
                elif color == 'blue':
                    if os.path.isfile(os.path.join(self.blue_result_save_dir, 'Result.log')) or self.timeoutFlag:
                        self.runFlag = True
                        break
                elif color == 'green':
                    if os.path.isfile(os.path.join(self.green_result_save_dir, 'Result.log')) or self.timeoutFlag:
                        self.runFlag = True
                        break
                elif color == 'white':
                    if os.path.isfile(os.path.join(self.white_result_save_dir, 'Result.log')) or self.timeoutFlag:
                        self.runFlag = True
                        break
                elif color == 'black':
                    if os.path.isfile(os.path.join(self.black_result_save_dir, 'Result.log')) or self.timeoutFlag:
                        self.runFlag = True
                        break
                time.sleep(0.2)

            # if self.analysis_color.lower() == 'red' or self.analysis_color.lower() == 'all color':
            #     if os.path.isfile(os.path.join(self.red_result_save_dir, 'Result.log')):
            #         with open(os.path.join(self.red_result_save_dir, 'Result.log'), 'r') as file:
            #             content = file.read().strip()
            #         if 'FAIL' in content:
            #             result = False
            #             self.SaveLogs(self.total_analysis_log, 'Red image analysis was FAIL')
            #         else:
            #             self.SaveLogs(self.total_analysis_log, 'Red image analysis was PASS')
            #     else:
            #         result = False
            #
            # if self.analysis_color.lower() == 'blue' or self.analysis_color.lower() == 'all color':
            #
            #     if os.path.isfile(os.path.join(self.blue_result_save_dir, 'Result.log')):
            #         with open(os.path.join(self.blue_result_save_dir, 'Result.log'), 'r') as file:
            #             content = file.read().strip()
            #         if 'FAIL' in content:
            #             result = False
            #             self.SaveLogs(self.total_analysis_log, 'Blue image analysis was FAIL')
            #         else:
            #             self.SaveLogs(self.total_analysis_log, 'Blue image analysis was PASS')
            #     else:
            #         result = False
            #
            # if self.analysis_color.lower() == 'green' or self.analysis_color.lower() == 'all color':
            #
            #     if os.path.isfile(os.path.join(self.green_result_save_dir, 'Result.log')):
            #         with open(os.path.join(self.green_result_save_dir, 'Result.log'), 'r') as file:
            #             content = file.read().strip()
            #         if 'FAIL' in content:
            #             result = False
            #             self.SaveLogs(self.total_analysis_log, 'Green image analysis was FAIL')
            #         else:
            #             self.SaveLogs(self.total_analysis_log, 'Green image analysis was PASS')
            #     else:
            #         result = False
            #
            # if self.analysis_color.lower() == 'white' or self.analysis_color.lower() == 'all color':
            #     if os.path.isfile(os.path.join(self.white_result_save_dir, 'Result.log')):
            #         with open(os.path.join(self.white_result_save_dir, 'Result.log'), 'r') as file:
            #             content = file.read().strip()
            #         if 'FAIL' in content:
            #             result = False
            #             self.SaveLogs(self.total_analysis_log, 'White image analysis was FAIL')
            #         else:
            #             self.SaveLogs(self.total_analysis_log, 'White image analysis was PASS')
            #     else:
            #         result = False
            # if self.analysis_color.lower() == 'black' or self.analysis_color.lower() == 'all color':
            #     if os.path.isfile(os.path.join(self.black_result_save_dir, 'Result.log')):
            #         with open(os.path.join(self.black_result_save_dir, 'Result.log'), 'r') as file:
            #             content = file.read().strip()
            #         if 'FAIL' in content:
            #             result = False
            #             self.SaveLogs(self.total_analysis_log, 'Black image analysis was FAIL')
            #         else:
            #             self.SaveLogs(self.total_analysis_log, 'Black image analysis was PASS')
            #     else:
            #         result = False
            #
            # with open(self.total_result_log, 'w') as resultFile:
            #     if result:
            #         resultFile.writelines('PASS')
            #     else:
            #         resultFile.writelines('FAIL')
            # self.SaveLogs(self.total_analysis_log, 'Analysis time: %ss' %str(round(time.time()-self.start_time,2)))

if __name__ == '__main__':
    # time_start = time.time()
    rgb_program = RGB_Analysis_Program()
    # rgb_program.Main(r'E:\python\LCD_Program\anh\J3Z4M44')
    # rgb_program.Main(r'C:\Users\V22110128\Desktop\2024.11.5\1\Analysis_Image')
    rgb_program.Main()
    # rgb_program.Main(r'E:\python\LCD_Program\6FB4M44')


    # path = r'E:\FAIL'
    # listFolder = os.listdir(path)
    # for svt in listFolder:
    #     print(svt)
    #     rgb_program.Main('%s\%s' %(path, svt))
    #     shutil.copytree(r'E:\python\LCD_Program\result', r'E:\Result\%s' %(svt))
    #     shutil.rmtree(r'E:\python\LCD_Program\result')
    #     time.sleep(1)
    # print(time.time()-time_start)
