from rest_framework.response import Response
from rest_framework.views import APIView


class RegisterView(APIView):
    def post(self, request):
        data = request.POST
        username = data.get('username')
        password = data.get('password')
        user = {"username": username, "password": password}
        return Response(user)
