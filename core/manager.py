from django.contrib.auth.models import BaseUserManager

class CustomUserManager(BaseUserManager):
    def create_user(self, login, password, is_staff=False, is_superuser=False):
        if not login:
            raise ValueError('Login must be set')

        user = self.model(
            login=login,
            is_staff=is_staff,
            is_superuser=is_superuser
        )

        user.is_active = True
        user.set_password(password)
        user.save(using=self._db)

        return user


    def create_superuser(self, login, password):
        user = self.create_user(
            login=login,
            password=password,
            is_staff=True,
            is_superuser=True,
        )
        user.save(using=self._db)
        return user
