# DLUG Chatbot Server

![Intro](./img/intro.png)

## Overview

DLUG Chatbot Server is Dankook Linux User Group's Chatting robot, using KakaoTalk Plusfriend
(https://pf.kakao.com/_uxaxjKu/chat)



## How to run

This server application was developed as a Python-based Flask framework. These settings are established at the time when you run from the local and deploy to the cloud.



### Local

```
export APP_SETTINGS="config.DevelopmentConfig"
```



### Azure, Heroku or other cloud services

```
export APP_SETTINGS="config.ProductionConfig"
```



See the config.py more information.



## Build status

[![Build Status](https://travis-ci.org/NEONKID/DLUGBot.svg?branch=master)](https://travis-ci.org/NEONKID/DLUGBot)



## Operation NOTICE

This system is based on PlusFriend, an old chatbot system operated by KakaoTalk (Korea).

However, the system is expected to **end in December 31, 2019.** Therefore, we will notify you that this service may also be terminated if you do not notice it on its own.
