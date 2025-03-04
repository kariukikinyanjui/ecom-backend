from django.db.models import Avg, Count
from rest_framework.views import APIView
from rest_framework.response import Response


class ProductAnalyticsView(APIView):
    '''
    Calculate product rating statistics:
    - Average rating
    - Rating distribution
    - Total reviews
    '''

    def get(self, request, product_id):
        stats = Review.objects.filter(product_id=product_id).aggregate(
            average_rating=Avg('rating'),
            total_reviews=Count('id'),
            five_star=Count('id', filter=models.Q(rating=5)),
            four_star=Count('id', filter=models.Q(rating=4)),
            three_star=Count('id', filter=models.Q(rating=3)),
            two_star=Count('id', filter=models.Q(rating=2)),
            one_star=Count('id', filter=models.Q(rating=1)),
        )
        return Response(stats)
