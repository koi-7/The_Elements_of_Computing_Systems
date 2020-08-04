# 9章 高水準言語

## HelloWorld/Main.jack のコンパイルから実行まで

java がない場合は事前に入れておく

```
$ sudo apt install openjdk-8-jdk
```

```tools/OS/``` ディレクトリ内の .vm ファイルをコンパイルしたい .jack ファイルがあるディレクトリにコピーしておく

```
tools$ cp ./OS/*.vm ../projects/09/HelloWorld/
tools$ ls ../projects/09/HelloWorld/
Array.vm     Main.jack  Math.vm    Output.vm  String.vm
Keyboard.vm  Main.vm    Memory.vm  Screen.vm  Sys.vm
```

コンパイルを行う

```
tools$ ./JackCompiler.sh ../projects/09/HelloWorld/
```

これで main.vm ファイルが作成されるので VM エミュレータで動作を確認する

![](https://user-images.githubusercontent.com/61448492/89265851-14b04900-d670-11ea-9dd0-5b64a4d47f1b.jpg)
