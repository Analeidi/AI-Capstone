## Mina

You can use the [editor on GitHub](https://github.com/Analeidi/AI-Capstone/edit/gh-pages/index.md) to maintain and preview the content for your website in Markdown files.

Whenever you commit to this repository, GitHub Pages will run [Jekyll](https://jekyllrb.com/) to rebuild the pages in your site, from the content in your Markdown files.

### Introduction

Chatbots are a prominent topic within AI which draw on natural language processing, natural language generation, and deep learning They're application ranges from virtual assistants such as Siri and Alexa to commercial use such as the automated chats you find on websites. For our project, we built a chatbot in TensorFlow using deep learning. To create the chatbot, we focused on a type of model called sequence-to-sequence (seq2seq) models. One of the most successful applications of seq2seq models was for the task of Neural Machine Translation (NMT), or translating between languages using neural networks. However, to apply neural networks to natural language, we first need to find a way to turn words into numbers. A NMT program does this by taking in input text and feeding it through an encoder, which converts it into a "thought" vector that represents the text's meaning. That vector is then passed through a decoder to give a translation.


### Data



### Models
This is the model architecture of a transformer. It takes in a sequence and outputs a sequence.
![Image](trnsfModel.png = 271x332)
This architecture has an encoder and decoder, which makes it ideal for translation.  
![Image](encoder-decoder.png = 271x332)
This design works well for Neural Machine Translation becuase it can encode a given language and then decode it into another. In this case though, we are "translating" from a question or comment to a response.
 
#### Let us first focus on the encoder
##### Input
Mina will take in a sequence of strings. However, we want to make this input be both understandable and informative. Hence, each word is tokenized and transformed into a number. Even more interestingly, each word that has a close relationship with another will have similar tokens. The embedding space refers to how the tokens will be saved physically closer to each other if they are close in meaning. Each word also goes through a positional encoding which gives context based on where the word is positioned at in the phrase.

##### Attention 
##### Feed Forward

#### Decoder










### Final Product

### Conclusion










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
