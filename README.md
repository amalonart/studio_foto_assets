# Zdjęcia na stronie: dodawanie, usuwanie i zmiana (Start, Portfolio, Galeria)

## 0. Gdzie są pliki
- Ścieżki poniżej liczę od katalogu assets:
  ```
  start/                                   slajdy strony głównej (bez miniatur)
  portfolio/full/   portfolio/thumbs/      te same nazwy plików
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
- Miniatura (`thumbs/`, `thumbial/`) musi mieć **dokładnie tę samą nazwę** co pełne zdjęcie w `full/`.

## 2. Dodawanie zdjęć
1. Skopiuj oryginały (jpg/png/heic) do właściwych katalogów:
   - **Start**: `start/`
   - **Portfolio**: te same pliki do `portfolio/full/` **i** do `portfolio/thumbs/`
   - **Galeria, istniejąca sesja**: do `gallery/<folder>/full/` **i** do `thumbial/`
   - **Galeria, nowa sesja**: utwórz `gallery/<N+1>_<nazwa_bez_pl_znakow>/` z `full/`, `thumbial/` i `overview.md`.
     - Najwyższy numer to najnowsza sesja, wyświetlana jako pierwsza.
     - URL to nazwa bez `N_`, z `_` zamienionym na `-`. Nie zmieniaj później nazwy folderu.
     - W `overview.md`: linia 1 to `# Tytuł` (bez spacji na początku), linia 2 to jedno zdanie intro (~120-150 znaków), które służy też jako meta description. Cały plik jest widoczny na stronie.
2. Nazw z aparatu **nie musisz zmieniać ręcznie**. Zrobi to GitHub po wrzuceniu pliku `name.md` (pkt 6 i 8).
   - Ręczna zmiana nazw według pkt 1 nadal działa. Wtedy w pkt 4 i 5 wklejasz wpisy ręcznie.
3. Uruchom skrypt zmieniający rozmiar: `bash convert-images.sh` z katalogu głównego repo.
   - `full` i start: maks. 2048 px, q90. Miniatury: 800 px szerokości, q80. Wynik to WebP z metadanymi copyright.
   - **Skrypt usuwa oryginały**, więc trzymaj kopie gdzie indziej.
   - `DIRS` w skrypcie wskazują na `src/assets/...`. Dla external zmień je na `src/assets_external/...` albo na ścieżki w lokalnym klonie repo assets.
   - Wymaga `imagemagick` i `webp` (cwebp, webpmux).
4. Wygeneruj przez AI plik `name.md` z nowymi nazwami i alt textami (pkt 6), zapisz go w katalogu prefiksu i wrzuć wszystko do github. GitHub zmieni nazwy i uzupełni `altText.ts` (pkt 8).
5. Tylko dla start: każde nowe zdjęcie dostaje wpis w `slideFocus.ts` (domyślnie `'50% 50%'`). Jeśli ludzie nie są na środku kadru, dopisz w `name.md` 4. kolumnę, np. `30% 50%`, albo popraw wartość w `slideFocus.ts` później. Pierwsza wartość to poziome położenie: 0% = lewo, 100% = prawo.


## 3. Usuwanie zdjęć
1. Usuń plik z `full/` (lub `start/`) **i** jego miniaturę z `thumbs/` lub `thumbial/`.
2. Usuń wpis z `altText.ts`. Dla start usuń też wpis z `slideFocus.ts`, jeśli istnieje.
3. Luki w numeracji nie przeszkadzają. Przenumerowanie jest opcjonalne, ale wtedy trzeba zmienić też klucze w `altText.ts` i `slideFocus.ts`.
4. Usunięcie całej sesji: skasuj folder `gallery/<folder>/` i wszystkie jego wpisy `gallery/<folder>/...` w `altText.ts`. Linki, strona sesji i sitemap znikną same.

## 4. Zmiana zdjęć
- **Podmiana zdjęcia przy tej samej nazwie**: usuń stare `.webp` z `full/` i miniatury, wrzuć nowy oryginał pod tą samą nazwą do obu katalogów i uruchom `convert-images.sh`.
  - Skrypt nie nadpisuje istniejących WebP, dlatego najpierw trzeba je usunąć.
  - Jeśli treść zdjęcia się zmieniła, popraw alt.
- **Zmiana kolejności**: zmień prefiks `NN` w `full/` i w miniaturach, potem zaktualizuj klucze w `altText.ts` (i `slideFocus.ts`).
- **Zmiana nazwy pliku**: dodaj wiersz do `name.md` (pkt 8): `stara-nazwa.webp | nowa-nazwa.webp | Alt text`. Albo ręcznie: zmień nazwę w obu katalogach, a w `altText.ts` zmień klucz i w razie potrzeby wartość.
- **Zmiana samego alt textu**: edytuj tylko wartość w `altText.ts`, klucz zostaje bez zmian.
- **Zmiana kadru slajdu na telefonie**: edytuj wartość w `slideFocus.ts`.

