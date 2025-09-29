# send_auto_coaについて
## システム概要
TKT用のCoa自動送信システムです。
### 動作環境
- OS  
    - MacOs
    - Linux(WSL2:Ubunts)
    - Windows11
### 実装言語
- Python3.10 
- ShellScript(zsh)で起動ファイル作る
- Windowsの場合はbatファイル作って起動させる。
### ソースコード
- GitHub Publicリポジトリで公開</br>
### 起動方法
#### Terminalまたはコマンドプロンプトから起動する場合
1. 上記sorceCodeをgitHubから自分のPCの任意のフォルダにfetchする。cloneまたはzipダウンロード。
1. Terminalまたはコマンドプロンプトを起動して、``python main.py``で走ります。 
1. いつ納期分のCoaを送信するか訊かれますので、20250911(2025年9月11日納期の場合)を入力してEnter。
### program動作
```bash
testreport
  |
  |- 輸出
  |   |
  |   |- S7-ABC-M15R-EX_25090555T_2025911_商社A-ﾊﾟｷｽﾀﾝ_AV062.pdf
  |   |- S11-KB-U-EX_25090453T_2025911_広州-会社_C855.pdf
  |   |- S9-U333-TH-R-EX_25090353T_2025911_広州-会社_C855.pdf
  |   |- S11-K3K3A-U-R-EX_25090352T_2025911_広州-会社_C855.pdf
  |   |- S6-V2323L-U-R-EX_25082251T_2025911_商社B-北米office_F250-1.pdf
  |   |- S6-V333B54S-T-R-EX_25090252T_2025911_商社B-北米office_F250-1.pdf
  |   |- S6-V333B54S-T-R-EX_25090253T_2025911_商社B-北米office_F250-1.pdf
  |   |-                              :
  |   |-                              :
  |
  |- zipFiles

        |
        |- 20250911
               |
               |- C855.zip
               |- F250-1.zip
               |
               |- 送信済
```
1. 納入日フォルダが存在しない場合は、営業課ﾌｫﾙﾀﾞ/testreport/輸出/の下に納入日フォルダ(20250911)とその中に送信済フォルダが作られる。
1. 営業課ﾌｫﾙﾀﾞ/testreport/輸出の中にあるcoa.pdfから納入日のcoaを注番ごとにzipにまとめて、納入日フォルダの中に入れられる。
1. coa.pdfが不足していたり、zip化の時に何らかのエラーが起きるとzipファイルは作られない。
1. そして、Email送信でzipファイルが添付されて向け先に送られる。送信に成功したzipファイルは送信済フォルダの中に入れられる。そして、納入日フォルダの中のzipファイルは削除される。
1. 2回目移行に実行すると、送信済フォルダ内のzipファイルから未送信の注番を求めて、zipファイルを作り納入日フォルダに入れる。
3. 再度20250617で成績書を送信した場合、pythonは20250617ディレクトリの中を調べて、送信先とCoaが同じものが存在していたら送信しない。20250617の中に存在しないCoaのみを送信する。
1. 複数のCoaを送信する時はzipファイルにまとめてから送信する
## 仕様書
- 下図はTKTで現行のCoa自動送信システムのクラス図である。<br/>
この実装では、Controlクラスが全ての仕事を請け負っていて、完全に手続き型のProgrammingになってしまっている。codeもクソでメンテしにくいので次のように変更する。<br/>
```mermaid
---
title: TKT send_mail
---
classDiagram
direction TB
class Main{
    + main()
}
class Control{
    + start()
}
class DateManage{
    + get_delivery_date():str
    + get_today():str
}
class FolderManage{
    + create_deli_date_folder():bool
}
class ShipmentInfo{
    - str_today
    - delivery_date
    - isTest
    - all_data
    - mail_infos
    - mukesaki_list
    + get_mail_infos():List<string>
    + get_shipment_list():List<List<string>>
    + get_zip_list():List<string>
}
class CoaPreparation{
    - zip_list
    - deli_date_folder
    + henkan():string
    + list_henkan():List<string>
    + create_zip():List
    + get_zipfile_info():List
    + get_should_send_list():List
}
class ZipCheck{
    - zip_list
    - deli_date_folder
    + henkan():str
    + zip_check():List
}
class MailManage{
    - mail_infos
    + send_mail():List
    + +get_finally_fail_mail():List
}
Main --> Control
Control --> DateManage
Control --> FolderManage
Control --> ShipmentInfo
Control --> CoaPreparation
Control --> ZipCheck
Control --> MailManage
```
---
そこで、TKT send_auto_coa モディファイ版は下図のように設計しなおした。(オブジェクト指向プログラミングっぽい設計)<br/>
Mainクラスから呼び出されたControlクラスはDateManageクラスにCoa送信日と今日の日時をもらう。そしてMailクラスのインスタンスを作る。MailクラスはCustomerクラスのインスタンスのリストを持っており、CustomerクラスはShippingProductクラスのインスタンスのリストを持ち、ShippingProductクラスはCoaのインスタンスをもっている。これで、Mailクラスの送信メソッドを呼び出せば、必要な顧客にCoaを送ってくれる。
should_send_coas = {'AHI832': {'タイ/小糸': [20250930T, 20250921T,...]}, 'AHI855': {'タイ/小糸': [...]} }

