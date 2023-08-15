from django.db import models
#from exam.models import School
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from address.models import Address



##################################################################################################
####################################    AUTHENTICATION      ######################################
class Role(models.Model):
    name = models.CharField(max_length=31)

    def __str__(self):
        return self.name

class UserAccountManager(BaseUserManager):
    def create_user(self, email, username, first_name, last_name, password=None):
        for i in [email, username, first_name, last_name, password]:
            if not i:
                raise ValueError(f"You must include your {i.__str__()}")

        email = self.normalize_email(email).lower()

        #   DEFAULT USERNAME FOR MIGRATED RECORDS

        if not username:
            username = first_name + '_' + last_name
        if not password:
            password = first_name + 23 + last_name
        user = self.model(
                        email=email,
                        username=username,
                        first_name=first_name,
                        last_name=last_name,)
        user.set_password(password)
        user.is_active=True
        
        user.save()
        
        return user

    def create_superuser(self, email, username, first_name, last_name, password):

        email = self.normalize_email(email).lower()
        user = self.model(email=email, last_name=last_name, first_name=first_name, username=username)
        user.is_superuser = True
        user.is_staff = True
        user.set_password(password)
        user.is_active = True

        user.save(using=self._db)
        print(user.is_staff)
        return user

                    

class UserAccount(AbstractBaseUser, PermissionsMixin):

    first_name = models.CharField(max_length=31)
    last_name = models.CharField(max_length=31)
    email = models.EmailField(max_length=255)
    username = models.CharField(max_length=63, unique=True) #   VALIDATE
    created_on = models.DateTimeField(auto_now_add=True, editable=False, null=True, blank=True)
    #phone = models.CharField(max_length=15)
    #school_name = models.CharField(max_length=64)
    #guardian_first_name = models.CharField(max_length=31)
    #guardian_first_name = models.CharField(max_length=31)


    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    is_executive = models.BooleanField(default=False)
    #school = models.ForeignKey(School, on_delete=models.CASCADE)
    #phone = models.CharField(max_length=15)

    objects = UserAccountManager()
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ('email', 'first_name', 'last_name')

    #   THIS REDUNDANT METHOD FIXES A BUG. REMOVE CAREFULLY
    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def get_short_name(self):
        return self.first_name

    class Meta:
        verbose_name_plural = 'User Accounts'
    
    def officer(self):
        pass

class Profile(models.Model):
    owner = models.OneToOneField(UserAccount, on_delete=models.CASCADE)

    phone_number = models.CharField(max_length=15, null=True, blank=True)
    
    #   role = models.ForeignKey(Role, on_delete=models.CASCADE)
    guardian_first_name = models.CharField(max_length=63, null=True, blank=True)
    guardian_last_name = models.CharField(max_length=63, null=True, blank=True)
    guardian_phone_number = models.CharField(max_length=15, null=True, blank=True)
    guardian_email = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f"{self.owner.first_name} {self.owner.last_name}"
##################################################################################################
##################################################################################################
