# Zdjęcia na stronie: dodawanie, usuwanie i zmiana (Start, Portfolio, Galeria)

## 0. Gdzie są pliki
- Ścieżki poniżej liczę od katalogu assets:
  ```
  start/                                   slajdy strony głównej (bez miniatur)
  portfolio/                               tu wrzucasz nowe zdjęcia + name.md
  portfolio/full/   portfolio/thumbial/    te same nazwy plików (robi GitHub)
  gallery/<N>_<sesja>/                     tu wrzucasz nowe zdjęcia + name.md
  gallery/<N>_<sesja>/full/  thumbial/  overview.md
  altText.ts                               opisy alt
  <prefiks>/name.md                        zmiana nazw + alt (pkt 8)
  slideFocus.ts                            kadr slajdów na telefonie
  ```

## 1. Nazwy plików
- Start i galeria: `NN-opis.webp` (2 cyfry). Portfolio: `NNN-opis.webp` (3 cyfry).
- `NN` to kolejność wyświetlania, bo pliki są sortowane po nazwie.
- Opis: małe litery, bez polskich znaków, słowa łączone myślnikiem `-`, 6-10 słów.
- Nazwy z aparatu (`IMG_1234`, `DSC_0001`, `1.jpg`) trzeba zmienić na opisowe.
- Miniatura (`thumbial/`) musi mieć **dokładnie tę samą nazwę** co pełne zdjęcie w `full/`. GitHub pilnuje tego sam, jeśli wrzucasz zdjęcia do głównego katalogu (pkt 2).

## 2. Dodawanie zdjęć
1. Skopiuj oryginały (jpg/png/heic, także gotowe `.webp`) **jeden raz** do głównego katalogu:
   - **Start**: `start/`
   - **Portfolio**: `portfolio/` (nie do `full/` ani `thumbial/`)
   - **Galeria, istniejąca sesja**: `gallery/<folder>/` (nie do `full/` ani `thumbial/`)
   - **Galeria, nowa sesja**: utwórz `gallery/<N+1>_<nazwa_bez_pl_znakow>/` z `overview.md` i wrzuć tam zdjęcia. `full/` i `thumbial/` utworzy GitHub.
     - Najwyższy numer to najnowsza sesja, wyświetlana jako pierwsza.
     - URL to nazwa bez `N_`, z `_` zamienionym na `-`. Nie zmieniaj później nazwy folderu.
     - W `overview.md`: linia 1 to `# Tytuł` (bez spacji na początku), linia 2 to jedno zdanie intro (~120-150 znaków), które służy też jako meta description. Cały plik jest widoczny na stronie.
2. Nazw z aparatu **nie musisz zmieniać ręcznie**. Zrobi to GitHub po wrzuceniu pliku `name.md` (pkt 6 i 8).
   - Ręczna zmiana nazw według pkt 1 nadal działa. Wtedy w pkt 4 i 5 wklejasz wpisy ręcznie.
3. Zmianę rozmiaru i rozłożenie do katalogów robi GitHub po wrzuceniu do `main` (skrypt `scripts/convert-images.sh`, pkt 8).
   - Zdjęcia z głównego katalogu (`portfolio/`, `gallery/<folder>/`) są konwertowane do pełnego rozmiaru, kopiowane do `full/` **i** `thumbial/`, a potem miniatury są zmniejszane.
   - `full` i start: maks. 2048 px, q90. Miniatury: 800 px szerokości, q80. Wynik to WebP z metadanymi copyright.
   - WebP większe niż limit (miniatura > 800 px szerokości, `full`/start > 2048 px) są zmniejszane w miejscu. WebP w limicie nie są ruszane.
   - **Skrypt usuwa oryginały** (jpg/png/heic) i zdjęcia z głównego katalogu; inne pliki (`overview.md`, `name_*.md`) zostają. Oryginały zostają w historii git, ale lepiej trzymaj kopie gdzie indziej.
   - Zdjęcie o tej samej nazwie co istniejące w `full/` je **nadpisuje** (podmiana zdjęcia).
   - Opcjonalnie lokalnie: `bash scripts/convert-images.sh` z katalogu głównego repo (domyślnie katalog `assets`, inny można podać jako argument). Wymaga `imagemagick` i `webp` (cwebp, webpmux).
