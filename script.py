#!./venv/bin/python3
from lyricsgenius import Genius
from fpdf import FPDF
import requests
import argparse
import json
import sys
import os


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--font", default="dejavusans", type=str, help="font to use")
    args = parser.parse_args()

    access_token = "x_nSCOcKUKwrG753-sM4DK8HGjs7kEHjJ-pZki5Kt6ja8Ux3sbvYjAKbcPaI4y_v"
    font = (args.font).lower()

    try:
        artist = input("Artist: ").strip().lower().title()
        album = input("Album: ").strip().lower().title()
    except EOFError:
        sys.exit("Script Interruption")

    songs = get_album(artist, album, access_token)
    artwork = download_artwork(songs)
    create_pdf(artwork, songs, font)

def get_album(artist, album, access_token):
    """
    Gets the lyrics for each song from Genius and the artwork URL.

    Parameters:
    artist (string): name of the artist
    album (string): name of the album
    access_token (string): Genius API access token

    Return:
    list: list of dictionnaries containing song information
    """
    if artist == "" or album == "":
        sys.exit("Invalid Artist/Album")
    try:
        result = Genius(access_token, remove_section_headers=True).search_album(album, artist)
    except:
        sys.exit("Genius Request Error")
    else:
        if result is None:
            sys.exit("No Genius Result")
        songs = []
        for track in result.tracks:
            song = track.song.to_dict()
            song["artwork"] = result.cover_art_url
            song["index"] = track.number
            song["album"] = album
            if not song["index"] is None:
                songs.append(song)
        return songs


def download_artwork(songs):
    """
    Gets the album artwork from URL and saves it as JPG image file.

    Parameters:
    songs (list): list of dictionnaries containing song information

    Return:
    string: path to the artwork image file
    """
    artist = songs[0]['artist']
    album = songs[0]['album']
    url = songs[0]["artwork"]
    try:
        response = requests.get(url)
    except requests.HTTPError:
        sys.exit("Artwork Request Error")
    except requests.exceptions.MissingSchema:
        sys.exit("Invalid Artwork URL")
    else:
        artwork = f"{artist.title()} - {album.title()}.jpg"
        with open(artwork, "wb") as file:
            file.write(response.content)
        return artwork


def create_pdf(artwork, songs, font):
    """
    Creates the final PDF using FPDF.
    
    Parameters:
    artwork (string): path to the artwork image file
    songs (list): list of dictionnaries containing song information
    font (string): font to use
    """
    artist = songs[0]['artist']
    album = songs[0]['album']
    file_name = f"{artist} - {album}.pdf"

    class PDF(FPDF):
        def header(self):
            if self.page_no() != 1 and os.path.exists("graphics/background_lyrics.png"):
                self.image("graphics/background_lyrics.png", x=0, y=0, w=210)
            elif os.path.exists("graphics/background_cover.png"):
                pdf.image("graphics/background_cover.png", x=0, y=0, w=210)

    # Setting parameters for PDF file
    pdf = PDF("P", "mm", (210, 297))
    if font not in ["courier", "helvetica", "times"]:
        try:
            pdf.add_font(font.lower(), "", f"./fonts/{font}.ttf")
        except FileNotFoundError:
            sys.exit("Invalid Font")
        try:
            pdf.add_font(font.lower(), "B", f"./fonts/{font}-Bold.ttf")
        except FileNotFoundError:
            pdf.add_font(font.lower(), "B", f"./fonts/{font}.ttf")
    pdf.set_margins(left=30, top=40, right=30)
    pdf.set_text_color(r=178, g=156, b=112)
    pdf.add_page()
    pdf.set_xy(10, 10)
    pdf.image(artwork, x=30, y=30, w=150)

    # Writing the tracklist on the first page
    pdf.set_xy(30, 190)
    pdf.set_font(font, style="B", size=18)
    pdf.cell(0, 0, text=f"{artist.title()} - {album.title()}")
    pdf.set_font(font, style="B", size=12)
    i = 0
    for song in songs:
        if song["index"] < 13:
            pdf.set_xy(30, 200 + i)
        elif song["index"] < 25:
            pdf.set_xy(105, 116 + i)
        else:
            break
        try:
            if len(song["title"]) > 20 and len(songs) >= (song["index"] + 12):
                pdf.cell(0, 0,  text=f"{song["index"]}. {(song["title"][:20]).upper().strip()}...")
            elif len(song["title"]) > 20 and song["index"] > 12:
                pdf.cell(0, 0,  text=f"{song["index"]}. {(song["title"][:20]).upper().strip()}...")
            else:
                pdf.cell(0, 0,  text=f"{song["index"]}. {(song["title"]).upper()}")
        except:
            pdf.cell(0, 0,  text=f"{song["index"]}.\n")
        i+= 7

    # Writing the lyrics and removing artwork file
    pdf.set_auto_page_break(auto=True, margin=30)
    print("")
    for song in songs:
        write_lyrics(pdf, font, song)
    print("")
    pdf.output(file_name)
    if os.path.exists(artwork):
        os.remove(artwork)


def write_lyrics(document, font, song):
    """
    Writes the lyrics of a song on one or more page(s).

    Parameters:
    document (object): PDF document
    font (string): font to use
    song (dictionnary): song information
    """
    index = song['index']
    if len(song['title']) < 45:
        title = song['title'].title()
    else:
        title = song['title'][:40].title() + "..."
    if not song['instrumental']:
        try:
            document.normalize_text(song['lyrics'])
        except:
            print((f"{index}. {title}:").ljust(75), (f"{'Encoding Error'}").rjust(15))
        else:
            lyrics = "\n".join(song['lyrics'].splitlines()[1:])
            document.add_page()
            document.set_font(font, style="B", size=18)
            document.cell(0, 0, text=title, align="C")
            document.set_xy(30, 50)
            document.set_font(font, style="", size=12)
            document.multi_cell(0, 5, text=lyrics, align="C")
            print((f"{index}. {title}:").ljust(75), (f"{'Done'}").rjust(15))
    else:
        print((f"{index}. {title}:").ljust(75), (f"{'No Lyrics'}").rjust(15))


if __name__ == "__main__":
    main()
