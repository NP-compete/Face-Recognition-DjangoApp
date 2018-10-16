from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import View

from django.shortcuts import render, redirect
from rest_framework.views import APIView
from rest_framework.response import Response

from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.utils.decorators import method_decorator
from django.contrib import messages


from .forms import UserLoginForm, UserRegForm, UserFaceRegForm, UserEditForm, UserProfileForm

from .utils import Base64ToNpImage, TensorflowBridge, Recognizer, DlibBridge

from django.http import JsonResponse


import pickle
# Create your views here.
@method_decorator(login_required, name='get')
class Home(View):
	def get(self,request):
		return render(request,'recognition/home.html')


class LogoutView(View):
	def get(self,request):
		logout(request)
		return redirect('recognition:home')



class UserLoginView(View):
	form_class=AuthenticationForm
	template_name='recognition/login.html'

	def get(self,request):
		form=self.form_class(None)
		messages.info(request, '')
		return render(request,self.template_name,{'form':form})

	def post(self,request):
		form=self.form_class(data=request.POST)

		if form.is_valid():
			# clean normalize data
			username=form.cleaned_data['username']
			password=form.cleaned_data['password']

			#return if credentials are correct

			user=authenticate(username=username,password=password)

			if user is not None:
				if user.is_active:
					login(request, user)
					#TODO Redirect to Face Registration pageß
					return redirect('recognition:home')
			else:
				messages.error(request,'Invalid Username/Password')
		else:
			messages.error(request,'error')
		return render(request,self.template_name,{'form':form})

class UserRegistrationView(View):
	form_class=UserRegForm
	template_name='recognition/register.html'

	def get(self,request):
		form=self.form_class(None)
		return render(request,self.template_name,{'form':form})

	def post(self,request):
		form= self.form_class(request.POST)

		if form.is_valid():
			user=form.save(commit=False)
			# clean normalize data
			username=form.cleaned_data['username']
			password=form.cleaned_data['password']
			user.set_password(password)
			user.save()

			#return if credentials are correct

			user=authenticate(username=username,password=password)

			if user is not None:
				if user.is_active:
					login(request, user)
					#TODO Redirect to Face Registration pageß
					return redirect('recognition:home')
		print('something is wrong')
		return render(request,self.template_name,{'form':form})


@method_decorator(login_required, name='get')
@method_decorator(login_required, name='post')
class UserFaceRegView(View):
	form_class=UserFaceRegForm
	template_name='recognition/settings/reg-face.html'
	base64ToNpImage= Base64ToNpImage()
	tfBridge=DlibBridge()
	recogzr=Recognizer()

	def get(self,request):
		form=self.form_class(None)
		messages.info(request, '')
		return render(request,self.template_name)

	def post(self,request):

		data = request.POST.getlist('imgs[]')
		images= self.base64ToNpImage.decodeArray(data)
		faces = self.tfBridge.imagesToFaces(images,(160,160))
		# return err if no face found
		if len(faces)==0:
			return JsonResponse({'status':'failed'}, status=201)
		else:
			ppFaces=self.tfBridge.preprocessFaces(faces)
			embedded=self.tfBridge.embeddFaces(ppFaces)
			request.user.facesignature.signatures=pickle.dumps(embedded)
			request.user.facesignature.face=data[0]
			request.user.save()
			self.recogzr.train(User.objects.all(),fn=128)
			return JsonResponse({'status':'success'}, status=201)

class UserFaceLogInView(APIView):
	base64ToNpImage= Base64ToNpImage()
	tfBridge=DlibBridge()
	recogzr=Recognizer()

	def post(self,request):
		data = request.POST.getlist('imgs[]')
		images= self.base64ToNpImage.decodeArray(data)
		faces = self.tfBridge.imagesToFaces(images,(160,160))
		# return err if no face found
		if len(faces)==0:
			return JsonResponse({'status':'failed', 'msg':'No face detected'}, status=201)
		else:
			ppFaces=self.tfBridge.preprocessFaces(faces)
			embedded=self.tfBridge.embeddFaces(ppFaces)
			print(type(embedded))
			userIds=self.recogzr.predict(embedded)
			if(len(userIds)==0):
				return JsonResponse({'status':'failed','msg':'User not recognized'}, status=201)
			try:
				user = User.objects.get(id=userIds[0])

				dist = self.recogzr.getDistance(embedded,user)
				print(dist);
				if(dist>0.4):
					return JsonResponse({'status':'failed','msg':'User not recognized'}, status=201)
				# login without password
				user.backend = 'django.contrib.auth.backends.ModelBackend'
				login(request, user)
				return JsonResponse({'status':'success'}, status=201)
			except  User.DoesNotExist:
			   	#handle the case when the user does not exist.
			   	return JsonResponse({'status':'failed', 'msg':'user does not exist'}, status=201)



@method_decorator(login_required, name='get')
@method_decorator(login_required, name='post')
class ProfileSettingsView(UpdateView):
	"""docstring for ProfileSettingsView"""
	form_class=UserFaceRegForm
	template_name='recognition/settings/profile.html'

	def get(self,request):
		user_form = UserEditForm(instance=request.user)
		profile_form = UserProfileForm(instance=request.user.profile)
		messages.info(request, '')
		return render(request, self.template_name, {
		'user_form': user_form,
		'profile_form': profile_form})

	def post(self,request):
		user_form = UserEditForm(request.POST or None, request.FILES or None, instance=request.user)
		profile_form = UserProfileForm(request.POST or None, request.FILES or None, instance=request.user.profile)
		if user_form.is_valid() and profile_form.is_valid():
			user_form.save()
			profile_form.save()
			messages.success(request, 'Your profile was successfully updated!')
			return redirect('recognition:edit-profile')
		else:
			messages.error(request,'Please correct the error below.')

		return render(request, self.template_name, {'user_form': user_form, 'profile_form': profile_form})
# login without password
# user.backend = 'django.contrib.auth.backends.ModelBackend'
# login(request, user)
