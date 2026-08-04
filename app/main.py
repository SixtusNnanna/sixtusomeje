from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.api.v1.base import router as api_router
from app.databaase.session import create_db_tables
from app.exceptions import ExistException, NotFoundExcept, NotZeroError, SameWareHouseTransferError, InSufficentStockError, StatusCompletedError
from fastapi.exceptions import RequestValidationError


@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_db_tables()
    yield


app = FastAPI(lifespan=lifespan)


@app.exception_handler(ExistException)
async def exist_exception_handler(request: Request, exc: ExistException):
    return JSONResponse(
        status_code=409,
        content={"detail": str(exc)},
    )


@app.exception_handler(NotFoundExcept)
async def not_found_exception_handler(request: Request, exc: NotFoundExcept):
    return JSONResponse(
        status_code=404,
        content={"detail": str(exc)}
    )

@app.exception_handler(StatusCompletedError)
async def status_exception_handler(request: Request, exc: StatusCompletedError):
    return JSONResponse(
        status_code=409,
        content={"detail":"Order Status is already Completed"}
    )

@app.exception_handler(NotZeroError)
async def no_zero_handler(request: Request, exc: NotZeroError):
    return JSONResponse(
        status_code=422,
        content={"detail": "Quantity cannot be zero"}
    )

@app.exception_handler(InSufficentStockError)
async def insufficient_stock_handler(request: Request, exc: InSufficentStockError):
    return JSONResponse(
        status_code=422,
        content={"detail": "Quantity cannot be zero"}
    )


@app.exception_handler(SameWareHouseTransferError)
async def same_warehouse_handler(request: Request, exc: SameWareHouseTransferError):
    return JSONResponse(
        status_code=409,
        content={
            "detail": "Cannot Transfer to the same ware house"
        },
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(
    request: Request,
    exc: RequestValidationError
):
    errors = []

    for error in exc.errors():
        errors.append({
            "field": error["loc"][-1],
            "message": error["msg"]
        })

    return JSONResponse(
        status_code=422,
        content={
            "detail": errors
        }
    )



app.include_router(api_router)







