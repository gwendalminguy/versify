# Versify

Versify generates a neat and nicely designed multipage PDF lyrics booklet for any given album of any given artist, with a first page showing the album artwork and tracklist.

## Description

When executed, the user is prompted for an artist name, then an album name. The first function (*get_album*) uses the *LyricsGenius* package to search for this album on the Genius.com website.
If found, it will return a list of dictionnaries (one for each song) containing information such as the track number, title, lyrics, and also an URL for the artwork.
The second function (*download_artwork*) uses this URL to download temporarily the artwork as an image file, that will be automatically deleted later.
The third function (*create_pdf*) uses the *FPDF* package to create a PDF file with a first page containing the album artwork and the tracklist. Then, for each song containing lyrics (instrumental songs are ignored), the fourth function (*write_lyrics*) is called to create one (or more) page(s) and write the song title and its lyrics. Finally, the PDF file is saved locally.

## Usage

### Fonts:

Although not required, Versify can be executed with a font other than the default one. To do so, the desired TTF font must first be installed in the *fonts* directory. This font can then be used by calling it as a command-line argument with **-f** or **--font**, followed by the name of the font family (without the extension):

```
python project.py -f dejavusans
```
or
```
python project.py --font dejavusans
```

It can take up to thirty seconds for Versify to execute, since the *LyricsGenius* package makes several API requests and uses *BeautifulSoup* for web scraping each song webpage from Genius.com to find its lyrics. Once done, the script will print for each song the song title followed by either **Done** or **No Lyrics** when successful.

The script will print **Encoding Error** if *FPDF* wasn't able to write the lyrics with the chosen font. This problem might come from unsupported characters that can't be used by the *FPDF* built-in fonts, and can be solved by using a Unicode font by specifying its name as a command-line argument.

### Graphics:

Versify is provided with a *graphics* directory containting two background images (named *background_poster.png* and *background_lyrics*.png), created with Adobe Illustrator. The Adobe Illustrator file is also included (named *background.ai*). If needed, this file can be used to modify these images.

If so, after modifying the images in Adobe Illustrator, they should be exported as PNG images in the *graphics* directory to replace the default ones (and named exactly the same). Versify will still work without these images, but the background for the whole final PDF will then be blank.

### Warning:

Although a Genius API Client Access Token is provided in Versify, a new one might be required, and can be generated through [Genius API Client Management](https://genius.com/api-clients/new). A Genius account is needed to create a new API Client. The old Client Access Token can then simply be replaced by the new one by changing the value of the *access_token* variable in the *main* function of Versify.

Because of Genius API restrictions, using a VPN while executing Versify might result in a Forbidden Access Error (403), displaying **Genius Request Error** when *LyricsGenius* searches for the lyrics. For the same reasons, executing Versify from a VPS or a GitHub Codespace might result in the same error. Disabling any VPN and executing Versify from a locally installed IDE such as Visual Studio Code should resolve this problem.

## Disclaimer

Since Versify uses Genius.com database to find lyrics and includes them in the final PDF file, the resulting file and its content must be limited to a personnal use only. **Any commercial use of the PDF file would constitute a _violation_ of the Genius.com conditions of use**, as stated in their [Terms of Service](https://genius.com/static/terms).
