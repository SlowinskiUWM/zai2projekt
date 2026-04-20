# Wykład 01 — Serializatory (1)

## Cel i przebieg prezentacji

### Serializator

Na potrzeby niniejszej prezentacji w pliku *serializers.py* został zdefiniowany serializator *MovieSerializerTEST*

```python
from rest_framework import serializers
from .models import Movie

class MovieSerializerTEST(serializers.Serializer):
    title = serializers.CharField(max_length=200)
    year = serializers.IntegerField()
    description = serializers.CharField(allow_blank=True)
    created_at = serializers.DateTimeField()

    def create(self, validated_data):
        return Movie.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.year = validated_data.get('year', instance.year)
        instance.description = validated_data.get('description', instance.description)
        instance.created_at = validated_data.get('created_at', instance.created_at)
        instance.save()
        return instance
```

### Pokaz działania serializatora *MovieSerializerTEST* w Django REST Framework

• serializacja obiektu modelu (*Movie*)

• renderowanie serializowanych danych do formatu *JSON*

• deserializacja danych wejściowych

- deserializacja
- walidacja danych

• zapis deserializowanych danych do bazy

- metoda *create()*
- metoda *update()*

## Środowisko

```python
python manage.py shell_plus
```

## Importy

```python
from movies.models import Movie
from movies.serializers import MovieSerializerTEST
from rest_framework.renderers import JSONRenderer
import io
from rest_framework.parsers import JSONParser
```

## 1. Serializacja obiektu

```python
m = Movie.objects.first()
m
#[Out]: <Movie: Pan Tadeusz (1999)>
serializer = MovieSerializerTEST(m)
serializer.data       
#[Out]: {'title': 'Pan Tadeusz', 
# 'year': 1999, 
# 'description': "Zmieniony opis filmu 'Pan Tadeusz'", 
# 'created_at': '2026-04-16T12:16:35.576408+02:00'}
#
# Wynik: słownik Pythona (nie JSON!)
```

> UWAGA!<br/>
> *serializer.data* to jest dokładnie to, co trafia do odpowiedzi API *(Response)*


## 2. Renderowanie danych do formatu *JSON* (renderer DRF)

```python
json = JSONRenderer().render(serializer.data)
json
#[Out]: b'{"title":"Pan Tadeusz",
# "year":1999,
# "description":"Zmieniony opis filmu \'Pan Tadeusz\'",
# "created_at":"2026-04-19T08:25:29.116779+02:00"}'
```

## 3. Deserializacja danych

### Dane wejściowe

```python
data = {"title":"Pan Tadeusz",
          "year":2000,
          "description":"Opis filmu \'Pan Tadeusz\'",
          "created_at":"2026-04-19T08:25:29.116779+02:00"}
```

### Deserializacja

```python
serializer = MovieSerializerTEST(data=data)
```

## 4. Walidacja danych

```python
serializer.is_valid(raise_exception=True)
#[Out]: True   
# UWAGA: jeżeli metoda .is_valid() zwraca True, 
# wypełniany jest danymi atrybut 'validated_data' serializatora
serializer.validated_data
#[Out]: {'title': 'Pan Tadeusz',
#[Out]:  'year': 2000,
#[Out]:  'description': "Opis filmu 'Pan Tadeusz'",
#[Out]:  'created_at': datetime.datetime(2026, 4, 19, 8, 25, 29, 116779, tzinfo=zoneinfo.ZoneInfo(key='Europe/Warsaw'))}
```

## 5. Zapis danych do bazy (create)

Aby zaprezentować metodę *create()* usunięto z bazy danych serializowany obiekt, stąd po  deserializacji dane są zapisywane do bazy jako nowy obiekt.

```python
Movie.objects.count()
#[Out]: 3
m.delete()
#[Out]: (1, {'movies.Movie': 1})
Movie.objects.count()
#[Out]: 2
movie = serializer.save()
movie
#[Out]: <Movie: Pan Tadeusz (2000)>
# Liczba obiektów w bazie:
Movie.objects.count()
#[Out]: 3
#
# UWAGA: podczas zapisu nowego obiektu do bazy danych 
# serializer.save() wywołuje metodę create() z serializatora.

```

