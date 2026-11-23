from django.db import connections
from django.db.utils import OperationalError
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from .tasks import noop_healthcheck_task


class HealthcheckView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        db_ok = True
        try:
            with connections["default"].cursor() as cursor:
                cursor.execute("SELECT 1")
                cursor.fetchone()
        except OperationalError:
            db_ok = False

        payload = {
            "status": "ok" if db_ok else "degraded",
            "database": db_ok,
            "celery_eager": noop_healthcheck_task.apply().successful(),
        }
        status_code = (
            status.HTTP_200_OK if db_ok else status.HTTP_503_SERVICE_UNAVAILABLE
        )
        return Response(payload, status=status_code)
