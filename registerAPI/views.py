from django.shortcuts import render
from django.shortcuts import redirect

# from .forms import Register,Login #NO forms in APIs, since receives data from external platform (not ours) which has a front-end (form)
from .models import Account
#REST
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .serializers import AccountSerializer, RegisterSerializer, LoginSerializer

returntoken=True

#region Helper functions
from hashlib import sha256
import jwt

jwtkey="secret"
algorithm="HS256"
def generateJWToken(serializer):
	token = jwt.encode(serializer.data, jwtkey, algorithm)
	return token
def decodeJWT(token):
	jsondata = jwt.decode(token, jwtkey, algorithm)
	return jsondata

def hashPassword(plain):
    return sha256(plain.rstrip().encode()).hexdigest()
#endregion

def index(request): #Not triggered here since path '/' commented in .urls.py since this API should only return data and not render pages
	# For Visuals, uncomment '' url path in .urls.py so that this function gets triggered
	return render(request,'index.html')

@api_view(['POST']) #REQUIRED FOR API TO WORK. Only allow POST method to use django rest framework in this function
def register(request):
	# form = Register(request.POST)
	# userform = form.cleaned_data
	serializer = RegisterSerializer(data=request.data)
	if serializer.is_valid():
		# serializer.save() #CAN'T, need to hash password
		userform=serializer.data #dictionary containing all fields defined in SerializedModel in .serializers.py
		username = userform['username']
		email = userform['email']
		password = hashPassword(str(userform['password']))
		Account.objects.create(username=username, email=email, password=password)
		
		#PROBLEM, "create" returns value BEFORE autogenerating user_id => get it again
		user=Account.objects.get(username=username, email=email, password=password)
		user= AccountSerializer(user, many=False) #AccountSer NOT RegisterSer since no user_id in RegisterSer so it will not be returned in reponse
		if returntoken:
			token= generateJWToken(user)
			return Response(token)
		else:
			return Response(user.data) #.data for serializers
	else:
		return Response(None)
	# VISUAL:
	# users= Account.objects.all()
	# return render(request, 'register.html', {'users':users, 'form':form})
	

@api_view(['POST']) #REQUIRED FOR API TO WORK. Only allow POST method to use django rest framework in this function
def login(request):
	# form = Login(request.POST)
	# userform = form.cleaned_data
	serializer = LoginSerializer(data=request.data)
	if serializer.is_valid():
		userform=serializer.data
		email = userform['email']
		password = hashPassword(str(userform['password']))
	
		# for user in Account.objects.all(): #WRONG APPROACH
		# 	if user.email==email and user.password==password: 
		try:
			user=Account.objects.get(email=email, password=password)
			# generateJWToken()
			user= AccountSerializer(user, many=False)
			if returntoken:
				token= generateJWToken(user)
				return Response(token)
			else:
				return Response(user.data) #.data for serializers
		except:
			#IF no Account found:
			return Response(None) #No .data since here not serializer, just data
	else:
		return Response(None)
	# VISUAL:
	# return render(request, 'login.html', {'user':user, 'form':form})


def logout(request, _id):
	return redirect('/')

@api_view(['GET']) #REQUIRED FOR API TO WORK. Only allows GET requests to access this function
def getAll(request):
	users=Account.objects.all()
	users= AccountSerializer(users, many=True) #If empty, returns empty list
	return Response(users.data) #.data for serializers

@api_view(['GET']) #REQUIRED FOR API TO WORK. Only allows GET requests to access this function
def getUser(request, _id):
	try:
		user=Account.objects.get(user_id=_id)
		user= AccountSerializer(user, many=False)
		return Response(user.data) #.data for serializers
		# return render(request, 'register.html', {'user':user})
	except:
		return Response(None) #if empty, returns None


@api_view(['POST']) #REQUIRED FOR API TO WORK. Only allows POST requests to access this function
def userUpdate(request,_id):
	try: #in case invalid id in url
		user= Account.objects.get(user_id=_id)
		serializer= AccountSerializer(isntance=user, data=request.data)

		if serializer.is_valid():
			serializer.save()
		return Response(serializer.data)
	except:
		return Response(None)

#No need for @api_view since doesn't return Response nor use API functions
def deleteUser(request, _id):
	try: #avoid invalid id in url
		user=Account.objects.get(user_id=_id)
		user.delete()
	except:
		pass
	return redirect('/')


# class isPermitted(APIView):
# 	permission_classes = (IsAuthenticated)
	
# 	def get(self, request):
# 		content = {'message': 'Hello, World!'}
# 		return Response(content)