## 6. Aktualizacja obiektu w bazie danych (update)

```python
movie = Movie.objects.last()
movie
#[Out]: <Movie: Pan Tadeusz (1999)>

data = {"title":"Pan Tadeusz",
          "year":2000,
          "description":"Opis filmu \'Pan Tadeusz\'",
          "created_at":"2026-04-19T08:25:29.116779+02:00"}
```

*movie* to obiekt pobrany z bazy danych, nazywany *instancją (instance)*. Są to dane, z jakimi uruchamiany jest np. formularz podczas aktualizacji, jeszcze inaczej: instance to obiekt przekazany do serializatora.

*data* to zmodyfikowane dane, które w momencie zapisu do bazy danych zaktualizują *movie*.

UWAGA!
Jeśli nie przekażemy *instance*, serializer utworzy nowy obiekt zamiast aktualizować istniejący.

```python
serializer = MovieSerializerTEST(movie, data=data)
serializer.is_valid(raise_exception=True)
serializer.save()
# Wywoływana jest metoda update(instance, validated_data)
```

**Co decyduje o tym, jaka metoda zostanie wywołana podczas serializer.save()?**

```python
serializer = MovieSerializerTEST(data=data)           → create()
serializer = MovieSerializerTEST(instance, data=data) → update()
```

## 7. Dla dociekliwych

Uwaga
W *Postmanie* dane zostałyby przygotowane w formacie *JSON* , a następnie wysłane do naszego serializatora jako strumień bajtów. Aby dokonać symulacji tego procesu, można użyć biblioteki *io.BytesIO(json)*, zmieniającej dane w formacie *JSON* na strumień bajtów, a następnie *JSONParser().parse(stream)*, dającej w wyniku słownik *Pythona*.

### Przygotowanie danych wejściowych

```python
stream = io.BytesIO(json)
```

### Parsowanie danych wejściowych do formatu słownika języka *Python*


```python
data = JSONParser().parse(stream)
```

Tak przygotowane dane mogą następnie zostać poddane deserializacji.

```python
serializer = MovieSerializerTEST(movie, data=data)
```


## 8. Wnioski

• serializer zamienia model → dict (serializacja)<br/>
• serializer zamienia dict → model (deserializacja)<br/>
• validated_data zawiera poprawne dane<br/>
• save() wywołuje:<br/>
  ◦ create() jeśli brak instance<br/>
  ◦ update() jeśli instance istnieje<br/>

## 9. Najważniejsze pojęcia

• instance → istniejący obiekt z bazy<br/>
• validated_data → dane po walidacji<br/>
• serializer.data → dane do odpowiedzi API<br/>

## 10. Uwagi

• serializer.data ≠ JSON (to Python dict)<br/>
• JSON powstaje dopiero przez renderer<br/>
• shell nie przeładowuje kodu → po zmianach w plikach konieczny jest restart konsoli<br/>


## Dodatkowa uwaga — serializacja wielu obiektów

Serializator może obsługiwać również listę obiektów. W tym celu należy użyć parametru *many=True*. *many=True* informuje serializator, że pracujemy na kolekcji obiektów, a nie pojedynczym obiekcie:

```python
movies = Movie.objects.all()
serializer = MovieSerializerTEST(movies, many=True)
serializer.data
# Out[51]: [
# {'title': 'Pan Samochodzik i templariusze', 
#  'year': 1999, 
#  'description': "Opis filmu 'Pan Samochodzik i templariusze'", 
#  'created_at': '2026-04-16T12:17:09.471279+02:00'}, 
# {'title': 'Pan Wołodyjowski', 
#  'year': 1965, 
#  'description': "Opis filmu 'Pan Wołodyjowski'", 
#  'created_at': '2026-04-19T01:26:41.565521+02:00'}, 
# {'title': 'Pan Tadeusz', 
#  'year': 2000, 
#  'description': "Zmieniony opis filmu 'Pan Tadeusz'", 
#  'created_at': '2026-04-19T08:25:29.116779+02:00'}]
```

Wynikiem jest lista słowników (jeden słownik dla każdego obiektu).
