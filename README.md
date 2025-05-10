# Versify

Versify is a simple tool generating a neat and nicely designed multipage PDF lyrics booklet for any given album of any given artist, with a first page showing the album artwork and its tracklist.

## 📋 Description

When executed, the user is prompted for an artist name, then an album name. Versify will use the *LyricsGenius* library to search for this album on the [Genius](https://genius.com) website. If found, it will create a list of dictionnaries (one for each song) containing information such as the track number, title, lyrics, and also an URL for the artwork.
This URL will be used to download temporarily the artwork as an image file, that will be automatically deleted later. After this, Versify will use the *FPDF* library to create a PDF file with a first page containing the album artwork and the tracklist. Then, for each song containing lyrics (instrumental songs are ignored), Versify will create one (or more) page(s) and write the song title and its lyrics. Finally, the PDF file is saved locally in the `pdf/` directory, which is automatically created if not existing.

## 📂 Project Structure

The project contains several files and directories, which are the following:

| Files | Description |
| :---- | :---------- |
| [`fonts/`](https://github.com/gwendalminguy/versify/tree/main/fonts) | The directory containing several open source TrueType fonts. |
| [`graphics/`](https://github.com/gwendalminguy/versify/tree/main/graphics) | The directory containing PNG background images. |
| [`requirements.txt`](https://github.com/gwendalminguy/versify/blob/main/requirements.txt) | The text file listing requirements for installation. |
| [`script.py`](https://github.com/gwendalminguy/versify/blob/main/script.py) | The python file containing the script. |

## ⚙️ Installation

In order to install Versify, the three steps of this guide must be followed:

**1. Cloning the repository**

To use Versify, this repository must be cloned locally, using the following command:

```
$ git clone https://github.com/gwendalminguy/versify.git
```

**2. Setting a virtual environment**

Setting a virtual environment is necessary before installing the requirements, and must be done at the root of the Versify directory. This will prevent from installing libraries globally, to avoid potential conflicts. It will also help ensure each library is installed with the right version. Setting a virtual environment can be achieved using the following commands:

```
$ cd versify/
$ python3 -m venv venv
$ source venv/bin/activate
```

**3. Installing the requirements**

In order to work, Versify needs all the libraries from the `requirements.txt` file. They can be installed with the following command:

```
$ pip install -r requirements.txt
```

## 🖥️ Usage

Versify can be launched using the following command:

```
$ ./script.py
```

The user will be prompted for an artist name, then an album name. It can take up to thirty seconds for Versify to find the lyrics and generate the PDF file, please be patient. Once done with Versify, the virtual environment should be disabled:

```
$ deactivate
```

### Fonts:

Although not required, Versify can be launched with a font other than the default one (which is set to be *dejavusans*). To do so, the desired TrueType font must first be installed in the `fonts/` directory. This font can then be used by calling it as a command-line argument with **-f** or **--font**, followed by the name of the font family (without the extension):

```
$ ./script.py -f <font>
```

The `fonts/` directory already contains several usable TrueType fonts, which are the following:

- dejavusans
- dejavuserif
- kinnari
- loma
- norasi
- purisa
- sawasdee
- tlwgtypewriter
- umpush
- waree

It can take a while for Versify to execute, since the *LyricsGenius* library makes several API requests and uses *BeautifulSoup* for web-scraping each song's webpage from [Genius](https://genius.com) to find its lyrics. Once done, the script will print to the terminal, for each song, the song title followed by either **Done** or **No Lyrics** when successful.

The script will print **Encoding Error** if *FPDF* wasn't able to write the lyrics with the chosen font. This problem might come from unsupported characters that can't be handled by the font, and can be solved by replacing it with a TrueType font.

### Graphics:

Versify is provided with a `graphics/` directory containting two background images (`background_cover.png` and `background_lyrics.png`), created with Adobe Illustrator. The Adobe Illustrator file is also included (`background.ai`). If needed, this file can be used to modify these images.

In this case, after modifying the images in Adobe Illustrator, they should be exported as PNG images in the `graphics/` directory to replace the default ones (and named exactly the same). Versify will still work without these images, but the background for the whole final PDF would then be blank.

### Warning:

Although a Genius API Client Access Token is provided in Versify, a new one might be required, and can be generated through [Genius API Client Management](https://genius.com/api-clients/new). A Genius account is needed to create a new API Client. The old Client Access Token can then simply be replaced by the new one by changing the value of the *access_token* variable at the beginning of the *main* function of the `script.py` file.

Because of Genius API restrictions, using a VPN while executing Versify might result in a Forbidden Access Error (403), displaying **Genius Request Error** when *LyricsGenius* searches for the lyrics. For the same reasons, executing Versify from a VPS or a GitHub Codespace might result in the same error. Disabling any VPN and executing Versify from a locally installed IDE such as Visual Studio Code should resolve this problem.

## ⚠️ Disclaimer

Since Versify uses the [Genius](https://genius.com) database to find lyrics and includes them in the final PDF file, the resulting file and its content must be limited to a personnal use only. **Any commercial use of the PDF file would constitute a violation of the [Genius](https://genius.com) conditions of use**, as stated in their [Terms of Service](https://genius.com/static/terms).
