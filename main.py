import os
import re
import time
from multiprocessing import Pool

import cv2
from transliterate import translit


path_to_vid = "videos/"  # Путь откуда брать видео
save_path = "results/"  # Путь, куда вывести результат


def find_video_filenames():
    """Поиск в директории файлов с расщирением .avi и .mp4"""
    directory = path_to_vid
    data = []
    for filename in os.listdir(directory):
        if filename.endswith('.avi') \
                or filename.endswith('.mp4'):
            data.append(filename)
    return data


def has_cyrillic(text):
    """Ищем, есть ли в названии кириллица"""
    return bool(re.search('[а-яА-Я]', text))


def main(file):
    """Основная часть программы"""
    video_filename = str(file)
    cyrillic = has_cyrillic(video_filename)
    frame_name = video_filename
    if cyrillic:
        frame_name = translit(
            frame_name,
            language_code='ru',
            reversed=True
        )
        print(f'Транслитерация: {frame_name}')
    start_time = time.monotonic()
    print(video_filename)
    if not os.path.isdir(video_filename):
        os.mkdir(f'{save_path}{video_filename}')
    start_action = ''
    finish_action = ''
    video = cv2.VideoCapture(path_to_vid + video_filename)
    ret, frame1 = video.read()
    ret, frame2 = video.read()
    last_action = 0
    count = 1
    action_count = 0
    while video.isOpened():
        try:
            difference = cv2.absdiff(
                frame1,
                frame2
            )
            gray = cv2.cvtColor(
                difference,
                cv2.COLOR_BGR2GRAY
            )
            blur = cv2.GaussianBlur(
                gray,
                (5, 5),
                0
            )
            _, threshold = cv2.threshold(
                blur,
                50,
                255,
                cv2.THRESH_BINARY
            )
            dilate = cv2.dilate(
                threshold,
                None,
                iterations=3
            )
            contour, _ = cv2.findContours(
                dilate,
                cv2.RETR_TREE,
                cv2.CHAIN_APPROX_SIMPLE
            )
            cv2.drawContours(
                frame1,
                contour,
                -1,
                (0, 0, 255),
                2
            )
            cv2.imshow(
                f'{frame_name}',
                frame1
            )
            if not contour:
                if last_action == 0:
                    last_action = 0
                    count = 1
                else:
                    print(f'В "{video_filename}" '
                          f'движение с {start_action} '
                          f'с. по {finish_action} с.'
                          )
                    time_list = open(
                        f'{save_path}{video_filename}'
                        f'/time_list_{video_filename}.txt',
                        'a'
                    )
                    time_list.write(f'Движение {action_count}: '
                                    f'время начала {str(start_action)}, '
                                    f'время окончания {str(finish_action)}\n')
                    last_action = 0
                    count = 1
            if contour:
                if last_action == 0:
                    start_action = round(
                        time.monotonic() - start_time,
                        2
                    )
                    action_count += 1
                    cv2.imwrite(
                        f'{save_path}{video_filename}'
                        f'/action_{str(action_count)}'
                        f'_{video_filename[:-4]}_%d.jpg' % count,
                        frame1
                    )

                if count == 36 or \
                        count == 72 or \
                        count == 108 or \
                        count == 144 or \
                        count == 180:
                    cv2.imwrite(
                        f'{save_path}{video_filename}'
                        f'/action_{str(action_count)}'
                        f'_{video_filename[:-4]}_%d.jpg' % count,
                        frame1
                    )
                else:
                    finish_action = round(
                        time.monotonic() - start_time,
                        2
                    )
                last_action = 1
                count += 1
            frame1 = frame2
            ret, frame2 = video.read()
            if cv2.waitKey(40) == ord('q'):
                break
        except Exception:
            print(f'Видео закончилось: {video_filename}')
            break
    video.release()


if __name__ == '__main__':
    if not os.path.isdir(save_path):
        os.mkdir(save_path)
    print('доступны файлы:')
    file_names = find_video_filenames()
    print(file_names)
    print('Следующие файлы запущены для распознавания:')
    p = Pool()  # Здесь можно ограничить количество ядер, например p = Pool(5)
    p.map(main, file_names)
    p.close()
    p.join()