```mermaid
---
title: TKT send_auto_coa モディファイ版
---
classDiagram

class Main{
    + main()
}
class Control{
    + start()
}
class FolderManage{
    - isTest: bool
    - delivery_date: str
    - deli_date_path: str
    + get_deli_date_path(): str
    + create_deli_date_folder()
    + create_sent_folder()
}
class UserInterface{
    + get_isTest(): bool
    + get_delivery_date(): str
}
class OrderNoShouldSend{
    - export_paints: List~List~str~~
    - mail_infos: List~List~str~~
    - destinations: List~str~
    - sent_order_nos: List~List~str~~
    + get_should_send_coas(): Dict[str, Dict[str, List~str~]:
    
}
class ExportPaintList{
    - delivery_date: str
    - all_data: List~List~obj~~
    + get_export_paints(): List~List~str~~
}
class MailInfo{
    - isTest: bool
    - mail_infos: List~List~str~~
    - destinations: List~str~
    + get_mail_infos: List~List~str~~
    + get_destinations: List~str~
}
class SentOrderNoFolder{
    - self.sent_order_nos: List~str~ 
    - self.sent_order_nos_thistime: List~str~
    - sent_folder_path
    + get_sent_order_nos(): List~str~
    + append_sent_order(str)
}
class Henkan{
    + henkan(str): str$
}
class Coa{
    - order_no: str
    - lot: str
}
class CoasShouldZip{
    - coas: List~Coa~
    - order_no: str
    - isTest: bool
    - deli_date_folder: str
    - destination: str
    + create_zip()
}
class DeliDateFolder{
    - success_ziped_coas: List~CoasShouldZip~$ 
    + append_ziped_coa(zip: CoasShouldZip)$
    + send_mail(): List~List~str~~
}
class MailManage{
    - isTest: bool
    - mail_infos: List~List~str~~
    + send_mail(str, str, str): List~str~
    - move_successSendZipFiles()
}
Main --> Control
Control --> FolderManage
Control --> UserInterface
Control --> OrderNoShouldSend
OrderNoShouldSend --> ExportPaintList
OrderNoShouldSend --> MailInfo
OrderNoShouldSend --> SentOrderNoFolder
ExportPaintList --> Henkan: call
SentOrderNoFolder --> Henkan: call
Control --> CoasShouldZip
Control --> Coa
Control --> MailManage
Control --> DeliDateFolder: instance
Coa"1" --o "1..*"CoasShouldZip
CoasShouldZip --o DeliDateFolder: 成功したzipのみ入る
MailManage"1" --o "1"DeliDateFolder
```
```mermaid
---
title: TKT send_auto_coa モディファイ版
---
classDiagram
direction LR

class Main{
    + main()
}
class Control{
    + start()
}
class DateManage{
    + get_delivery_date():str
    + get_today():str
}
class Mail{
    - customer_list:List<Customer>
}
class Customer{
    - name:str
    - mail_address:str
    - staff:str
    - cc:str
    - shipping_product_list:ShippingProduct[]
}
class ShippingProduct{
    - hinban:str
    - hinmei:str
    - ireme:float
    - cans:int
    - deliveryDate:int
    - coa:Coa
}
class Coa{
    - hinban:str
    - lotNo:str
    + file_name:str
}
Main --> Control
Control --> DateManage
Control --> Mail
Mail "1" o-- "1..*" Customer
Customer "1" o-- "1..*" ShippingProduct
ShippingProduct "1" o-- "1" Coa
```
## logに残す項目
| 項目 | object    | クラス     |
| :--- | :---:   | :---: |
| delivery_dateに送信が必要なcoa | ExportPaintList    | Control     |
| delivery_dateに送信が必要な注文番号 |  zipfile_info   | Control     |
| 送信が完了している注文番号 |     | Control     |
| 送信が必要な注文番号 | zip_list    | Control     |
| zipに成功した注文番号 | success_zip    | Control     |
| zipに失敗した注文番号 | fail_list    | Control     |
| 送信に成功した注文番号 | success_send_mail   | Control     |
| 送信に失敗した注文番号 | fail_send_mail    | Control     |
| zipまたは送信で失敗した注文番号 | finally_fail_mail    | Control     |