4. Wygeneruj przez AI plik `name.md` z nowymi nazwami i alt textami (pkt 6), zapisz go w katalogu prefiksu i wrzuć wszystko do github. GitHub zmieni nazwy i uzupełni `altText.ts` (pkt 8).
5. Tylko dla start: każde nowe zdjęcie dostaje wpis w `slideFocus.ts` (domyślnie `'50% 50%'`). Jeśli ludzie nie są na środku kadru, dopisz w `name.md` 4. kolumnę, np. `30% 50%`, albo popraw wartość w `slideFocus.ts` później. Pierwsza wartość to poziome położenie: 0% = lewo, 100% = prawo.


## 3. Usuwanie zdjęć
1. Usuń plik z `full/` (lub `start/`) **i** jego miniaturę z `thumbial/`.
2. Usuń wpis z `altText.ts`. Dla start usuń też wpis z `slideFocus.ts`, jeśli istnieje.
3. Luki w numeracji nie przeszkadzają. Przenumerowanie jest opcjonalne, ale wtedy trzeba zmienić też klucze w `altText.ts` i `slideFocus.ts`.
4. Usunięcie całej sesji: skasuj folder `gallery/<folder>/` i wszystkie jego wpisy `gallery/<folder>/...` w `altText.ts`. Linki, strona sesji i sitemap znikną same.

## 4. Zmiana zdjęć
- **Podmiana zdjęcia przy tej samej nazwie**: wrzuć nowy oryginał pod tą samą nazwą (np. `07-opis.jpg`) do głównego katalogu (`portfolio/`, `gallery/<folder>/`) i wrzuć do github. GitHub nadpisze `full/` i `thumbial/` (pkt 8).
  - Start: usuń stare `.webp` ze `start/` i wrzuć nowy oryginał (skrypt nie nadpisuje WebP w limicie rozmiaru).
  - Jeśli treść zdjęcia się zmieniła, popraw alt.
- **Zmiana kolejności**: zmień prefiks `NN` w `full/` i w miniaturach, potem zaktualizuj klucze w `altText.ts` (i `slideFocus.ts`).
- **Zmiana nazwy pliku**: dodaj wiersz do `name.md` (pkt 8): `stara-nazwa.webp | nowa-nazwa.webp | Alt text`. Plik, którego nie ma w głównym katalogu, jest zmieniany w `full/` i `thumbial/`. Albo ręcznie: zmień nazwę w obu katalogach, a w `altText.ts` zmień klucz i w razie potrzeby wartość.
- **Zmiana samego alt textu**: edytuj tylko wartość w `altText.ts`, klucz zostaje bez zmian.
- **Zmiana kadru slajdu na telefonie**: edytuj wartość w `slideFocus.ts`.

## 5. Format `altText.ts`
- Linia: `    'KLUCZ': 'Alt text',` z 4 spacjami wcięcia, pojedynczymi cudzysłowami i przecinkiem na końcu.
- KLUCZ to prefiks katalogu plus nazwa pliku `.webp`, bez `full/` ani `thumbial/`.
- Miniatura korzysta z alt textu pełnego zdjęcia.
- Wartość to jedno polskie zdanie z polskimi znakami, bez kropki na końcu, 6-14 słów.
- Brak wpisu oznacza ogólny alt typu „… | zdjęcie N”, co jest złe dla SEO.

## 6. Nazwy i alt texty przez AI → `name.md` (jeden katalog)
1. Wyślij do AI nowe zdjęcia z **jednego** głównego katalogu. Nazwy plików muszą zostać bez zmian (np. `IMG_1234.jpg` albo `IMG_1234.webp`, jeśli konwertowano lokalnie). Rozszerzenie i wielkość liter w `name.md` nie muszą się zgadzać (pkt 8).
   - galeria: nowe pliki z `gallery/<folder>/`
   - portfolio: nowe pliki z `portfolio/`
   - start: nowe pliki z `start/`
