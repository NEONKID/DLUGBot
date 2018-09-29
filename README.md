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



