def say_hello(request):
        request.full_host = "Fixed in processor : " + request.full_host
        return {'say_hello' : "Hello", }