2. AI widzi tylko obrazy, a nie folder. Dlatego w 1. linii promptu wpisujesz ręcznie **prefiks** (`PREFIKS = ...`), a w 2. linii **numer pierwszego nowego zdjęcia** (`START = ...`, czyli ostatni numer w katalogu + 1). Przykłady:

   | Wysyłany katalog | 1. linia promptu | 2. linia | Gdzie zapisać `name.md` |
   | --- | --- | --- | --- |
   | `start/` | `PREFIKS = start/` | `START = 15` | `start/name.md` |
   | `portfolio/` | `PREFIKS = portfolio/` | `START = 104` | `portfolio/name.md` |
   | `gallery/2_sesja_plenerowa_w_parku/` | `PREFIKS = gallery/2_sesja_plenerowa_w_parku/` | `START = 21` | `gallery/2_sesja_plenerowa_w_parku/name.md` |
   | nowa sesja, np. `gallery/12_sesja_slubna_lukow/` | `PREFIKS = gallery/12_sesja_slubna_lukow/` | `START = 1` | `gallery/12_sesja_slubna_lukow/name.md` |

3. Zasady prefiksu:
   - Wpisujesz go ze slashami `/`, z `/` na końcu.
   - Nie wpisuj w nim `full/` ani `thumbial/`.
   - Galeria: nazwa folderu **dokładnie jak na dysku**. Jest `4_`, więc piszesz `4_`, a nie `04_`.
4. Sprawdź wynik:
   - czy stara nazwa zgadza się z plikiem (rozszerzenie i wielkość liter mogą się różnić),
   - czy nowa nazwa jest zgodna z pkt 1 (numer, małe litery, bez polskich znaków),
   - czy alt zgadza się ze zdjęciem i ma polskie znaki,
   - czy AI nie wymyśliło imion ani miejsc.

   Zapisz odpowiedź jako `name.md` w katalogu prefiksu (tabela wyżej) i wrzuć do github.

### Prompt do AI (popraw tylko 1. i 2. linię)
```
PREFIKS = gallery/2_sesja_plenerowa_w_parku/
START = 21

Jesteś asystentem SEO i dostępności dla strony fotografki ślubnej i portretowej.
Dla załączonych zdjęć generujesz nową nazwę pliku i tekst alternatywny (alt) po polsku.

Pomiń pliki niebędące zdjęciami (.DS_Store, ._*, .md).
Kolejność: rosnąco po obecnej nazwie pliku.

NOWA NAZWA:
- NN-opis.webp, gdzie NN to kolejny numer od START (pierwsze zdjęcie = START).
- Numer: 3 cyfry gdy PREFIKS = portfolio/, w pozostałych 2 cyfry (np. 07, 21, 104).
- Opis: 6-10 słów, małe litery, bez polskich znaków, słowa łączone "-",
  tylko a-z, 0-9 i "-". Opis streszcza alt.

ALT:
- Opisz to, co widać: kto, co robi, gdzie/tło, ważny detal (światło, kolor, pora dnia).
- Słowa z PREFIKSU to podpowiedź; imiona i miejsca tylko stamtąd,
  z polskimi znakami (np. lazienki krolewskie -> Łazienki Królewskie, lukow -> Łuków).
- Jedno zdanie, 6-14 słów, maks. 120 znaków, wielka litera, BEZ kropki na końcu.
- Czarno-białe -> "Czarno-białe zdjęcie: ...". Dron -> ", ujęcie z drona".
- Nie zaczynaj od "Zdjęcie przedstawia" / "Na zdjęciu".
- Bez marki, emoji, znaków "·" "–" "—" "|"; apostrof ' zamień na ’.
- Każdy alt unikalny.

FORMAT ODPOWIEDZI (ŚCISŁY):
- Tylko wiersze, bez wstępu i bez markdown.
- Każdy wiersz: obecna nazwa pliku | nowa nazwa | alt

PRZYKŁADY WIERSZY:
IMG_1234.webp | 21-kobieta-w-kapeluszu-na-tle-drzew.webp | Kobieta w słomkowym kapeluszu na tle zielonych drzew w parku
DSC_0042.webp | 22-para-lezaca-w-trawie-ujecie-z-drona.webp | Para leżąca w zielonej trawie, ujęcie z drona

Zdjęcie nierozpoznane -> wiersz:
# TODO obecna nazwa pliku: nie rozpoznano

KONTROLA: każdy wiersz ma dokładnie 2 znaki "|", nowe nazwy idą kolejno od START,
żaden wiersz nie zawiera "<", ">" ani słowa "PREFIKS".
```

