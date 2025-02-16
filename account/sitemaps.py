from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from . models import Post



class PostSitemap(Sitemap):
	def items(self):
		return Post.objects.all()
	
	def lastmod(self, obj):
		return obj.updated_at
	
class StaticViewSitemap(Sitemap):
	priority = 0.5
	changefreq = "daily"

	def items(self):
		return ['landing-page']
	
	def location(self, item):
		return reverse(item)
