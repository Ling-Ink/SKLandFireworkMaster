import cv2
import numpy
import libadb
import logging

logger = logging.getLogger(__name__)
block_size = 55

def get_black_percent(mat, x0, x1, y0, y1):
    num = 0
    for x in range(x0, x1):
        for y in range(y0, y1):
            color_data = mat[x][y]
            if color_data[0] <= 120 & color_data[1] <= 120 & color_data[2] <= 120:
                 num += 1
    return num / ((x1 - x0) * (y1 - y0))

def get_color_percent(mat, color):
    num = 0
    for line in mat:
        for pixel in line:
            color_data = pixel
            if (color_data[0] >= color[0]) & (color_data[1] >= color[1]) & (color_data[2] >= color[2]):
                 num += 1
    return num / 3200

if __name__ == "__main__":
    logger.setLevel(logging.DEBUG)
    d = libadb.adb()
    d.connect("127.0.0.1:16384")
    last_count = 0
    count_ctx = False
    same_count = 0
    input_count = 0
    while True:
        img_pil = d.screencap()
        img_cv2 = cv2.cvtColor(numpy.asarray(img_pil), cv2.COLOR_RGB2BGR)
        height, width, _ = img_cv2.shape
        matrix_1 = img_cv2[225:515, 185:475]
        matrix_2 = img_cv2[600:890, 177:467]
        matrix_tag = img_cv2[340:380, 95:175] #bc2c62
        magenta_percent = get_color_percent(matrix_tag, (90, 40, 180))
        if magenta_percent < 0.8:
            continue
        
        imgadd = cv2.add(matrix_1,matrix_2)
        img_gray = cv2.cvtColor(imgadd,cv2.COLOR_RGB2GRAY)
        img_rgb = cv2.cvtColor(img_gray,cv2.COLOR_GRAY2BGR)
        ret,thresh = cv2.threshold(img_rgb,250,255,cv2.THRESH_BINARY)
        
        skip_loop = False
        matrix = []
        for x in range(0, 5):
            row = []
            for y in range(0, 5):
                rect_x1 = 15 + x * block_size
                rect_x2 = 50 + x * block_size
                rect_y1 = 15 + y * block_size
                rect_y2 = 50 + y * block_size
                cv2.rectangle(thresh, (rect_x1,rect_y1), (rect_x2, rect_y2), (0, 255, 0), 0)
                black_percent = get_black_percent(thresh, rect_x1, rect_x2, rect_y1 - 5, rect_y2)
                row.append(black_percent)
                if skip_loop: break
            if skip_loop: break
            matrix.append(row)
        if skip_loop:
            continue
        count = 0
        for row in matrix:
            for block in row:
                if block != 0.0:
                    count += 1
        if count == last_count:
            same_count += 1
            if same_count >= 20:
                count_ctx = False
                same_count = 0
            if not count_ctx:
                print('tap: clear')
                d.tap(729, 1145) # 清除
                print(count)
                count_ctx = True
                for i in str(count):
                    match i:
                        case '0':
                            print('tap: 0')
                            d.tap(208, 1138)
                        case '1':
                            print('tap: 1')
                            d.tap(107, 1274)
                        case '2':
                            print('tap: 2')
                            d.tap(287, 1274)
                        case '3':
                            print('tap: 3')
                            d.tap(460, 1274)
                        case '4':
                            print('tap: 4')
                            d.tap(640, 1274)
                        case '5':
                            print('tap: 5')
                            d.tap(808, 1274)
                        case '6':
                            print('tap: 6')
                            d.tap(206, 1397)
                        case '7':
                            print('tap: 7')
                            d.tap(381, 1395)
                        case '8':
                            print('tap: 8')
                            d.tap(550, 1390)
                        case '9':
                            print('tap: 9')
                            d.tap(725, 1401)
                    cv2.waitKey(100)
                input_count += 1
                print('input_count:', input_count)
        else:
            last_count = count
            count_ctx = False
            print("=>", same_count)
            same_count = 0
        cv2.imshow('img', thresh)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break