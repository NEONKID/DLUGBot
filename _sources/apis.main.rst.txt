Main API
========

.. http:get:: /

   DLUGBot 최상위 엔드포인트 입니다

   **Example Request**:

   .. code-block:: http

      GET   /  HTTP/1.1
      Host: example.com
      Accept: application/json, text/javascript

   **Example Response**:

   .. code-block:: http

      HTTP/1.1 200 OK
      Vary: Accept
      Content-Type: text/javascript

      [ "hello D.L.U.G Chat Bot Server" ]

   :reqheader Accept: the response content type depends on :mailheader:`Accept` header of request
   :reqheader Content-Type: this depends on :mailheader:`Accept` header of request

   :statuscode 200: 성공