import logging
from datetime import datetime

logger = logging.getLogger('metrics')

class MetricsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Логируем запрос
        start_time = datetime.now()
        response = self.get_response(request)
        duration = (datetime.now() - start_time).total_seconds()

        # Логируем информацию о запросе
        logger.info(
            f"Path: {request.path}, Method: {request.method}, "
            f"Status Code: {response.status_code}, Duration: {duration:.3f}s"
        )
        # Сбор метрик (например, успешные и неуспешные запросы)
        if response.status_code >= 400:
            logger.warning(f"Failed request: {request.path}")
        else:
            logger.info(f"Successful request: {request.path}")

        return response
