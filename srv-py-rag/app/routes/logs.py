import os
from fastapi import APIRouter, Query
from fastapi.responses import PlainTextResponse
from app.settings import LOGS_DIR, APP_NAME
from app.routes.common.responses import ResponseMessages, ErrorResponse
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/logs", tags=["logs"])

@router.get("",
            summary="Get Logs",
            description=" Get log file for specific date. Administrator rights are required. "
                        "The content of the logs depends on the logging level set.",
            response_class=PlainTextResponse,
            responses={
                404: {"model": ErrorResponse, "description": "File not found"},
                500: {"model": ErrorResponse, "description": "Internal server error"},
            }
)
async def get_logs(
    year: int = Query(..., description="Year of log file"),
    month: int = Query(..., description="Month of log file"),
    day: int = Query(..., description="Day of log file")
):
    log_filename = f"{APP_NAME}_{year:04d}-{month:02d}-{day:02d}.log"
    log_filepath = os.path.join(LOGS_DIR, log_filename)
    logger.info(f"log_filepath = {log_filepath}")

    if not os.path.isfile(log_filepath):
        return ResponseMessages.error_404(f"Log file {log_filename} not found.")

    try:
        with open(log_filepath, 'r', encoding='utf-8') as file:
            log_content = file.read()
        return PlainTextResponse(content=log_content, status_code=200)
    except Exception as e:
        logger.error(f"Error reading log file: {str(e)}")
        return ResponseMessages.error_500(f"Error reading file: {str(e)}")