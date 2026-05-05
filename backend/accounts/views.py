from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import update_session_auth_hash
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from .serializers import UserRegistrationSerializer, PasswordUpdateSerializer, EmailUpdateSerializer


class UserRegistrationView(APIView):
	permission_classes = [permissions.AllowAny]

	def post(self, request):
		serializer = UserRegistrationSerializer(data=request.data)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data, status=status.HTTP_201_CREATED)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PasswordUpdateView(APIView):
	permission_classes = [permissions.IsAuthenticated]

	def put(self, request):
		user = request.user
		serializer = PasswordUpdateSerializer(data=request.data)
		if serializer.is_valid():
			if not user.check_password(serializer.data.get("old_password")):
				return Response({"old_password": "Wrong password."}, status=status.HTTP_400_BAD_REQUEST)
			user.set_password(serializer.data.get("new_password"))
			user.save()
			update_session_auth_hash(request, user)
			print("Password updated successfully")
			return Response({"detail": "Password updated successfully"},status=status.HTTP_204_NO_CONTENT)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class EmailUpdateView(APIView):
	permission_classes = [permissions.IsAuthenticated]

	def put(self, request):
		user = request.user
		serializer = EmailUpdateSerializer(user, data=request.data)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

