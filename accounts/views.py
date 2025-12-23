
from rest_framework import generics
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import User
from .serializers import UserSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from .token_serializers import MyTokenObtainPairSerializer
from rest_framework import permissions, status
from rest_framework.views import APIView
from .permissions import IsAdmin

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

# This view lets users register for the LMS (students, teachers, or admins).
# It uses DRF's CreateAPIView, which handles all the details of creating a new user record.
class UserCreate(generics.CreateAPIView):
    """
    API view for creating new users.

    Uses Django Rest Framework's generic CreateAPIView, so you don't have to write the logic yourself.
    Just specify the model and serializer, and DRF takes care of the rest.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def me(request):
    user = request.user
    data = {
        "id": user.id,
        "username": getattr(user, "username", None),
        "email": getattr(user, "email", None),
        "role": getattr(user, "role", None),
        "is_staff": getattr(user, "is_staff", False),
        "is_superuser": getattr(user, "is_superuser", False),
    }
    return Response(data)

class AdminUserList(APIView):
    permission_classes = [IsAdmin]

    def get(self, request):
        qs = User.objects.all().order_by('id')
        data = [
            {
                "id": u.id,
                "username": u.username,
                "email": u.email,
                "role": getattr(u, "role", None),
                "is_staff": u.is_staff,
                "is_superuser": u.is_superuser,
            }
            for u in qs
        ]
        return Response(data)

class AdminUserDetail(APIView):
    permission_classes = [IsAdmin]

    def patch(self, request, user_id: int):
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({"detail": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        role = request.data.get("role")
        is_staff = request.data.get("is_staff")
        is_superuser = request.data.get("is_superuser")

        updated_fields = []
        if role in {"student", "teacher", "admin"}:
            user.role = role
            updated_fields.append("role")
        if isinstance(is_staff, bool):
            user.is_staff = is_staff
            updated_fields.append("is_staff")
        if isinstance(is_superuser, bool):
            user.is_superuser = is_superuser
            updated_fields.append("is_superuser")

        if updated_fields:
            user.save(update_fields=updated_fields)

        return Response({
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "role": getattr(user, "role", None),
            "is_staff": user.is_staff,
            "is_superuser": user.is_superuser,
        })

