from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from core.utils import auto_save_current_user

User = get_user_model()

class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Event(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='events')
    event_date = models.DateField()
    location = models.CharField(max_length=255,null=True)
    contactinfo = models.CharField(max_length=255,null=True)
    titre = models.CharField(max_length=255,null=True)


    def __str__(self):
        return f"Event: {self.category.name}"

class Carpooling(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='carpoolings')
    departure_time = models.TimeField()
    destination = models.CharField(max_length=255, null=True)
    depart = models.CharField(max_length=255, null=True)
    nbsiege = models.IntegerField(null=True)  # Define nbsiege as a separate field
    duree = models.IntegerField(null=True)    # Define duree as a separate field
    contactinfo = models.CharField(max_length=255, null=True)


    def __str__(self):
        return f"Carpooling: {self.category.name}"


class Stage(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='stages')
    departure_time = models.DateField()
    typestage = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(99999)])
    societe = models.CharField(max_length=255)
    duree = models.IntegerField()
    sujet = models.CharField(max_length=255)
    contactinfo = models.CharField(max_length=255)
    specialite = models.CharField(max_length=255)

    def __str__(self):
        return f"Stage: {self.category.name}"
class Logement(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='Logement')
    start_date = models.DateField()
    end_date = models.DateField()
    location = models.TextField()
    description = models.TextField()
    contactinfo = models.CharField(max_length=255)


    def __str__(self):
        return f"Logement: {self.category.name}"

class Absence(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='absences')
    start_date = models.DateField()
    end_date = models.DateField()
    reason = models.TextField()

    def __str__(self):
        return f"Absence: {self.category.name}"

class Post(models.Model):
    text = models.CharField(max_length=140, blank=True, null=True)
    image = models.ImageField(upload_to='post_images')
    user = models.ForeignKey(User, on_delete=models.PROTECT, editable=False)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    categories = models.ManyToManyField(Category)
    event = models.ForeignKey(Event, on_delete=models.SET_NULL, blank=True, null=True)
    carpooling = models.ForeignKey(Carpooling, on_delete=models.SET_NULL, blank=True, null=True)
    absence = models.ForeignKey(Absence, on_delete=models.SET_NULL, blank=True, null=True)
    stage = models.ForeignKey(Stage, on_delete=models.SET_NULL, blank=True, null=True)
    logement = models.ForeignKey(Logement, on_delete=models.SET_NULL, blank=True, null=True)


    class Meta:
        ordering = ['-created_on']

    def __str__(self):
        return str(self.pk)

    def save(self, *args, **kwargs):
        auto_save_current_user(self)
        super(Post, self).save(*args, **kwargs)

    @property
    def likes_count(self):
        return self.like_set.count()

    @property
    def comments_count(self):
        return self.comment_set.count()

class Comment(models.Model):
    text = models.CharField(max_length=240)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, editable=False)
    commented_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.text

    def save(self, *args, **kwargs):
        auto_save_current_user(self)
        super(Comment, self).save(*args, **kwargs)

class Like(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, editable=False)
    liked_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.post.id)

    def save(self, *args, **kwargs):
        auto_save_current_user(self)
        super(Like, self).save(*args, **kwargs)

class Follow(models.Model):
    user = models.ForeignKey(User, related_name='follow_follower', on_delete=models.CASCADE, editable=False)
    followed = models.ForeignKey(User, related_name='follow_followed', on_delete=models.CASCADE)
    followed_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user} --> {self.followed}"

    def save(self, *args, **kwargs):
        auto_save_current_user(self)
        super(Follow, self).save(*args, **kwargs)

class SavedPost(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, editable=False)
    saved_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.post.pk)

    def save(self, *args, **kwargs):
        auto_save_current_user(self)
        super(SavedPost, self).save(*args, **kwargs)
