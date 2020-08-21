# 11章 コンパイラ#2：コード生成

## 概要

10章で作った構文解析気を拡張し、完全版の Jack コンパイラを完成させる。

## 方針

### 第1段階：シンボルテーブル

プログラム中に出てくる識別子をコンパイラに理解させるためにシンボルテーブルを生成する。

### 第2段階：コード生成

テストプログラムをテキストに記載された順番通りにコンパイルできるようにコンパイラを拡張していく。コンパイルしてできた VM ファイルと OS の VM ファイルをテスト環境にコピーし（例えば以下の通り）、VM エミュレータで期待通りの動作がなされるか確認する。

```
test_dir
  ├ Array.vm
  ├ Keyboard.vm
  ├ Math.vm
  ├ Memory.vm
  ├ Output.vm
  ├ Screen.vm
  ├ String.vm
  ├ Sys.vm
  └ (コンパイラが生成した VM ファイル)
```

## 実装

### 前置き

- テキストによれば VMWriter のコンストラクタの引数はなしになっているが、簡略化のためアウトプットする VM ファイルを引数にとるようにした
- テキストだけではどうしても理解が追いつかなかったのでまず公式で用意されたコンパイラ（tools/JackCompiler.sh）で Jack ファイルをコンパイルし、生成された VM ファイルを参考にコンパイラを書き進めた
- テキストに記載された API の他に、次トークンの存在確認と次トークンの読み込みを同時に行う forward メソッドを記述した

### シンボルテーブル

- 辞書を2つ用意（それぞれサブルーチン用の辞書、クラス用の辞書）し、それらをリストでつなぎ合わせた
  - 例えば Pong/PongGame.jack の moveBall メソッドの部分をコンパイルすると（インデックスの順番はバラバラだが）以下のようなテーブルができる
    ```
    [{'ballLeft': ('int', 'var', 3),
      'ballRight': ('int', 'var', 4),
      'batLeft': ('int', 'var', 1),
      'batRight': ('int', 'var', 2),
      'bouncingDirection': ('int', 'var', 0),
      'this': ('PongGame', 'argument', 0)},
     {'ball': ('Ball', 'field', 1),
      'bat': ('Bat', 'field', 0),
      'batWidth': ('int', 'field', 6),
      'exit': ('boolean', 'field', 3),
      'instance': ('PongGame', 'static', 0),
      'lastWall': ('int', 'field', 5),
      'score': ('int', 'field', 4),
      'wall': ('int', 'field', 2)}]
    ```

### コード生成

#### compileClass

- class をコンパイルする
- className を記憶しておく

#### compileClassVarDec

- classVerDec をコンパイルする
- スタティック変数、フィールド変数があればシンボルテーブルに登録する
- フィールド変数の数を記憶しておく

#### compileSubroutine

- subroutineDec、subroutineBody、subroutineCall をコンパイルする
- subroutineDec、subroutineBody
  - constructor 宣言では Memory.alloc を用いてメモリ領域を確保する
  - method 宣言ではシンボルテーブルへの登録を行い、argument のアドレスを pointer に退避させる
- subroutineCall
  - サブルーチン呼び出しの基本的な規則は p.208 の通り
  - コード生成においては p.257 の手法を用いる
    - method 宣言でのシンボルテーブル登録がここで活きる

#### compileParameterList

- parameterList をコンパイルする
- パラメータの数を記憶しておく
- パラメータがあればシンボルテーブルに登録する

#### compileVarDec

- varDec をコンパイルする
- ローカル変数の数を記憶しておく
- ローカル変数があればシンボルテーブルに登録する

#### compileStatements

- statements をコンパイルする

#### compileDo

- do をコンパイルする
- do 文では返り値は使われないので適当な場所に pop しておく（例えば temp）

#### compileLet

- let をコンパイルする
- let 文では返り値を変数もしくは配列に代入する必要がある
  - 代入先が変数の場合は変数の情報をシンボルテーブルから取得し、値を pop する
  - 代入先が配列の場合
    1. アドレス計算
    2. '=' 後の expression の評価
    3. 計算したアドレスへの pop

    の順番で処理するようにする

    ```
    ///// let a[i] = exp /////

    push ...       // i の評価結果を push
    push ...       // 配列 a の push
    add            // アドレス計算
    push ...       // exp の評価結果を push
    pop temp 0     // exp の結果を temp へ退避
    pop pointer 1  //
    push temp 0
    pop that 0
    ```

#### compileWhile

- while をコンパイルする
- ラベルに付ける番号はリセットせずに実装した
  - label 宣言するたびに低レイヤで番号付けの処理が行われるため、本来はコンパイル時点で番号が重複しても問題ない（はず）

#### compileReturn

- return をコンパイルする
- 返り値がなければ適当な値（ここでは 0）を push する
  - この値は先の do 文で述べた通り、すぐに適当な場所に pop される

#### compileIf

- if をコンパイルする
- ラベルの番号付けは while 文の時と同様

#### compileExpression

- expressoin をコンパイルする
- 乗算または徐算を行うには Math クラスを呼び出す

#### compileTerm

- term をコンパイルする
- 配列の処理は let 文で述べた時と同じ
- stringConstant（文字列）の処理
  - まず文字列の長さを push し、String.new を呼び出すことで文字列の長さ分のメモリ領域が確保される（ものと思われる）
  - ASCII 文字は数値に変換して push し、String.appendChar で先に確保したメモリ領域に詰んでいく（ものと思われる）

#### compileExpressionList

- expressionList をコンパイルする
- 式の数は記憶しておく
  - サブルーチン呼び出しの際に使われる


