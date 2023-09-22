# TCPA
import math
import pandas as pd
from typing import Any
import time
import requests
import threading


class Tcpa:
    def __init__(self) -> None:
        self.tcpa = None
        self.lat1 = None
        self.lat2 = None
        self.lon1 = None
        self.lon2 = None
        self.sog1 = None
        self.sog2 = None
        self.cog1 = None
        self.cog2 = None
        self.cur = 0

    def __loadData(self) -> pd.DataFrame:
        FILENAME: str = "./ais20171001_top5/ais_top3_mmsi440123380.csv"
        # data
        data = pd.read_csv(FILENAME)
        return data
    # 위/경도로 표시된 두 지점 간의 거리를 계산(Haversine 공식 사용)

    def __setting(self, main, target) -> None:
        self.lat1 = main.Latitude
        self.lat2 = target.Latitude
        self.lon1 = main.Longitude
        self.lon2 = target.Longitude
        self.sog1 = main.SOG
        self.sog2 = target.SOG
        self.cog1 = main.COG
        self.cog2 = target.COG

    def __haversine_dist(self) -> Any:
        R = 6371  # 지구의 반경 (단위: km)
        dlat = math.radians(self.lat2 - self.lat1)
        dlon = math.radians(self.lon2 - self.lon1)
        a = math.sin(dlat / 2) * math.sin(dlat / 2) + math.cos(math.radians(self.lat1)) * \
            math.cos(math.radians(self.lat2)) * \
            math.sin(dlon / 2) * math.sin(dlon / 2)
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        distance = R * c
        return distance

    # 두 선박의 Lat, Lon, COG, SOG 정보를 사용하여 TCPA를 계산

    def __calculate_tcpa(self) -> None:

        # 두 선박의 거리 계산
        distance = self.__haversine_dist()

        # COG 값을 라디안 단위로 변환
        cog1_rad = math.radians(self.cog1)
        cog2_rad = math.radians(self.cog2)

        # 두 선박의 상대 속도 계산
        relative_speed = math.sqrt(
            self.sog1**2 + self.sog2**2 - 2 * self.sog1 * self.sog2 * math.cos(cog2_rad - cog1_rad))

        # TCPA 계산
        time_to_closest_point = distance / relative_speed

        # 분 단위로 변환
        self.tcpa = time_to_closest_point * 60

    def get(self) -> int:
        return self.cur

    def run(self, targetAIS: pd.DataFrame, ip: str, startIndex: int = 0) -> None:
        data = self.__loadData()
        i = startIndex
        while not threading.currentThread().stopped():
            ais = data.iloc[i]
            # 값 설정
            self.__setting(ais, targetAIS)
            # TCPA 계산
            self.__calculate_tcpa()

            if self.tcpa < 6:  # 위험
                requests.post(f"http://{ip}/ais_data",
                              data={"TCPA": self.tcpa, "status": "위험"})
            else:  # 안전
                requests.post(f"http://{ip}/ais_data",
                              data={"TCPA": self.tcpa, "status": "안전"})
            # Top3는 컬럼이 182개

            i = (i+1) % 181
            self.cur = i
            time.sleep(5)


class WorkerThread(threading.Thread):
    def __init__(self, tcpa, param) -> None:
        super().__init__()
        self.obj = tcpa
        self.param = param
        self.stop_flag = False

    def run(self):
        self.obj.run(self.param[0], self.param[1], self.param[2])

    def stop(self):
        self.stop_flag = True

    def stopped(self):
        return self.stop_flag


if __name__ == "__main__":
    pass
