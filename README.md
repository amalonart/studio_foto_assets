# Zdjęcia na stronie: dodawanie, usuwanie i zmiana (Start, Portfolio, Galeria)

## 0. Gdzie są pliki
- Ścieżki poniżej liczę od katalogu assets:
  ```
  start/                                   slajdy strony głównej (bez miniatur)
  portfolio/full/   portfolio/thumbs/      te same nazwy plików
  gallery/<N>_<sesja>/full/  thumbial/  overview.md
  altText.ts                               opisy alt
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
2. Zmień nazwy plików według pkt 1. Numerację kontynuuj od ostatniego pliku. Wstawienie zdjęcia w środek oznacza przenumerowanie kolejnych.
3. Uruchom skrypt zmieniający rozmiar: `bash convert-images.sh` z katalogu głównego repo.
   - `full` i start: maks. 2048 px, q90. Miniatury: 800 px szerokości, q80. Wynik to WebP z metadanymi copyright.
   - **Skrypt usuwa oryginały**, więc trzymaj kopie gdzie indziej.
   - `DIRS` w skrypcie wskazują na `src/assets/...`. Dla external zmień je na `src/assets_external/...` albo na ścieżki w lokalnym klonie repo assets.
   - Wymaga `imagemagick` i `webp` (cwebp, webpmux).
4. Wygeneruj alt texty przez AI (pkt 6) i wklej je do `altText.ts` (pkt 5).
5. Tylko dla start: jeśli ludzie nie są na środku kadru, dodaj wpis do `slideFocus.ts`, np. `'03-opis.webp': '30% 50%'`. Pierwsza wartość to poziome położenie: 0% = lewo, 100% = prawo.
6. Sprawdź lokalnie: `npm run dev` (strona Start, Portfolio, Galeria, sesja, linki na Start i O mnie), potem `npm run build`, który musi przejść.
7. Commit i push. Repo assets: merge do `main` uruchamia auto deploy. Internal: push do `master`.

## 3. Usuwanie zdjęć
1. Usuń plik z `full/` (lub `start/`) **i** jego miniaturę z `thumbs/` lub `thumbial/`.
2. Usuń wpis z `altText.ts`. Dla start usuń też wpis z `slideFocus.ts`, jeśli istnieje.
3. Luki w numeracji nie przeszkadzają. Przenumerowanie jest opcjonalne, ale wtedy trzeba zmienić też klucze w `altText.ts` i `slideFocus.ts`.
4. Usunięcie całej sesji: skasuj folder `gallery/<folder>/` i wszystkie jego wpisy `gallery/<folder>/...` w `altText.ts`. Linki, strona sesji i sitemap znikną same.
5. Uruchom `npm run build`, potem commit i push.

## 4. Zmiana zdjęć
- **Podmiana zdjęcia przy tej samej nazwie**: usuń stare `.webp` z `full/` i miniatury, wrzuć nowy oryginał pod tą samą nazwą do obu katalogów i uruchom `convert-images.sh`.
  - Skrypt nie nadpisuje istniejących WebP, dlatego najpierw trzeba je usunąć.
  - Jeśli treść zdjęcia się zmieniła, popraw alt.
- **Zmiana kolejności**: zmień prefiks `NN` w `full/` i w miniaturach, potem zaktualizuj klucze w `altText.ts` (i `slideFocus.ts`).
- **Zmiana nazwy pliku**: zmień nazwę w obu katalogach, a w `altText.ts` zmień klucz i w razie potrzeby wartość.
- **Zmiana samego alt textu**: edytuj tylko wartość w `altText.ts`, klucz zostaje bez zmian.
- **Zmiana kadru slajdu na telefonie**: edytuj wartość w `slideFocus.ts`.

## 5. Format `altText.ts`
- Linia: `    'KLUCZ': 'Alt text',` z 4 spacjami wcięcia, pojedynczymi cudzysłowami i przecinkiem na końcu.
- KLUCZ to prefiks katalogu plus nazwa pliku `.webp`, bez `full/`, `thumbs/` ani `thumbial/`.
- Miniatura korzysta z alt textu pełnego zdjęcia.
- Wartość to jedno polskie zdanie z polskimi znakami, bez kropki na końcu, 6-14 słów.
- Brak wpisu oznacza ogólny alt typu „… | zdjęcie N”, co jest złe dla SEO.

## 6. Alt texty przez AI (jeden katalog miniatur)
1. Po konwersji wyślij do AI **jeden** katalog miniatur. Nazwy plików muszą zostać bez zmian.
   - galeria: `gallery/<folder>/thumbial/`
   - portfolio: `portfolio/thumbs/`, najlepiej tylko nowe pliki
   - start: nowe pliki z `start/`, bo slajdy nie mają miniatur
2. AI widzi tylko obrazy, a nie nazwę folderu. Dlatego **prefiks wpisujesz ręcznie** w 1. linii promptu (`PREFIKS = ...`) według tabeli:

   | Wysyłany katalog miniatur | 1. linia promptu | Przykładowy klucz |
   | --- | --- | --- |
   | `start/` | `PREFIKS = start/` | `start/03-para-lezaca-w-trawie-ujecie-z-drona.webp` |
   | `portfolio/thumbs/` | `PREFIKS = portfolio/` | `portfolio/106-para-na-plazy-ujecie-z-drona.webp` |
   | `gallery/1_sesja_kobieca_spotkanie_z_julia/thumbial/` | `PREFIKS = gallery/1_sesja_kobieca_spotkanie_z_julia/` | `gallery/1_sesja_kobieca_spotkanie_z_julia/05-julia-na-schodach.webp` |
   | `gallery/2_spotkanie_z_artystka_paula_smyk/thumbial/` | `PREFIKS = gallery/2_spotkanie_z_artystka_paula_smyk/` | `gallery/2_spotkanie_z_artystka_paula_smyk/01-sylwetka-pauli-smyk-na-tle-obrazu-z-kobieca-twarza-i-zlotem.webp` |
   | `gallery/3_sesja_rodzinno_brzuszkowa/thumbial/` | `PREFIKS = gallery/3_sesja_rodzinno_brzuszkowa/` | `gallery/3_sesja_rodzinno_brzuszkowa/07-rodzice-z-corka-na-lace.webp` |
   | `gallery/4_sesja_slubna_lazienki_krolewskie/thumbial/` | `PREFIKS = gallery/4_sesja_slubna_lazienki_krolewskie/` | `gallery/4_sesja_slubna_lazienki_krolewskie/41-para-mloda-na-moscie.webp` |
   | nowa sesja, np. `gallery/5_sesja_slubna_lukow/thumbial/` | `PREFIKS = gallery/5_sesja_slubna_lukow/` | `gallery/5_sesja_slubna_lukow/01-para-mloda-w-parku.webp` |

3. Zasady prefiksu:
   - Wpisujesz go ze slashami `/`, z `/` na końcu.
   - Nie wpisuj w nim `full/`, `thumbs/` ani `thumbial/`.
   - Galeria: nazwa folderu **dokładnie jak na dysku**. Jest `4_`, więc piszesz `4_`, a nie `04_`.
4. Sprawdź wynik:
   - czy opis zgadza się ze zdjęciem i ma polskie znaki,
   - czy AI nie wymyśliło imion ani miejsc,
   - czy klucze zgadzają się z nazwami plików,
   - czy jest format z pkt 5.

   Potem wklej linie przed `}` w `altText.ts`. Jeśli zdjęcie ma już wpis, podmień tylko tekst za dwukropkiem.

### Prompt do AI (popraw tylko 1. linię)
```
PREFIKS = gallery/2_spotkanie_z_artystka_paula_smyk/

