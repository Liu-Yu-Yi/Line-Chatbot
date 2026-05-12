class UserState:
    """用戶狀態管理類 [cite: 35, 37]"""
    def __init__(self):
        self.current_state = None  # 當前狀態 [cite: 39]
        self.waiting_for_input = False  # 是否等待用戶輸入 [cite: 40]
        self.context = {}  # 上下文數據存儲 [cite: 41]

    def set_state(self, state, waiting_for_input=False):
        """設置當前狀態 [cite: 42, 43]"""
        self.current_state = state [cite: 44]
        self.waiting_for_input = waiting_for_input [cite: 45]

    def reset(self):
        """重置狀態 [cite: 46, 47]"""
        self.current_state = None [cite: 48]
        self.waiting_for_input = False [cite: 50]
        self.context = {} [cite: 51]

    def set_context(self, key, value):
        """設置上下文數據 [cite: 52, 53]"""
        self.context[key] = value [cite: 54]

    def get_context(self, key, default=None):
        """獲取上下文數據 [cite: 55, 56]"""
        return self.context.get(key, default) [cite: 57]
