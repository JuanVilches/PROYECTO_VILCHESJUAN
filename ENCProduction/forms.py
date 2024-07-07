#acá iran los formularios que vayamos a utilizar, usaremos los que ya nos da django

from django import forms

from users.models import User

class RegisterForm(forms.Form):
    #atributos necesarios para registrar un usuario
    username = forms.CharField(required=True, min_length=4, max_length=50,
                               widget= forms.TextInput(attrs={
                                    'class': 'form-control',
                                    'id':'username',
                                    'placeholder': 'Username'}) #widget es para aplicar estilos a estos formularios que ofrece django
                               )
    email = forms.EmailField(required=True,
                               widget= forms.EmailInput(attrs={
                                    'class': 'form-control',
                                    'id':'email',
                                    'placeholder': 'email@example.com'}))
    password = forms.CharField(required=True,
                               widget= forms.PasswordInput(attrs={
                                    'class': 'form-control'}))
    password2 = forms.CharField(label='Confirmar password',
                                required=True,
                               widget= forms.PasswordInput(attrs={
                                    'class': 'form-control'}))
    
    
    #al poner el prefijo clean_ le indicamos a django que implementaremos una validacion sobre username
    #este metodo se ejecuta cuando se ejecuta el metodo is_valid en views.py
 #al poner "clean" en el nombre de la funcion, le indicamos a django que la funcion implementará una validación sobre el campo username
    def clean_username(self):#validacion sobre campo username para saber que este no está en la base de datos y poder registrarlo
        username = self.cleaned_data.get('username')

        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('El username ya se encuentra en uso')

        return username

    def clean_email(self):#validacion sobre campo email para saber que este no está en la base de datos y poder registrarlo
        email = self.cleaned_data.get('email')

        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('El email ya se encuentra en uso')

        return email

    def clean(self): #clean se usa en los campos que dependen de otros campos, como password2
        #Cuando defines un método clean en un formulario Django, estás agregando validaciones adicionales que involucran múltiples campos.
        #Este método se llama después de que Django haya validado los campos individuales pero antes de que se acceda a los datos limpios.
        
        cleaned_data = super().clean() #se ejecuta el metodo clean de la clase padre, o sea "form"

        if cleaned_data.get('password2') != cleaned_data.get('password'):
            self.add_error('password2', 'El password no coincide')#a password2 le agregamos el mensaje de error
            
    def save(self):#agregamos un metodo para crear nuevos usuarios a nuestro formulario
        return User.objects.create_user(
                self.cleaned_data.get('username'),
                self.cleaned_data.get('email'),
                self.cleaned_data.get('password'),
            )
