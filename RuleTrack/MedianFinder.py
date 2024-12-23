import heapq

class MedianFinder:
    def __init__(self):
        self.max_heap = []  # 存储较小的一半（最大堆）
        self.min_heap = []  # 存储较大的一半（最小堆）

    def append(self, num: int):
        # 将新数添加到最大堆
        heapq.heappush(self.max_heap, -num)

        # 将最大堆的最大元素移动到最小堆
        heapq.heappush(self.min_heap, -heapq.heappop(self.max_heap))

        # 保持两个堆的大小平衡
        if len(self.max_heap) < len(self.min_heap):
            heapq.heappush(self.max_heap, -heapq.heappop(self.min_heap))

    def find_median(self) -> float:
        if len(self.max_heap) > len(self.min_heap):
            if len(self.max_heap) > 0:
                return -self.max_heap[0] # 最大堆的最大元素
            else:
                return -1
        if len(self.max_heap) > 0 and len(self.min_heap) > 0:
            return (-self.max_heap[0] + self.min_heap[0]) / 2  # 两个堆的根的平均值
        return -1

    def clear(self):
        """清空所有数据"""
        self.max_heap = []
        self.min_heap = []
    
    def empty(self) -> bool:
        """判断是否为空"""
        return len(self.max_heap) == 0 and len(self.min_heap) == 0
    
    def size(self) -> int:
        return len(self.max_heap) + len(self.min_heap)

if __name__ == "__main__":
    # 使用示例
    finder = MedianFinder()
    finder.add_num(1)
    print(finder.find_median())  # 输出 1.0
    finder.add_num(3)
    print(finder.find_median())  # 输出 2.0
    finder.add_num(2)
    print(finder.find_median())  # 输出 2.0

    # 清空数据
    finder.clear()
    print(finder.find_median())  # 此时没有数据，需处理空情况