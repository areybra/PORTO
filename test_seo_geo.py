import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'config.settings.development'
import django
django.setup()

# Test SEO metadata generation
from apps.core.seo import build_meta, json_ld_person, json_ld_organization, json_ld_breadcrumb, to_jsonld
from django.test import RequestFactory
factory = RequestFactory()

# Test 1: Landing page SEO
req = factory.get('/')
seo = build_meta(
    req,
    title='Test Title',
    description='Test Desc',
    keywords='test, keywords',
    og_image='https://example.com/image.jpg',
    canonical_path='/test',
)
print('Test 1 - SEO generation:', 'PASS' if seo['title'] == 'Test Title' else 'FAIL')

# Test 2: JSON-LD generation
person = json_ld_person()
org = json_ld_organization()
breadcrumb = json_ld_breadcrumb([('Home', '/')])
combined = to_jsonld(person, org, breadcrumb)
print('Test 2 - JSON-LD generation:', 'PASS' if isinstance(combined, str) else 'FAIL')

# Test 3: Project detail SEO
from apps.portfolio.models import Project, Category, Technology
from apps.core.models import SiteProfile

cat = Category.objects.create(name='Test Cat', slug='test-cat')
tech = Technology.objects.create(name='Test Tech')
profile, _ = SiteProfile.objects.get_or_create()

project = Project.objects.create(
    title='Test Project',
    slug='test-project',
    description='Test Description',
    excerpt='Test Excerpt',
    status='published',
    category=cat,
    featured=False,
    featured_order=0,
    github_url='',
    demo_url='',
    technologies=[tech],
    created_at='2024-01-01T00:00:00Z',
    updated_at='2024-01-01T00:00:00Z',
)

# Test 4: Blog detail SEO
from apps.blog.models import Post, Category as BlogCategory, Tag

blog_cat = BlogCategory.objects.create(name='Test Blog Cat', slug='test-blog-cat')
tag = Tag.objects.create(name='Test Tag')

post = Post.objects.create(
    title='Test Post',
    slug='test-post',
    excerpt='Test Post Excerpt',
    content='Test Content',
    status='published',
    category=blog_cat,
    is_featured=False,
    is_spotlight=False,
    image_url='https://example.com/post-image.jpg',
    published_at='2024-01-01T00:00:00Z',
    created_at='2024-01-01T00:00:00Z',
    tags=[tag],
)

print('Test 4 - Model creation:', 'PASS' if all([
    Project.objects.filter(slug='test-project').exists(),
    Post.objects.filter(slug='test-post').exists()
]) else 'FAIL')

# Test 5: WhatsApp redirect logic
from apps.contact.forms import ContactMessageForm

form_data = {
    'name': 'Test User',
    'email': 'test@example.com',
    'phone': '+123456789',
    'message': 'Test message'
}
form = ContactMessageForm(data=form_data)
print('Test 5 - Form validation:', 'PASS' if form.is_valid() else 'FAIL')

print('All tests completed.')
