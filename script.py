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
    parser.add_argument("-f", "--font", default="times", type=str, help="font to use")
    args = parser.parse_args()

    access_token = "x_nSCOcKUKwrG753-sM4DK8HGjs7kEHjJ-pZki5Kt6ja8Ux3sbvYjAKbcPaI4y_v"
    font = (args.font).lower()
    artist = input("Artist: ").strip().lower().title()
    album = input("Album: ").strip().lower().title()
    
    songs = get_album(artist, album, access_token)
    artwork = download_artwork(artist, album, songs[0])
    create_pdf(artist, album, artwork, songs, font)


def get_album(artist, album, access_token):
    # Getting the lyrics for each song from Genius and the artwork URL
    if artist == "" or album == "":
        sys.exit("Invalid Artist/Album")
    try:
        result = Genius(access_token, remove_section_headers=True).search_album(album, artist)
    except:
        sys.exit("Genius Request Error")
    else:
        if result == None:
            sys.exit("No Genius Result")
        songs = []
        for track in result.tracks:
            song = track.song.to_dict()
            song["artwork"] = result.cover_art_url
            song["index"] = track.number
            if not song["index"] == None:
                songs.append(song)
        return songs


def download_artwork(artist, album, song):
    url = song["artwork"]
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


def create_pdf(artist, album, artwork, songs, font):
    # Creating the final PDF with FPPDF
    file_name = f"{artist} - {album}.pdf"
    class PDF(FPDF):
        def header(self):
            if self.page_no() != 1 and os.path.exists("graphics/background_lyrics.png"):
                self.image("graphics/background_lyrics.png", x=0, y=0, w=210)
            elif os.path.exists("graphics/background_cover.png"):
                pdf.image("graphics/background_cover.png", x=0, y=0, w=210)

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
        if len(song["title"]) > 20 and len(songs) >= (song["index"] + 12):
            pdf.cell(0, 0,  text=f"{song["index"]}. {(song["title"][:20]).upper().strip()}...\n")
        elif len(song["title"]) > 20 and song["index"] > 12:
            pdf.cell(0, 0,  text=f"{song["index"]}. {(song["title"][:20]).upper().strip()}...\n")
        else:
            pdf.cell(0, 0,  text=f"{song["index"]}. {(song["title"]).upper()}\n")
        i += 7

    # Writing the lyrics and removing artwork file
    pdf.set_auto_page_break(auto=True, margin=30)
    for song in songs:
        write_lyrics(pdf, font, song["index"], song["title"], song["lyrics"], song["instrumental"])
    pdf.output(file_name)
    if os.path.exists(artwork):
        os.remove(artwork)


def write_lyrics(document, font, index, title, lyrics, instrumental):
    if not instrumental:
        try:
            document.normalize_text(lyrics)
        except:
            print((f"{index}. {title}:").ljust(50), (f"{'Encoding Error'}").rjust(15))
        else:
            lyrics = "\n".join(lyrics.splitlines()[1:])
            document.add_page()
            document.set_font(font, style="B", size=18)
            document.cell(0, 0, text=title.title(), align="C")
            document.set_xy(30, 50)
            document.set_font(font, style="", size=12)
            document.multi_cell(0, 5, text=lyrics, align="C")
            print((f"{index}. {title}:").ljust(50), (f"{'Done'}").rjust(15))
    else:
        print((f"{index}. {title}:").ljust(50), (f"{'No Lyrics'}").rjust(15))


if __name__ == "__main__":
    main()
