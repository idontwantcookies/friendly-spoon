from datetime import datetime, timedelta

from django.test import TestCase

from .models import Candlestick
from .services import MediaMovelExponencial, IndiceForcaRelativa
from .factories import CandlestickFactory

# Create your tests here.
class CandlestickTests(TestCase):
	def create_candlesticks(self, n):
		candlesticks = []
		stop = datetime.now()
		start = stop - timedelta(days=n)
		for i in range(n):
			cs = CandlestickFactory.build(datetime=start + timedelta(days=i), type=Candlestick.DAY, close=i)
			candlesticks.append(cs)
		Candlestick.objects.bulk_create(candlesticks)
		return start, stop

	def test_media_movel_exponencial_20(self):
		start, stop = self.create_candlesticks(100)
		result = MediaMovelExponencial(start, stop + timedelta(days=1)).execute()
		self.assertEqual(round(result[-1], 3), 89.5)
