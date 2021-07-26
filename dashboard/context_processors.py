"""Context usable in all templates of the project"""

from .forms import CommunityResearchForm


def get_substitute_form(request):
    """Print a form to post data on SubstituteForm
    of products app"""
    form = CommunityResearchForm(request.POST or None)
    return {'research_form': form}