## 5. Format `altText.ts`
- Linia: `    'KLUCZ': 'Alt text',` z 4 spacjami wcięcia, pojedynczymi cudzysłowami i przecinkiem na końcu.
- KLUCZ to prefiks katalogu plus nazwa pliku `.webp`, bez `full/`, `thumbs/` ani `thumbial/`.
- Miniatura korzysta z alt textu pełnego zdjęcia.
- Wartość to jedno polskie zdanie z polskimi znakami, bez kropki na końcu, 6-14 słów.
- Brak wpisu oznacza ogólny alt typu „… | zdjęcie N”, co jest złe dla SEO.

## 6. Nazwy i alt texty przez AI → `name.md` (jeden katalog miniatur)
1. Po konwersji wyślij do AI **jeden** katalog miniatur, tylko nowe pliki. Nazwy plików muszą zostać bez zmian (np. `IMG_1234.webp`).
   - galeria: `gallery/<folder>/thumbial/`
   - portfolio: `portfolio/thumbs/`
   - start: nowe pliki z `start/`, bo slajdy nie mają miniatur
2. AI widzi tylko obrazy, a nie folder. Dlatego w 1. linii promptu wpisujesz ręcznie **prefiks** (`PREFIKS = ...`), a w 2. linii **numer pierwszego nowego zdjęcia** (`START = ...`, czyli ostatni numer w katalogu + 1). Przykłady:

   | Wysyłany katalog miniatur | 1. linia promptu | 2. linia | Gdzie zapisać `name.md` |
   | --- | --- | --- | --- |
   | `start/` | `PREFIKS = start/` | `START = 15` | `start/name.md` |
   | `portfolio/thumbs/` | `PREFIKS = portfolio/` | `START = 104` | `portfolio/name.md` |
   | `gallery/2_sesja_plenerowa_w_parku/thumbial/` | `PREFIKS = gallery/2_sesja_plenerowa_w_parku/` | `START = 21` | `gallery/2_sesja_plenerowa_w_parku/name.md` |
   | nowa sesja, np. `gallery/12_sesja_slubna_lukow/thumbial/` | `PREFIKS = gallery/12_sesja_slubna_lukow/` | `START = 1` | `gallery/12_sesja_slubna_lukow/name.md` |

3. Zasady prefiksu:
   - Wpisujesz go ze slashami `/`, z `/` na końcu.
   - Nie wpisuj w nim `full/`, `thumbs/` ani `thumbial/`.
   - Galeria: nazwa folderu **dokładnie jak na dysku**. Jest `4_`, więc piszesz `4_`, a nie `04_`.
4. Sprawdź wynik:
   - czy stara nazwa zgadza się z plikiem znak w znak,
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
- Zrób `git pull`, bo GitHub dodaje własny commit.

## 8. Automatyczna zmiana nazw (`name.md`)
- `name.md` leży w katalogu prefiksu: `start/`, `portfolio/` albo `gallery/<folder>/` (nie w `full/`).
- Wiersz: `stara-nazwa | nowa-nazwa.webp | Alt text`. Dla start można dodać 4. kolumnę z kadrem: `| 30% 50%`.
  - Puste linie i linie zaczynające się od `#` są pomijane.
  - Stara nazwa może mieć dowolne rozszerzenie (np. `IMG_1.jpg` → `15-opis.jpg`); klucz w `altText.ts` zawsze ma `.webp`.
- Po wrzuceniu do `main` GitHub Action (`.github/workflows/notify-fe.yml`) uruchamia `scripts/apply_names.py`:
  1. sprawdza wszystkie wiersze; przy jakimkolwiek błędzie (brak pliku, zajęta nazwa, zła nazwa, pusty alt) nic nie zmienia i kończy się błędem, a FE nie jest powiadamiane,
  2. zmienia nazwę w `full/` **i** w `thumbs/`/`thumbial/` (start: w `start/`),
  3. w `altText.ts` dodaje lub podmienia wpis `prefiks + nowa nazwa` i usuwa wpis starej nazwy,
  4. dla start: w `slideFocus.ts` dodaje wpis (4. kolumna albo `50% 50%`); przy zmianie nazwy istniejącego slajdu zachowuje jego kadr,
  5. zmienia `name.md` na `name_<RRRRMMDD-GGMMSS>.md` (tylko `name.md` jest przetwarzany, stare pliki są pomijane),
  6. robi commit „Apply name.md renames” i dopiero potem powiadamia repo FE.
- Lokalny test przed wrzuceniem: `python3 scripts/apply_names.py assets` (zmienia pliki od razu).
