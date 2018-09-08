import mimesis.schema as ms


def make_character(seed):
    _ = ms.Field(locale="en", seed=seed)
    ja = ms.Field(locale="ja", seed=seed)
    description = lambda: {
        "id": _("uuid"),
        "name": _("person.full_name"),
        "name_kanji": ja("person.full_name"),
        "name_romaji": _("person.full_name"),
        "avatar": _("person.avatar"),
        "url": _("internet.home_page"),
        "first_appearance_anime": _("numbers.between", minimum=1, maximum=152),
        "first_appearance_manga": _("numbers.between", minimum=1, maximum=999),
    }
    schema = ms.Schema(schema=description)
    character = schema.create(iterations=1)[0]
    return character