## 7. Kontrola
- Po przebiegu GitHuba (zakładka Actions) w katalogu jest `name_<data>.md` zamiast `name.md`, a nazwy plików są nowe.
- Liczba nowych wpisów w `altText.ts` = liczba nowych plików w `full/` (dla start: w `start/`).
- W głównym katalogu (`portfolio/`, `gallery/<folder>/`) nie ma już zdjęć, tylko `.md`.
- Zrób `git pull`, bo GitHub dodaje własny commit.

## 8. Automatyczna zmiana nazw (`name.md`)
- `name.md` leży w katalogu prefiksu, razem z nowymi zdjęciami: `start/`, `portfolio/` albo `gallery/<folder>/` (nie w `full/`).
- Wiersz: `stara-nazwa | nowa-nazwa.webp | Alt text`. Dla start można dodać 4. kolumnę z kadrem: `| 30% 50%`.
  - Puste linie i linie zaczynające się od `#` są pomijane.
  - Stara nazwa może mieć dowolne rozszerzenie (np. `IMG_1.jpg` → `15-opis.jpg`); klucz w `altText.ts` zawsze ma `.webp`.
  - Szukanie starej nazwy (bez względu na wielkość liter): najpierw dokładnie taka nazwa, potem ta sama nazwa z `.webp`. Np. `IMG4240.JPG` znajdzie `IMG4240.JPG`, `img4240.jpg`, a jeśli ich nie ma, `IMG4240.webp` / `img4240.webp`. Plik po zmianie zachowuje swoje prawdziwe rozszerzenie.
- Po wrzuceniu do `main` GitHub Action (`.github/workflows/notify-fe.yml`) uruchamia `scripts/apply_names.py`:
  1. sprawdza wszystkie wiersze; przy jakimkolwiek błędzie (brak pliku, zajęta nazwa, zła nazwa, pusty alt) nic nie zmienia i kończy się błędem, a FE nie jest powiadamiane,
  2. zmienia nazwę w głównym katalogu (nowe zdjęcia); jeśli pliku tam nie ma, w `full/` **i** `thumbial/` (już opublikowane zdjęcie); start: w `start/`,
  3. w `altText.ts` dodaje lub podmienia wpis `prefiks + nowa nazwa` i usuwa wpis starej nazwy,
  4. dla start: w `slideFocus.ts` dodaje wpis (4. kolumna albo `50% 50%`); przy zmianie nazwy istniejącego slajdu zachowuje jego kadr,
  5. zmienia `name.md` na `name_<RRRRMMDD-GGMMSS>.md` (tylko `name.md` jest przetwarzany, stare pliki są pomijane),
  6. uruchamia `scripts/convert-images.sh` (pkt 2.3): zdjęcia z głównego katalogu konwertuje do pełnego rozmiaru, kopiuje do `full/` i `thumbial/` i usuwa z głównego katalogu, potem zmniejsza miniatury i za duże WebP; błąd konwersji = brak powiadomienia FE,
  7. robi commit „Apply name.md renames / resize images” (tylko gdy coś się zmieniło) i dopiero potem powiadamia repo FE.
- Lokalny test przed wrzuceniem: `python3 scripts/apply_names.py assets` (zmienia pliki od razu).
