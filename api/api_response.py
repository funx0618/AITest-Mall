"""
ApiResponse - 统一响应对象
职责：封装 API 响应，提供统一的数据访问接口
"""


class ApiResponse:
    """统一 API 响应封装，Client 层返回此对象，由上层进行业务断言"""

    def __init__(self, status_code: int, json_data: dict, text: str):
        self.status_code = status_code
        self.json = json_data
        self.text = text

    @property
    def ok(self) -> bool:
        """HTTP 状态码是否为 2xx"""
        return 200 <= self.status_code < 300

    @property
    def code(self) -> int:
        """业务 code（从 JSON body 中提取）"""
        return self.json.get("code", -1)

    @property
    def data(self) -> dict:
        """业务 data（从 JSON body 中提取）"""
        return self.json.get("data", {})

    @property
    def message(self) -> str:
        """业务 message（从 JSON body 中提取）"""
        return self.json.get("message", "")

    def __repr__(self) -> str:
        return f"ApiResponse(status={self.status_code}, code={self.code})"
