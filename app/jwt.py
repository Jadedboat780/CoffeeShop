# from fastapi import FastAPI, HTTPException, Depends, Request
# from fastapi.responses import JSONResponse
# from fastapi_jwt_auth import AuthJWT
# from fastapi_jwt_auth.exceptions import AuthJWTException
# from config import settings
#
# @AuthJWT.load_config
# def get_config():
#     return settings.JWT_SECRET
#
# @app.exception_handler(AuthJWTException)
# def authjwt_exception_handler(request: Request, exc: AuthJWTException):
#     return JSONResponse(
#         status_code=exc.status_code,
#         content={"detail": exc.message}
#     )