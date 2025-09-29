import mojimoji

class Henkan():

    @staticmethod
    def henkan(word: str)-> str:
        """
         半角￥、全角の空白を削除、
         小文字を大文字に統一する関数
        """
        word = word.replace(" ", "")
        word = word.replace("　", "")
        word = mojimoji.zen_to_han(word)
        word = word.upper()
        return word
