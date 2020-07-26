# 5章 コンピュータアーキテクチャ

## Memory

![Memory](https://user-images.githubusercontent.com/61448492/88470179-402a8980-cf34-11ea-88c2-257b60e212db.png)

- ```address``` の最上位ビットが 0 なら通常のデータ領域（RAM16K）に、1 ならスクリーン領域（Screen）に書き込む
- 出力の選択も ```address``` から判断
  - ビットの並び方とインデックスの関係に注意（p.326 参照、先人の知恵）
- テストをする際はハードウェアシミュレータ右上の ```View:``` 項目を ```Screen``` に設定する

## CPU

![CPU](https://user-images.githubusercontent.com/61448492/88451277-4ff09200-ce90-11ea-87ad-34897b9343ed.png)

- Jump の分岐は各自いい感じになるように頑張る
- ```instruction``` において ```instruction[15]``` と他ビットの AND をとることで A 命令と C 命令の区別をはっきりさせた

```
And16(a[0]=instruction[15], a[1]=instruction[15], a[2]=instruction[15],
      a[3]=instruction[15], a[4]=instruction[15], a[5]=instruction[15],
      a[6]=instruction[15], a[7]=instruction[15], a[8]=instruction[15],
      a[9]=instruction[15], a[10]=instruction[15], a[11]=instruction[15],
      a[12]=instruction[15], a[13]=instruction[15], a[14]=instruction[15],
      a[15]=instruction[15],
      b=instruction,
      out[15]=inst,
      out[12]=a,
      out[11]=c1, out[10]=c2, out[9]=c3, out[8]=c4, out[7]=c5, out[6]=c6,
      out[5]=d1, out[4]=d2, out[3]=d3,
      out[2]=j1, out[1]=j2, out[0]=j3);
```

## Computer
