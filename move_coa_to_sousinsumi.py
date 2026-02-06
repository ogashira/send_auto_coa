import os
import zipfile
import shutil
from typing import List, Dict
import platform


class MoveCoaToSousinsumi:

    def list_contents_of_zip_files(self, deli_date_path):
        """

    指定されたディレクトリ内のすべてのzipファイルの中身（ファイル名
    ）をリストアップし、
        それらを結合して一つのリストとして返します。

        Args:
            directory_path (str): 検索するディレクトリのパス。

        Returns:
            list:
    すべてのzipファイルから抽出されたファイル名のリスト。

    エラーが発生した場合は、エラーメッセージを含む場合もあります。
        """
        all_filenames = []

        directory_path = f'{deli_date_path}/送信済'
        # 指定されたディレクトリが存在するかチェック
        if not os.path.isdir(directory_path):
            print(f"エラー: 指定されたパス '{directory_path}' はディレクトリではありません。")
            return []

        # ディレクトリツリーをウォークしてzipファイルを探す
        for root, _, files in os.walk(directory_path):
            for file in files:
                if file.endswith(".zip"):
                    zip_filepath = os.path.join(root, file)
                    try:
                        with zipfile.ZipFile(zip_filepath, 'r') as zf:
                            # zipファイル内のファイル名を取得してリストに追加
                            all_filenames.extend(zf.namelist())
                    except zipfile.BadZipFile:
                        print(f"警告: '{zip_filepath}' は不正なzipファイルです。スキップします。")
                    except Exception as e:
                        print(f"エラー: '{zip_filepath}' の処理中に予期せぬエラーが発生しました: {e}")

        return all_filenames


    def move_files_to_sousinsumi(self, filenames_to_move)-> Dict:
        """

    指定されたソースフォルダから、リストに記載されているファイル名を探し、
        それらのファイルを指定されたデスティネーションフォルダに移動します

        Args:
            source_folder (str): ファイルを探す元のフォルダのパス。
            destination_folder (str): ファイルを移動する先のフォルダのパス
            filenames_to_move (list): 移動したいファイル名のリスト (例:
    ["file1.txt", "image.jpg"])。

        Returns:
            dict:
    移動されたファイル、見つからなかったファイル、エラーが発生したファイル
    リストを含む辞書。
        """

        source_folder = r'\\192.168.1.247\共有\営業課ﾌｫﾙﾀﾞ\testreport\輸出'
        destination_folder = r'\\192.168.1.247\共有\営業課ﾌｫﾙﾀﾞ\testreport\輸出\送信済み(Robot)'
        if platform.system() == 'Linux':
            source_folder = r'/mnt/public/営業課ﾌｫﾙﾀﾞ/testreport/輸出'
            destination_folder = r'/mnt/public/営業課ﾌｫﾙﾀﾞ/testreport/輸出/送信済み(Robot)'

        moved_files: List[str] = []
        not_found_files = []
        error_files = []

        print(f"'{source_folder}' から '{destination_folder}' へファイルを移動中...")

        # 移動対象のファイル名をセットに変換して高速検索
        filenames_set = set(filenames_to_move)
        found_and_moved_in_this_run = set() # 今回の実行で移動されたファイルを追跡

        # ソースフォルダをウォークしてファイルを探す
        for file in os.listdir(source_folder):
            if file in filenames_set and file not in found_and_moved_in_this_run:
                source_filepath = os.path.join(source_folder, file)
                destination_filepath = os.path.join(destination_folder, file)

                try:
                    shutil.move(source_filepath, destination_filepath)
                    moved_files.append(file)
                    found_and_moved_in_this_run.add(file) # 移動したファイルを記録
                    # print(f"'{source_filepath}' を '{destination_filepath}' に移動しました。")

                except FileNotFoundError:
                    # これはos.walkで見つかっているので通常は発生しないはずですが、念のため
                    print(f"エラー: 移動元ファイル '{source_filepath}' が見つかりません。")
                    error_files.append(f"{file} (移動元NotFound)")
                except PermissionError:
                    print(f"エラー: '{source_filepath}' を移動する権限がありません。")
                    error_files.append(f"{file} (権限エラー)")
                except Exception as e:
                    print(f"エラー: '{file}' の移動中に予期せぬエラーが発生しました: {e}")
                    error_files.append(f"{file} (予期せぬエラー: {e})")

        # 最終的に見つからなかったファイルを特定
        for filename in filenames_to_move:
            if filename not in found_and_moved_in_this_run:
                not_found_files.append(filename)

        return {
            "moved_files": moved_files,
            "not_found_files": not_found_files,
            "errors": error_files
        }


