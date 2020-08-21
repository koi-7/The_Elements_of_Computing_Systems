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

- テキストによれば VMWriter のコンストラクタの引数はなしになっているが、簡略化のためアウトプットする VM ファイルを引数にとるようにした。
- テキストだけではどうしても理解が追いつかなかったのでまず公式で用意されたコンパイラ（tools/JackCompiler.sh）で Jack ファイルをコンパイルし、生成された VM ファイルを参考にコンパイラを書き進めた。

### シンボルテーブル

- 辞書を2つ用意（それぞれサブルーチン用の辞書、クラス用の辞書）し、それらをリストでつなぎ合わせた。
  - 例えば Pong/PongGame.jack の moveBall メソッドの部分をコンパイルすると（インデックスの順番はバラバラだが）以下のようなテーブルができる。
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
