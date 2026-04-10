# ZAI – Projekt 2 (Backend API w Django)

Repozytorium zawiera materiały do wykładów oraz kolejne etapy budowy projektu API.

Każdy wykład znajduje się w osobnym branchu:

* `wyklad01` – podstawy DRF (serializers, viewsets)
* `wyklad02` – autoryzacja + integracja z API
* `wyklad03` – async + bulk import

---

## Jak korzystać z repozytorium

### 0. Przejdź do wybranego katalogu - `clone` utworzy lokalne repozytorium w Twoim bieżącym katalogu

### 1. Sklonuj repozytorium

```bash
git clone https://github.com/SlowinskiUWM/zai2projekt
cd zai2projekt
```

---

### 2. Pobierz wszystkie branche

```bash
git fetch --all
```

---

### 3. Sprawdź dostępne branche

```bash
git branch -a
```

Zobaczysz listę, np.:

```
remotes/origin/wyklad01
remotes/origin/wyklad02
remotes/origin/wyklad03
```

---

### 4. Przełącz się na wybrany wykład

```bash
git switch wyklad01
```

Jeśli to pierwszy raz:

```bash
git switch -c wyklad01 origin/wyklad01
```


Jeżeli przełączysz się po raz pierwszy na wybrany wykład poleceniem `git switch wyklad0X` musisz samodzielnie ustawić połączenie między lokalnym branchem a jego źródłem w repozytorium.
Wykonaj poniższe polecenia:

```bash

```
git branch --set-upstream-to=origin/wyklad0X wyklad0X
git pull
---

## Jak pracować z materiałami

Każdy branch to stan projektu po wykładzie.

Możesz:

✔ analizować kod
✔ uruchamiać projekt lokalnie
✔ porównywać zmiany między wykładami

---

## Przydatne komendy

### Sprawdzenie aktualnego brancha

```bash
git branch
```

---

### Przełączanie się między wykładami

```bash
git switch wyklad02
git switch wyklad03
```

---

### Aktualizacja repozytorium

```bash
git pull
```

---

## Wskazówka

Najlepiej pracować tak:

1. przełącz się na branch z wykładu
2. uruchom projekt
3. analizuj kod
4. próbuj modyfikować samodzielnie

---



