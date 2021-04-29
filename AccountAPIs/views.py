from django.shortcuts import render
from django.shortcuts import redirect

# from .forms import Register,Login #NO forms in APIs, since receives data from external platform (not ours) which has a front-end (form)
from .models import Account
#REST
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .serializers import AccountSerializer, RegisterSerializer, LoginSerializer
import requests #to call apis

accepted_paths=['register','login','update','delete']

#region Helper functions
from hashlib import sha256
import jwt

jwtkey="secret"
algorithm="HS256"
def generateJWToken(serializer):
	token = jwt.encode(serializer.data, jwtkey, algorithm)
	return token
def decodeJWT(token): #If correct token -> decodes data; else Raises invalid signature error
	jsondata = jwt.decode(token, jwtkey, algorithm)
	return jsondata

def hashPassword(plain):
    return sha256(plain.rstrip().encode()).hexdigest()

def createSession(request, token): #save token instead of saving all attributes in plaintext in session
	request.session['jwt'] = token
def deleteSession(request):
	request.session['jwt'] = None
def checkAuth(request):
	isloggedin = 0
	try: #to avoid errors in case invalid signature in decode
		if(request.session['jwt'] != None):
		   decodeJWT(request.session['jwt']) #data isn't collected here but in later functions when called for security
		   isloggedin = 1
	except:
		isloggedin = 0
	return isloggedin
#endregion

#region Front-end
def index(request): #This is not an API since this API should only return data and not render pages
	isloggedin = checkAuth(request)
	return render(request,'index.html', {'isloggedin':isloggedin})

def front_end(request, _path): #Gets all other urls so no need to seperate each front-end function
	if _path not in accepted_paths:
		return redirect('/')
	else: #NOTE: BAD COZ UPDATE AND DELETE DON'T HAVE HTML AND NEED CHECKAUTH
		try: 
			if request.method == 'POST': #prevent letting others like Get access Post Api
				r = requests.post('http://localhost:8000/api-{}'.format(_path), params=request.POST) #Call api
				print(r)
				return render(request, '{}.html'.format(_path), r.json())
			else: #If using other than Post => goto Register page
				return render(request, '{}.html'.format(_path))
		except Exception as e:
			return render(request, 'index.html', {'error':'Cannot connect to api: '+str(e)})

def logout(request): #NOT using _id anymore, just deleting token in session
	deleteSession(request)
	return redirect('/')


def register(request):
	try: 
		if request.method == 'POST': #prevent letting others like Get access Post Api
			r = requests.post('http://localhost:8000/api-register', params=request.POST) #Call api
			print(r)
			return render(request, 'register.html', r.json())
		else: #If using other than Post => goto Register page
			return render(request, 'register.html')
	except Exception as e:
		return render(request, 'index.html', {'error':'Cannot connect to api: '+str(e)})
	# return redirect('/') #better to rerender since also sending an error

def login(request):
	# form = Login(request.POST)
	# userform = form.cleaned_data
	try: 
		if request.method == 'POST': #prevent letting others like Get access Post Api
			r = requests.post('http://localhost:8000/api-login', params=request.POST) #Call api
			return render(request, 'login.html', r.json())
		else: #If using other than Post => goto Login page
			return render(request, 'login.html')
	except Exception as e:
		return render(request, 'login.html', {'error':'Cannot connect to api: '+str(e)})

def deleteUser(request): #NOT using _id anymore since taking that value from sesison var
	if (checkAuth(request)==0): #check if autheticated
		return redirect('/') #Cannot return Response since not using @api here
	else:
		try: 
			if request.method == 'POST': #prevent letting others like Get access Post Api
				r = requests.post('http://localhost:8000/api-delete', params=request.POST) #Call api
				print(r)
				return render(request, 'index.html', r.json())
			else: #If using other than Post => fabricated packet, redirect
				return redirect('/')
		except Exception as e:
			return render(request, 'index.html', {'error':'Cannot connect to api: '+str(e)})
		# return redirect('/') #better to rerender since also sending an error

def userUpdate(request): #NOT using _id anymore since taking that value from sesison var
	if (checkAuth(request)==0): #check if autheticated
		return redirect('/') #Cannot return Response since not using @api here
	else:
		try: 
			if request.method == 'POST': #prevent letting others like Get access Post Api
				r = requests.post('http://localhost:8000/api-update', params=request.POST) #Call api
				print(r)
				return render(request, 'index.html', r.json())
			else: #If using other than Post => fabricated packet, redirect
				return redirect('/')
		except Exception as e:
			return render(request, 'index.html', {'error':'Cannot connect to api: '+str(e)})
		# return redirect('/') #better to rerender since also sending an error
#endregion


@api_view(['POST']) #REQUIRED FOR API TO WORK. Only allow POST method to use django rest framework in this function
def registerAPI(request):
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
		
		# return Response(user.data) #.data for serializers
		token= generateJWToken(user)
		createSession(request, token)
		return Response(token)
	else:
		return Response({'error':'Failed to Register: Data inserted is Invalid'})


@api_view(['POST']) #REQUIRED FOR API TO WORK. Only allow POST method to use django rest framework in this function
def loginAPI(request):
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

			# return Response(user.data) #.data for serializers
			token= generateJWToken(user)
			createSession(request, token)
			return Response(token)
			
		except Exception as e:
			#IF no Account found:
			return Response({'error':'Failed to get user: '+str(e)})
	else:
		return Response({'error':'Failed to Login: Data inserted is Invalid'})


@api_view(['POST']) #REQUIRED FOR API TO WORK. Only allows POST requests to access this function
def userUpdateAPI(request): #NOT using _id anymore since taking that value from sesison var
	if (checkAuth(request)==0): #check if autheticated
		return Response({'error':'Not authenticated'})
		# return redirect('/')
	else:
		userinfo = decodeJWT(request.session['jwt'])
		_id = userinfo['user_id']
	
		try: #avoid invalid id in db (also previously in url)
			user= Account.objects.get(user_id=_id)
			serializer= AccountSerializer(isntance=user, data=request.data)

			if serializer.is_valid():
				serializer.save()
				#Update token in sesison
				# user=Account.objects.get(user_id=_id) #NO NEED to reget updated data SINCE ALREADY IN PREVIOUS SERIALIZER
				# user= AccountSerializer(user, many=False)
				token= generateJWToken(serializer)
				createSession(request, token)
				# return Response(serializer.data)
				return Response({'jwt':token})
			else:
				return Response({'error':'Failed to Update: Data inserted is Invalid', 'jwt':request.session['jwt']}) #Not "token" since not declared in func outside 'if' above
		except Exception as e:
			return Response({'error':'Failed to get user: '+str(e)})

@api_view(['POST']) #REQUIRED FOR API TO WORK. Needed when returning Response
def deleteUserAPI(request): #NOT using _id anymore since taking that value from sesison var from POST in request
	if (checkAuth(request)==0): #check if autheticated
		return Response({'error':'Not authenticated'})
		# return redirect('/')
	else:
		try: #avoid invalid id in db (also previously in url)
			userinfo = decodeJWT(request.session['jwt'])
			_id = userinfo['user_id']
			user=Account.objects.get(user_id=_id)
			user.delete()
			deleteSession(request)
			return Response({'error':None})
		except Exception as e:
			return Response({'error':'Failed to delete user: '+str(e)})

#region For Devs ONLY
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
	except Exception as e:
		return Response({'error':'Failed to get user: '+str(e)})

#endregion