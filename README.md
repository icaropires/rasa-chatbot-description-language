# rasa-chatbot-description-language

[![Build Status](https://travis-ci.com/icaropires/rasa-chatbot-description-language.svg?branch=master)](https://travis-ci.com/icaropires/rasa-chatbot-description-language)

An attempt of crafting a specific purpose language for describing rasa chatbots


## Alert

It's an initial and experimental version, many of the rasa features are still not supported. But any contributions are welcome!


## Features

The goal of the project is to provide a simplified format for rasa training data
merging all the possible features in only one file. Here their format:

### Intents

```
[intent: hello]
> hi
> how are you?
> hey there
```

### Utters

```
[utter: goodbye]
- bye
- hasta la vista
- bis bald
```

### Synonyms

They could be defined inside the content of intents and utters, like this:

```
[intent: programming]
- I love {elm}{lang:C|Python} 
```

or in a separated block:

```
[synonym: elm]
- C
- Python
```

### Entities

They could be defined inside the content of intents and utters, like this:

```
[intent: movies]
- I love {Interstellar}{movie} 
```

### Stories

```
[star-wars]                                                                     
> I don't believe.
- I find your lack of faith disturbing.
```


## Installing

The package is available on pypi, so you can install with:

```
$ pip install rasa_language --user
```


## Executing

First of all, it is needed to have a bot created with [Rasa](https://rasa.com/).
This step is explained [here](https://rasa.com/docs/rasa/user-guide/rasa-tutorial/).

At the root directory of the bot, execute
Na raiz do diretório do bot, execute o


## Contributing

Just open any Issue or Pull Request and we'll be happy to answer!
