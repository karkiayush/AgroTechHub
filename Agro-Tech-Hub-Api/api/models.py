from typing import Iterable
from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from django.core.exceptions import ValidationError
from django.utils import timezone


class MyUserManager(BaseUserManager):
    def create_user(self, email, name, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError("Users must have an email address")

        user = self.model(
            email=self.normalize_email(email),
            name=name,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, password=None):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            email,
            password=password,
            name=name,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class MyUser(AbstractBaseUser):
    email = models.EmailField(
        verbose_name="email address",
        max_length=255,
        unique=True,
    )
    name = models.TextField(default="Guest")
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = MyUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["name"]

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin


class Post(models.Model):
    # means that each post is associated with the user which helps in creating one to many relationship

    author = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    content = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to="post_images", blank=True, null=True)
    pdf = models.FileField(upload_to="pdf_files", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    # this method is used for validation of the post if they are correctly posted or not
    def clean(self):
        if not self.content and not self.image and not self.pdf:
            raise ValidationError("You cannnot post empty field")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Post by {self.author.name} on {self.created_at}"


class Comment(models.Model):

    comment = models.TextField()
    author = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    commented_on = models.ForeignKey(Post, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"comment by {self.author.name} on {self.commented_on.author}"


class Video(models.Model):
    caption = models.CharField(default="Video 1", max_length=100)
    video = models.FileField(upload_to="video/%Y/")
    author = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    uploaded_at = models.DateTimeField(default=timezone.now)


class VideoComment(models.Model):
    author = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    comment = models.CharField(max_length=200)
    commented_on = models.ForeignKey(Video, on_delete=models.CASCADE)
    commented_at = models.DateTimeField(default=timezone.now)


class Mychats(models.Model):
    me = models.ForeignKey(to=MyUser,on_delete=models.CASCADE,related_name='it_me')
    frnd = models.ForeignKey(to=MyUser,on_delete=models.CASCADE,related_name='my_frnd')
    chats = models.JSONField(default=dict)
    
class Expense(models.Model):
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=100)
    date = models.DateField()
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.category}: {self.amount}"

class CitizenshipVerification(models.Model):
    user = models.OneToOneField(MyUser, on_delete=models.CASCADE)
    citizenship_card = models.ImageField(upload_to='citizenship_cards/')
    is_verified = models.BooleanField(default=False)
    verification_request_sent = models.BooleanField(default=False)
    verification_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Verification for {self.user.name}"

    def save(self, *args, **kwargs):
        if self.is_verified and not self.verification_date:
            self.verification_date = timezone.now()
        super().save(*args, **kwargs)
        
class Role(models.Model):
    ROLE_CHOICES = [
        ('farmer', 'Farmer'),
        ('buyer', 'Buyer'),
    ]
    
    user = models.OneToOneField(MyUser, on_delete=models.CASCADE)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)

    def __str__(self):
        return f'{self.user.name} - {self.role}'
    





class Product(models.Model):
    name = models.CharField(max_length=100)
    productimage = models.ImageField(upload_to='productimage/')
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    farmer = models.ForeignKey(MyUser, related_name='products_as_farmer', on_delete=models.CASCADE)
    user = models.ForeignKey(MyUser, related_name='products_as_user', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
