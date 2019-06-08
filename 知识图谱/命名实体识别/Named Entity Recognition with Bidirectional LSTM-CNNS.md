## Named Entity Recognition with Bidirectional LSTM-CNNS

本论文提出了一种LSTM-CNNs的神经网络框架，用于做命名实体识别。下面详细介绍一下框架的细节

1. **CNN用来提取词中的字符级特征**(英文中一般是前缀信息、后缀信息)，也就是对字符进行编码

   结构入下图，一开始随机初始化一张所有字符的向量查找表。查找单词对应的字符向量,作为CNN

   的输入，之后分别经过卷积、池化得到字符级别的特征。注意到还有一个Type，其实这是对字符

   类型(upper case、lower case、punctuation、other)进行编码区别下文的词类型特征。

   ![](https://raw.githubusercontent.com/zyxdSTU/Image/master/LSTM-CNN1.PNG)

2. **预训练的词向量作为词级特征**。在这里作者使用的是SENNA中形成的50维向量。作者也试了Glove、

   word2vec。**预训练的词向量在训练的时候可以更改,而不是frozen**

3. **提取词大小写特征**。词嵌入中，大小写信息被丢弃了。所以需要另外对大小写特征进行编码，

   大小写分为四种类型allCpas, upperInitial, lowercase,mixedCaps, noinfo.

4. 词汇特征(Lexicon Features)

   作者不仅考虑了以上几种特征，也考虑了外部的词汇特征。作者从DBpedia中提取了所有与实验语料同类别(Person、Organization、Location、Miscellaneous)的命名实体，然后对每个句子用n-gram方法对DBpedia中每一个类别的实体库进行匹配进行部分匹配(partialmatch),具体得匹配规则可以看论文中的描述，匹配到的结果打上相应的命名实体Tag。一个简单的例子。比如句子中的China就是匹配了Location类实体库中的实体China.Japanese就是匹配了MISC类实体库中的实体(词Japanese出现在实体的中间)。

   ![](https://raw.githubusercontent.com/zyxdSTU/Image/master/LSTM-CNN2.PNG)

5. 总体的神经网络结构如下

   ![](https://raw.githubusercontent.com/zyxdSTU/Image/master/LSTM-CNN3.PNG)

6. 在总的神经网络图简化了Output Layers.其详细的结构如下，经过线性层，log-softmax层，最后相加得到

   最后的输出

   ![](https://raw.githubusercontent.com/zyxdSTU/Image/master/LSTM-CNN4.PNG)

   



文章里面的一些要点

1. 命名实体识别中，输入的句子是变长的，为了能够成批训练，作者首先把语料按照

   句子长度聚集成组。同时在数据预处理的过程中将数字0-9替换成0

2. 其实作者最后还是加上了CRF层，只是没有明确指出来。
3. 作者最后还指明了word2vec框架的缺点。大小写敏感，忽略了符号、标点的信息 。











