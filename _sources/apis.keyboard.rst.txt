.. _dlugBot_keyboard:

Keyboard API
============

.. http:get:: /keyboard

   DLUG 플러스 친구 초기 로딩시 나타나는 메뉴 API 입니다

   **Example Request**:

   .. code-block:: http

      GET   /keyboard   HTTP/1.1
      Host: example.com
      Accept: application/json, text/javascript

   **Example Response**:

   .. code-block:: http

      HTTP/1.1 200 OK
      Vary: Accept
      Content-Type: application/json

      [
         {
            "type": "buttons",
            "buttons": {
               "Menu 1",
               "Menu 2",
               "Menu 3"
            }
         }
      ]

   :reqheader Accept: the response content type depends on :mailheader:`Accept` header of request
   :reqheader Content-Type: this depends on :mailheader:`Accept` header of request

   :statuscode 200: 성공