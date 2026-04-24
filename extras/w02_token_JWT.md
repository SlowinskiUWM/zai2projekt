# Zaawansowane aplikacje internetowe

<br>

## Token JWT w Django REST API

<br>

Dokumentacja Django REST Framework dostępna jest <a href="https://www.django-rest-framework.org/" target="_blank">tutaj</a>.

Dokumentacja pakietu **djangorestframework-simplejwt** dostępna jest <a href="https://django-rest-framework-simplejwt.readthedocs.io/en/latest/" target="_blank">tutaj</a>.

<br>

### Instalacja niezbędnych pakietów

<font size="2">

```bash
pip install djangorestframework-simplejwt
```

</font>

<br>

### Konfiguracja `settings.py`

<font size="2">

```python

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
}
```

</font>

<br>

Można również dodać opcjonalną konfigurację czasu wygaśnięcia tokenu:

<font size="2">

```python
from datetime import timedelta

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=5),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=7),
}
```

</font>

<br>

### Endpointy do uwierzytelniania (urls.py - na poziomie API)

<font size="2">

```python
from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    ...
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]
```

</font>

<br>

### Przykład uzyskania tokenu

<font size="2">

```http
POST /api/token/
Content-Type: application/json

{
    "username": "admin",
    "password": "admin"
}
```

Odpowiedź:

```json
{
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJ...XVCJ9...",
    "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJ...XVCJ9..."
}
```

</font>

<br>

Token należy przesyłać w nagłówku zapytań do chronionych zasobów:

<font size="2">

```
Authorization: Bearer <ACCESS_TOKEN>
```

</font>

<br>

---

## Ograniczanie dostępu – widoki oparte o funkcje

<br>

Jeśli używamy **funkcyjnych widoków API**, należy użyć dekoratora `@permission_classes`:

<font size="2">

```python
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def example_view(request):
    return Response({"message": f"Witaj {request.user.username}!"})
```

</font>

<br>

---

## Ograniczanie dostępu – widoki oparte na klasach

<br>

W przypadku widoków opartych o klasy, np. widoków generycznych lub viewsetów, używamy atrybutu `permission_classes`:

<font size="2">

```python
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from movies.models import Movie
from movies.serializers import MovieSerializer

class MovieViewSet(ModelViewSet):
    queryset = Movie.objects.all().order_by('-id')
    serializer_class = MovieSerializer
    permission_classes = [IsAuthenticated]
```

</font>

<br>

Jeśli użytkownik nie dostarczy prawidłowego tokenu JWT, serwer zwróci błąd:

<font size="2">

```json
{
    "detail": "Nie podano danych uwierzytelniających.",
    "code": "not_authenticated"
}
```

</font>

<br>

---
