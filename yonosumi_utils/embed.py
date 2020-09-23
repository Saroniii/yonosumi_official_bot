from discord import Embed

class SaicaEmbed(Embed):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        try:
            colour = kwargs['colour']
        except KeyError:
            colour = kwargs.get('color', 0x59b9c6)
        self.colour = colour
    

class EmbedUtils:

    @staticmethod
    def link(title :str, url :str):
        """Embed内で使えるURLのMarkdownを返します。"""
        return f"[{title}]({url})"
