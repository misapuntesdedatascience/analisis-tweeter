from textblob import TextBlob
import preprocessor as p
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

import tweepy
from tweepy import OAuthHandler
from tweepy import Stream
from tweepy.streaming import StreamListener
import socket
import json
import string

from time import sleep, strftime

# Configuración de credenciales
consumer_key='xxxxxxx'
consumer_secret='xxxxxxxxx'
access_token ='yyyyyyyy'
access_secret='yyyyyyyy'


class TweetsListener(StreamListener):

  def __init__(self, csocket):
      self.client_socket = csocket


  def on_data(self, data):
    
    try:
        sleep(8)       
        
        msg = json.loads(data) # Create a message from json file
        fecha = msg['created_at']
        print(f'\nFecha: {fecha}\n')
        autor = msg['user']['screen_name']
        print(f'Autor: @{autor}')
        print("\n")       
        print("Tweet: \n")
        if 'retweeted_status' in msg.keys():
            if 'extended_tweet' in msg['retweeted_status']:
                tweet = msg['retweeted_status']['extended_tweet']['full_text']                
                print(tweet)
                print('\nEl tweet completo está en:\n retweeted_status --> extended_tweet')
                             
            else:         
                tweet = msg['retweeted_status']['text']               
                print(tweet)
                print('\nEl tweet completo está en:\n retweeted_status --> text')
               
                        
        elif 'extended_tweet' in msg.keys():
            tweet = msg['extended_tweet']['full_text']                      
            print(tweet) 
            print('\nEl tweet completo está en:\n extended_tweet --> full_text')
         
        
        else:
            tweet = msg['text']                    
            print(tweet) 
            print('\nEl tweet completo está en: text')            
                    
        analysis = TextBlob(p.clean(tweet))


        # Descomentar las dos lineas siguientes para Español
        # analysis_ready = analysis.translate(to='en')
        # y = analysis_ready.sentiment.polarity 
        
        # Descomentar la liena siguiente para Inglés
        y = analysis.sentiment.polarity 
        
        #print(analysis_ready)
        print("\n")
        print(f'Sentiment Analysis:{y}')
        
        print("\n----------------------------")
        return True
        
    except BaseException as e:        
        print("Error on_data: %s" % str(e))
    return True

  def on_error(self, status):
      print(status)
      return True

    
def sendData(c_socket):
  auth = OAuthHandler(consumer_key, consumer_secret)
  auth.set_access_token(access_token, access_secret)

  twitter_stream = Stream(auth, TweetsListener(c_socket), tweet_mode='extended')
  twitter_stream.filter(track=['trump'])

if __name__ == "__main__":
  s = socket.socket()         # Create a socket object
  host = "localhost"     # Get local machine name
  port = 9999                 # Reserve a port for your service.
  s.bind((host, port))        # Bind to the port

  print("Listening on port: %s" % str(port))

  s.listen(5)                 # Now wait for client connection.
  c, addr = s.accept()        # Establish connection with client.

  print("Received request from: " + str(addr ))

  sendData( c )