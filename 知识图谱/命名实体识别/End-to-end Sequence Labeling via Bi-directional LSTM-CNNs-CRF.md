## End-to-end Sequence Labeling via Bi-directional LSTM-CNNs-CRF

本论文提出了一种利用双向LSTM+CNN+CRF的神经网络框架，实现端到端的序列标注方法。

具体得过程如下

1. 利用CNN提取词的形态学特征(比如词的前缀和后缀)，并将特征编码为特征向量

   ![](https://raw.githubusercontent.com/zyxdSTU/Image/master/CNN.PNG)

2. 利用预训练的方法，获得词的特征向量

   作者试了Random(**随机初始化**),Senna,Word2Vec,Glove发现Glove效果最佳，

   作者解释Word2Vec在NER任务中，性能比Senna,Glove差的原因是word2Vec

   对大小写敏感，并且排除了许多普遍的标记比如标点符号、数字等

3. 字特征和词特征组合作为双向LSTM的输入 

4. 双向LSTM的输出输入到CRF层(我的理解是双向LSTM的输出为每个单词被标记为各个状态的概率向量)

5. 利用维特比算法求出概率最大的路径

总的神经网路框架

![](https://raw.githubusercontent.com/zyxdSTU/Image/master/completeNN.PNG)

#### 优化算法

本文为了提高方法的性能，几乎神经网络优化算法用了个遍

1. Early Stopping
2. Fine Tuning
3. Dropout Training (CNN， LSTM中虚线部分都用了Dropout 方法)

#### 杂项

作者最后在文章中指出，提出的方法在标记OOBV数据(数据既没有出现在训练集也没有出现在嵌入集)的

F1值优于LSTM-CNN, 这在一定程度说明联合CRF的有效性。