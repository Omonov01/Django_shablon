from django.db import models
from django.utils.translation import gettext_lazy as _

class NewsArticle(models.Model):
    created_at = models.DateTimeField(_("Created at"),
    auto_now_add=True)
    title = models.CharField(verbose_name=_("Title"), max_length=255)
    body = models.TextField(verbose_name=_("Body"))
    theme = models.CharField(verbose_name=_("Theme"), max_length=20)
    
    class Meta:
        db_table = 'articles'
        verbose_name = _("News Article")
        verbose_name_plural = _("News Articles")
        
        def __str__(self):
            return self.title



#