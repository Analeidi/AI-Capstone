# Mina
A quirky chatbot

## Introduction

Chatbots are a prominent topic within AI which draw on natural language processing, natural language generation, and deep learning. They're application ranges from virtual assistants such as Siri and Alexa to commercial use such as the automated chats you find on websites. For our project, we built a chatbot in TensorFlow using deep learning. To create the chatbot, we focused on a type of model called sequence-to-sequence (seq2seq) models. One of the most successful applications of seq2seq models was for the task of Neural Machine Translation (NMT), or translating between languages using neural networks. However, to apply neural networks to natural language, we first need to find a way to turn words into numbers. A NMT program does this by taking in input text and feeding it through an encoder, which converts it into a "thought" vector that represents the text's meaning. That vector is then passed through a decoder to give a translation.

![encoder decoder architecture](encdec.jpg)
*Luong, Bravado, Zhao https://github.com/tensorflow/nmt*

If you think about it, any model that we can use for translation can also be used in a chatbot. By pairing responses together, we train the model to recognize conversational patterns and assosciate inputs with certain outputs. In some ways creating a chatbot is even harder than translation. When translating between languages there is usually only a few correct translations, but when it comes to conversation, there could be hundreds or thousands of possible ways to respond.

## Data

In order to train our chatbot, we need lots of paired response data (e.g. questions and answers). To generate this data, we looked to the popular online forum, Reddit. There is a website called <pushshift.io> that archives all the comments posted on Reddit and allows you to download them by time period, which gave us the data we needed. Now, there are millions of comments that get posted to Reddit everyday and not all of them are very useful. Because we wanted to train the chatbot on good data, we filtered comments to only include those which have a score of at least three (to get better quality comments) and were an acceptable length. In addition, the comments do not list the parent comment they are replying to but only the id of the parent comment, so we have to search for the text of the parent comment. In order to efficiently run the data cleaning process, we inserted the comments into a database as we read through the original text file.

Later, we decided we wanted to combine the Reddit comments with more data to create a more robust chatbot. The [Cornell Movie Dialog Corpus](https://www.cs.cornell.edu/~cristian/Cornell_Movie-Dialogs_Corpus.html) is a collection of conversations from movie scripts which is commonly used to train many chatbots. While the Reddit comments provided interesting responses, the movie dialog was more polished. We opted to use 150,000 reply pairs from each source.


## Models

### BRNN
The first type of seq2seq model we used was a Recurrent Neural Network (RNN). RNNs are useful when dealing with sequence data and we want to remember information about what we have already seen. These networks remember past information by having the nodes that correspond to the previous piece of the sequence feed in to the next nodes.


### Transformer Model
The second seq2seq model that we used was a transformer model. Unlike the BRNN that has to take each word a sentence at a time, a transformer uses parallelization and takes in all words at once, which makes it significantly faster. This transformer's architecture takes in the comment/quesion as an input (bottom left), the reponse as an output (bottom right), which in reality can be thought about as another input, and finally outputs a probability of what the next response word should be.  
![Image](trnsfModel.png ) *From Vaswani et al. in ‘Attention Is All You Need’*\

This architecture has an encoder and decoder, which makes it ideal for translation. In this case though, we are "translating" from a comment/question to a response.  
![Image](encoder-decoder.png) *From Vaswani et al. in ‘Attention Is All You Need’*\

#### Input
To make the comment or question understandable and informative to the model, each word is tokenized and transformed into a number. 
![Image](Tokenized_Sample.png) 

 Even more interestingly, each word that has a close relationship with another will have similar tokens. The embedding space refers to how the tokens will be saved physically closer to each other if they are close in meaning. The following is not from our model but does a good job at demonstrating what embedding space is. 
 ![Image](embedding.png) *Anzor Gozalishvili https://www.anz2.blog/nlp/relations-in-bert-embedding-space/*

 After the input embedding, each word goes through a positional encoding which looks specifically to where the word is positioned at in the phrase and thus provides additional context. 
#### Encoder
The comment/question is now ready for the encoder! The encoder has two layers: the attention layer and the feed forward layer.
##### Multi-Head Attention Layer
The attention model looks at how important each word is in relation to the other words. Hence each word will have its own vector and because it is a multi-head attention layer, it will get an average vector of its importance. 
##### Feed Forward
The feed forward layer changes the form of the attention layer, so that it is acceptable for the coming encoding or decoding block. 
#### Decoder
Before entering the decoder block, the answer (not the comment/question) goes through the same embedding as the input layer where the words are tokenized and then are given a postional encoding. Once it reaches the decoder, it will go through a masked multi-head attention layer, a normal multi-head attention layer, and a feed forward layer. 

##### Masked Multi-Head Attention
The answer goes through the same procedure as the multi-head attention that the comment/question went through, but at this point, the model uses both the answer attention vector and the comment/question attention vector to see what words from the answer relate to that of the comment/question. The reason that there is masking is because the decoder wants to predict what will be the next word in the answer. It can use the previous and current word from the answer as well as all the comment/question words but not the actual answer word. The multi-head attention is similar to this layer but without the masking, and the feed forward layer does tha same thing as it did with the encoder. 


### Final Product

### Conclusion
The results of both of the models
what we could change moving forward
what is out of our control at the moment










Markdown is a lightweight and easy-to-use syntax for styling your writing. It includes conventions for

```markdown
Syntax highlighted code block

# Header 1
## Header 2
### Header 3

- Bulleted
- List

1. Numbered
2. List

**Bold** and _Italic_ and `Code` text

[Link](url) and ![Image](src)
```

For more details see [GitHub Flavored Markdown](https://guides.github.com/features/mastering-markdown/).

### Jekyll Themes

Your Pages site will use the layout and styles from the Jekyll theme you have selected in your [repository settings](https://github.com//AI-Capstone/settings). The name of this theme is saved in the Jekyll `_config.yml` configuration file.

### Support or Contact

Having trouble with Pages? Check out our [documentation](https://docs.github.com/categories/github-pages-basics/) or [contact support](https://github.com/contact) and we’ll help you sort it out.
