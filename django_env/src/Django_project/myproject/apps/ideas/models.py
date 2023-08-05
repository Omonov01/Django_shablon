from django.db import models
from django.urls import reverse
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from myproject.apps.core.models import (object_relation_base_factory as generic_relation,)
from myproject.apps.core.models import (CreationModificationDateBase,MetaTagsBase,UrlBase)
from myproject.apps.core.model_fields import (MultilingualCharField,MultilingualTextField,)


FavoriteObjectBase = generic_relation(is_required=True,)

OwnerBase = generic_relation(
    prefix="owner",
    prefix_verbose=_("Owner"),
    is_required=True,
    add_related_name=True,
    limit_content_type_choices_to={"model__in": ("user","group",)})

from myproject.apps.core.models import (
    CreationModificationDateBase,
    MetaTagsBase,
    UrlBase,
    )
# Create your models here.
class Like(FavoriteObjectBase, OwnerBase):
    class Meta:
        verbose_name = _("Like")
        verbose_name_plural = _("Likes")
        def __str__(self):
            return _("{owner} likes {object}").format(owner=self.owner_content_object,object=self.content_object)
        


class Idea(CreationModificationDateBase, MetaTagsBase, UrlBase):
    author = models.ForeignKey(settings.AUTH_USER_MODEL,verbose_name=_("Author"),on_delete=models.SET_NULL,blank=True,null=True,)
    category = models.ManyToManyField("categories.Category",verbose_name=_("Category"),blank=True,related_name="ideas")
    title = MultilingualCharField(_("Title"), max_length=200,)
    content = MultilingualTextField(_("Content"),)
    slug = models.SlugField(_("Slug for URLs"), max_length=50)
    # other fields…
    def __str__(self):
            return self.title
        
    def get_url_path(self):
            return reverse("idea_details", kwargs={
        "idea_id": str(self.pk),
        })
    
    class Meta:
        verbose_name = _("Idea")
        verbose_name_plural = _("Ideas")
        constraints = [
            models.UniqueConstraint(fields=["title"],condition=~models.Q(author=None),name="unique_titles_for_each_author",),
            models.CheckConstraint(check=models.Q(title__iregex=r"^\S.*\S$"
            # starts with non-whitespace,
            # ends with non-whitespace,
            # anything in the middle
            ),name="title_has_no_leading_and_trailing_whitespaces",)]

    
        
    
    
    def clean(self):
        import re
        if self.author and Idea.objects.exclude(pk=self.pk).filter(author=self.author,title=self.title,).exists():
            raise ValidationError(_("Each idea of the same user should have a unique title."))
        if not re.match(r"^\S.*\S$", self.title):
            raise ValidationError(_("The title cannot start or end with a whitespace."))


class IdeaTranslations(models.Model):
    idea = models.ForeignKey(Idea,verbose_name=_("Idea"),on_delete=models.CASCADE,related_name="translations",)
    language = models.CharField(_("Language"), max_length=7)
    title = models.CharField(_("Title"),max_length=200,)
    content = models.TextField(_("Content"),)
    
    class Meta:
        verbose_name = _("Idea Translations")
        verbose_name_plural = _("Idea Translations")
        ordering = ["language"]
        unique_together = [["idea", "language"]]
        
        def __str__(self):
            return self.title

        