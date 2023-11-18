import asyncio
import threading
import time
from functools import partial
from pathlib import Path

import cv2
import numpy as np
from aiogram import Bot
from aiogram.types import BufferedInputFile, Message


class Videostream:
    def __init__(self, chat_id: int, bot: Bot, cam_id: int | str) -> None:
        self.chat_id: int = chat_id
        self.cam_id: int | str = cam_id
        self.bot: Bot = bot
        self.cap: cv2.VideoCapture | None = None
        self.img: np.ndarray = np.ndarray((320, 480, 3))
        self.frame_obj: str | None = None
        self.video_stream_task: asyncio.Task | None = None
        self.object_detector_task: asyncio.Task | None = None
        self.image_worker_task: asyncio.Task | None = None
        self.lock = threading.Lock()

    # Видеопоток
    async def video_stream(
            self,
            classnames: tuple[str],
            net: cv2.dnn.DetectionModel,
    ) -> None:
        self.cap = cv2.VideoCapture(self.cam_id)

        if not self.cap.isOpened():
            msg = "Error: 'Could not open stream'"
            raise RuntimeError(msg)

        self.image_worker_task = asyncio.create_task(
            asyncio.to_thread(
                self._create_img_worker,
                classnames=classnames,
                net=net)
        )

        self.object_detector_task = asyncio.create_task(self._frame_object_detector())

    # получаем картинку
    def _create_img(self, classnames: tuple[str], net: cv2.dnn_DetectionModel) -> None:
        ok, img = self.cap.read()

        if not ok:
            msg = "Could not read image from camera"
            raise RuntimeError(msg)

        # настраиваем рамку
        threshold = 0.45
        nms_threshold = 0.55
        class_ids, confs, bbox = net.detect(img, confThreshold=threshold)
        bbox = list(bbox)
        confs = list(np.array(confs).reshape(1, -1)[0])
        confs = list(map(float, confs))
        indices = cv2.dnn.NMSBoxes(bbox, confs, threshold, nms_threshold)

        objects = []

        with self.lock:
            for i in indices:
                box = bbox[i]
                x, y, w, h = box
                cv2.rectangle(
                    img,
                    (x, y),
                    (x + w, h + y),
                    color=(0, 255, 0),
                    thickness=2,
                )
                cv2.putText(
                    img,
                    classnames[class_ids[i] - 1],
                    (box[0] + 5, box[1] - 5),
                    cv2.FONT_HERSHEY_COMPLEX,
                    fontScale=0.8,
                    color=(0, 255, 0),
                    thickness=2,
                )

                # список с объектами в кадре
                objects.append(
                    f"{classnames[class_ids[i] - 1]} - {round(confs[i] * 100)}%",
                )

            self.img = img

            # преобразовываем в строку
            self.frame_obj = "{}".format(", ".join(objects)) if objects else None

    # оповещение об объектах в кадре
    async def _frame_object_detector(self) -> None:
        while self.cap.isOpened():
            # если в кадре есть какой-либо объект, бот будет оповещать каждые 10 секунд
            if self.frame_obj:
                await self.send_warning(
                    chat_id=self.chat_id,
                    frame=self.get_frame(self.img),
                    frame_obj=self.frame_obj,
                )
                await asyncio.sleep(10)

            else:
                await asyncio.sleep(0.3)

    def _create_img_worker(self, classnames: tuple[str], net: cv2.dnn_DetectionModel) -> None:

        while self.cap.isOpened():
            self._create_img(classnames=classnames, net=net)

            time.sleep(0.3)

    # отправка оповещения в чат пользователя
    async def send_warning(
            self,
            chat_id: int,
            frame: BufferedInputFile,
            frame_obj: str,
    ) -> None:
        await self.bot.send_photo(chat_id=chat_id, photo=frame, caption=frame_obj)

    # запуск видеопотока
    def run_stream(
            self,
            classnames: tuple[str],
            net: cv2.dnn.DetectionModel,
    ) -> asyncio.Task:
        self.video_stream_task = asyncio.create_task(self.video_stream(classnames, net))
        return self.video_stream_task

    # остановка видеопотока
    def stop_stream(self) -> None:
        self.cap.release()
        self.video_stream_task.cancel() if self.video_stream_task else None
        self.object_detector_task.cancel() if self.object_detector_task else None
        self.video_stream_task = None
        self.object_detector_task = None

    # сохранение кадра в буффер
    @staticmethod
    def get_frame(img: np.ndarray) -> BufferedInputFile:
        ok, buffer = cv2.imencode(".jpg", img)
        return BufferedInputFile(buffer.tobytes(), filename="frame.jpg")

    # отправка кадра
    async def send_frame(self, msg: Message) -> None:
        img, frame_obj = self.get_frame(self.img), self.frame_obj
        await msg.answer_photo(photo=img, caption=frame_obj)


class ChatVideoStreams:
    def __init__(self) -> None:
        self.livestreams: dict[int, Videostream] = {}
        self.net = self._create_net()
        self.classnames = self._create_classnames()

    # создание модели распознавания
    @staticmethod
    def _create_net() -> cv2.dnn.DetectionModel:
        config_path = "stream/ssd_mobilenet_v3_large_coco_2020_01_14.pbtxt"
        weights_path = "stream/frozen_inference_graph.pb"

        # настраиваем распознавание
        net = cv2.dnn_DetectionModel(weights_path, config_path)
        net.setInputSize(320, 320)
        net.setInputScale(1.0 / 127.5)
        net.setInputMean((127.5, 127.5, 127.5))
        net.setInputSwapRB(swapRB=True)
        return net

    # определение классов из датасэта
    @staticmethod
    def _create_classnames() -> tuple[str]:
        # загружаем модель, веса и датасет имён для распознавания
        with Path("stream/classnames.txt").open(encoding="utf-8") as f:
            return tuple(line.strip().capitalize() for line in f.readlines())

    # обработка ошибок остановки потока
    def _done_callback(self, task: asyncio.Task, chat_id: int) -> None:
        if task.done():
            try:
                if exception := task.exception():
                    livestream = self.livestreams[chat_id]
                    livestream.stop_stream()
                    asyncio.create_task(
                        livestream.bot.send_message(
                            chat_id=chat_id,
                            text=f"Видеопоток остановлен!\n\n{exception}",
                        ),
                    )
                self.livestreams.pop(chat_id)
            except asyncio.CancelledError:
                pass

    # создание объекта видеопотока
    def add_live_stream(self, chat_id: int, livestream: Videostream) -> Videostream:
        if chat_id in self.livestreams:
            msg = "Stream already exists"
            raise KeyError(msg)

        self.livestreams[chat_id] = livestream
        task = self.livestreams[chat_id].run_stream(self.classnames, self.net)
        task.add_done_callback(partial(self._done_callback, chat_id=chat_id))

        return self.livestreams[chat_id]

    # получение объекта видеопотока
    def get_live_stream(self, chat_id: int) -> Videostream:
        if chat_id not in self.livestreams:
            msg = "Stream not found"
            raise KeyError(msg)

        return self.livestreams[chat_id]

    # удаление объекта видеопотока
    def stop_live_stream(self, chat_id: int) -> Videostream:
        livestream = self.get_live_stream(chat_id)
        livestream.stop_stream()

        return self.livestreams.pop(chat_id)
