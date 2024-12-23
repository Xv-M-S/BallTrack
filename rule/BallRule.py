import numpy as np
from MedianFinder import MedianFinder
"""
原则：使用规则尽量过滤结果而不消除结果。至少保证每帧保留一个检测结果。
"""
class BallTracker:
    def __init__(self, distance_threshold, ratio_threshold):
        self.distance_threshold = distance_threshold  # 最大允许距离
        self.center_points = []  # 存储球的中心点
        self.size_history = MedianFinder()  # 存储球的大小信息
        self.ratio_threshold = ratio_threshold
        
        self.sum_area = 0
        self.min_area = 0
        self.max_area = 0
        self.avg_area = 0
        self.middle_area = 0 # 一个视频序列的面积大小的平均值，如果是刚开始则为无

    def compute_center(self, box):
        """计算框的中心点"""
        try:
            x1, y1, x2, y2, confidence = box  # 解包框信息
        except:
            print("error:" + str(box))
            x1, y1, x2, y2 = box
            confidence = 0.4
        center_x = (x1 + x2) / 2
        center_y = (y1 + y2) / 2
        return (center_x, center_y, confidence)

    def distance(self, p1, p2):
        """计算两个点之间的欧几里德距离"""
        return np.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)

    def filter_boxes(self, boxes):
        """过滤不符合要求的框"""
        filtered_boxes = []
        if self.avg_area == 0: # 一个序列的第一帧，不过滤任何数据
            return boxes
        for box in boxes:
            center_x, center_y, confidence = self.compute_center(box)
            width = box[2] - box[0]
            height = box[3] - box[1]
            area = width * height
            
            # 检查面积区域差异是否在允许范围内
            if abs(area - self.avg_area)/self.avg_area < self.ratio_threshold: 
                filtered_boxes.append((center_x, center_y, width, height, confidence))
        return filtered_boxes

    def get_max_confidence(self, boxes):
        # 选择置信度最大的点
        max_confidence_box = None
        max_confidence = 0  # 初始化最大置信度
        for box in boxes:
            print(box)
            try:
                confidence = box[4]
            except:
                print("error:" + str(box))
                confidence = 0.4
            if confidence > max_confidence:
                max_confidence = confidence
                max_confidence_box = box
        return max_confidence_box
        
    def get_center_and_area(self, max_confidence_box):
        center_x, center_y, _ = self.compute_center(max_confidence_box)
        center = (center_x,center_y)
        
        width = max_confidence_box[2] - max_confidence_box[0]
        height = max_confidence_box[3] - max_confidence_box[1]
        area = width * height

        return center,area
       

    def update_tracking(self, current_boxes):
        """更新球的跟踪状态，并返回res_box"""
        res_box = None
        filtered_boxes = self.filter_boxes(current_boxes)

        if not filtered_boxes:
            # 如果全部被过滤，则直接选择置信度最大的球
            # 如果为序列第一个开头，直接选择置信度最大的球
            max_conf_box = self.get_max_confidence(current_boxes)
            center,area = self.get_center_and_area(max_conf_box)
            self.center_points.append(center)
            self.size_history.append(area)
            self.sum_area += area

            res_box = max_conf_box
            return res_box
        if not self.center_points:
            max_conf_box = self.get_max_confidence(filtered_boxes)
            center,area = self.get_center_and_area(max_conf_box)
            self.center_points.append(center)
            self.size_history.append(area)
            self.sum_area += area

            res_box = max_conf_box
            return res_box

        
        distance_box = None
        min_distance = 8096
        # 选择距离最近的框 or 综合距离和置信度考虑
        has_res = False
        for box in filtered_boxes:
            center = (box[0], box[1])
            # 检查与前几个框的距离
            if self.center_points:
                # 计算与最后一个中心点的距离
                last_center = self.center_points[-1]
                distance = self.distance(last_center, center)
                if distance <= self.distance_threshold and distance < min_distance:
                    min_distance = distance
                    distance_box = box
                    has_res = True
        
        if has_res:
            center,area = self.get_center_and_area(distance_box)
            self.center_points.append(center)
            self.size_history.append(area)
            self.sum_area += area
            
            res_box = distance_box
        else:
            # 此时要清空，说明开始了一个新的序列帧
            max_conf_box = self.get_max_confidence(filtered_boxes)
            center,area = self.get_center_and_area(max_conf_box)
            self.size_history.clear()
            self.center_points.clear()
            self.sum_area = 0
            self.middle_area = 0
            
            self.center_points.append(center)
            self.size_history.append(area)
            self.sum_area += area

            res_box = max_conf_box
            
        # 获取area的平均值or中位值
        if not self.size_history.empty():
            self.middle_area = self.size_history.find_median()
            self.avg_area = self.sum_area / self.size_history.size()
        
        return res_box

if __name__ == '__main__':   
    # 使用示例
    distance_threshold = 50  # 设定距离阈值
    size_thresholds = (100, 1000)  # 设定面积阈值
    tracker = BallTracker(distance_threshold, size_thresholds)

    # 假设有一帧检测结果
    current_boxes = [
        (100, 100, 120, 120, 0.9),  # 框格式: (x1, y1, x2, y2, confidence)
        (150, 150, 170, 170, 0.8),
        (300, 300, 320, 320, 0.95)
    ]

    tracker.update_tracking(current_boxes)