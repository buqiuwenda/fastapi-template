from typing import Any, Dict
from fastapi.responses import JSONResponse



# 统一返回格式
def res(
    code: int = 200,
    msg: str = "成功",
    data: Any = None
) -> Dict[str, Any]:
    return {
        "code": code,
        "msg": msg,
        "data": data
    }

# 统一异常返回
def res_err(
    msg: str = "失败",
    code: int = 400,
    data: Any = None
) -> JSONResponse:
    return JSONResponse(
        content={"code": code, "msg": msg, "data": data},
        status_code=code
    )