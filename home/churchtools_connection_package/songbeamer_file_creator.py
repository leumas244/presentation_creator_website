import codecs
FileEncoding = "ISO-8859-15"

def create_a_new_songbeamer_file(event_name: str, event_folder: str) -> str:
    complete_filename = event_folder + event_name + '.col'
    with codecs.open(complete_filename, 'w', FileEncoding) as f:
        f.write("object AblaufPlanItems: TAblaufPlanItems\n  items = <\n  >\nend")

    return complete_filename


def write_in_col(filename, statement):
    with codecs.open(filename, 'r', FileEncoding) as f:
        lines = f.readlines()

    del lines[len(lines) - 1]
    del lines[len(lines) - 1]

    with codecs.open(filename, 'w', FileEncoding) as f:
        for l in lines:
            f.write(l)
        f.write(statement)
        f.write('\n  >\nend')


def add_item_state(filename, state):
    if state:
        statement = "    item\n      Caption = 'finaler Plan'\n      Color = clBlack\n      BGColor = clGreen\n    end"
    else:
        statement = "    item\n      Caption = 'NICHT finaler Plan'\n      Color = clBlack\n      BGColor = clRed\n    end"

    write_in_col(filename, statement)


def add_item_normal(filename, title):
    title = title.replace("'", "'#39'")
    statement = "    item\n      Caption = '" + title + "'\n      Color = 33023\n    end"

    write_in_col(filename, statement)


def add_item_header(filename, title):
    title = title.replace("'", "'#39'")
    statement = "    item\n      Caption = '" + title + "'\n      Color = clBlack\n      BGColor = 10150353\n    end"

    write_in_col(filename, statement)


def add_item_song(filename, song_path, title):
    title = title.replace("'", "'#39'")
    if song_path == "No File Found":
        statement = "    item\n      Caption = 'NOT FOUND: " + title + "'\n      Color = clBlack\n      BGColor = clRed\n    end"

        write_in_col(filename, statement)
    elif song_path == "No song set":
        statement = "    item\n      Caption = '" + title + " Noch kein Lied gesetzt'\n      Color = clBlack\n      BGColor = clRed\n    end"

        write_in_col(filename, statement)
    else:
        songname = song_path.split('/')

        if len(songname) == 2:
            title = songname[1].replace('.sng', '')
        else:
            title = songname[0].replace('.sng', '')

        title = title.replace("'", "'#39'")
        song_path = song_path.replace("'", "'#39'")

        statement = "    item\n      Caption = '" + title + "'\n      Color = clBlue\n      FileName = '" + song_path + "'\n    end"

        write_in_col(filename, statement)


def add_item_countdown(filename, countdown_path):
    countdown_title = \
        countdown_path.split("/")[len(countdown_path.split("/")) - 1].split(".")[0]

    statement = "    item\n      Caption = '" + countdown_title + "'\n      Color = clRed\n      FileName = '" + countdown_path + "'\n    end"

    write_in_col(filename, statement)


def add_item_vaterunser(filename, title):
    title = title.replace("'", "'#39'")
    statement = "    item\n      Caption = '" + title + "'\n      Color = 33023\n    end" \
                                                        "    item\n      Caption = 'Vaterunser'\n      Color = 16750652\n      FileName = 'Ev. Gesangsbuch (alle)\Vater unser.sng'\n    end"

    write_in_col(filename, statement)