# Przepisy Babci Marysi

Zbiór rodzinnych przepisów odtworzonych ze starych, odręcznych notatek.
Każdy przepis zawiera zdjęcie oryginalnej kartki oraz jej przepisaną treść.

## Struktura

```
przepisy/
  <slug>/
    skan-1.jpg      # zdjęcie oryginalnej kartki (może być kilka: skan-2.jpg …)
    przepis.md      # dane przepisu + dokładna transkrypcja
szablon/
  przepis.md        # pusty szablon nowego przepisu
HERMES.md           # instrukcje dla agenta budującego stronę
```

## Dodawanie przepisu

1. Utwórz folder `przepisy/<slug>/`.
2. Wrzuć zdjęcie(a) kartki jako `skan-1.jpg`, `skan-2.jpg` …
3. Skopiuj `szablon/przepis.md` i uzupełnij.
4. Po sprawdzeniu transkrypcji ustaw `status: "zweryfikowany"`.
