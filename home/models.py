# models.py

from django.db import models
from wagtail.models import Page, Orderable
from wagtail.admin.panels import FieldPanel, PageChooserPanel, InlinePanel
from wagtail.fields import RichTextField
from modelcluster.fields import ParentalKey
from django.utils.timezone import now  # Import to get current time

# The Show model, related to the Homepage model
class Show(Orderable):
    homepage = ParentalKey(
        'Homepage',  # Points to the Homepage model
        on_delete=models.CASCADE,
        related_name='shows',
        null=False,  # Required to be non-nullable
        default=None,  
    )
    name = models.CharField(max_length=255, help_text="Name of the show.")
    date_time = models.DateTimeField(help_text="Date and time of the show.")
    venue = models.CharField(max_length=255, help_text="Venue of the show.")
    venue_url = models.URLField(blank=True, help_text="Google Maps link or URL for the venue.")
    description = RichTextField(blank=True, help_text="Description of the show.")
    poster_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        help_text="Poster image for the show."
    )
    ticket_url = models.URLField(blank=True, help_text="URL for purchasing tickets.")

    # Panels for editing in the Wagtail admin
    panels = [
        FieldPanel('name'),
        FieldPanel('date_time'),
        FieldPanel('venue'),
        FieldPanel('venue_url'),
        FieldPanel('description'),
        FieldPanel('poster_image'),
        FieldPanel('ticket_url'),
    ]

    def __str__(self):
        return self.name

# The Single model, related to the Homepage model
class Single(Orderable):
    homepage = ParentalKey(
        'Homepage',  # Points to the Homepage model
        on_delete=models.CASCADE,
        related_name='singles',
        null=False,
        default=None,
    )
    title = models.CharField(max_length=255, help_text="Title of the single", null=True, blank=True)
    description = RichTextField(blank=True, help_text="Description of the single.")
    image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        help_text="Image for the single.",
    )
    buy_url = models.URLField(blank=True, help_text="URL to purchase the single.")

    panels = [
        FieldPanel('title'),
        FieldPanel('description'),
        FieldPanel('image'),
        FieldPanel('buy_url'),
    ]

    def __str__(self):
        return self.title


# The Album model, related to the Homepage model
class Album(Orderable):
    homepage = ParentalKey(
        'Homepage',  # Points to the Homepage model
        on_delete=models.CASCADE,
        related_name='albums',
        null=False,
        default=None,
    )
    title = models.CharField(max_length=255, help_text="Title of the album.", null=True, blank=True)
    description = RichTextField(blank=True, help_text="Description of the album.")
    price = models.DecimalField(max_digits=10, decimal_places=2, help_text="Price of the album.")
    venmo_id = models.CharField(max_length=255, blank=True, help_text="Venmo ID for payment.")
    image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        help_text="Album cover image.",
    )
    buy_url = models.URLField(blank=True, help_text="URL to purchase the album.")

    panels = [
        FieldPanel('title'),
        FieldPanel('description'),
        FieldPanel('price'),
        FieldPanel('venmo_id'),
        FieldPanel('image'),
        FieldPanel('buy_url'),
    ]

    def __str__(self):
        return self.title


# The Homepage model
class Homepage(Page):
    lead_text = models.CharField(
        max_length=140,
        blank=True,
        help_text='Subheading text under the banner title',
    )
    button = models.ForeignKey(
        'wagtailcore.Page',
        blank=True,
        null=True,
        related_name='+',
        help_text='Select an optional page to link to',
        on_delete=models.SET_NULL,
    )
    button_text = models.CharField(
        max_length=50,
        default='Read More',
        blank=False,
        help_text='Button text',
    )
    header_background_image = models.ForeignKey(
        'wagtailimages.Image',
        blank=True,
        null=True,
        related_name='+',
        help_text='The banner background image.',
        on_delete=models.SET_NULL,
    )
    banner_background_image1 = models.ForeignKey(
        'wagtailimages.Image',
        blank=True,
        null=True,
        related_name='+',
        help_text='The first banner background image.',
        on_delete=models.SET_NULL,
    )
    banner_background_image2 = models.ForeignKey(
        'wagtailimages.Image',
        blank=True,
        null=True,
        related_name='+',
        help_text='The second banner background image.',
        on_delete=models.SET_NULL,
    )
    banner_background_image3 = models.ForeignKey(
        'wagtailimages.Image',
        blank=True,
        null=True,
        related_name='+',
        help_text='The third banner background image.',
        on_delete=models.SET_NULL,
    )
    content = models.TextField(
        blank=True,
        help_text='Content text below the carousel.',
    )
    # Helper methods to get old and new shows
    def get_upcoming_shows(self):
        """Return upcoming shows."""
        return self.shows.filter(date_time__gte=now()).order_by('date_time')

    def get_past_shows(self):
        """Return past shows."""
        return self.shows.filter(date_time__lt=now()).order_by('-date_time')

    content_panels = Page.content_panels + [
        FieldPanel('lead_text'),
        PageChooserPanel('button'),
        FieldPanel('button_text'),
        FieldPanel('header_background_image'),
        FieldPanel('banner_background_image1'),
        FieldPanel('banner_background_image2'),
        FieldPanel('banner_background_image3'),
        FieldPanel('content'),
        InlinePanel('shows', label="Shows"),  # Shows panel
        InlinePanel('singles', label="Singles"),  # Singles panel for the shop
        InlinePanel('albums', label="Albums"),  # Albums panel for the shop
    ]