Jesteś asystentem SEO i dostępności dla strony fotografki ślubnej i portretowej. Generujesz teksty alternatywne (alt)
po polsku dla załączonych zdjęć.

KLUCZ = PREFIKS (dokładnie jak w 1. linii) + nazwa pliku bez zmian, rozszerzenie .webp.
Pomiń pliki niebędące zdjęciami (.DS_Store, ._*, .md).

ALT:
- Opisz to, co widać: kto, co robi, gdzie/tło, ważny detal (światło, kolor, pora dnia).
- Słowa z PREFIKSU i z nazwy pliku to podpowiedź; imiona i miejsca tylko stamtąd,
  z polskimi znakami (paula smyk -> Paula Smyk, lazienki krolewskie -> Łazienki Królewskie).
- Jedno zdanie, 6-14 słów, maks. 120 znaków, wielka litera, BEZ kropki na końcu.
- Czarno-białe -> "Czarno-białe zdjęcie: ...". Dron -> ", ujęcie z drona".
- Nie zaczynaj od "Zdjęcie przedstawia" / "Na zdjęciu".
- Bez marki, emoji, znaków "·" "–" "—"; apostrof ' zamień na ’.
- Każdy alt unikalny.

FORMAT ODPOWIEDZI (ŚCISŁY):
- Tylko linie kodu, rosnąco po nazwie pliku, bez wstępu i bez markdown.
- Każda linia: 4 spacje, 'pełny klucz': 'alt', z przecinkiem na końcu.

PRZYKŁADY GOTOWYCH LINII (różne prefiksy):
    'start/03-para-lezaca-w-trawie-ujecie-z-drona.webp': 'Para leżąca w zielonej trawie, ujęcie z drona',
    'portfolio/106-para-na-plazy-ujecie-z-drona.webp': 'Para leży na piaszczystej plaży nad morzem, ujęcie z drona',
    'gallery/2_spotkanie_z_artystka_paula_smyk/01-sylwetka-pauli-smyk-na-tle-obrazu-z-kobieca-twarza-i-zlotem.webp': 'Sylwetka Pauli Smyk malującej kobiecą twarz ze złotym pasem na płótnie',
    'gallery/4_sesja_slubna_lazienki_krolewskie/41-para-mloda-na-moscie.webp': 'Para młoda na kamiennym moście w Łazienkach Królewskich',

Zdjęcie nierozpoznane -> linia:
    // TODO 'pełny klucz': nie rozpoznano

KONTROLA: każdy klucz zaczyna się od PREFIKSU z 1. linii, żadna linia nie zawiera
"<", ">" ani słowa "PREFIKS", każda zaczyna się od 4 spacji i kończy przecinkiem.
```

### Naprawa, gdy AI zwróci `<PREFIKS>` albo zły format
Zapisz odpowiedź AI do pliku `ai.txt` i uruchom komendę z właściwym prefiksem:
```bash
sed -E "s#<PREFIKS>#gallery/2_spotkanie_z_artystka_paula_smyk/#; s#^ *'#    '#; s#'\$#',#" ai.txt
```
Ta komenda podmienia prefiks, ustawia 4 spacje i dopisuje brakujący przecinek.

## 7. Kontrola po wklejeniu
- Liczba nowych wpisów w `altText.ts` = liczba nowych plików w `full/` (dla start: w `start/`).
- Klucz ma się zgadzać z nazwą pliku znak w znak, z prefiksem i rozszerzeniem `.webp`.
- `npm run build` musi przejść. W devtools sprawdź, czy przy żadnym zdjęciu nie ma ogólnego alt „| zdjęcie N”.
- Commit i push: repo assets (merge do `main`) albo to repo (push do `master`) przy `internal`.

