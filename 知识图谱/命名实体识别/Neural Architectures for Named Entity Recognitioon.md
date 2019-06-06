## Neural Architectures for Named Entity Recognitioon

本文提出了两个方法用于命名实体识别

一种是双向LSTM+CRF, 一种是Transition-Based Chunking Model(基于Stack-LSTM)

双向LSTM+CRF理解了，Transition-Based Chunking Model深层次的原理感觉必须实现才能掌握

双向LSTM+CRF的框架如下

![](https://raw.githubusercontent.com/zyxdSTU/Image/master/NER.PNG)

需要说明的几点

作者说明在Bi-LSTM输出和CRF Layer加入一层隐层，可以有效得提高方法的性能。

#### 词嵌入

![](https://raw.githubusercontent.com/zyxdSTU/Image/master/NER2.PNG)

词嵌入的神经网路架构如下

1. 随机初始化一张查找表，包含所有字符的字向量

2. 经过双向LSTM输入基于字符的词嵌入结果，再和预训练的基于词的词嵌入结果组合

   作为词的输入 。