from rest_framework import viewsets, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.db import DatabaseError, connections
from pymongo.errors import PyMongoError
from helpers.mongodb_connection import MongoDBConnection


class MainViewSet(viewsets.ViewSet):
    permission_classes = [AllowAny]

    def list(self, request):
        try:
            for connection in connections.all():
                with connection.cursor() as cursor:
                    cursor.execute("SELECT 1")
                    result = cursor.fetchone()
                    if result != (1,):
                        raise DatabaseError("Relational database query failed")
            mongo_db = MongoDBConnection().get_database()
            if mongo_db is None:
                raise PyMongoError("MongoDB connection is not available")
            try:
                mongo_db.client.admin.command("ping")
            except Exception as e:
                raise PyMongoError(f"MongoDB ping failed: {str(e)}")
            return Response({"status": "healthy"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {"status": "unhealthy", "error": str(e)},
                status=status.HTTP_503_SERVICE_UNAVAILABLE,
            )
