# DepictIt

![depictit_logo](https://github.com/stevelaskaridis/depictit/blob/master/depictIt_logo.png)

## Description

The idea behind this application is to create a game which uses Facebook [Messenger bot](https://messengerplatform.fb.com) as it's frontend and [Google Vision API](https://cloud.google.com/vision/) as its backend to emulate a taboo like game. The aim of the game is to describe to your team the picture without saying the words below it. The team with the most points wins.

This is an Python Django application developed during [HackZurich](http://hackzurich.com) 2016.
 
## Contributors

| Name | github account |
| --- | --- |
| Stefanos Laskaridis | [@stevelaskaridis](https://github.com/stevelaskaridis) |
| Nikolaos Kokkinis Ntrenis | [@nickkok](https://github.com/nickkok) |

## Deployment

To deploy the application, you need an https connection to/from your host and a Facebook account.
We have opted for [Heroku](https://www.heroku.com), which takes care both https traffic and certificates and hosting.
On its backend, it's using the Google's Cloud Vision API in order to get the keywords describing each image. The Messenger bot can be considered as a client frontend for the API.

The application is in a very early age of development but functional.
