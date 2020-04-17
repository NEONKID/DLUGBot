Message API
===========

.. http:post:: /message

   | DLUG 플러스 친구 각 메시지를 응답하는 API 입니다
   | (이 API는 카카오톡 플러스 친구 플랫폼에 정해진 대로 받아옵니다)

   **Example Request**:

   .. code-block:: http

      POST   /message   HTTP/1.1
      Host: example.com
      Accept: application/json
      Content-Type: application/json

      [
         {
            "content": "요청 메시지"
         }
      ]

   **Example Response**:

   .. code-block:: http

      HTTP/1.1 200 OK
      Vary: Accept
      Content-Type: application/json

      [
         {
            "message": {
               "text": "메시지 내용"
            }
         }
      ]

   :reqheader Accept: the response content type depends on :mailheader:`Accept` header of request
   :reqheader Content-Type: this depends on :mailheader:`Accept` header of request

   :statuscode 200: 성공